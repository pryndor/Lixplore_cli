"""
Turns alert results into Telegram, email (HTML + text) and Markdown digests.
"""

import html
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

SOURCE_LABELS = {
    "pubmed": "PubMed", "europepmc": "EuropePMC", "arxiv": "arXiv",
    "crossref": "Crossref", "doaj": "DOAJ",
}



@dataclass
class AlertResult:
    """One search's new papers, grouped by the source they came from."""
    name: str
    query: str
    by_source: Dict[str, List[Dict]] = field(default_factory=dict)
    # Papers the source reports in the window beyond those fetched
    # (raise LIXPLORE_MAX_RESULTS to see them)
    not_shown: Dict[str, int] = field(default_factory=dict)

    @property
    def articles(self) -> List[Dict]:
        return [a for items in self.by_source.values() for a in items]

    @property
    def total(self) -> int:
        return len(self.articles)

    @property
    def counts(self) -> Dict[str, int]:
        return {s: len(items) for s, items in self.by_source.items()}


def _label(source: str) -> str:
    return SOURCE_LABELS.get(source, source)


def _source_head(r: AlertResult, source: str) -> str:
    """'PubMed: 5 new' or 'PubMed: 20 new (+39 more not shown)'."""
    text = f"{_label(source)}: {len(r.by_source[source])} new"
    if r.not_shown.get(source):
        text += f" (+{r.not_shown[source]} more matches not listed)"
    return text

# Inline formatting per chat style: (escape, bold, italic, link)
_STYLES = {
    # Telegram and Matrix HTML
    "html": (html.escape, "<b>{}</b>".format, "<i>{}</i>".format,
             lambda t, u: f'<a href="{html.escape(u)}">{t}</a>'),
    # CommonMark: Teams, ntfy, custom webhooks
    "markdown": (lambda s: s.replace("[", "(").replace("]", ")").replace("*", "\\*"),
                 "**{}**".format, "_{}_".format, lambda t, u: f"[{t}]({u})"),
    # Discord: angle brackets stop every link unfurling into a preview
    "discord": (lambda s: s.replace("[", "(").replace("]", ")").replace("*", "\\*"),
                "**{}**".format, "*{}*".format, lambda t, u: f"[{t}](<{u}>)"),
    # Slack mrkdwn, also used by Google Chat
    "slack": (lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
              "*{}*".format, "_{}_".format, lambda t, u: f"<{u}|{t}>"),
    "plain": (str, str, str, lambda t, u: f"{t}\n    {u}"),
}

def _authors(article: Dict, limit: int = 3) -> str:
    authors = article.get("authors") or []
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",") if a.strip()]
    if not authors:
        return ""
    shown = ", ".join(authors[:limit])
    return shown + (" et al." if len(authors) > limit else "")


def _link(article: Dict) -> str:
    if article.get("url"):
        return article["url"]
    if article.get("doi"):
        return f"https://doi.org/{article['doi']}"
    return ""


def _counts(counts: Dict[str, int]) -> str:
    return ", ".join(f"{_label(s)} {n}" for s, n in counts.items() if n)


def subject(results: List[AlertResult]) -> str:
    total = sum(r.total for r in results)
    return f"Lixplore: {total} new paper{'s' if total != 1 else ''} ({date.today():%d %b %Y})"


def messages(results: List[AlertResult], failures: List[str], style: str, limit: int) -> List[str]:
    """Chat-formatted digest split into messages of at most `limit` bytes."""
    esc, bold, italic, link = _STYLES[style]
    blocks = [bold(esc("📚 " + subject(results)))]
    for r in results:
        head = "\n" + bold(esc(f"🔎 {r.name}")) + esc(f" — {r.total} new")
        if r.total:
            head += " " + italic(esc(f"({_counts(r.counts)})"))
        blocks.append(head)
        for source, articles in r.by_source.items():
            blocks.append(bold(esc(f"▸ {_source_head(r, source)}")))
            for i, a in enumerate(articles, 1):
                title = esc(a.get("title") or "Untitled")
                url = _link(a)
                line = f"{i}. " + (link(title, url) if url else title)
                meta = " · ".join(x for x in (_authors(a), a.get("journal") or "", str(a.get("year") or "")) if x)
                if meta:
                    line += "\n    " + italic(esc(meta))
                blocks.append(line)
    if failures:
        blocks.append("\n" + esc("⚠️ Failed: " + "; ".join(failures)))
    return chunk(blocks, limit)


def _size(s: str) -> int:
    # Bytes, not characters: several chat APIs (WeCom, DingTalk, Feishu) cap
    # payloads in UTF-8 bytes, and bytes >= characters keeps the rest safe too
    return len(s.encode("utf-8"))


def _truncate(s: str, limit: int) -> str:
    while _size(s) > limit - 3:
        s = s[: max(1, len(s) - max(1, (_size(s) - limit) // 3 + 1))]
    return s + "…"


def chunk(blocks: List[str], limit: int) -> List[str]:
    out, current = [], ""
    for block in blocks:
        if _size(block) > limit:
            block = _truncate(block, limit)
        if current and _size(current) + _size(block) + 1 > limit:
            out.append(current)
            current = block
        else:
            current = f"{current}\n{block}" if current else block
    if current:
        out.append(current)
    return out


def short_summary(results: List[AlertResult], limit: int) -> str:
    """Counts plus the first titles, for push services with tiny message limits."""
    lines = []
    for r in results:
        lines.append(f"{r.name}: {r.total} new ({_counts(r.counts)})" if r.total else f"{r.name}: 0 new")
        for a in r.articles[:3]:
            lines.append(f"• {a.get('title') or 'Untitled'}")
    text = "\n".join(lines)
    return text if _size(text) <= limit else _truncate(text, limit)

def email_html(results: List[AlertResult], failures: List[str]) -> str:
    muted = "color:#57606a;font-size:13px"
    parts = [
        '<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:760px;color:#1f2328">',
        f'<h2 style="margin:0 0 12px">{html.escape(subject(results))}</h2>',
    ]
    for r in results:
        parts.append(
            f'<h3 style="margin:24px 0 4px;border-bottom:1px solid #d0d7de;padding-bottom:4px">'
            f'{html.escape(r.name)} <span style="font-weight:normal;color:#57606a">— {r.total} new</span></h3>'
        )
        sub = f"Query: <code>{html.escape(r.query)}</code>"
        if r.total:
            sub += f" · {html.escape(_counts(r.counts))}"
        parts.append(f'<div style="{muted};margin-bottom:8px">{sub}</div>')
        if not r.total:
            parts.append('<p style="color:#57606a">No new papers.</p>')
        for source, articles in r.by_source.items():
            parts.append(f'<h4 style="margin:14px 0 4px">{html.escape(_source_head(r, source))}</h4>')
            parts.append('<ol style="padding-left:20px;margin-top:4px">')
            for a in articles:
                title = html.escape(a.get("title") or "Untitled")
                link = _link(a)
                title_html = f'<a href="{html.escape(link)}" style="color:#0969da">{title}</a>' if link else title
                meta = " · ".join(html.escape(x) for x in (
                    _authors(a), a.get("journal") or "", str(a.get("year") or "")) if x)
                parts.append(f'<li style="margin-bottom:10px">{title_html}<div style="{muted}">{meta}</div></li>')
            parts.append("</ol>")
    if failures:
        parts.append(f'<p style="color:#9a6700">⚠️ Failed: {html.escape("; ".join(failures))}</p>')
    if any(r.not_shown for r in results):
        parts.append(f'<p style="{muted}">"More matches not listed" = further papers the database found in the search window '
                     "(some may have been sent before). Raise LIXPLORE_MAX_RESULTS to list them.</p>")
    parts.append(
        '<p style="color:#8c959f;font-size:12px;margin-top:24px">Sent by '
        '<a href="https://github.com/pryndor/Lixplore_cli" style="color:#8c959f">Lixplore Alerts</a>. '
        "Change searches under your fork's Settings → Secrets and variables → Actions → Variables.</p>"
    )
    parts.append("</div>")
    return "\n".join(parts)


def plain_text(results: List[AlertResult], failures: List[str]) -> str:
    lines = [subject(results), ""]
    for r in results:
        lines.append(f"== {r.name} — {r.total} new" + (f" ({_counts(r.counts)})" if r.total else ""))
        lines.append(f"   query: {r.query}")
        for source, articles in r.by_source.items():
            lines.append(f"-- {_source_head(r, source)}")
            for i, a in enumerate(articles, 1):
                lines.append(f"{i}. {a.get('title') or 'Untitled'}")
                meta = " · ".join(x for x in (_authors(a), a.get("journal") or "", str(a.get("year") or "")) if x)
                if meta:
                    lines.append(f"   {meta}")
                if _link(a):
                    lines.append(f"   {_link(a)}")
        lines.append("")
    if failures:
        lines.append("Failed: " + "; ".join(failures))
    return "\n".join(lines)


def markdown(results: List[AlertResult], failures: List[str]) -> str:
    lines = [f"## {subject(results)}", ""]
    for r in results:
        lines.append(f"### {r.name} — {r.total} new")
        lines.append(f"`{r.query}`" + (f" · {_counts(r.counts)}" if r.total else ""))
        lines.append("")
        for source, articles in r.by_source.items():
            lines.append(f"**{_source_head(r, source)}**")
            lines.append("")
            for i, a in enumerate(articles, 1):
                title = (a.get("title") or "Untitled").replace("[", "(").replace("]", ")")
                link = _link(a)
                lines.append(f"{i}. [{title}]({link})" if link else f"{i}. {title}")
            lines.append("")
    if failures:
        lines.append("> ⚠️ Failed: " + "; ".join(failures))
    return "\n".join(lines)
