# Profiles & Templates

Profiles and templates allow you to save and reuse complex configurations, making it easy to run repeated searches with consistent settings.

---

## Profiles

### What are Profiles?

Profiles save your command-line configuration (flags and their values) so you can reuse them without typing everything again.

### Creating a Profile

Use `--save-profile` to save your current command configuration:

```bash
# Create a profile for Nature-style exports
lixplore -P -q "test" -X bibtex --sort newest -S first:20 --save-profile nature_style

# Create a profile for comprehensive searches
lixplore -A -q "test" -m 100 -D --enrich --sort newest --save-profile comprehensive

# Create a profile for quick PDF searches
lixplore -x -q "test" -m 50 --show-pdf-links --save-profile arxiv_pdfs
```

### Using a Profile

Load a saved profile with `--load-profile`:

```bash
# Use the nature_style profile with a new query
lixplore -q "stem cells" --load-profile nature_style

# Use comprehensive profile
lixplore -q "quantum computing" --load-profile comprehensive

# Use arxiv_pdfs profile
lixplore -q "neural networks" --load-profile arxiv_pdfs
```

### Listing Profiles

View all saved profiles:

```bash
lixplore --list-profiles
```

Output:
```
Saved Profiles:
1. nature_style
   - Sources: PubMed
   - Export: bibtex
   - Sort: newest
   - Selection: first:20

2. comprehensive
   - Sources: All
   - Max results: 100
   - Deduplicate: Yes
   - Enrich: Yes
   - Sort: newest

3. arxiv_pdfs
   - Sources: arXiv
   - Max results: 50
   - Show PDF links: Yes
```

### Deleting a Profile

Remove a profile you no longer need:

```bash
lixplore --delete-profile nature_style
```

### Profile Storage

Profiles are stored in:
```
~/.lixplore/profiles.json
```

You can back up this file to preserve your profiles.

---

## Templates

### What are Templates?

Templates are custom export format templates. While profiles save command configurations, templates customize how data is exported.

### Available Templates

List all available templates:

```bash
lixplore --list-templates
```

### Using a Template

Apply a template when exporting:

```bash
# Use a custom template
lixplore -P -q "research" -m 50 --template my_custom_template -X csv -o results.csv
```

### Creating Custom Templates

Templates are stored in:
```
~/.lixplore/templates/
```

Create a custom template by adding a file there. For example, create `~/.lixplore/templates/minimal.txt`:

```
{title}
{authors}
{year}
{doi}
---
```

Then use it:

```bash
lixplore -P -q "topic" -m 20 --template minimal
```

---

## Common Profile Examples

### Research Monitoring Profile

For daily monitoring of new research:

```bash
# Create the profile
lixplore -A -q "test" -m 50 -D --sort newest -S first:20 -X xlsx --save-profile daily_monitor

# Use daily with different topics
lixplore -q "COVID-19" --load-profile daily_monitor -o covid_daily.xlsx
lixplore -q "machine learning" --load-profile daily_monitor -o ml_daily.xlsx
```

### Citation Export Profile

For exporting citations:

```bash
# Create profile
lixplore -P -q "test" -m 100 -X bibtex --sort year --save-profile citation_export

# Use for different topics
lixplore -q "neuroscience" --load-profile citation_export -o neuro.bib
lixplore -q "genomics" --load-profile citation_export -o genomics.bib
```

### Comprehensive Review Profile

For literature reviews:

```bash
# Create profile with all features
lixplore -A -q "test" -m 500 -D --enrich --sort newest -S first:100 -X xlsx --save-profile lit_review

# Use for your review topic
lixplore -q "CRISPR applications" --load-profile lit_review -o crispr_review.xlsx
```

### Open Access PDF Profile

For finding free PDFs:

```bash
# Create profile
lixplore -x -q "test" -m 100 --show-pdf-links --save-profile free_pdfs

# Use for different topics
lixplore -q "machine learning" --load-profile free_pdfs
lixplore -q "physics" --load-profile free_pdfs
```

---

## Profile Best Practices

### 1. Name Profiles Descriptively

```bash
# Good names
--save-profile daily_covid_monitor
--save-profile bibtex_export_top50
--save-profile arxiv_pdfs_recent

# Poor names
--save-profile profile1
--save-profile temp
--save-profile test
```

### 2. Create Profiles for Repeated Tasks

If you run the same search pattern more than 3 times, create a profile for it.

### 3. Version Your Profiles

When updating a profile, create a new version:

```bash
lixplore ... --save-profile my_search_v2
```

### 4. Document Your Profiles

Keep a text file documenting what each profile does:

```bash
# Create a documentation file
cat > ~/.lixplore/profile_docs.txt << 'DOCS'
daily_monitor: Daily research monitoring, top 20 newest from all sources
citation_export: BibTeX export sorted by year
lit_review: Comprehensive review with 100 articles, enriched
free_pdfs: arXiv searches with PDF links
DOCS
```

### 5. Backup Your Profiles

```bash
# Backup profiles
cp ~/.lixplore/profiles.json ~/.lixplore/profiles_backup.json

# Or commit to version control
cd ~
git add .lixplore/profiles.json
git commit -m "Update lixplore profiles"
```

---

## Combining Profiles with Other Features

### Profiles + Automation

Use profiles in cron jobs:

```bash
# crontab -e
0 9 * * * lixplore -q "COVID-19 $(date +%Y)" --load-profile daily_monitor -o /home/user/covid_$(date +%Y%m%d).xlsx
```

### Profiles + Annotations

Use profiles to search, then annotate:

```bash
# Search using profile
lixplore -q "interesting topic" --load-profile comprehensive

# Annotate important results
lixplore --annotate 5 --rating 5 --tags "important"
```

### Profiles + Interactive Mode

Combine profiles with interactive browsing:

```bash
lixplore -q "research topic" --load-profile comprehensive -i
```

---

## Profile Storage Format

Profiles are stored as JSON in `~/.lixplore/profiles.json`:

```json
{
  "nature_style": {
    "sources": ["pubmed"],
    "export_format": "bibtex",
    "sort": "newest",
    "selection": "first:20"
  },
  "comprehensive": {
    "sources": ["all"],
    "max_results": 100,
    "deduplicate": true,
    "enrich": true,
    "sort": "newest"
  }
}
```

You can manually edit this file if needed.

---

## Troubleshooting

### Profile not found

```bash
Error: Profile 'my_profile' not found
```

Solution: List available profiles with `--list-profiles`

### Profile conflicts

If a profile has settings that conflict with command-line flags:

```bash
# Profile sets -m 100, but you also specify -m 50
lixplore -q "topic" -m 50 --load-profile my_profile
```

Command-line flags always override profile settings.

### Corrupted profile file

If your profile file gets corrupted:

```bash
# Restore from backup
cp ~/.lixplore/profiles_backup.json ~/.lixplore/profiles.json

# Or delete and start fresh
rm ~/.lixplore/profiles.json
```

---

## Advanced: Sharing Profiles

### Export a Profile

```bash
# Copy profile to share with colleagues
cp ~/.lixplore/profiles.json ~/shared_profiles.json
```

### Import a Profile

```bash
# Merge someone else's profiles with yours
# Manual merge required - edit ~/.lixplore/profiles.json
```

### Team Profiles

For research teams, keep profiles in version control:

```bash
# In your project directory
mkdir .lixplore-profiles
cp ~/.lixplore/profiles.json .lixplore-profiles/team_profiles.json
git add .lixplore-profiles/
git commit -m "Add team search profiles"
```

Team members can then:

```bash
cp .lixplore-profiles/team_profiles.json ~/.lixplore/profiles.json
```

---

## Summary

- **Profiles** save command configurations for reuse
- **Templates** customize export formats
- Use `--save-profile` to create, `--load-profile` to use
- List with `--list-profiles`, delete with `--delete-profile`
- Perfect for automation and repeated searches
- Store in `~/.lixplore/profiles.json`

---

**Next**: [Custom APIs](custom-apis.md) | [Back to Advanced Features](automation.md)
