# Utility Flags

> **Complete documentation for utility and configuration flags**

## Table of Contents

- [History & Cache](#history--cache)
- [Profile Management](#profile-management)
- [Template Management](#template-management)
- [Custom API Management](#custom-api-management)
- [PDF Configuration](#pdf-configuration)
- [Reference Manager Configuration](#reference-manager-configuration)
- [Help & Examples](#help--examples)

---

## History & Cache

### `-H, --history`

**Description:** Show search history.

**Syntax:**
```bash
lixplore -H
lixplore --history
```

**Type:** Boolean flag

**Storage:** `~/.lixplore_history.json`

**History Includes:**
- Timestamp
- Query string
- Sources searched
- Result count

### Examples

**Example 1: View History**
```bash
lixplore --history
```

**Output:**
```
SEARCH HISTORY (15 searches)

[1] 2024-12-28 14:30:15 (2 hours ago)
    Query: machine learning
    Sources: PubMed, Crossref
    Results: 95

[2] 2024-12-27 09:15:42 (1 day ago)
    Query: COVID-19 AND vaccine
    Sources: All sources
    Results: 247
```

---

### `--refresh`

**Description:** Bypass cache and fetch fresh results.

**Syntax:**
```bash
lixplore [SOURCE] -q "QUERY" --refresh
```

**Type:** Boolean flag

**Cache Duration:** 7 days (default)

### Examples

**Example 1: Fresh Search**
```bash
lixplore -P -q "breaking news topic" -m 10 --refresh
```

**Example 2: Update Cached Search**
```bash
lixplore -A -q "COVID-19" -m 50 --refresh -D
```

---

## Profile Management

### `--save-profile`

**Description:** Save current export settings as reusable profile.

**Syntax:**
```bash
lixplore [OPTIONS] --save-profile NAME
```

**Storage:** `~/.lixplore/profiles/`

### Examples

**Example 1: Save Profile**
```bash
lixplore -P -q "test" -X xlsx --export-fields title authors year --save-profile quick_export
```

---

### `--load-profile`

**Description:** Load previously saved export profile.

**Syntax:**
```bash
lixplore -q "QUERY" --load-profile NAME
```

### Examples

**Example 1: Load Profile**
```bash
lixplore -P -q "new research" --load-profile quick_export
```

---

### `--list-profiles`

**Description:** List all saved export profiles.

**Syntax:**
```bash
lixplore --list-profiles
```

### Examples

**Example 1: View Profiles**
```bash
lixplore --list-profiles
```

**Output:**
```
Saved export profiles:
  • quick_export
      Format: xlsx
      Fields: title, authors, year
  • comprehensive
      Format: csv,ris,bibtex
      Citation: apa
```

---

### `--delete-profile`

**Description:** Delete saved export profile.

**Syntax:**
```bash
lixplore --delete-profile NAME
```

### Examples

**Example 1: Delete Profile**
```bash
lixplore --delete-profile old_profile
```

---

## Template Management

### `--list-templates`

**Description:** List all available export templates.

**Syntax:**
```bash
lixplore --list-templates
```

**Built-in Templates:** nature, science, ieee

### Examples

**Example 1: View Templates**
```bash
lixplore --list-templates
```

**Output:**
```
Available export templates:
  • nature
      Format: xlsx
      Description: Nature journal format
  • science
      Format: csv
      Description: Science journal format
  • ieee
      Format: bibtex
      Description: IEEE citation format
```

---

## Custom API Management

### `--list-custom-apis`

**Description:** List all configured custom API sources.

**Syntax:**
```bash
lixplore --list-custom-apis
```

### Examples

**Example 1: View Custom APIs**
```bash
lixplore --list-custom-apis
```

**Output:**
```
Configured custom API sources:
  • springer
      Springer Nature API
      Requires authentication
  • base
      Bielefeld Academic Search Engine
```

---

### `--create-api-examples`

**Description:** Create example custom API configurations.

**Syntax:**
```bash
lixplore --create-api-examples
```

**Creates:** `~/.lixplore/custom_apis.json` with templates

### Examples

**Example 1: Setup API Templates**
```bash
lixplore --create-api-examples
```

**Output:**
```
Created example API configurations in ~/.lixplore/custom_apis.json
Example APIs: Springer, BASE, IEEE (templates only)
Edit the file and add your API keys to enable.
```

**Configuration File:**
```json
{
  "springer": {
    "name": "Springer",
    "base_url": "https://api.springernature.com/meta/v2/json",
    "api_key_param": "api_key",
    "query_param": "q",
    "requires_auth": true,
    "api_key": "YOUR_KEY_HERE"
  }
}
```

---

## PDF Configuration

### `--set-scihub-mirror`

**Description:** Configure SciHub mirror URL for PDF downloads.

**Syntax:**
```bash
lixplore --set-scihub-mirror URL
```

**Storage:** `~/.lixplore/config.json`

### Examples

**Example 1: Configure SciHub**
```bash
lixplore --set-scihub-mirror https://sci-hub.se
```

**Example 2: Update Mirror**
```bash
lixplore --set-scihub-mirror https://sci-hub.st
```

**Common Mirrors:**
- https://sci-hub.se
- https://sci-hub.st
- https://sci-hub.ru

**Disclaimer:** Use SciHub responsibly and at your own discretion. Check your institution's policies.

---

### `--show-pdf-dir`

**Description:** Show PDF download directory location and statistics.

**Syntax:**
```bash
lixplore --show-pdf-dir
```

**PDF Directory:** `~/Lixplore_PDFs/`

### Examples

**Example 1: Check PDF Directory**
```bash
lixplore --show-pdf-dir
```

**Output:**
```
PDF download directory: /home/user/Lixplore_PDFs/
Total PDFs downloaded: 127
```

---

## Reference Manager Configuration

### `--configure-zotero`

**Description:** Configure Zotero API access credentials.

**Syntax:**
```bash
lixplore --configure-zotero API_KEY USER_ID
```

**Storage:** `~/.lixplore/zotero_config.json`

### Setup Process

**Step 1: Get API Credentials**
1. Visit: https://www.zotero.org/settings/keys
2. Create new private key with read/write access
3. Note your User ID (numeric, in settings)

**Step 2: Configure Lixplore**
```bash
lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID
```

### Examples

**Example 1: Initial Setup**
```bash
lixplore --configure-zotero ABC123DEF456GHI789 1234567
```

**Output:**
```
Zotero API configured successfully!
API Key: ABC123...789
User ID: 1234567

Test connection...
✓ Connection successful
✓ Library accessible (142 items)

You can now use:
  --add-to-zotero
  --show-zotero-collections
```

---

### `--show-zotero-collections`

**Description:** List Zotero collections with their keys.

**Syntax:**
```bash
lixplore --show-zotero-collections
```

**Requires:** Zotero API configuration

### Examples

**Example 1: List Collections**
```bash
lixplore --show-zotero-collections
```

**Output:**
```
Zotero Collections:

[1] My Library (root)
    Key: N/A (use without --zotero-collection)

[2] PhD Research
    Key: ABC123DEF
    Items: 45

[3] Literature Review
    Key: GHI789JKL
    Items: 127

[4] Methodology Papers
    Key: MNO456PQR
    Items: 23

Use collection key with:
  lixplore -P -q "query" --add-to-zotero --zotero-collection ABC123DEF
```

---

## Help & Examples

### `--examples`

**Description:** Show quick examples (tldr-style) and exit.

**Syntax:**
```bash
lixplore --examples
```

**Type:** Boolean flag

### Examples

**Example 1: View Examples**
```bash
lixplore --examples
```

**Output:**
```
LIXPLORE - Quick Examples

BASIC SEARCH
  Search PubMed:
    $ lixplore -P -q "cancer treatment" -m 10

MULTI-SOURCE SEARCH
  Search all sources with deduplication:
    $ lixplore -A -q "COVID-19" -m 50 -D

EXPORT
  Export to Excel:
    $ lixplore -P -q "diabetes" -m 20 -X xlsx

[... more examples ...]
```

---

## Configuration Files

### File Locations

```
~/.lixplore/
├── config.json              # General configuration
├── profiles/                # Saved export profiles
│   ├── quick_export.json
│   └── comprehensive.json
├── custom_apis.json         # Custom API configurations
├── zotero_config.json       # Zotero credentials
└── templates/               # Custom export templates
    └── custom_template.json

~/.lixplore_cache.json       # Search results cache
~/.lixplore_history.json     # Search history
~/.lixplore_annotations.json # Article annotations
```

### Manual Configuration

**Edit Configuration:**
```bash
# Main config
nano ~/.lixplore/config.json

# Custom APIs
nano ~/.lixplore/custom_apis.json

# Zotero
nano ~/.lixplore/zotero_config.json
```

**Clear Cache:**
```bash
rm ~/.lixplore_cache.json
```

**Clear History:**
```bash
rm ~/.lixplore_history.json
```

**Backup Annotations:**
```bash
cp ~/.lixplore_annotations.json ~/backup/annotations_backup.json
```

---

## Best Practices

### 1. Regular Profile Management

```bash
# Save commonly used workflows
lixplore -P -q "test" -X xlsx --export-fields title authors year --save-profile standard_export

# List profiles periodically
lixplore --list-profiles

# Clean up unused profiles
lixplore --delete-profile old_profile
```

### 2. API Key Security

**DO:**
- Store API keys in configuration files
- Use environment variables for sensitive keys
- Restrict file permissions: `chmod 600 ~/.lixplore/zotero_config.json`

**DON'T:**
- Share configuration files publicly
- Commit API keys to version control
- Use shared credentials

### 3. Cache Management

```bash
# Use cache for speed (default)
lixplore -P -q "query" -m 20

# Bypass cache when needed
lixplore -P -q "latest news" -m 10 --refresh

# Review from cache
lixplore -R 1 2 3  # Uses cached results
```

### 4. History Tracking

```bash
# Review recent searches
lixplore --history

# Reproduce previous search
# Copy query from history and re-run
lixplore -P -q "exact query from history" -m 50
```

---

## Troubleshooting

### Problem: Zotero connection fails

**Solution: Verify credentials**
```bash
# Reconfigure
lixplore --configure-zotero NEW_API_KEY NEW_USER_ID

# Test connection
lixplore --show-zotero-collections
```

### Problem: Custom API not working

**Solution: Check configuration**
```bash
# List configured APIs
lixplore --list-custom-apis

# Recreate examples
lixplore --create-api-examples

# Edit and verify
nano ~/.lixplore/custom_apis.json
```

### Problem: Cache issues

**Solution: Clear and refresh**
```bash
# Remove cache
rm ~/.lixplore_cache.json

# Force fresh search
lixplore -P -q "query" -m 20 --refresh
```

### Problem: Profile not loading

**Solution: List and verify**
```bash
# List profiles
lixplore --list-profiles

# Check profile exists
ls ~/.lixplore/profiles/

# Delete and recreate
lixplore --delete-profile problematic_profile
lixplore -P -q "test" -X xlsx --save-profile new_profile
```

---

**Last Updated:** 2024-12-28
