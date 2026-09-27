"""
Lixplore Alerts: search for papers published since the last run and send a
digest by email and/or Telegram.

    lixplore-alerts run         fetch, send, remember what was sent
    lixplore-alerts dry-run     fetch and print the digest, send nothing
    lixplore-alerts test        send a short test message to every channel
    lixplore-alerts check       validate configuration only
    lixplore-alerts init        create a .env settings template here
    lixplore-alerts schedule    print the cron / Task Scheduler line for this folder
"""

import argparse
import importlib
import os
import sys
import time
from datetime import date, timedelta
from typing import Dict, List

from . import notify, render
from .config import DAY_NAMES, AlertConfig, ConfigError, load_config, load_dotenv, parse_days
from .state import SeenState

REPORT_DIR = "reports"
ATTACH_EXT = {"csv": "csv", "bibtex": "bib", "ris": "ris", "json": "json", "xlsx": "xlsx"}


def _mark(ok: bool) -> str:
    return "configured" if ok else "not configured"


def print_summary(cfg: AlertConfig) -> None:
    since = date.today() - timedelta(days=cfg.lookback_days)
    print("=" * 60)
    print("Lixplore Alerts")
    print("=" * 60)
    print(f"Alerts ({len(cfg.alerts)}):")
    if not cfg.alerts:
        print("  (none yet: set LIXPLORE_QUERIES, one search per line)")
    for a in cfg.alerts:
        label = a.query if a.name == a.query else f"{a.name}: {a.query}"
        print(f"  - {label}  [{', '.join(a.sources)}]")
    print(f"Window:        {since} -> {date.today()} ({cfg.lookback_days} days)")
    print(f"Max results:   {cfg.max_results} per query per source")
    print(f"Attachment:    {cfg.attach_format}")
    print("Channels:")
    for name, on in notify.status(cfg.channel_env):
        print(f"  {'✅' if on else '⚪'} {name}")
    print(f"PubMed key:    {_mark(bool(os.environ.get('PUBMED_API_KEY')))} (optional)")
    print("=" * 60)


def fetch(cfg: AlertConfig, state: SeenState):
    """Returns (results, failures, all_new_articles)."""
    from lixplore import dispatcher  # deferred: pulls in all source modules

    since = date.today() - timedelta(days=cfg.lookback_days)
    results: List[render.AlertResult] = []
    failures: List[str] = []
    all_new: List[Dict] = []

    for alert in cfg.alerts:
        found: List[Dict] = []
        not_shown: Dict[str, int] = {}
        for source in alert.sources:
            try:
                module = importlib.import_module(f"lixplore.sources.{source}")
                articles = module.search(alert.query, cfg.max_results, since=since)
                total = getattr(module, "last_total", None)
                print(f"[{alert.name}] {source}: fetched {len(articles)}"
                      + (f" of {total} in window" if total is not None else ""))
                # Only a capped fetch hides anything
                if total and len(articles) >= cfg.max_results and total > len(articles):
                    not_shown[source] = total - len(articles)
                found.extend(articles)
            except Exception as e:  # one bad source must not sink the digest
                print(f"[{alert.name}] {source} failed: {e}")
                failures.append(f"{alert.name} / {source}: {e}")
            if source == "pubmed":
                time.sleep(0.4)  # NCBI allows 3 requests/second without an API key

        if cfg.dedupe and len(found) > 1:
            found = dispatcher.deduplicate_advanced(found, strategy="auto", keep_preference="most_complete")

        result = render.AlertResult(alert.name, alert.query,
                                    by_source={s: [] for s in alert.sources}, not_shown=not_shown)
        for a in found:
            if not state.is_seen(a):
                result.by_source.setdefault(a.get("source", ""), []).append(a)
        print(f"[{alert.name}] {result.total} new after dedupe and history check")
        results.append(result)
        all_new.extend(result.articles)

    return results, failures, all_new


def write_reports(results, failures, all_new, attach_format: str):
    os.makedirs(REPORT_DIR, exist_ok=True)
    md = render.markdown(results, failures)
    with open(os.path.join(REPORT_DIR, "digest.md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(REPORT_DIR, "digest.html"), "w", encoding="utf-8") as f:
        f.write(render.email_html(results, failures))

    # Shows the digest on the workflow run page even with no channel configured
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(md + "\n")

    if attach_format == "none" or not all_new:
        return None
    from lixplore.utils.export import export_results
    path = os.path.abspath(os.path.join(
        REPORT_DIR, f"lixplore_alerts_{date.today():%Y%m%d}.{ATTACH_EXT[attach_format]}"))
    return export_results(all_new, attach_format, path)


def cmd_run(cfg: AlertConfig, dry_run: bool) -> int:
    state = SeenState(cfg.state_file)
    if state.is_first_run:
        print("First run: no history yet, sending everything in the window.")

    results, failures, all_new = fetch(cfg, state)
    attachment = write_reports(results, failures, all_new, cfg.attach_format)
    total = len(all_new)
    print(f"\nTotal new papers: {total}")

    if dry_run:
        print("\n" + render.plain_text(results, failures))
        print("Dry run: nothing sent, history not updated.")
        return 0

    channels = notify.configured(cfg.channel_env)
    if not channels:
        print("\nWARNING: no delivery channel configured. Add e.g. EMAIL_* or TELEGRAM_* secrets.")
        print("The digest is in the workflow run summary and the 'reports' artifact.")
        return 0

    if total == 0 and not cfg.send_when_empty:
        print("Nothing new; skipping notifications (set LIXPLORE_SEND_WHEN_EMPTY=true to always send).")
        return 0

    errors = notify.deliver(cfg.channel_env, notify.Digest(results, failures, attachment))
    if len(errors) == len(channels):
        print("All channels failed; history not updated so the next run retries.")
        return 1

    state.mark(all_new)
    state.save()
    print(f"History updated: {cfg.state_file}")
    for channel, error in errors.items():
        # Shows as a warning on the workflow run without failing it,
        # so the working channel doesn't get re-sent every hour
        print(f"::warning title=Lixplore {channel} delivery failed::{error}")
    return 0


def cmd_test(cfg: AlertConfig) -> int:
    if not notify.configured(cfg.channel_env):
        print("No delivery channel configured. Add e.g. EMAIL_* or TELEGRAM_* secrets.")
        return 1
    if cfg.alerts:
        queries = "\n".join(f"• {a.name} [{', '.join(a.sources)}]" for a in cfg.alerts)
        watching = f"Watching {len(cfg.alerts)} search(es):\n{queries}"
    else:
        watching = "No searches yet: set LIXPLORE_QUERIES to start receiving papers."
    text = f"✅ Lixplore Alerts is set up.\n\n{watching}"
    errors = notify.deliver(cfg.channel_env, notify.Digest([], test_text=text))
    return 1 if errors else 0


def cmd_init(path: str, force: bool) -> int:
    if os.path.exists(path) and not force:
        print(f"{path} already exists; not overwriting. Use `lixplore-alerts init --force` to replace it.")
        return 1
    template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "env.example")
    with open(template, encoding="utf-8") as src, open(path, "w", encoding="utf-8") as dst:
        dst.write(src.read())
    print(f"Created {os.path.abspath(path)}")
    print("Next: add your searches and one channel's settings, then run:")
    print("  lixplore --alerts check     # validate")
    print("  lixplore --alerts test      # test message")
    print("  lixplore --alerts schedule  # how to run it automatically")
    return 0


def cmd_schedule(hour: int) -> int:
    """Print (not install) the scheduler entry for running alerts from this folder."""
    try:
        days = parse_days(os.environ.get("LIXPLORE_SEND_DAYS", "") or "daily")
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return 2
    folder = os.getcwd()
    python = sys.executable
    every_day = len(days) == 7

    print(f"Run alerts from {folder} at {hour:02d}:00 local time on "
          f"{'every day' if every_day else ', '.join(DAY_NAMES[d] for d in days)}.")
    print("(Days come from LIXPLORE_SEND_DAYS; change the hour with --hour.)\n")

    if os.name == "nt":
        schedule = "/SC DAILY" if every_day else "/SC WEEKLY /D " + ",".join(DAY_NAMES[d].upper() for d in days)
        action = f'cmd /c cd /d \\"{folder}\\" && \\"{python}\\" -m lixplore.alerts run >> alerts.log 2>&1'
        print("Windows: run this once in Command Prompt:\n")
        print(f'  schtasks /Create /TN "Lixplore Alerts" /TR "{action}" {schedule} /ST {hour:02d}:00')
        print("\nRemove later with:  schtasks /Delete /TN \"Lixplore Alerts\"")
    else:
        # cron counts Sunday as 0
        cron_days = "*" if every_day else ",".join(str((d + 1) % 7) for d in days)
        print("Linux / macOS: run `crontab -e` and add this line:\n")
        print(f'  0 {hour} * * {cron_days} cd "{folder}" && "{python}" -m lixplore.alerts run >> alerts.log 2>&1')
        print("\nThe computer must be on at that time. For delivery without your computer,")
        print("fork the repository and use GitHub Actions instead (see the alerts guide).")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="lixplore-alerts",
        description="Send new-paper digests by email, Telegram, Discord, Slack and more. Configured through environment variables.",
    )
    parser.add_argument("mode", nargs="?", default="run",
                        choices=["run", "dry-run", "test", "check", "init", "schedule"])
    parser.add_argument("--queries", help="Override LIXPLORE_QUERIES for this run")
    parser.add_argument("--lookback-days", type=int, help="Override the search window")
    parser.add_argument("--env-file", default=".env", help="Load variables from this file (default: .env)")
    parser.add_argument("--force", action="store_true", help="init: overwrite an existing .env")
    parser.add_argument("--hour", type=int, default=8, choices=range(24), metavar="0-23",
                        help="schedule: local hour to run (default: 8)")
    args = parser.parse_args(argv)

    if args.mode == "init":
        return cmd_init(args.env_file, args.force)
    load_dotenv(args.env_file)
    if args.mode == "schedule":
        return cmd_schedule(args.hour)
    try:
        cfg = load_config(args.queries, require_queries=args.mode in ("run", "dry-run"))
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return 2
    if args.lookback_days:
        cfg.lookback_days = args.lookback_days

    print_summary(cfg)
    if args.mode == "check":
        return 0
    if args.mode == "test":
        return cmd_test(cfg)
    return cmd_run(cfg, dry_run=args.mode == "dry-run")


if __name__ == "__main__":
    sys.exit(main())
