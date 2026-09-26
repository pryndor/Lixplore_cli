"""
Lixplore Alerts: search for papers published since the last run and send a
digest by email and/or Telegram.

    lixplore-alerts run         fetch, send, remember what was sent
    lixplore-alerts dry-run     fetch and print the digest, send nothing
    lixplore-alerts test        send a short test message to every channel
    lixplore-alerts check       validate configuration only
"""

import argparse
import importlib
import os
import sys
import time
from datetime import date, timedelta
from typing import Dict, List

from . import notify, render
from .config import AlertConfig, ConfigError, load_config, load_dotenv
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
    for a in cfg.alerts:
        label = a.query if a.name == a.query else f"{a.name}: {a.query}"
        print(f"  - {label}  [{', '.join(a.sources)}]")
    print(f"Window:        {since} -> {date.today()} ({cfg.lookback_days} days)")
    print(f"Max results:   {cfg.max_results} per query per source")
    print(f"Attachment:    {cfg.attach_format}")
    print(f"Email:         {_mark(cfg.email_enabled)}")
    print(f"Telegram:      {_mark(cfg.telegram_enabled)}")
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
        for source in alert.sources:
            try:
                module = importlib.import_module(f"lixplore.sources.{source}")
                articles = module.search(alert.query, cfg.max_results, since=since)
                print(f"[{alert.name}] {source}: {len(articles)} in window")
                found.extend(articles)
            except Exception as e:  # one bad source must not sink the digest
                print(f"[{alert.name}] {source} failed: {e}")
                failures.append(f"{alert.name} / {source}: {e}")
            if source == "pubmed":
                time.sleep(0.4)  # NCBI allows 3 requests/second without an API key

        if cfg.dedupe and len(found) > 1:
            found = dispatcher.deduplicate_advanced(found, strategy="auto", keep_preference="most_complete")

        new = [a for a in found if not state.is_seen(a)]
        counts: Dict[str, int] = {}
        for a in new:
            counts[a.get("source", "")] = counts.get(a.get("source", ""), 0) + 1
        print(f"[{alert.name}] {len(new)} new after dedupe and history check")
        results.append((alert.name, alert.query, new, counts))
        all_new.extend(new)

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


def deliver(cfg: AlertConfig, subject: str, html_body: str, text_body: str,
            tg_messages: List[str], attachment=None) -> Dict[str, str]:
    """Send to every configured channel. Returns {channel: error} for failures."""
    errors: Dict[str, str] = {}
    if cfg.email_enabled:
        try:
            notify.send_email(cfg.email, subject, html_body, text_body, attachment)
            print("Email: sent")
        except Exception as e:
            errors["email"] = str(e)
            print(f"Email: FAILED - {e}")
    if cfg.telegram_enabled:
        try:
            notify.send_telegram(cfg.telegram, tg_messages, attachment)
            print("Telegram: sent")
        except Exception as e:
            errors["telegram"] = str(e)
            print(f"Telegram: FAILED - {e}")
    return errors


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

    if not (cfg.email_enabled or cfg.telegram_enabled):
        print("\nWARNING: no delivery channel configured. Add EMAIL_* or TELEGRAM_* secrets.")
        print("The digest is in the workflow run summary and the 'reports' artifact.")
        return 0

    if total == 0 and not cfg.send_when_empty:
        print("Nothing new; skipping notifications (set LIXPLORE_SEND_WHEN_EMPTY=true to always send).")
        return 0

    errors = deliver(
        cfg, render.subject(results),
        render.email_html(results, failures), render.plain_text(results, failures),
        render.telegram_messages(results, failures), attachment,
    )

    configured = int(cfg.email_enabled) + int(cfg.telegram_enabled)
    if len(errors) == configured:
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
    if not (cfg.email_enabled or cfg.telegram_enabled):
        print("No delivery channel configured. Add EMAIL_* or TELEGRAM_* secrets.")
        return 1
    queries = "\n".join(f"• {a.name} [{', '.join(a.sources)}]" for a in cfg.alerts)
    text = f"✅ Lixplore Alerts is set up.\n\nWatching {len(cfg.alerts)} search(es):\n{queries}"
    html_body = "<p>" + render.html.escape(text).replace("\n", "<br>") + "</p>"
    errors = deliver(cfg, "Lixplore Alerts: test message", html_body, text,
                     [render.html.escape(text)])
    return 1 if errors else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="lixplore-alerts",
        description="Send new-paper digests by email and Telegram. Configured through environment variables.",
    )
    parser.add_argument("mode", nargs="?", default="run", choices=["run", "dry-run", "test", "check"])
    parser.add_argument("--queries", help="Override LIXPLORE_QUERIES for this run")
    parser.add_argument("--lookback-days", type=int, help="Override the search window")
    parser.add_argument("--env-file", default=".env", help="Load variables from this file (default: .env)")
    args = parser.parse_args(argv)

    load_dotenv(args.env_file)
    try:
        cfg = load_config(args.queries)
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
