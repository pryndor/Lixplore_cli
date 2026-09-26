"""
Alert configuration read from environment variables.

Every setting comes from the environment so the GitHub workflow can be
configured entirely through repository Variables and Secrets, and a local
run can use the same names from a shell or a .env file.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

VALID_SOURCES = ("pubmed", "europepmc", "arxiv", "crossref", "doaj")
DAY_NAMES = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

# Short codes match the main CLI's -s flag
SOURCE_CODES = {"P": "pubmed", "E": "europepmc", "X": "arxiv", "C": "crossref", "J": "doaj"}


# Every delivery-related variable the channels in notify.py read
CHANNEL_VARS = (
    "EMAIL_SENDER", "EMAIL_PASSWORD", "EMAIL_RECEIVERS", "EMAIL_SENDER_NAME", "SMTP_SERVER", "SMTP_PORT",
    "TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "TELEGRAM_MESSAGE_THREAD_ID",
    "DISCORD_WEBHOOK_URL", "DISCORD_BOT_TOKEN", "DISCORD_MAIN_CHANNEL_ID",
    "SLACK_WEBHOOK_URL", "SLACK_BOT_TOKEN", "SLACK_CHANNEL_ID",
    "TEAMS_WEBHOOK_URL",
    "GOOGLE_CHAT_WEBHOOK_URL",
    "MATRIX_HOMESERVER", "MATRIX_ACCESS_TOKEN", "MATRIX_ROOM_ID",
    "WECHAT_WEBHOOK_URL", "WECHAT_MSG_TYPE",
    "FEISHU_WEBHOOK_URL", "FEISHU_WEBHOOK_SECRET", "FEISHU_WEBHOOK_KEYWORD",
    "DINGTALK_WEBHOOK_URL", "DINGTALK_SECRET",
    "NTFY_URL", "NTFY_TOKEN",
    "GOTIFY_URL", "GOTIFY_TOKEN",
    "PUSHOVER_USER_KEY", "PUSHOVER_API_TOKEN",
    "PUSHPLUS_TOKEN", "PUSHPLUS_TOPIC",
    "SERVERCHAN3_SENDKEY",
    "ASTRBOT_URL", "ASTRBOT_TOKEN",
    "CUSTOM_WEBHOOK_URLS", "CUSTOM_WEBHOOK_BEARER_TOKEN", "CUSTOM_WEBHOOK_BODY_TEMPLATE",
    "WEBHOOK_VERIFY_SSL",
)


class ConfigError(ValueError):
    pass


@dataclass
class Alert:
    name: str
    query: str
    sources: List[str]


@dataclass
class AlertConfig:
    alerts: List[Alert]
    max_results: int = 20
    lookback_days: int = 3
    dedupe: bool = True
    send_when_empty: bool = False
    attach_format: str = "csv"
    state_file: str = ".lixplore-state/seen.json"
    # Raw delivery settings (EMAIL_*, TELEGRAM_*, DISCORD_*, ...); see notify.CHANNELS
    channel_env: Dict[str, str] = field(default_factory=dict)


def load_dotenv(path: str = ".env") -> None:
    """Minimal .env loader for local runs; real environment variables win."""
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1].replace("\\n", "\n")  # "a\nb" -> two lines
            else:
                value = value.strip("'")
            os.environ.setdefault(key.strip(), value)


def _env(name: str, default: str = "") -> str:
    value = os.environ.get(name, "")
    return value.strip() if value.strip() else default


def _bool(name: str, default: bool) -> bool:
    value = _env(name)
    if not value:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def _int(name: str, default: int) -> int:
    value = _env(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{name} must be a whole number, got {value!r}")


def parse_sources(text: str, where: str) -> List[str]:
    """Accept 'pubmed,arxiv' or short codes like 'PX'."""
    text = text.strip()
    if not text:
        return []
    if "," not in text and text.isupper() and all(c in SOURCE_CODES for c in text):
        return [SOURCE_CODES[c] for c in text]
    sources = [s.strip().lower() for s in text.split(",") if s.strip()]
    unknown = [s for s in sources if s not in VALID_SOURCES]
    if unknown:
        raise ConfigError(
            f"Unknown source(s) {', '.join(unknown)} in {where}. "
            f"Valid: {', '.join(VALID_SOURCES)}"
        )
    return sources


def parse_queries(text: str, default_sources: List[str]) -> List[Alert]:
    """
    Parse LIXPLORE_QUERIES.

    Accepted forms (one alert per line, '#' starts a comment):
        semaglutide AND obesity
        GLP-1 | semaglutide AND obesity | pubmed,europepmc
    or a JSON list: [{"name": ..., "query": ..., "sources": [...]}]
    """
    text = text.strip()
    if not text:
        raise ConfigError(
            "LIXPLORE_QUERIES is empty. Add it under Settings -> Secrets and variables "
            "-> Actions -> Variables, one search query per line."
        )

    if text.startswith("["):
        try:
            items = json.loads(text)
        except json.JSONDecodeError as e:
            raise ConfigError(f"LIXPLORE_QUERIES looks like JSON but is invalid: {e}")
        alerts = []
        for i, item in enumerate(items, 1):
            query = str(item.get("query", "")).strip()
            if not query:
                raise ConfigError(f"LIXPLORE_QUERIES JSON item {i} has no 'query'")
            sources = item.get("sources") or default_sources
            if isinstance(sources, str):
                sources = parse_sources(sources, f"JSON item {i}")
            else:
                sources = parse_sources(",".join(sources), f"JSON item {i}")
            alerts.append(Alert(item.get("name") or query, query, sources))
        return alerts

    alerts = []
    for lineno, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 1:
            alerts.append(Alert(parts[0], parts[0], default_sources))
        elif len(parts) in (2, 3):
            name, query = parts[0], parts[1]
            if not query:
                raise ConfigError(f"LIXPLORE_QUERIES line {lineno} has an empty query")
            sources = parse_sources(parts[2], f"LIXPLORE_QUERIES line {lineno}") if len(parts) == 3 else []
            alerts.append(Alert(name or query, query, sources or default_sources))
        else:
            raise ConfigError(
                f"LIXPLORE_QUERIES line {lineno} has too many '|' separators. "
                "Use: name | query | sources"
            )
    if not alerts:
        raise ConfigError("LIXPLORE_QUERIES has no queries (only blank or comment lines)")
    return alerts


def parse_days(text: str) -> List[int]:
    """'mon-fri', 'mon,thu', 'daily' -> weekday numbers (Mon=0)."""
    text = text.strip().lower()
    if not text or text in ("daily", "all", "*"):
        return list(range(7))
    days = set()
    for part in text.split(","):
        part = part.strip()[:3] if "-" not in part else part.strip()
        if "-" in part:
            start, end = (p.strip()[:3] for p in part.split("-", 1))
            if start not in DAY_NAMES or end not in DAY_NAMES:
                raise ConfigError(f"LIXPLORE_SEND_DAYS: bad range {part!r}")
            i, j = DAY_NAMES.index(start), DAY_NAMES.index(end)
            while True:
                days.add(i)
                if i == j:
                    break
                i = (i + 1) % 7
        elif part in DAY_NAMES:
            days.add(DAY_NAMES.index(part))
        elif part:
            raise ConfigError(f"LIXPLORE_SEND_DAYS: unknown day {part!r}")
    return sorted(days)


def default_lookback(send_days: List[int]) -> int:
    """Longest gap between sends, plus 2 days to catch late-indexed records."""
    if not send_days:
        return 3
    gaps = [((send_days[(i + 1) % len(send_days)] - d) % 7) or 7 for i, d in enumerate(send_days)]
    return max(gaps) + 2


def load_config(queries_override: Optional[str] = None) -> AlertConfig:
    default_sources = parse_sources(_env("LIXPLORE_SOURCES", "pubmed,europepmc,arxiv"), "LIXPLORE_SOURCES")
    alerts = parse_queries(queries_override or _env("LIXPLORE_QUERIES"), default_sources)

    send_days = parse_days(_env("LIXPLORE_SEND_DAYS", "daily"))
    lookback_raw = _env("LIXPLORE_LOOKBACK_DAYS", "auto")
    lookback = default_lookback(send_days) if lookback_raw == "auto" else _int("LIXPLORE_LOOKBACK_DAYS", 3)

    attach = _env("LIXPLORE_ATTACH_FORMAT", "csv").lower()
    if attach not in ("csv", "bibtex", "ris", "json", "xlsx", "none"):
        raise ConfigError(f"LIXPLORE_ATTACH_FORMAT must be csv, bibtex, ris, json, xlsx or none, got {attach!r}")

    return AlertConfig(
        alerts=alerts,
        max_results=_int("LIXPLORE_MAX_RESULTS", 20),
        lookback_days=max(1, lookback),
        dedupe=_bool("LIXPLORE_DEDUPE", True),
        send_when_empty=_bool("LIXPLORE_SEND_WHEN_EMPTY", False),
        attach_format=attach,
        state_file=_env("LIXPLORE_STATE_FILE", ".lixplore-state/seen.json"),
        channel_env={name: _env(name) for name in CHANNEL_VARS if _env(name)},
    )
