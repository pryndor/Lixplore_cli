"""
Turns alert results into Telegram, email (HTML + text) and Markdown digests.
"""

import html
from datetime import date
from typing import Dict, List, Tuple

SOURCE_LABELS = {
    "pubmed": "PubMed", "europepmc": "EuropePMC", "arxiv": "arXiv",
    "crossref": "Crossref", "doaj": "DOAJ",
}

# (alert name, query, new articles, per-source counts)
AlertResult = Tuple[str, str, List[Dict], Dict[str, int]]

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
    return ", ".join(f"{SOURCE_LABELS.get(s, s)} {n}" for s, n in counts.items() if n)


def subject(results: List[AlertResult]) -> str:
    total = sum(len(r[2]) for r in results)
    return f"Lixplore: {total} new paper{'s' if total != 1 else ''} ({date.today():%d %b %Y})"


def messages(results: List[AlertResult], failures: List[str], style: str, limit: int) -> List[str]:
    """Chat-formatted digest split into messages of at most `limit` characters."""
    esc, bold, italic, link = _STYLES[style]
    blocks = [bold(esc("📚 " + subject(results)))]
    for name, _query, articles, counts in results:
        head = "\n" + bold(esc(f"🔎 {name}")) + esc(f" — {len(articles)} new")
        if counts:
            head += " " + italic(esc(f"({_counts(counts)})"))
        blocks.append(head)
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
    for name, _query, articles, _counts_ in results:
        lines.append(f"{name}: {len(articles)} new")
        for a in articles[:3]:
            lines.append(f"• {a.get('title') or 'Untitled'}")
    text = "\n".join(lines)
    return text if _size(text) <= limit else _truncate(text, limit)

def email_html(results: List[AlertResult], failures: List[str]) -> str:
    parts = [
        '<div style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:760px;color:#1f2328">',
        f'<h2 style="margin:0 0 12px">{html.escape(subject(results))}</h2>',
    ]
    for name, query, articles, counts in results:
        parts.append(
            f'<h3 style="margin:24px 0 4px;border-bottom:1px solid #d0d7de;padding-bottom:4px">'
            f'{html.escape(name)} <span style="font-weight:normal;color:#57606a">— {len(articles)} new</span></h3>'
        )
        sub = f"Query: <code>{html.escape(query)}</code>"
        if counts:
            sub += f" · {html.escape(_counts(counts))}"
        parts.append(f'<div style="color:#57606a;font-size:13px;margin-bottom:8px">{sub}</div>')
        if not articles:
            parts.append('<p style="color:#57606a">No new papers.</p>')
            continue
        parts.append('<ol style="padding-left:20px">')
        for a in articles:
            title = html.escape(a.get("title") or "Untitled")
            link = _link(a)
            title_html = f'<a href="{html.escape(link)}" style="color:#0969da">{title}</a>' if link else title
            meta = " · ".join(html.escape(x) for x in (
                _authors(a), a.get("journal") or "", str(a.get("year") or ""),
                SOURCE_LABELS.get(a.get("source", ""), a.get("source", "")),
            ) if x)
            parts.append(
                f'<li style="margin-bottom:10px">{title_html}'
                f'<div style="color:#57606a;font-size:13px">{meta}</div></li>'
            )
        parts.append("</ol>")
    if failures:
        parts.append(f'<p style="color:#9a6700">⚠️ Failed: {html.escape("; ".join(failures))}</p>')
    parts.append(
        '<p style="color:#8c959f;font-size:12px;margin-top:24px">Sent by '
        '<a href="https://github.com/pryndor/Lixplore_cli" style="color:#8c959f">Lixplore Alerts</a>. '
        "Change queries under your fork's Settings → Secrets and variables → Actions → Variables.</p>"
    )
    parts.append("</div>")
    return "\n".join(parts)


def plain_text(results: List[AlertResult], failures: List[str]) -> str:
    lines = [subject(results), ""]
    for name, query, articles, counts in results:
        lines.append(f"== {name} — {len(articles)} new ({_counts(counts)})" if counts else f"== {name} — {len(articles)} new")
        lines.append(f"   query: {query}")
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
    for name, query, articles, counts in results:
        lines.append(f"### {name} — {len(articles)} new")
        lines.append(f"`{query}`" + (f" · {_counts(counts)}" if counts else ""))
        lines.append("")
        for i, a in enumerate(articles, 1):
            title = (a.get("title") or "Untitled").replace("[", "(").replace("]", ")")
            link = _link(a)
            lines.append(f"{i}. [{title}]({link})" if link else f"{i}. {title}")
        lines.append("")
    if failures:
        lines.append("> ⚠️ Failed: " + "; ".join(failures))
    return "\n".join(lines)
