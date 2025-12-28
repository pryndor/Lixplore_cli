# Lixplore Documentation

This directory contains the complete documentation for Lixplore_cli - Academic Literature Explorer.

## Documentation Structure

```
docs/
├── index.md                          # Homepage
├── getting-started/                  # Getting started guides
│   ├── installation.md               # How to install
│   ├── quickstart.md                 # 5-minute quick start
│   ├── basic-usage.md                # Basic concepts
│   └── first-search.md               # First search tutorial
├── guide/                            # User guides
│   ├── search-sources.md             # Source-specific search guide
│   ├── filtering.md                  # Filtering and sorting
│   ├── export.md                     # Export formats guide
│   ├── annotations.md                # Annotation system
│   ├── interactive.md                # Interactive modes
│   └── pdf.md                        # PDF management
├── advanced/                         # Advanced features
│   ├── automation.md                 # Cron jobs and automation
│   ├── ai-integration.md             # AI integration (OpenAI, Gemini)
│   ├── profiles.md                   # Profiles and templates
│   ├── custom-apis.md                # Custom API integration
│   └── zotero.md                     # Zotero integration
├── reference/                        # Command reference
│   ├── flags-overview.md             # All 95 flags overview
│   ├── source-flags.md               # Source selection flags
│   ├── search-flags.md               # Search parameter flags
│   ├── filter-flags.md               # Filtering flags
│   ├── display-flags.md              # Display option flags
│   ├── export-flags.md               # Export flags
│   ├── annotation-flags.md           # Annotation flags
│   ├── interactive-flags.md          # Interactive mode flags
│   └── utility-flags.md              # Utility flags
├── examples/                         # Examples and use cases
│   ├── workflows.md                  # Common workflows
│   ├── use-cases.md                  # Real research scenarios
│   ├── integrations.md               # Tool integration examples
│   └── automation-examples.md        # Automation examples
└── about/                            # About section
    ├── changelog.md                  # Version history
    ├── contributing.md               # How to contribute
    ├── license.md                    # MIT License
    └── faq.md                        # Frequently asked questions
```

## Building the Documentation

### Install Dependencies

```bash
pip install mkdocs mkdocs-material
```

### Local Development

```bash
# Serve documentation locally
mkdocs serve

# Open http://127.0.0.1:8000 in your browser
```

### Build Static Site

```bash
# Build to site/ directory
mkdocs build
```

### Deploy to GitHub Pages

```bash
# Deploy to gh-pages branch
mkdocs gh-deploy
```

## Quick Scripts

We provide convenience scripts:

### Quick Setup and Preview

```bash
./quick_docs_setup.sh
```

### Full Deployment

```bash
# Test locally first
./deploy_docs.sh

# Deploy to GitHub Pages
./deploy_docs.sh --deploy
```

## Documentation Features

- **Search**: Full-text search across all documentation
- **Dark Mode**: Toggle between light and dark themes
- **Mobile Responsive**: Works on all devices
- **Code Highlighting**: Syntax highlighting for all code examples
- **Navigation**: Easy navigation with tabs and sidebar
- **Copy Code**: One-click code copying
- **GitHub Integration**: Links to source code and issues

## Contributing to Documentation

To improve the documentation:

1. Edit the Markdown files in `docs/`
2. Test locally with `mkdocs serve`
3. Submit a pull request

See [Contributing Guide](about/contributing.md) for details.

## Documentation URLs

- **Local**: http://127.0.0.1:8000 (when running `mkdocs serve`)
- **Production**: https://pryndor.github.io/Lixplore_cli/

## Support

- **Issues**: https://github.com/pryndor/Lixplore_cli/issues
- **Discussions**: https://github.com/pryndor/Lixplore_cli/discussions

---

Built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
