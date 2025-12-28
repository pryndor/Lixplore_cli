# Lixplore Documentation Guide

Complete documentation for Lixplore_cli - Academic Literature Explorer

## 📚 Documentation Overview

The Lixplore documentation is built with MkDocs and Material theme, providing a beautiful, searchable, and user-friendly experience.

**Live Documentation:** https://pryndor.github.io/Lixplore_cli/

## 🚀 Quick Start

### Option 1: Quick Setup (Recommended)

```bash
./quick_docs_setup.sh
```

This will:
- Install MkDocs and dependencies
- Build the documentation
- Start a local server at http://127.0.0.1:8000

### Option 2: Manual Setup

```bash
# Install dependencies
pip install mkdocs mkdocs-material

# Preview locally
mkdocs serve

# Open http://127.0.0.1:8000
```

## 📋 Documentation Contents

### 1. Getting Started (4 pages)
- Installation Guide
- 5-Minute Quick Start
- Basic Usage Concepts
- First Search Tutorial

### 2. User Guide (6 pages)
- Search & Sources
- Filtering & Sorting
- Export Formats
- Annotations & Tags
- Interactive Modes
- PDF Management

### 3. Advanced Features (5 pages)
- Automation & Cron Jobs
- AI Integration (OpenAI, Gemini)
- Profiles & Templates
- Custom APIs
- Zotero Integration

### 4. Command Reference (9 pages)
**ALL 95 flags documented with detailed examples:**
- Flags Overview
- Source Selection Flags (8 flags)
- Search Parameter Flags (4 flags)
- Filtering Flags (7 flags)
- Display Flags (9 flags)
- Export Flags (15 flags)
- Annotation Flags (13 flags)
- Interactive Flags (3 flags)
- Utility Flags (12 flags)

### 5. Examples (4 pages)
- Common Workflows
- Real Research Use Cases
- Tool Integrations
- Automation Examples

### 6. About (4 pages)
- FAQ
- Contributing Guide
- License (MIT)
- Changelog

**Total: 32 comprehensive documentation pages**

## 🧪 Testing Documentation

Run the test suite to verify everything is set up correctly:

```bash
./test_docs.sh
```

This checks:
- All required files exist
- MkDocs builds successfully
- Documentation structure is correct

## 🌐 Deployment

### Deploy to GitHub Pages

```bash
# Interactive deployment with preview
./deploy_docs.sh

# Direct deployment
./deploy_docs.sh --deploy
```

This will:
1. Build the documentation
2. Push to `gh-pages` branch
3. Make it live at https://pryndor.github.io/Lixplore_cli/

### Enable GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** section
3. Under **Source**, select `gh-pages` branch
4. Click **Save**

Your documentation will be live within a few minutes!

## 🔄 Automatic Deployment

Documentation automatically deploys on every push to `main` branch when files in `docs/` or `mkdocs.yml` change.

This is configured in `.github/workflows/docs.yml`

## 📝 Editing Documentation

All documentation is in Markdown format in the `docs/` directory:

```bash
docs/
├── index.md                    # Homepage
├── getting-started/            # Getting started guides
├── guide/                      # User guides
├── advanced/                   # Advanced features
├── reference/                  # Command reference (all flags)
├── examples/                   # Examples and use cases
└── about/                      # About, FAQ, license
```

### To edit:

1. Edit the `.md` files in `docs/`
2. Preview changes: `mkdocs serve`
3. Commit and push
4. Documentation auto-deploys!

## 🎨 Documentation Features

- **Full-Text Search**: Search across all documentation
- **Dark Mode**: Toggle between light/dark themes
- **Mobile Responsive**: Works on phones, tablets, desktops
- **Code Highlighting**: Syntax highlighting for all examples
- **Copy Code Buttons**: One-click code copying
- **Navigation**: Tabbed navigation + sidebar
- **GitHub Integration**: Links to source and issues
- **Fast**: Static site generation for speed

## 📦 Dependencies

```bash
pip install mkdocs mkdocs-material
```

That's it! No other dependencies needed.

## 🔧 Customization

### Theme Settings

Edit `mkdocs.yml` to customize:
- Colors and theme
- Navigation structure
- Features and extensions
- Social links

### Adding New Pages

1. Create `.md` file in appropriate `docs/` subdirectory
2. Add to navigation in `mkdocs.yml`
3. Preview with `mkdocs serve`

## 📊 Documentation Statistics

- **Total Pages**: 32
- **Total Flags Documented**: 95
- **Code Examples**: 200+
- **Search Indexed**: Yes
- **Mobile Optimized**: Yes
- **PDF Export**: Available
- **Dark Mode**: Yes

## 🆘 Troubleshooting

### "mkdocs: command not found"

```bash
pip install mkdocs mkdocs-material
# Add to PATH if needed
export PATH=$PATH:~/.local/bin
```

### Build Errors

```bash
# Validate configuration
mkdocs build

# Check for broken links
mkdocs build --strict
```

### Deployment Issues

```bash
# Clean build
rm -rf site/
mkdocs gh-deploy --force
```

## 📚 Resources

- **MkDocs**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **GitHub Pages**: https://pages.github.com/
- **Markdown Guide**: https://www.markdownguide.org/

## 💡 Tips

1. **Preview Before Deploy**: Always test locally first
2. **Check Mobile**: Test on different screen sizes
3. **Use Search**: Verify search works for key terms
4. **Verify Links**: Check all internal links work
5. **Read Build Output**: Watch for warnings

## 🎯 Next Steps

1. **Test Locally**: `./quick_docs_setup.sh`
2. **Verify Content**: Check all pages load correctly
3. **Deploy**: `./deploy_docs.sh --deploy`
4. **Share**: Your docs are live at https://pryndor.github.io/Lixplore_cli/

## ✅ Checklist

- [ ] Documentation builds without errors
- [ ] All pages accessible
- [ ] Search works
- [ ] Examples are correct
- [ ] Links work
- [ ] Mobile responsive
- [ ] Dark mode works
- [ ] Deployed to GitHub Pages

---

**Questions?** Open an issue at https://github.com/pryndor/Lixplore_cli/issues

**Documentation built with ❤️ using MkDocs Material**
