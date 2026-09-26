# Paper Alerts (Email, Telegram, Discord, Slack & more)

Get new papers matching your searches delivered by email, Telegram, Discord, Slack, Teams and 12 other channels on a schedule, run for free by GitHub Actions. You don't need a server, and you don't edit any files: everything is set in your fork's **Settings**.

Each digest lists only papers that are new since the last one, grouped by search, with title, authors, journal and a link. A CSV (or BibTeX/RIS) of the same papers is attached, ready for Zotero or Mendeley.

## Setup (about 5 minutes)

### 1. Fork the repository

Click **Fork** on [github.com/pryndor/Lixplore_cli](https://github.com/pryndor/Lixplore_cli).

In your fork, open the **Actions** tab and click **"I understand my workflows, go ahead and enable them"**. GitHub turns scheduled workflows off in new forks until you do this.

### 2. Add your searches

Go to **Settings → Secrets and variables → Actions → Variables → New repository variable**.

Name: `LIXPLORE_QUERIES`. Value: one search per line.

```
semaglutide AND obesity
CRISPR base editing
```

To give a search a name, or its own sources, use `name | query | sources`:

```
GLP-1 | semaglutide AND obesity | pubmed,europepmc
LLM agents | large language model agents | arxiv
```

Sources: `pubmed`, `europepmc`, `arxiv`, `crossref`, `doaj`, or the CLI letters (`PEX`). Queries use each source's normal search syntax, the same as `lixplore -q`.

!!! tip "Keep your topics private"
    Variables are visible to anyone who can see the repository. To keep searches private, create `LIXPLORE_QUERIES` as a **Secret** instead. Both work.

### 3. Add at least one delivery channel

Add these under **Settings → Secrets and variables → Actions → Secrets**. Configure as many channels as you like; every configured one receives the digest. Variable names match the daily_stock_analysis project, so the same secrets work in both.

#### Email

| Secret | Value |
|---|---|
| `EMAIL_SENDER` | Address that sends the digest, e.g. `you@gmail.com` |
| `EMAIL_PASSWORD` | An **app password**, not your normal password |
| `EMAIL_RECEIVERS` | Optional. Comma-separated recipients. Defaults to the sender |

For Gmail, create an app password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords); 2-Step Verification must be on. The SMTP server is picked automatically for Gmail, Outlook/Hotmail, Yahoo, iCloud, Zoho, Proton, QQ and 163. For any other provider, also add `SMTP_SERVER` and `SMTP_PORT`.

#### Telegram

| Secret | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | From [@BotFather](https://t.me/BotFather): send `/newbot` and copy the token |
| `TELEGRAM_CHAT_ID` | Your chat ID. Comma-separate several to send to more than one chat |
| `TELEGRAM_MESSAGE_THREAD_ID` | Optional. A topic ID in a forum-style group |

To find your chat ID, send any message to your new bot, then open `https://api.telegram.org/bot<TOKEN>/getUpdates` and copy `"chat":{"id": ...}`. For a group, add the bot to the group first; group IDs start with `-`.

#### Other channels

| Channel | Secrets | Notes |
|---|---|---|
| Discord | `DISCORD_WEBHOOK_URL` | Channel → Edit → Integrations → Webhooks. Or bot mode: `DISCORD_BOT_TOKEN` + `DISCORD_MAIN_CHANNEL_ID` |
| Slack | `SLACK_WEBHOOK_URL` | Incoming Webhooks app. Or bot mode: `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID`. The webhook form also works for Mattermost and Rocket.Chat |
| Microsoft Teams | `TEAMS_WEBHOOK_URL` | Channel → Workflows → "Post to a channel when a webhook request is received" |
| Google Chat | `GOOGLE_CHAT_WEBHOOK_URL` | Space → Apps & integrations → Webhooks |
| Matrix / Element | `MATRIX_HOMESERVER`, `MATRIX_ACCESS_TOKEN`, `MATRIX_ROOM_ID` | e.g. `https://matrix.org`, a bot account's token, `!abc:matrix.org` |
| WeCom (WeChat Work) | `WECHAT_WEBHOOK_URL` | Group robot URL. Variable `WECHAT_MSG_TYPE=text` if markdown doesn't render |
| Feishu / Lark | `FEISHU_WEBHOOK_URL` | Custom bot. Optional `FEISHU_WEBHOOK_SECRET` (signature check) and `FEISHU_WEBHOOK_KEYWORD` (keyword check) |
| DingTalk | `DINGTALK_WEBHOOK_URL` | Robot URL. Optional `DINGTALK_SECRET` for signed requests |
| ntfy | `NTFY_URL` | Full topic URL, e.g. `https://ntfy.sh/my-papers-x7k2`. Optional `NTFY_TOKEN` |
| Gotify | `GOTIFY_URL`, `GOTIFY_TOKEN` | Your server URL and an application token |
| Pushover | `PUSHOVER_USER_KEY`, `PUSHOVER_API_TOKEN` | Sends a short summary (Pushover caps messages at 1024 characters) |
| PushPlus | `PUSHPLUS_TOKEN` | Optional `PUSHPLUS_TOPIC` for group push |
| ServerChan3 | `SERVERCHAN3_SENDKEY` | |
| AstrBot | `ASTRBOT_URL` | Optional `ASTRBOT_TOKEN` signs requests |
| Custom webhook | `CUSTOM_WEBHOOK_URLS` | Comma-separated. See below |

Set `WEBHOOK_VERIFY_SSL=false` only for a self-hosted ntfy, Gotify, AstrBot or custom endpoint with a self-signed certificate.

#### Custom webhook: WhatsApp, SMS and anything else

`CUSTOM_WEBHOOK_URLS` receives a JSON POST with `subject`, `total`, `text`, `markdown`, and `alerts` (each with its `articles`). Point it at n8n, Zapier, Make or IFTTT to forward digests to WhatsApp, SMS, Notion, a spreadsheet or anything those tools support. Add `CUSTOM_WEBHOOK_BEARER_TOKEN` if the endpoint needs auth.

To send a different body shape, set `CUSTOM_WEBHOOK_BODY_TEMPLATE` (a Variable). It can use `$title`, `$title_json`, `$content` and `$content_json`. For example, for Bark:

```
{"title": $title_json, "body": $content_json}
```

### 4. Test it

Open **Actions → Lixplore Alerts → Run workflow**:

- **test** sends a short "you're set up" message to every configured channel.
- **dry-run** fetches papers and shows the digest on the run page without sending anything.
- **run** does a real send.

That's it. From now on the digest arrives automatically.

## Schedule

Set these as Variables:

| Variable | Default | Example |
|---|---|---|
| `LIXPLORE_SEND_DAYS` | `daily` | `mon-fri`, `mon,thu`, `mon` |
| `LIXPLORE_SEND_HOUR_UTC` | `6` | `2` for about 07:30 in India, `13` for about 09:00 US Eastern |

GitHub schedules can't read variables, so the workflow wakes up every hour and sends once per send day, as soon as the chosen hour has passed. GitHub may start scheduled runs 5–30 minutes late. Hourly wake-ups are free on public repositories. On a **private** fork each check counts as about one Actions minute, roughly 720 of the 2,000 free minutes a month.

## All settings

Everything is optional except `LIXPLORE_QUERIES` and one delivery channel.

| Name | Where | Default | Meaning |
|---|---|---|---|
| `LIXPLORE_QUERIES` | Variable or Secret | — | Searches, as above |
| `LIXPLORE_SOURCES` | Variable | `pubmed,europepmc,arxiv` | Sources for lines that don't list their own |
| `LIXPLORE_MAX_RESULTS` | Variable | `20` | Newest papers fetched per search per source |
| `LIXPLORE_LOOKBACK_DAYS` | Variable | `auto` | Search window. `auto` = longest gap between send days + 2 |
| `LIXPLORE_DEDUPE` | Variable | `true` | Merge the same paper found in several sources |
| `LIXPLORE_SEND_WHEN_EMPTY` | Variable | `false` | Send a "0 new papers" digest too |
| `LIXPLORE_ATTACH_FORMAT` | Variable | `csv` | `csv`, `bibtex`, `ris`, `json`, `xlsx` or `none` |
| `EMAIL_SENDER_NAME` | Variable | `Lixplore Alerts` | Display name on the email |
| `PUBMED_EMAIL`, `PUBMED_API_KEY` | Secret | — | Optional. Only raises NCBI's rate limit from 3 to 10 requests/second; useful with many PubMed searches |

## How "new" is decided

Each source is asked only for papers added in the search window: PubMed entry date, Europe PMC first-index date, arXiv submission date, Crossref DOI registration date, and DOAJ record creation date. The window overlaps previous runs by two days to catch records indexed late.

Papers already sent are remembered on a small `lixplore-state` branch that the workflow maintains in your fork. A paper is skipped if its DOI or title matches one sent in the last 120 days. The history is updated only after at least one channel delivers successfully, so a failed send is retried at the next hourly check.

!!! note "Crossref matching is loose"
    Crossref ranks by word overlap and ignores `AND`/`OR`, so filtering it to only new records can surface weak matches. It is not in the default sources for that reason.

## Running locally or on your own server

The same settings work outside GitHub. Put them in a `.env` file (see `.env.example`) and run:

```bash
pip install lixplore-cli
lixplore-alerts check      # validate settings
lixplore-alerts dry-run    # preview, send nothing
lixplore-alerts test       # test message to each channel
lixplore-alerts run        # fetch, send, remember
```

`lixplore --alerts [run|dry-run|test|check]` does the same from the main command. Normal searches (`lixplore -P -q ...`) are unchanged; alerts are an extra feature you only use if you want them.

Schedule it with cron, for example every weekday at 08:00:

```
0 8 * * 1-5  cd ~/lixplore-alerts && lixplore-alerts run
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| Workflow never runs | Enable workflows in your fork's Actions tab |
| `LIXPLORE_QUERIES is not set` | Add the variable. The name is case-sensitive |
| Email `Authentication failed` | Use an app password, not your account password |
| Telegram `chat not found` | Message the bot first, or add it to the group, then recheck the chat ID |
| One channel fails | The others still send. The run shows a warning naming the failed channel |
| No message arrived | Nothing new is not sent unless `LIXPLORE_SEND_WHEN_EMPTY=true`. The run page summary shows what was found |
| Want to resend everything | Delete the `lixplore-state` branch in your fork |
