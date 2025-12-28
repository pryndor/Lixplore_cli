# Lixplore

> **Academic Literature Search & Export CLI Tool**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://pryndor.github.io/Lixplore_cli/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/pryndor/Lixplore_cli)
[![PyPI version](https://badge.fury.io/py/lixplore-cli.svg)](https://pypi.org/project/lixplore-cli/)
[![Issues](https://img.shields.io/github/issues/pryndor/Lixplore_cli)](https://github.com/pryndor/Lixplore_cli/issues)
<a href="https://www.buymeacoffee.com/lixplore" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-40DCA5?style=flat&logo=buy-me-a-coffee" alt="Buy Me A Coffee"></a>

Search across multiple academic databases (PubMed, arXiv, Crossref, DOAJ, EuropePMC) with Boolean operators, smart selection, and export to 8 formats including EndNote, Excel, and BibTeX.

**📚 [Complete Documentation](https://pryndor.github.io/Lixplore_cli/)** | **🐛 [Report Issues](https://github.com/pryndor/Lixplore_cli/issues)**

---

## ✨ Features

### Core Features
- 🔍 **Multi-Source Search** - Search 5 academic databases simultaneously (PubMed, arXiv, Crossref, DOAJ, EuropePMC)
- 🔤 **Boolean Operators** - Advanced queries with AND, OR, NOT, parentheses
- 📊 **Smart Sorting** - Sort by relevance, newest, oldest, journal, or author
- 🔢 **Smart Selection** - Export odd/even, ranges, first/last N articles
- 💾 **8 Export Formats** - CSV, Excel, JSON, BibTeX, RIS, EndNote, XML
- 📖 **Review Mode** - View articles in separate terminal windows
- 🎯 **Deduplication** - Advanced duplicate removal with multiple strategies
- 📁 **Organized Exports** - Auto-organized folders by format type

### Advanced Features
- 📥 **PDF Downloads** - Automatic PDF downloads from PMC, arXiv, Unpaywall, and SciHub (optional)
- 🔗 **PDF Link Display** - Show clickable PDF links for open access articles in terminal (NEW!)
- 📚 **Reference Manager Integration** - Direct Zotero API integration and Mendeley RIS export
- 📊 **Statistics Dashboard** - Comprehensive analytics with visualizations (publication trends, top journals, top authors)
- 🎨 **Interactive TUI Mode** - Browse, select, and export with an interactive terminal UI
- 📝 **Citation Export** - Format citations in APA, MLA, Chicago, IEEE styles
- 🔧 **Custom API Integration** - Plugin architecture for any REST API (Springer, BASE, etc.)
- 💡 **Metadata Enrichment** - Auto-enrich results from multiple APIs (Crossref, PubMed, arXiv)
- 💾 **Smart Caching** - 7-day cache with automatic expiration
- 📄 **Pagination** - Browse large result sets with automatic pagination
- 🎯 **Export Profiles** - Save and reuse export configurations
- 📋 **Export Templates** - Predefined templates (Nature, Science, IEEE)
- 🗜️ **Export Compression** - ZIP compression for batch exports

### Documentation
- 📚 **[Complete Documentation Site](https://pryndor.github.io/Lixplore_cli/)** - Comprehensive online documentation
- 📖 **32+ Documentation Pages** - Getting started, user guides, command reference, examples
- 🔍 **All 95 Flags Documented** - Detailed examples for every command-line flag
- 🎓 **Step-by-Step Tutorials** - From installation to advanced workflows
- 💡 **Quick Examples** - Built-in examples with `--examples` flag
- 📄 **Man Page** - Traditional Unix man page included

### 🚀 NEW! Interactive Modes
- 🐚 **Shell Mode** - Persistent terminal session (like OpenBB Terminal)
- 🧙 **Wizard Mode** - Guided step-by-step workflows for beginners
- 📝 **Annotation System** - Rate, tag, comment, and organize your research library

---

## 🎯 Three Ways to Use Lixplore

### 1️⃣ Shell Mode (NEW!) - Persistent Interactive Session

**Perfect for power users and continuous workflows**

```bash
lixplore --shell

# Inside shell - no need to type 'lixplore' repeatedly!
lixplore> search "cancer treatment" -P -m 20
lixplore> annotate 5 --rating 5 --tags "important"
lixplore> list annotations
lixplore> export markdown
```

### 2️⃣ Wizard Mode (NEW!) - Guided Workflows

**Perfect for beginners and learning**

```bash
lixplore --wizard

# Follow interactive prompts - no flags to memorize!
What do you want to do?
  1. Search for articles
  2. Annotate an article
  3. View my annotations
  ...
```

### 3️⃣ Command Line - Traditional Flags

**Perfect for scripting and automation**

```bash
lixplore -P -q "machine learning" -m 20 -X xlsx
```

**📖 See [INTERACTIVE_MODES_GUIDE.md](INTERACTIVE_MODES_GUIDE.md) for complete guide**

---

## 🆕 What's New in Version 2.0

Lixplore has been massively upgraded with powerful new features:

### 📥 PDF Download & Link Display
**Download PDFs** automatically with smart fallback chain:
- PubMed Central (open access)
- arXiv (preprints)
- DOI Resolution via Unpaywall
- SciHub fallback (optional, user-configured)

```bash
lixplore -P -q "open access" -m 10 --download-pdf
```

**Show PDF Links** directly in search results (NEW!):
- Display clickable PDF links for open access articles
- Works in modern terminals (iTerm2, GNOME Terminal, Windows Terminal)
- No download required - click to open in browser

```bash
lixplore -x -q "machine learning" -m 10 --show-pdf-links
```

### 📚 Reference Manager Integration
Direct integration with your favorite reference managers:
- **Zotero**: API integration with collection support
- **Mendeley**: RIS export for easy import

**Setup Zotero (one-time):**
1. Get API key: https://www.zotero.org/settings/keys
2. Configure: `lixplore --configure-zotero YOUR_API_KEY YOUR_USER_ID`

**Usage:**
```bash
# Add to Zotero library
lixplore -P -q "research" -m 10 --add-to-zotero

# Add to specific collection
lixplore -P -q "AI" -m 20 --add-to-zotero --zotero-collection 4FCVPNAP
```

### 📊 Statistics Dashboard
Comprehensive analytics with beautiful ASCII visualizations:
- Publication trends by year
- Top journals and authors
- Source distribution
- Metadata completeness

```bash
lixplore -P -q "AI" -m 100 --stat
```

### 🎨 Interactive TUI Mode
Browse results with a rich interactive terminal interface:
- Navigate pages with keyboard
- Select articles visually
- Export selected items
- View detailed information

```bash
lixplore -P -q "machine learning" -m 50 -i
```

### 🔧 Custom API Integration
Add ANY API source via simple JSON configuration:
- No code modification needed
- Supports Springer, BASE, and more
- Plugin architecture for extensibility

```bash
lixplore --custom-api springer -q "quantum physics" -m 20
```

### 💡 Smart Enhancements
- **Metadata Enrichment**: Auto-fill missing data from multiple APIs
- **Export Profiles**: Save and reuse export configurations
- **Citation Formatting**: Export as APA, MLA, Chicago, IEEE
- **Batch Export**: Export to multiple formats simultaneously
- **Deduplication Strategies**: Multiple algorithms with customization

---

## 🚀 Quick Start

### Installation

```bash
# From PyPI (recommended)
pip install lixplore-cli

# From source
git clone https://github.com/pryndor/Lixplore_cli.git
cd Lixplore_cli
pip install -e .
```

### Basic Usage

```bash
# Search PubMed
lixplore -P -q "cancer treatment" -m 10

# Search all sources with deduplication
lixplore -A -q "COVID-19" -m 50 -D

# Export to Excel
lixplore -P -q "diabetes" -m 20 -X xlsx -o results.xlsx
```

---

## 📚 Documentation

### 📖 [Complete Online Documentation](https://pryndor.github.io/Lixplore_cli/)

Visit our comprehensive documentation site for:
- **Getting Started Guides** - Installation and first search tutorial
- **User Guides** - Search, filtering, export, annotations, PDF management
- **Command Reference** - All 95 flags with detailed examples
- **Advanced Features** - Automation, AI integration, Zotero, custom APIs
- **Examples** - Common workflows, use cases, tool integrations

### Quick Help

```bash
# Show quick examples
lixplore --examples

# Show complete help
lixplore --help

# View man page (after installing)
man lixplore

# Browse online documentation
# https://pryndor.github.io/Lixplore_cli/
```

### Key Commands

#### Search Sources
```bash
-P, --pubmed       # Search PubMed
-C, --crossref     # Search Crossref
-J, --doaj         # Search DOAJ
-E, --europepmc    # Search EuropePMC
-x, --arxiv        # Search arXiv
-A, --all          # Search all sources
-s PX              # Combined (PubMed + arXiv)
```

#### Boolean Operators
```bash
# AND - both terms required
lixplore -P -q "cancer AND treatment" -m 10

# OR - either term
lixplore -P -q "cancer OR tumor" -m 10

# NOT - exclude term
lixplore -P -q "diabetes NOT type1" -m 10

# Complex queries
lixplore -P -q "(cancer OR tumor) AND treatment" -m 20
```

#### Export Formats
```bash
-X csv      # CSV format
-X xlsx     # Excel with formatting
-X json     # JSON structured data
-X bibtex   # BibTeX for LaTeX
-X ris      # RIS for reference managers
-X enw      # EndNote Tagged (recommended)
-X endnote  # EndNote XML
-X xml      # Generic XML
```

#### Smart Selection
```bash
# Export odd-numbered articles
lixplore -P -q "research" -m 50 -S odd -X csv

# Export first 10 articles
lixplore -P -q "cancer" -m 50 -S first:10 -X xlsx

# Export range
lixplore -P -q "study" -m 50 -S 10-20 -X enw

# Mixed patterns
lixplore -P -q "science" -m 50 -S 1 3 5-10 odd -X csv
```

#### Sorting
```bash
--sort newest   # Latest publications first
--sort oldest   # Earliest publications first
--sort journal  # Alphabetical by journal
--sort author   # Alphabetical by author
```

#### Review Mode
```bash
# Step 1: Search
lixplore -P -q "aspirin" -m 10

# Step 2: Review in separate terminal
lixplore -R 2

# Close review window: Press 'q' or Ctrl+C
```

#### PDF Links
```bash
# Show clickable PDF links in results
lixplore -x -q "neural networks" -m 10 --show-pdf-links

# Combine with abstracts
lixplore -P -q "cancer" -m 20 -a --show-pdf-links

# Multi-source with PDF links
lixplore -A -q "COVID-19" -m 50 -D --show-pdf-links
```

---

## 🎯 Use Cases

### 1. Literature Review
```bash
# Search all sources, deduplicate, sort newest, export top 20
lixplore -A -q "machine learning healthcare" -m 100 -D \
  --sort newest -S first:20 -X xlsx -o ml_healthcare.xlsx
```

### 2. Boolean Search with Export
```bash
# Advanced query with multiple conditions
lixplore -P -q "(COVID-19 OR coronavirus) AND (vaccine OR treatment)" \
  -m 50 --sort newest -X enw -o covid_papers.enw
```

### 3. Quick Sample Review
```bash
# Search 50, export odd-numbered (25 articles)
lixplore -A -q "cancer immunotherapy" -m 50 -D \
  -S odd -X csv -o cancer_sample.csv
```

### 4. Historical Research
```bash
# Sort by oldest to study evolution
lixplore -P -q "diabetes" -m 100 --sort oldest \
  -X xlsx -o diabetes_history.xlsx
```

### 5. Multi-Step Workflow
```bash
# 1. Search
lixplore -P -q "neuroscience" -m 20

# 2. Review specific articles
lixplore -R 2 5 8

# 3. Export selected
lixplore -P -q "neuroscience" -m 20 -S 2 5 8 -X enw
```

---

## 📊 Export Formats

All exports are automatically organized into folders:

```
exports/
├── csv/              # CSV files
├── excel/            # Excel files (.xlsx)
├── json/             # JSON files
├── bibtex/           # BibTeX files
├── ris/              # RIS files
├── endnote_tagged/   # EndNote Tagged (.enw)
├── endnote_xml/      # EndNote XML files
└── xml/              # Generic XML files
```

---

## 🔧 Advanced Features

### Smart Selection Patterns

| Pattern | Syntax | Example | Result |
|---------|--------|---------|--------|
| Specific | `1 3 5` | `-S 1 3 5` | Articles #1, #3, #5 |
| Range | `1-10` | `-S 1-10` | Articles #1 through #10 |
| Odd | `odd` | `-S odd` | Odd-numbered articles |
| Even | `even` | `-S even` | Even-numbered articles |
| First N | `first:10` | `-S first:10` | First 10 articles |
| Last N | `last:5` | `-S last:5` | Last 5 articles |
| Mixed | `1 3 5-10` | `-S 1 3 5-10` | Combined patterns |

### Sort Options

- `relevant` - Default API order (most relevant first)
- `newest` - Latest publications (2025 → 2020)
- `oldest` - Earliest publications (1990 → 2000)
- `journal` - Alphabetical by journal name
- `author` - Alphabetical by first author

---

## 🖥️ Platform Support

Lixplore works on all major platforms:

- ✅ **Linux** (all distributions)
- ✅ **macOS** (10.14+)
- ✅ **Windows** (10+)

### Platform-Specific Notes

#### Linux
Review feature works with: xfce4-terminal, gnome-terminal, konsole, xterm, alacritty, kitty

#### macOS
Review feature uses Terminal.app

#### Windows
Review feature uses cmd.exe

---

## 📦 Installation Methods

### Method 1: PyPI (Recommended)
```bash
pip install lixplore-cli
```

### Method 2: From Source
```bash
git clone https://github.com/pryndor/Lixplore_cli.git
cd Lixplore_cli
pip install -e .
```

### Method 3: Using pipx (Isolated)
```bash
pipx install lixplore
```

---

## 🔍 Requirements

- Python 3.7 or higher
- Internet connection for API access
- Terminal emulator (for review feature)

### Dependencies

- `biopython` - PubMed/NCBI API access
- `requests` - HTTP requests
- `litstudy` - Literature study support
- `openpyxl` - Excel export support

All dependencies are automatically installed.

---

## 📖 Man Page

After installation, install the man page:

```bash
sudo cp docs/lixplore.1 /usr/local/share/man/man1/
sudo mandb -q
man lixplore
```

---

## ☕ Support the Project

If you find Lixplore useful for your research, consider supporting its development!

<a href="https://www.buymeacoffee.com/lixplore" target="_blank" rel="noopener noreferrer">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;">
</a>

**Why support?**
- ✨ Keeps the project actively maintained and updated
- 🚀 Helps add new features and integrations
- 📚 Supports free, open-source academic tools
- 🌍 Makes research more accessible to everyone

> *"If you value independent research tools and open access to literature, consider buying me a coffee ☕—it helps keep development and research going!"*

Your support enables:
- Regular updates and bug fixes
- New API integrations (IEEE Xplore, Scopus, Web of Science)
- Advanced features (LLM integration, citation networks, collaboration tools)
- Better documentation and tutorials
- Faster response to issues and feature requests

**Other ways to support:**
- ⭐ Star the repository on GitHub
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📖 Improve documentation
- 🔀 Contribute code via pull requests
- 📢 Share Lixplore with your research community

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- PubMed/NCBI for providing free API access
- arXiv for open preprint access
- Crossref for DOI metadata
- DOAJ for open access journal data
- EuropePMC for European literature access

---

## 📧 Support & Community

- **📚 Documentation:** [https://pryndor.github.io/Lixplore_cli/](https://pryndor.github.io/Lixplore_cli/)
- **🐛 Issues:** [GitHub Issues](https://github.com/pryndor/Lixplore_cli/issues)
- **❓ FAQ:** [Documentation FAQ](https://pryndor.github.io/Lixplore_cli/about/faq/)

---

## 🔗 Quick Links

- **📦 PyPI Package:** [https://pypi.org/project/lixplore-cli/](https://pypi.org/project/lixplore-cli/)
- **💻 GitHub Repository:** [https://github.com/pryndor/Lixplore_cli](https://github.com/pryndor/Lixplore_cli)
- **📚 Documentation:** [https://pryndor.github.io/Lixplore_cli/](https://pryndor.github.io/Lixplore_cli/)
- **🐛 Issue Tracker:** [https://github.com/pryndor/Lixplore_cli/issues](https://github.com/pryndor/Lixplore_cli/issues)
- **🚀 Changelog:** [https://pryndor.github.io/Lixplore_cli/about/changelog/](https://pryndor.github.io/Lixplore_cli/about/changelog/)
- **🤝 Contributing Guide:** [https://pryndor.github.io/Lixplore_cli/about/contributing/](https://pryndor.github.io/Lixplore_cli/about/contributing/)

---

**Made with ❤️ for the research community**
