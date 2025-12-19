# Lixplore Deployment Guide

Complete guide for deploying Lixplore as a Python package on PyPI and GitHub.

---

## 📋 Prerequisites

1. **GitHub Account** - For repository hosting
2. **PyPI Account** - For package distribution (https://pypi.org/account/register/)
3. **Python 3.7+** - For building and testing
4. **Git** - For version control

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Update repository URLs in files:**
   - `setup.py` - Change `yourusername/lixplore` to your GitHub username
   - `pyproject.toml` - Update URLs
   - `README.md` - Update badges and links

2. **Update author information:**
   - `setup.py` - Update author name and email
   - `pyproject.toml` - Update author details
   - `LICENSE` - Update copyright holder

### Step 2: Initialize Git Repository

```bash
cd ~/Lixplore_cli

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Lixplore v1.0.0"
```

### Step 3: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `lixplore`
3. Description: "Academic Literature Search & Export CLI Tool"
4. Public or Private (Public recommended for PyPI)
5. Don't initialize with README (we already have one)
6. Create repository

### Step 4: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/yourusername/lixplore.git

# Push
git branch -M main
git push -u origin main
```

### Step 5: Set Up PyPI

1. **Create PyPI account:** https://pypi.org/account/register/
2. **Verify email**
3. **Enable 2FA** (recommended)
4. **Create API token:**
   - Go to https://pypi.org/manage/account/token/
   - Create token with scope: "Entire account"
   - **Save the token** (you'll need it for GitHub Actions)

### Step 6: Configure GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: (paste your PyPI token)
6. Click "Add secret"

### Step 7: Build and Test Locally

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Check the package
twine check dist/*

# Test installation locally
pip install dist/lixplore-1.0.0-py3-none-any.whl

# Test it works
lixplore --help
lixplore --examples
```

### Step 8: Upload to PyPI (Manual First Time)

```bash
# Upload to Test PyPI first (recommended)
twine upload --repository testpypi dist/*

# Test install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ lixplore

# If everything works, upload to real PyPI
twine upload dist/*
```

### Step 9: Create GitHub Release

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `Lixplore v1.0.0 - Initial Release`
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

**This will automatically trigger the GitHub Action to publish to PyPI!**

### Step 10: Verify Installation

```bash
# Install from PyPI
pip install lixplore

# Test it works
lixplore --help
lixplore -P -q "test" -m 2
```

---

## 🔄 Updating the Package

### For Future Releases

1. **Update version number:**
   - `setup.py` - Update version
   - `pyproject.toml` - Update version
   - `CHANGELOG.md` - Add new version section

2. **Commit changes:**
   ```bash
   git add .
   git commit -m "Release v1.1.0"
   git push
   ```

3. **Create new GitHub release:**
   - Tag: `v1.1.0`
   - GitHub Actions will automatically publish to PyPI

---

## 📦 Package Structure

```
lixplore/
├── .github/
│   └── workflows/
│       ├── publish.yml     # Auto-publish to PyPI
│       └── test.yml        # Cross-platform testing
├── docs/
│   ├── lixplore.1         # Man page
│   ├── lixplore.md        # TLDR page
│   └── README.md
├── lixplore/              # Main package
│   ├── __init__.py
│   ├── cli.py
│   ├── commands.py
│   ├── dispatcher.py
│   ├── search.py
│   ├── sources/
│   └── utils/
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
├── README.md
├── requirements.txt
└── setup.py
```

---

## 🖥️ Platform-Specific Notes

### Linux
- Works out of the box
- Man page can be installed system-wide
- All terminal emulators supported

### macOS
- Works out of the box
- Man page installation: `sudo cp docs/lixplore.1 /usr/local/share/man/man1/`
- Uses Terminal.app for review feature

### Windows
- Works with cmd.exe
- Man page not applicable (use `lixplore --help`)
- Review feature uses cmd.exe

---

## 🧪 Testing Before Release

```bash
# Test on Python 3.7
pyenv install 3.7.17
pyenv local 3.7.17
pip install -e .
lixplore --help

# Test on Python 3.11
pyenv install 3.11.0
pyenv local 3.11.0
pip install -e .
lixplore --help

# Test basic functionality
lixplore -P -q "test" -m 2
lixplore --examples
```

---

## 📊 GitHub Actions

### Auto-Publish Workflow
- Triggers on: New release created
- Builds package
- Uploads to PyPI
- Requires: `PYPI_API_TOKEN` secret

### Testing Workflow
- Triggers on: Push to main/develop
- Tests on: Linux, macOS, Windows
- Python versions: 3.7, 3.8, 3.9, 3.10, 3.11
- Runs basic functionality tests

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Update all URLs in files
- [ ] Update author information
- [ ] Test locally on multiple Python versions
- [ ] Run `python -m build` successfully
- [ ] Run `twine check dist/*` with no errors
- [ ] Test installation from wheel file
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Create PyPI account and API token
- [ ] Add `PYPI_API_TOKEN` to GitHub secrets
- [ ] Test on Test PyPI first
- [ ] Create GitHub release
- [ ] Verify auto-publish works
- [ ] Test installation from PyPI
- [ ] Update badges in README

---

## 🆘 Troubleshooting

### Build Fails
```bash
# Clean and rebuild
rm -rf build/ dist/ *.egg-info
python -m build
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### GitHub Actions Fails
- Check `PYPI_API_TOKEN` secret is set correctly
- Verify token has correct permissions
- Check GitHub Actions logs for details

---

## 🎉 After Successful Deployment

1. Update README badges with actual PyPI version
2. Share on social media / research communities
3. Submit to lists:
   - Awesome CLI tools
   - Awesome Python
   - Research software directories
4. Create documentation website (optional)
5. Set up issue templates
6. Create contributing guidelines

---

## 📧 Support

If you encounter issues during deployment:
- Check GitHub Actions logs
- Review PyPI package page
- Open an issue on GitHub

---

**Good luck with your deployment!** 🚀
