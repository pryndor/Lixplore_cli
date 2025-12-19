# Lixplore

> **Academic Literature Search & Export CLI Tool**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/lixplore.svg)](https://badge.fury.io/py/lixplore)

Search across multiple academic databases (PubMed, arXiv, Crossref, DOAJ, EuropePMC) with Boolean operators, smart selection, and export to 8 formats including EndNote, Excel, and BibTeX.

---

## ✨ Features

- 🔍 **Multi-Source Search** - Search 5 academic databases simultaneously
- 🔤 **Boolean Operators** - Advanced queries with AND, OR, NOT, parentheses
- 📊 **Smart Sorting** - Sort by relevance, newest, oldest, journal, or author
- 🔢 **Smart Selection** - Export odd/even, ranges, first/last N articles
- 💾 **8 Export Formats** - CSV, Excel, JSON, BibTeX, RIS, EndNote, XML
- 📖 **Review Mode** - View articles in separate terminal windows
- 🎯 **Deduplication** - Remove duplicates across multiple sources
- 📁 **Organized Exports** - Auto-organized folders by format type
- 📚 **Complete Documentation** - Man page, help, examples, TLDR

---

## 🚀 Quick Start

### Installation

```bash
# From PyPI (recommended)
pip install lixplore

# From source
git clone https://github.com/yourusername/lixplore.git
cd lixplore
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

### Quick Help

```bash
# Show quick examples
lixplore --examples

# Show complete help
lixplore --help

# View man page (after installing)
man lixplore
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
pip install lixplore
```

### Method 2: From Source
```bash
git clone https://github.com/yourusername/lixplore.git
cd lixplore
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

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/lixplore/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/lixplore/discussions)
- **Email:** lixplore@example.com

---

## 🔗 Links

- [PyPI Package](https://pypi.org/project/lixplore/)
- [GitHub Repository](https://github.com/yourusername/lixplore)
- [Documentation](https://github.com/yourusername/lixplore#readme)
- [Issue Tracker](https://github.com/yourusername/lixplore/issues)

---

**Made with ❤️ for the research community**
