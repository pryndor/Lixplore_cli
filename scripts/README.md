# Development Scripts

Helper scripts for local documentation development and testing.

**Note:** These scripts are optional. GitHub Actions handles automatic deployment when you push to `main` branch.

## Scripts

### 📄 deploy_docs.sh
Full-featured documentation deployment script.

**Usage:**
```bash
cd /path/to/Lixplore_cli
./scripts/deploy_docs.sh           # Preview locally
./scripts/deploy_docs.sh --deploy  # Deploy to GitHub Pages
```

**Features:**
- Validates documentation structure
- Builds documentation site
- Starts local preview server
- Optionally deploys to GitHub Pages

---

### 📄 quick_docs_setup.sh
Quick local documentation preview.

**Usage:**
```bash
cd /path/to/Lixplore_cli
./scripts/quick_docs_setup.sh
```

**What it does:**
- Installs MkDocs if needed
- Builds documentation
- Starts server at http://127.0.0.1:8000

**Alternative:** Run `mkdocs serve` directly from project root.

---

### 📄 test_docs.sh
Documentation verification and testing.

**Usage:**
```bash
cd /path/to/Lixplore_cli
./scripts/test_docs.sh
```

**What it does:**
- Checks all 39 documentation files exist
- Validates mkdocs.yml configuration
- Tests documentation build
- Reports pass/fail status

---

## Standard MkDocs Commands

You can also use standard MkDocs commands directly:

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Preview locally
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

## Automatic Deployment

The repository uses GitHub Actions for automatic deployment:
- Edit files in `docs/` directory
- Commit and push to `main` branch
- GitHub Actions automatically builds and deploys
- Live at: https://pryndor.github.io/Lixplore_cli/

No manual deployment needed! 🚀
