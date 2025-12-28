# Automation Scripts and Examples

> **Automate literature searches, monitoring, and workflows**

## Table of Contents

- [Shell Scripts](#shell-scripts)
- [Cron Jobs](#cron-jobs)
- [Python Automation](#python-automation)
- [CI/CD Integration](#cicd-integration)
- [Monitoring & Alerts](#monitoring--alerts)

---

## Shell Scripts

### Daily Literature Monitor

**Monitor field for new publications daily:**

```bash
#!/bin/bash
# daily_monitor.sh - Daily literature monitoring script

# Configuration
TOPIC="machine learning healthcare"
DAYS_BACK=1
OUTPUT_DIR="$HOME/Literature/Daily"
LOG_FILE="$HOME/Literature/daily_monitor.log"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Get today's date
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
FILENAME="daily_${TODAY}.xlsx"

# Log start
echo "[$(date)] Starting daily monitor for: $TOPIC" >> "$LOG_FILE"

# Run search
lixplore -A -q "$TOPIC" \
  -d "$YESTERDAY" "$TODAY" \
  -m 100 \
  -D \
  --sort newest \
  -X xlsx \
  -o "$OUTPUT_DIR/$FILENAME" >> "$LOG_FILE" 2>&1

# Check if any results
if [ -f "$OUTPUT_DIR/$FILENAME" ]; then
    LINES=$(wc -l < "$OUTPUT_DIR/$FILENAME")
    echo "[$(date)] Found $LINES new articles" >> "$LOG_FILE"

    # Send notification (optional)
    if [ "$LINES" -gt 1 ]; then
        echo "Daily update: $LINES new articles on $TOPIC" | \
            mail -s "Literature Update - $TODAY" user@example.com
    fi
else
    echo "[$(date)] No results found" >> "$LOG_FILE"
fi

echo "[$(date)] Daily monitor completed" >> "$LOG_FILE"
```

**Usage:**
```bash
chmod +x daily_monitor.sh
./daily_monitor.sh
```

### Weekly Summary Script

**Generate weekly research summary:**

```bash
#!/bin/bash
# weekly_summary.sh - Weekly literature summary

WEEK_START=$(date -d "7 days ago" +%Y-%m-%d)
WEEK_END=$(date +%Y-%m-%d)
WEEK_NUM=$(date +%V)
OUTPUT_DIR="$HOME/Literature/Weekly"

mkdir -p "$OUTPUT_DIR"

TOPICS=("machine learning" "deep learning" "neural networks" "AI healthcare")

echo "Weekly Literature Summary - Week $WEEK_NUM"
echo "Period: $WEEK_START to $WEEK_END"
echo "================================="

for TOPIC in "${TOPICS[@]}"; do
    echo ""
    echo "Topic: $TOPIC"

    FILENAME="week${WEEK_NUM}_${TOPIC// /_}.xlsx"

    lixplore -A -q "$TOPIC" \
        -d "$WEEK_START" "$WEEK_END" \
        -m 200 \
        -D \
        --sort newest \
        -X xlsx \
        -o "$OUTPUT_DIR/$FILENAME"

    if [ -f "$OUTPUT_DIR/$FILENAME" ]; then
        COUNT=$(wc -l < "$OUTPUT_DIR/$FILENAME")
        echo "  Found: $((COUNT - 1)) articles"
    fi
done

echo ""
echo "Summary complete. Files saved to: $OUTPUT_DIR"
```

### Multi-Topic Batch Search

**Search multiple topics in one script:**

```bash
#!/bin/bash
# batch_search.sh - Batch search multiple topics

OUTPUT_DIR="$HOME/Literature/Batch_$(date +%Y%m%d)"
mkdir -p "$OUTPUT_DIR"

# Array of search queries
declare -a QUERIES=(
    "CRISPR gene editing"
    "cancer immunotherapy"
    "machine learning diagnostics"
    "COVID-19 variants"
    "quantum computing"
)

# Search parameters
MAX_RESULTS=100
DATE_FROM="2023-01-01"
DATE_TO="2024-12-31"

for QUERY in "${QUERIES[@]}"; do
    echo "Searching: $QUERY"

    # Create safe filename
    SAFE_NAME=$(echo "$QUERY" | tr ' ' '_' | tr '/' '_')

    # Search and export
    lixplore -A -q "$QUERY" \
        -d "$DATE_FROM" "$DATE_TO" \
        -m "$MAX_RESULTS" \
        -D \
        --enrich \
        -X xlsx,bibtex \
        -o "$OUTPUT_DIR/${SAFE_NAME}"

    # Brief pause to avoid rate limiting
    sleep 2
done

echo "Batch search complete. Results in: $OUTPUT_DIR"
```

---

## Cron Jobs

### Setup Cron Job

**Daily 8 AM literature check:**

```bash
# Edit crontab
crontab -e

# Add this line:
0 8 * * * /home/user/scripts/daily_monitor.sh

# Explanation:
# 0    - Minute (0)
# 8    - Hour (8 AM)
# *    - Every day of month
# *    - Every month
# *    - Every day of week
```

### Weekly Monday Morning Summary

```bash
# Crontab entry for weekly summary every Monday at 9 AM
0 9 * * 1 /home/user/scripts/weekly_summary.sh
```

### Monthly Comprehensive Review

```bash
# First day of every month at 10 AM
0 10 1 * * /home/user/scripts/monthly_review.sh
```

### Monthly Review Script

```bash
#!/bin/bash
# monthly_review.sh - Comprehensive monthly literature review

MONTH=$(date -d "last month" +%Y-%m)
MONTH_START="${MONTH}-01"
MONTH_END=$(date -d "${MONTH_START} +1 month -1 day" +%Y-%m-%d)
OUTPUT_DIR="$HOME/Literature/Monthly/$MONTH"

mkdir -p "$OUTPUT_DIR"

echo "Monthly Review: $MONTH"
echo "Period: $MONTH_START to $MONTH_END"

# Main research topic
lixplore -A -q "main research topic" \
    -d "$MONTH_START" "$MONTH_END" \
    -m 500 \
    -D strict \
    --enrich \
    --stat \
    -X xlsx,bibtex \
    -o "$OUTPUT_DIR/monthly_review"

# Generate statistics report
lixplore -A -q "main research topic" \
    -d "$MONTH_START" "$MONTH_END" \
    -m 500 \
    -D \
    --stat \
    --stat-top 30 > "$OUTPUT_DIR/statistics.txt"

echo "Monthly review complete: $OUTPUT_DIR"
```

---

## Python Automation

### Automated Literature Monitor

**Python script for intelligent monitoring:**

```python
#!/usr/bin/env python3
"""
literature_monitor.py - Automated literature monitoring with intelligence
"""

import subprocess
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

class LiteratureMonitor:
    def __init__(self, config_file="monitor_config.json"):
        with open(config_file) as f:
            self.config = json.load(f)

    def search_topic(self, topic, days_back=1):
        """Search for recent publications on topic"""
        today = datetime.now().date()
        start_date = (today - timedelta(days=days_back)).isoformat()
        end_date = today.isoformat()

        output_file = f"results_{topic.replace(' ', '_')}_{today}.json"

        cmd = [
            'lixplore', '-A', '-q', topic,
            '-d', start_date, end_date,
            '-m', '100',
            '-D',
            '--sort', 'newest',
            '-X', 'json',
            '-o', output_file
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if os.path.exists(f"exports/json/{output_file}"):
            with open(f"exports/json/{output_file}") as f:
                return json.load(f)
        return []

    def monitor_topics(self):
        """Monitor all configured topics"""
        results = {}

        for topic in self.config['topics']:
            print(f"Monitoring: {topic}")
            papers = self.search_topic(topic, self.config['days_back'])
            results[topic] = papers
            print(f"  Found: {len(papers)} papers")

        return results

    def generate_report(self, results):
        """Generate HTML report"""
        html = "<html><body>"
        html += f"<h1>Literature Monitor Report</h1>"
        html += f"<p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>"

        for topic, papers in results.items():
            html += f"<h2>{topic} ({len(papers)} papers)</h2>"

            if papers:
                html += "<ul>"
                for paper in papers[:10]:  # Top 10
                    html += f"<li><strong>{paper.get('title', 'No title')}</strong><br>"
                    html += f"Authors: {', '.join(paper.get('authors', [])[:3])}<br>"
                    html += f"Year: {paper.get('year', 'N/A')}</li>"
                html += "</ul>"
            else:
                html += "<p>No new papers found</p>"

        html += "</body></html>"
        return html

    def send_email(self, html_content):
        """Send email report"""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Literature Monitor - {datetime.now().strftime('%Y-%m-%d')}"
        msg['From'] = self.config['email']['from']
        msg['To'] = self.config['email']['to']

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send email (configure SMTP settings)
        # with smtplib.SMTP(self.config['email']['smtp_server']) as server:
        #     server.send_message(msg)

        print("Email would be sent (SMTP not configured)")

    def run(self):
        """Run monitoring workflow"""
        print(f"Starting literature monitor: {datetime.now()}")

        # Search all topics
        results = self.monitor_topics()

        # Generate report
        report = self.generate_report(results)

        # Save report
        report_file = f"report_{datetime.now().strftime('%Y%m%d')}.html"
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"Report saved: {report_file}")

        # Send email if configured
        if self.config.get('email_enabled'):
            self.send_email(report)

        print("Monitor complete")

if __name__ == "__main__":
    monitor = LiteratureMonitor()
    monitor.run()
```

**Configuration File (monitor_config.json):**

```json
{
    "topics": [
        "machine learning healthcare",
        "CRISPR gene editing",
        "quantum computing"
    ],
    "days_back": 1,
    "email_enabled": false,
    "email": {
        "from": "monitor@example.com",
        "to": "researcher@example.com",
        "smtp_server": "smtp.example.com"
    }
}
```

**Run:**
```bash
chmod +x literature_monitor.py
./literature_monitor.py
```

### Author Tracking Script

**Monitor specific researchers:**

```python
#!/usr/bin/env python3
"""
author_tracker.py - Track publications by specific authors
"""

import subprocess
import json
from datetime import datetime, timedelta

AUTHORS = [
    "LeCun Y",
    "Hinton G",
    "Bengio Y",
    "Ng AY"
]

def track_author(author_name, months_back=6):
    """Track author's recent publications"""
    today = datetime.now().date()
    start_date = (today - timedelta(days=months_back*30)).isoformat()
    end_date = today.isoformat()

    output_file = f"author_{author_name.replace(' ', '_')}_{today}.json"

    cmd = [
        'lixplore', '-x', '-au', author_name,
        '-d', start_date, end_date,
        '-m', '100',
        '--sort', 'newest',
        '-X', 'json',
        '-o', output_file
    ]

    subprocess.run(cmd)

    print(f"\nAuthor: {author_name}")
    print(f"Search period: {start_date} to {end_date}")
    print(f"Results saved: exports/json/{output_file}")

def main():
    print("Author Tracking Report")
    print("=" * 50)

    for author in AUTHORS:
        track_author(author)

    print("\nTracking complete!")

if __name__ == "__main__":
    main()
```

---

## CI/CD Integration

### GitHub Actions Workflow

**Automated literature updates in GitHub:**

```yaml
# .github/workflows/literature-update.yml

name: Daily Literature Update

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  update-literature:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Lixplore
        run: pip install lixplore

      - name: Run literature search
        run: |
          TODAY=$(date +%Y-%m-%d)
          YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

          lixplore -A -q "machine learning" \
            -d "$YESTERDAY" "$TODAY" \
            -m 100 \
            -D \
            -X xlsx,bibtex \
            -o "literature/daily_$TODAY"

      - name: Commit results
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add literature/
          git commit -m "Update literature: $(date +%Y-%m-%d)" || echo "No changes"
          git push
```

### GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml

stages:
  - search
  - process
  - deploy

variables:
  TOPIC: "machine learning healthcare"

literature_search:
  stage: search
  image: python:3.10
  script:
    - pip install lixplore
    - TODAY=$(date +%Y-%m-%d)
    - YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
    - lixplore -A -q "$TOPIC" -d "$YESTERDAY" "$TODAY" -m 100 -D -X json -o results.json
  artifacts:
    paths:
      - exports/json/results.json
    expire_in: 1 week

process_results:
  stage: process
  image: python:3.10
  dependencies:
    - literature_search
  script:
    - python process_results.py exports/json/results.json
  artifacts:
    paths:
      - processed_results/
    expire_in: 1 week

deploy_report:
  stage: deploy
  dependencies:
    - process_results
  script:
    - echo "Deploy report to internal server"
  only:
    - schedules
```

---

## Monitoring & Alerts

### Telegram Bot Notifications

**Send alerts via Telegram:**

```python
#!/usr/bin/env python3
"""
telegram_monitor.py - Send literature updates via Telegram
"""

import subprocess
import requests
from datetime import datetime, timedelta

# Telegram Bot Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram_message(message):
    """Send message via Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def monitor_literature():
    """Monitor literature and send alerts"""
    today = datetime.now().date()
    yesterday = (today - timedelta(days=1)).isoformat()
    today_str = today.isoformat()

    # Run search
    result = subprocess.run([
        'lixplore', '-A', '-q', 'machine learning',
        '-d', yesterday, today_str,
        '-m', '50',
        '-D'
    ], capture_output=True, text=True)

    # Parse output for count
    output = result.stdout

    if "Found" in output:
        message = f"*Literature Update - {today}*\n\n"
        message += f"Topic: Machine Learning\n"
        message += f"New papers found\n\n"
        message += f"Check your reports folder for details"

        send_telegram_message(message)

if __name__ == "__main__":
    monitor_literature()
```

### Slack Integration

**Post updates to Slack:**

```python
#!/usr/bin/env python3
"""
slack_monitor.py - Post literature updates to Slack
"""

import subprocess
import requests
from datetime import datetime, timedelta

SLACK_WEBHOOK_URL = "YOUR_WEBHOOK_URL"

def send_slack_message(text, attachments=None):
    """Send message to Slack"""
    payload = {"text": text}
    if attachments:
        payload["attachments"] = attachments

    requests.post(SLACK_WEBHOOK_URL, json=payload)

def monitor_and_notify():
    """Monitor literature and notify Slack"""
    today = datetime.now().date()
    yesterday = (today - timedelta(days=1)).isoformat()
    today_str = today.isoformat()

    # Run search
    subprocess.run([
        'lixplore', '-A', '-q', 'AI research',
        '-d', yesterday, today_str,
        '-m', '100',
        '-D',
        '-X', 'json',
        '-o', 'daily_results.json'
    ])

    # Read results
    import json
    try:
        with open('exports/json/daily_results.json') as f:
            papers = json.load(f)

        if papers:
            text = f":books: Daily Literature Update - {today}"
            attachments = [{
                "color": "good",
                "fields": [
                    {"title": "Papers Found", "value": str(len(papers)), "short": True},
                    {"title": "Topic", "value": "AI Research", "short": True}
                ]
            }]

            send_slack_message(text, attachments)
    except:
        pass

if __name__ == "__main__":
    monitor_and_notify()
```

### Email Digest

**Weekly email digest:**

```python
#!/usr/bin/env python3
"""
email_digest.py - Send weekly email digest
"""

import subprocess
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

def generate_weekly_digest():
    """Generate weekly literature digest"""
    today = datetime.now().date()
    week_ago = (today - timedelta(days=7)).isoformat()
    today_str = today.isoformat()

    # Run search
    subprocess.run([
        'lixplore', '-A', '-q', 'your research topic',
        '-d', week_ago, today_str,
        '-m', '200',
        '-D',
        '--stat',
        '-X', 'json',
        '-o', 'weekly_digest.json'
    ])

    # Load results
    with open('exports/json/weekly_digest.json') as f:
        papers = json.load(f)

    # Create HTML email
    html = f"""
    <html>
    <head><style>
        body {{ font-family: Arial, sans-serif; }}
        .paper {{ margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px; }}
        .title {{ font-weight: bold; color: #333; }}
        .authors {{ color: #666; font-size: 0.9em; }}
    </style></head>
    <body>
    <h1>Weekly Literature Digest</h1>
    <p>Week of {week_ago} to {today_str}</p>
    <p>Total papers: {len(papers)}</p>
    <hr>
    """

    for i, paper in enumerate(papers[:20], 1):  # Top 20
        html += f"""
        <div class="paper">
            <div class="title">{i}. {paper.get('title', 'No title')}</div>
            <div class="authors">{', '.join(paper.get('authors', [])[:3])}</div>
            <div>{paper.get('journal', 'N/A')} ({paper.get('year', 'N/A')})</div>
        </div>
        """

    html += "</body></html>"

    # Send email
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Weekly Literature Digest - {today}"
    msg['From'] = "monitor@example.com"
    msg['To'] = "researcher@example.com"

    msg.attach(MIMEText(html, 'html'))

    # Configure and send (update SMTP settings)
    # with smtplib.SMTP('smtp.example.com') as server:
    #     server.send_message(msg)

    print(f"Digest generated: {len(papers)} papers")
    with open(f"digest_{today}.html", 'w') as f:
        f.write(html)

if __name__ == "__main__":
    generate_weekly_digest()
```

---

## Best Practices

### 1. Error Handling

```bash
#!/bin/bash
# robust_search.sh - Search with error handling

set -e  # Exit on error

trap 'echo "Error on line $LINENO"' ERR

if ! command -v lixplore &> /dev/null; then
    echo "Error: lixplore not installed"
    exit 1
fi

lixplore -P -q "topic" -m 50 -X xlsx -o results.xlsx || {
    echo "Search failed"
    exit 1
}

echo "Search completed successfully"
```

### 2. Logging

```bash
#!/bin/bash
# search_with_logging.sh

LOG_FILE="$HOME/lixplore_automation.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Starting automated search"
lixplore -P -q "topic" -m 50 -X csv 2>&1 | tee -a "$LOG_FILE"
log "Search completed"
```

### 3. Resource Management

```bash
#!/bin/bash
# Rate limiting and resource management

DELAY_BETWEEN_SEARCHES=5  # seconds

for TOPIC in "${TOPICS[@]}"; do
    lixplore -P -q "$TOPIC" -m 100 -X xlsx
    sleep $DELAY_BETWEEN_SEARCHES
done
```

---

**Last Updated:** 2024-12-28
