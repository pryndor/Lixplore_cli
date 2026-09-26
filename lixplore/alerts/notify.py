"""
Delivery channels. Each one switches on when its required settings exist,
so users enable a channel just by adding its secrets.

To add a channel: write send_<name>(env, digest) and list it in CHANNELS.
"""

import base64
import hashlib
import hmac
import html
import json
import os
import re
import smtplib
import time
import uuid
from dataclasses import dataclass, field
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from string import Template
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import quote_plus

import requests

from . import render


@dataclass
class Digest:
    """Everything a channel may need; each channel picks its own format."""
    results: List[render.AlertResult]
    failures: List[str] = field(default_factory=list)
    attachment: Optional[str] = None
    test_text: Optional[str] = None  # set for `lixplore-alerts test`

    @property
    def subject(self) -> str:
        return "Lixplore Alerts: test message" if self.test_text else render.subject(self.results)

    def chat(self, style: str, limit: int) -> List[str]:
        if self.test_text:
            esc = html.escape if style == "html" else str
            return [esc(self.test_text)]
        return render.messages(self.results, self.failures, style, limit)

    def text(self) -> str:
        return self.test_text or render.plain_text(self.results, self.failures)

    def email_html(self) -> str:
        if self.test_text:
            return "<p>" + html.escape(self.test_text).replace("\n", "<br>") + "</p>"
        return render.email_html(self.results, self.failures)

    def short(self, limit: int) -> str:
        return self.test_text or render.short_summary(self.results, limit)


def _split(value: str) -> List[str]:
    return [v.strip() for v in re.split(r"[,;\n]", value or "") if v.strip()]


def _post(url: str, retries: int = 3, **kwargs) -> requests.Response:
    """POST with retry on rate limits. Errors never include the URL, which may hold a token."""
    kwargs.setdefault("timeout", 30)
    method = kwargs.pop("method", "POST")
    for attempt in range(retries):
        resp = requests.request(method, url, **kwargs)
        if resp.status_code == 429 and attempt < retries - 1:
            wait = resp.headers.get("Retry-After") or 5
            try:
                wait = float(wait)
            except ValueError:
                wait = 5
            time.sleep(min(wait, 30))
            continue
        if not resp.ok:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        return resp
    return resp


def _pace(i: int) -> None:
    if i:
        time.sleep(1)  # chat webhooks rate-limit bursts of messages


def _verify_ssl(env: Dict[str, str]) -> bool:
    # Self-hosted endpoints (ntfy, Gotify, AstrBot, custom) may use self-signed certs
    return (env.get("WEBHOOK_VERIFY_SSL") or "true").lower() not in ("0", "false", "no", "off")


# ---------------------------------------------------------------- email

# (server, port, implicit SSL) by sender domain, so most users need only
# EMAIL_SENDER + EMAIL_PASSWORD
SMTP_BY_DOMAIN = {
    "gmail.com": ("smtp.gmail.com", 587, False),
    "googlemail.com": ("smtp.gmail.com", 587, False),
    "outlook.com": ("smtp-mail.outlook.com", 587, False),
    "hotmail.com": ("smtp-mail.outlook.com", 587, False),
    "live.com": ("smtp-mail.outlook.com", 587, False),
    "yahoo.com": ("smtp.mail.yahoo.com", 465, True),
    "icloud.com": ("smtp.mail.me.com", 587, False),
    "me.com": ("smtp.mail.me.com", 587, False),
    "zoho.com": ("smtp.zoho.com", 465, True),
    "proton.me": ("smtp.protonmail.ch", 587, False),
    "qq.com": ("smtp.qq.com", 465, True),
    "163.com": ("smtp.163.com", 465, True),
}


def _smtp_settings(env: Dict[str, str]) -> Tuple[str, int, bool]:
    if env.get("SMTP_SERVER"):
        port = int(env.get("SMTP_PORT") or 587)
        return env["SMTP_SERVER"], port, port == 465
    domain = env["EMAIL_SENDER"].rsplit("@", 1)[-1].lower()
    if domain in SMTP_BY_DOMAIN:
        return SMTP_BY_DOMAIN[domain]
    raise RuntimeError(f"No known SMTP server for '{domain}'. Set SMTP_SERVER and SMTP_PORT.")


def send_email(env: Dict[str, str], digest: Digest) -> None:
    server, port, use_ssl = _smtp_settings(env)
    sender = env["EMAIL_SENDER"]
    receivers = _split(env.get("EMAIL_RECEIVERS")) or [sender]

    msg = MIMEMultipart("mixed")
    msg["Subject"] = digest.subject
    msg["From"] = formataddr((env.get("EMAIL_SENDER_NAME") or "Lixplore Alerts", sender))
    msg["To"] = ", ".join(receivers)
    body = MIMEMultipart("alternative")
    body.attach(MIMEText(digest.text(), "plain", "utf-8"))
    body.attach(MIMEText(digest.email_html(), "html", "utf-8"))
    msg.attach(body)
    if digest.attachment and os.path.isfile(digest.attachment):
        with open(digest.attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(digest.attachment))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(digest.attachment)}"'
        msg.attach(part)

    smtp = smtplib.SMTP_SSL(server, port, timeout=30) if use_ssl else smtplib.SMTP(server, port, timeout=30)
    try:
        if not use_ssl:
            smtp.starttls()
        smtp.login(sender, env["EMAIL_PASSWORD"])
        smtp.sendmail(sender, receivers, msg.as_string())
    finally:
        smtp.quit()


# ---------------------------------------------------------------- chat apps

def send_telegram(env: Dict[str, str], digest: Digest) -> None:
    base = f"https://api.telegram.org/bot{env['TELEGRAM_BOT_TOKEN']}"
    extra = {"message_thread_id": env["TELEGRAM_MESSAGE_THREAD_ID"]} if env.get("TELEGRAM_MESSAGE_THREAD_ID") else {}
    for chat_id in _split(env["TELEGRAM_CHAT_ID"]):
        for text in digest.chat("html", 4000):
            _post(base + "/sendMessage", data={
                "chat_id": chat_id, "text": text, "parse_mode": "HTML",
                "disable_web_page_preview": "true", **extra})
        if digest.attachment and os.path.isfile(digest.attachment):
            with open(digest.attachment, "rb") as f:
                content = f.read()
            _post(base + "/sendDocument", data={"chat_id": chat_id, **extra},
                  files={"document": (os.path.basename(digest.attachment), content)})


def send_discord(env: Dict[str, str], digest: Digest) -> None:
    messages = digest.chat("discord", 1900)
    for url in _split(env.get("DISCORD_WEBHOOK_URL")):
        for i, text in enumerate(messages):
            _pace(i)
            _post(url, json={"content": text, "username": "Lixplore Alerts"})
        if digest.attachment and os.path.isfile(digest.attachment):
            with open(digest.attachment, "rb") as f:
                _post(url, files={"file": (os.path.basename(digest.attachment), f.read())})
    if env.get("DISCORD_BOT_TOKEN") and env.get("DISCORD_MAIN_CHANNEL_ID"):
        url = f"https://discord.com/api/v10/channels/{env['DISCORD_MAIN_CHANNEL_ID']}/messages"
        headers = {"Authorization": f"Bot {env['DISCORD_BOT_TOKEN']}"}
        for i, text in enumerate(messages):
            _pace(i)
            _post(url, headers=headers, json={"content": text})


def send_slack(env: Dict[str, str], digest: Digest) -> None:
    # Webhook form also works for Mattermost and Rocket.Chat
    messages = digest.chat("slack", 3500)
    for url in _split(env.get("SLACK_WEBHOOK_URL")):
        for i, text in enumerate(messages):
            _pace(i)
            _post(url, json={"text": text, "unfurl_links": False})
    if env.get("SLACK_BOT_TOKEN") and env.get("SLACK_CHANNEL_ID"):
        headers = {"Authorization": f"Bearer {env['SLACK_BOT_TOKEN']}"}
        for i, text in enumerate(messages):
            _pace(i)
            resp = _post("https://slack.com/api/chat.postMessage", headers=headers, json={
                "channel": env["SLACK_CHANNEL_ID"], "text": text, "unfurl_links": False})
            if not resp.json().get("ok"):
                raise RuntimeError(f"Slack API: {resp.json().get('error')}")


def send_google_chat(env: Dict[str, str], digest: Digest) -> None:
    for url in _split(env["GOOGLE_CHAT_WEBHOOK_URL"]):
        for i, text in enumerate(digest.chat("slack", 3900)):
            _pace(i)
            _post(url, json={"text": text})


def send_teams(env: Dict[str, str], digest: Digest) -> None:
    # Teams "Workflows" webhook (the replacement for retired Office 365 connectors)
    for url in _split(env["TEAMS_WEBHOOK_URL"]):
        for i, text in enumerate(digest.chat("markdown", 20000)):
            _pace(i)
            card = {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard", "version": "1.4",
                "body": [{"type": "TextBlock", "text": text, "wrap": True}],
            }
            _post(url, json={"type": "message", "attachments": [
                {"contentType": "application/vnd.microsoft.card.adaptive", "content": card}]})


def send_matrix(env: Dict[str, str], digest: Digest) -> None:
    server = env["MATRIX_HOMESERVER"].rstrip("/")
    room = requests.utils.quote(env["MATRIX_ROOM_ID"], safe="")
    headers = {"Authorization": f"Bearer {env['MATRIX_ACCESS_TOKEN']}"}
    for text in digest.chat("html", 30000):
        plain = html.unescape(re.sub(r"<[^>]+>", "", text))
        url = f"{server}/_matrix/client/v3/rooms/{room}/send/m.room.message/{uuid.uuid4().hex}"
        _post(url, method="PUT", headers=headers, json={
            "msgtype": "m.text", "body": plain,
            "format": "org.matrix.custom.html", "formatted_body": text.replace("\n", "<br>")})


# ---------------------------------------------------------------- push

def send_ntfy(env: Dict[str, str], digest: Digest) -> None:
    headers = {"Title": digest.subject.encode("utf-8"), "Markdown": "yes", "Tags": "books"}
    if env.get("NTFY_TOKEN"):
        headers["Authorization"] = f"Bearer {env['NTFY_TOKEN']}"
    for url in _split(env["NTFY_URL"]):
        for i, text in enumerate(digest.chat("markdown", 3500)):
            _pace(i)
            _post(url, data=text.encode("utf-8"), headers=headers, verify=_verify_ssl(env))


def send_pushover(env: Dict[str, str], digest: Digest) -> None:
    _post("https://api.pushover.net/1/messages.json", data={
        "token": env["PUSHOVER_API_TOKEN"], "user": env["PUSHOVER_USER_KEY"],
        "title": digest.subject[:250], "message": digest.short(1000)})


def send_gotify(env: Dict[str, str], digest: Digest) -> None:
    url = env["GOTIFY_URL"].rstrip("/")
    if not url.endswith("/message"):
        url += "/message"
    _post(url, headers={"X-Gotify-Key": env["GOTIFY_TOKEN"]}, verify=_verify_ssl(env), json={
        "title": digest.subject,
        "message": "\n".join(digest.chat("markdown", 10 ** 9)),
        "extras": {"client::display": {"contentType": "text/markdown"}},
    })


# ---------------------------------------------------------------- China-region apps

def _check_errcode(resp: requests.Response, key: str = "errcode") -> None:
    # These APIs answer HTTP 200 with an error code in the body
    body = resp.json() if resp.content else {}
    code = body.get(key, body.get("code", 0))
    if code not in (0, 200, None):
        raise RuntimeError(f"{code}: {body.get('errmsg') or body.get('msg') or body.get('message')}")


def send_wechat(env: Dict[str, str], digest: Digest) -> None:
    # WeCom (WeChat Work) group robot
    msg_type = (env.get("WECHAT_MSG_TYPE") or "markdown").lower()
    style = "plain" if msg_type == "text" else "markdown"
    limit = 2000 if msg_type == "text" else 4000
    for i, text in enumerate(digest.chat(style, limit)):
        _pace(i)
        _check_errcode(_post(env["WECHAT_WEBHOOK_URL"], json={"msgtype": msg_type, msg_type: {"content": text}}))


def send_feishu(env: Dict[str, str], digest: Digest) -> None:
    # Feishu / Lark custom bot webhook, with optional signing secret and keyword
    keyword = env.get("FEISHU_WEBHOOK_KEYWORD", "")
    for i, text in enumerate(digest.chat("markdown", 18000)):
        _pace(i)
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {"title": {"tag": "plain_text", "content": digest.subject}},
                "elements": [{"tag": "div", "text": {"tag": "lark_md",
                                                     "content": f"{keyword} {text}" if keyword else text}}],
            },
        }
        if env.get("FEISHU_WEBHOOK_SECRET"):
            ts = str(int(time.time()))
            to_sign = f"{ts}\n{env['FEISHU_WEBHOOK_SECRET']}".encode("utf-8")
            payload["timestamp"] = ts
            payload["sign"] = base64.b64encode(hmac.new(to_sign, digestmod=hashlib.sha256).digest()).decode()
        _check_errcode(_post(env["FEISHU_WEBHOOK_URL"], json=payload), key="code")


def send_dingtalk(env: Dict[str, str], digest: Digest) -> None:
    for i, text in enumerate(digest.chat("markdown", 18000)):
        _pace(i)
        url = env["DINGTALK_WEBHOOK_URL"]
        if env.get("DINGTALK_SECRET"):
            ts = str(round(time.time() * 1000))
            mac = hmac.new(env["DINGTALK_SECRET"].encode("utf-8"),
                           f"{ts}\n{env['DINGTALK_SECRET']}".encode("utf-8"), hashlib.sha256).digest()
            url += ("&" if "?" in url else "?") + f"timestamp={ts}&sign={quote_plus(base64.b64encode(mac))}"
        _check_errcode(_post(url, json={"msgtype": "markdown",
                                        "markdown": {"title": digest.subject, "text": text}}))


def send_pushplus(env: Dict[str, str], digest: Digest) -> None:
    for i, text in enumerate(digest.chat("markdown", 18000)):
        _pace(i)
        payload = {"token": env["PUSHPLUS_TOKEN"], "title": digest.subject,
                   "content": text, "template": "markdown"}
        if env.get("PUSHPLUS_TOPIC"):
            payload["topic"] = env["PUSHPLUS_TOPIC"]
        _check_errcode(_post("https://www.pushplus.plus/send", json=payload), key="code")


def send_serverchan3(env: Dict[str, str], digest: Digest) -> None:
    key = env["SERVERCHAN3_SENDKEY"]
    match = re.match(r"sctp(\d+)t", key)
    url = f"https://{match.group(1)}.push.ft07.com/send/{key}.send" if match else f"https://sctapi.ftqq.com/{key}.send"
    text = "\n".join(digest.chat("markdown", 10 ** 9))
    _check_errcode(_post(url, json={"title": digest.subject, "desp": text}), key="code")


def send_astrbot(env: Dict[str, str], digest: Digest) -> None:
    body = json.dumps({"content": digest.email_html()}, sort_keys=True)
    headers = {"Content-Type": "application/json"}
    if env.get("ASTRBOT_TOKEN"):
        ts = str(int(time.time()))
        headers["X-Timestamp"] = ts
        headers["X-Signature"] = hmac.new(env["ASTRBOT_TOKEN"].encode("utf-8"),
                                          f"{ts}.{body}".encode("utf-8"), hashlib.sha256).hexdigest()
    _post(env["ASTRBOT_URL"], data=body.encode("utf-8"), headers=headers, verify=_verify_ssl(env))


# ---------------------------------------------------------------- automation

def send_custom_webhook(env: Dict[str, str], digest: Digest) -> None:
    """
    JSON POST for n8n, Zapier, Make, IFTTT, Bark, Home Assistant or your own service.

    CUSTOM_WEBHOOK_BODY_TEMPLATE replaces the default payload; it may use
    $title, $title_json, $content and $content_json, e.g.
        {"msg_type": "text", "text": $content_json}
    """
    content = "\n".join(digest.chat("markdown", 10 ** 9))
    template = (env.get("CUSTOM_WEBHOOK_BODY_TEMPLATE") or "").strip()
    if template:
        body = Template(template).safe_substitute(
            title=digest.subject, title_json=json.dumps(digest.subject, ensure_ascii=False),
            content=content, content_json=json.dumps(content, ensure_ascii=False))
        try:
            json.loads(body)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"CUSTOM_WEBHOOK_BODY_TEMPLATE does not render to valid JSON: {e}")
    else:
        body = json.dumps({
            "subject": digest.subject,
            "total": sum(len(r[2]) for r in digest.results),
            "text": digest.text(),
            "markdown": content,
            "alerts": [
                {"name": name, "query": query, "count": len(articles), "by_source": counts,
                 "articles": articles}
                for name, query, articles, counts in digest.results
            ],
            "failures": digest.failures,
            "test": bool(digest.test_text),
        }, default=str, ensure_ascii=False)

    headers = {"Content-Type": "application/json; charset=utf-8"}
    if env.get("CUSTOM_WEBHOOK_BEARER_TOKEN"):
        headers["Authorization"] = f"Bearer {env['CUSTOM_WEBHOOK_BEARER_TOKEN']}"
    for url in _split(env["CUSTOM_WEBHOOK_URLS"]):
        _post(url, data=body.encode("utf-8"), headers=headers, verify=_verify_ssl(env))


def _all(*keys: str) -> Callable[[Dict[str, str]], bool]:
    return lambda env: all(env.get(k) for k in keys)


def _either(*checks: Callable[[Dict[str, str]], bool]) -> Callable[[Dict[str, str]], bool]:
    return lambda env: any(check(env) for check in checks)


# Same channels and variable names as daily_stock_analysis, plus Teams,
# Google Chat and Matrix. (name, is-configured check, sender)
CHANNELS: List[Tuple[str, Callable[[Dict[str, str]], bool], Callable[[Dict[str, str], Digest], None]]] = [
    ("Email", _all("EMAIL_SENDER", "EMAIL_PASSWORD"), send_email),
    ("Telegram", _all("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"), send_telegram),
    ("Discord", _either(_all("DISCORD_WEBHOOK_URL"), _all("DISCORD_BOT_TOKEN", "DISCORD_MAIN_CHANNEL_ID")), send_discord),
    ("Slack", _either(_all("SLACK_WEBHOOK_URL"), _all("SLACK_BOT_TOKEN", "SLACK_CHANNEL_ID")), send_slack),
    ("Microsoft Teams", _all("TEAMS_WEBHOOK_URL"), send_teams),
    ("Google Chat", _all("GOOGLE_CHAT_WEBHOOK_URL"), send_google_chat),
    ("Matrix", _all("MATRIX_HOMESERVER", "MATRIX_ACCESS_TOKEN", "MATRIX_ROOM_ID"), send_matrix),
    ("WeCom", _all("WECHAT_WEBHOOK_URL"), send_wechat),
    ("Feishu", _all("FEISHU_WEBHOOK_URL"), send_feishu),
    ("DingTalk", _all("DINGTALK_WEBHOOK_URL"), send_dingtalk),
    ("ntfy", _all("NTFY_URL"), send_ntfy),
    ("Gotify", _all("GOTIFY_URL", "GOTIFY_TOKEN"), send_gotify),
    ("Pushover", _all("PUSHOVER_USER_KEY", "PUSHOVER_API_TOKEN"), send_pushover),
    ("PushPlus", _all("PUSHPLUS_TOKEN"), send_pushplus),
    ("ServerChan3", _all("SERVERCHAN3_SENDKEY"), send_serverchan3),
    ("AstrBot", _all("ASTRBOT_URL"), send_astrbot),
    ("Custom webhook", _all("CUSTOM_WEBHOOK_URLS"), send_custom_webhook),
]


def configured(env: Dict[str, str]) -> List[str]:
    return [name for name, is_set, _ in CHANNELS if is_set(env)]


def status(env: Dict[str, str]) -> List[Tuple[str, bool]]:
    on = set(configured(env))
    return [(name, name in on) for name, _, _ in CHANNELS]


def deliver(env: Dict[str, str], digest: Digest) -> Dict[str, str]:
    """Send to every configured channel. Returns {channel: error} for failures."""
    errors: Dict[str, str] = {}
    for name, is_set, send in CHANNELS:
        if not is_set(env):
            continue
        try:
            send(env, digest)
            print(f"{name}: sent")
        except Exception as e:  # one broken channel must not block the others
            errors[name] = str(e)
            print(f"{name}: FAILED - {e}")
    return errors
