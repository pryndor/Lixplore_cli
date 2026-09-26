"""
Decides whether an hourly scheduled run should send today's digest.

GitHub cron schedules cannot read repository variables, so the workflow runs
every hour and this gate checks LIXPLORE_SEND_DAYS / LIXPLORE_SEND_HOUR_UTC.
Sending once the hour has passed (rather than only in that exact hour) keeps
a delayed or dropped GitHub cron run from skipping a whole day.

Standard library only: it runs before dependencies are installed.
Prints "send=true|false" for $GITHUB_OUTPUT.
"""

import os
import sys
from datetime import datetime, timezone

from .config import ConfigError, parse_days


def decide(now: datetime, days: str, hour: str, last_run: str, has_queries: bool):
    if not has_queries:
        return False, "LIXPLORE_QUERIES is not set; nothing to do"
    try:
        send_days = parse_days(days)
        send_hour = int(hour)
    except (ConfigError, ValueError) as e:
        return False, f"bad schedule settings: {e}"
    if now.weekday() not in send_days:
        return False, f"{now:%A} is not a send day"
    if now.hour < send_hour:
        return False, f"before send hour {send_hour:02d}:00 UTC"
    if last_run == now.date().isoformat():
        return False, "already ran today"
    return True, "due"


def main() -> int:
    last_run = ""
    path = os.environ.get("LIXPLORE_LAST_RUN_FILE", ".lixplore-state/last_run")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            last_run = f.read().strip()

    send, reason = decide(
        datetime.now(timezone.utc),
        os.environ.get("LIXPLORE_SEND_DAYS", "") or "daily",
        os.environ.get("LIXPLORE_SEND_HOUR_UTC", "") or "6",
        last_run,
        bool(os.environ.get("LIXPLORE_QUERIES", "").strip()),
    )
    print(f"Schedule check: {reason}", file=sys.stderr)
    print(f"send={'true' if send else 'false'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
