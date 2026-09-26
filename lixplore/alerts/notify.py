"""
Delivery channels: email (SMTP) and Telegram (Bot API).
"""

import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Dict, List, Optional

import requests

# SMTP settings picked from the sender's domain so most users only need
# EMAIL_SENDER + EMAIL_PASSWORD. (server, port, implicit SSL)
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


def _smtp_settings(email_cfg: Dict[str, str]):
    if email_cfg.get("smtp_server"):
        port = int(email_cfg.get("smtp_port") or 587)
        return email_cfg["smtp_server"], port, port == 465
    domain = email_cfg["sender"].rsplit("@", 1)[-1].lower()
    if domain in SMTP_BY_DOMAIN:
        return SMTP_BY_DOMAIN[domain]
    raise RuntimeError(
        f"No known SMTP server for '{domain}'. Set the SMTP_SERVER and SMTP_PORT secrets."
    )


def send_email(email_cfg: Dict[str, str], subject: str, html_body: str, text_body: str,
               attachment: Optional[str] = None) -> None:
    server, port, use_ssl = _smtp_settings(email_cfg)
    receivers = [r.strip() for r in email_cfg["receivers"].replace(";", ",").split(",") if r.strip()]

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = formataddr((email_cfg.get("sender_name") or "Lixplore Alerts", email_cfg["sender"]))
    msg["To"] = ", ".join(receivers)

    body = MIMEMultipart("alternative")
    body.attach(MIMEText(text_body, "plain", "utf-8"))
    body.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(body)

    if attachment and os.path.isfile(attachment):
        with open(attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
        part["Content-Disposition"] = f'attachment; filename="{os.path.basename(attachment)}"'
        msg.attach(part)

    if use_ssl:
        smtp = smtplib.SMTP_SSL(server, port, timeout=30)
    else:
        smtp = smtplib.SMTP(server, port, timeout=30)
        smtp.starttls()
    try:
        smtp.login(email_cfg["sender"], email_cfg["password"])
        smtp.sendmail(email_cfg["sender"], receivers, msg.as_string())
    finally:
        smtp.quit()


def send_telegram(tg_cfg: Dict[str, str], messages: List[str],
                  attachment: Optional[str] = None) -> None:
    base = f"https://api.telegram.org/bot{tg_cfg['token']}"
    chat_ids = [c.strip() for c in tg_cfg["chat_ids"].split(",") if c.strip()]
    for chat_id in chat_ids:
        extra = {"message_thread_id": tg_cfg["thread_id"]} if tg_cfg.get("thread_id") else {}
        for text in messages:
            _telegram_call(base + "/sendMessage", data={
                "chat_id": chat_id, "text": text, "parse_mode": "HTML",
                "disable_web_page_preview": "true", **extra,
            })
        if attachment and os.path.isfile(attachment):
            with open(attachment, "rb") as f:
                content = f.read()
            _telegram_call(base + "/sendDocument", data={"chat_id": chat_id, **extra},
                           files={"document": (os.path.basename(attachment), content)})


def _telegram_call(url: str, data: Dict, files=None, retries: int = 3) -> None:
    for attempt in range(retries):
        resp = requests.post(url, data=data, files=files, timeout=30)
        if resp.status_code == 429 and attempt < retries - 1:
            wait = resp.json().get("parameters", {}).get("retry_after", 5)
            time.sleep(min(int(wait), 30))
            continue
        if not resp.ok:
            # Never echo the URL: it contains the bot token
            description = resp.json().get("description", resp.text[:200]) if resp.content else ""
            raise RuntimeError(f"Telegram API error {resp.status_code}: {description}")
        return
