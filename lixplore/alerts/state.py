"""
Remembers which articles were already sent so each digest holds only new ones.

An article is keyed by its DOI and by a normalised-title hash; it counts as
seen if either key matches, which also catches the same paper arriving from
a different source without a DOI.
"""

import hashlib
import json
import os
import re
from datetime import date, timedelta
from typing import Dict, List

PRUNE_AFTER_DAYS = 120


def article_keys(article: Dict) -> List[str]:
    keys = []
    doi = (article.get("doi") or "").strip().lower()
    if doi:
        keys.append("doi:" + re.sub(r"^https?://(dx\.)?doi\.org/", "", doi))
    title = re.sub(r"[^a-z0-9]+", " ", (article.get("title") or "").lower()).strip()
    if title:
        keys.append("title:" + hashlib.sha1(title.encode("utf-8")).hexdigest()[:16])
    if not keys and article.get("url"):
        keys.append("url:" + article["url"].strip())
    return keys


class SeenState:
    def __init__(self, path: str):
        self.path = path
        self.seen: Dict[str, str] = {}
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    self.seen = json.load(f).get("seen", {})
            except (OSError, json.JSONDecodeError):
                print(f"[alerts] state file {path} unreadable, starting fresh")

    @property
    def is_first_run(self) -> bool:
        return not self.seen

    def is_seen(self, article: Dict) -> bool:
        return any(k in self.seen for k in article_keys(article))

    def mark(self, articles: List[Dict]) -> None:
        today = date.today().isoformat()
        for article in articles:
            for key in article_keys(article):
                self.seen[key] = today

    def save(self) -> None:
        cutoff = (date.today() - timedelta(days=PRUNE_AFTER_DAYS)).isoformat()
        self.seen = {k: v for k, v in self.seen.items() if v >= cutoff}
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"seen": self.seen}, f, indent=0, sort_keys=True)
