# Lixplore - Quick Deploy Reference Card

**5-Step Deployment in 20 Minutes**

---

## 🚀 Step 1: Update Files (5 min)

Replace `yourusername` with your GitHub username in:

```bash
# 1. setup.py (line 21)
url='https://github.com/YOUR_USERNAME/lixplore',

# 2. pyproject.toml (lines 58-60)
Homepage = "https://github.com/YOUR_USERNAME/lixplore"
Repository = "https://github.com/YOUR_USERNAME/lixplore"

# 3. README.md (multiple lines - search and replace)
yourusername → YOUR_USERNAME
```

Update author info:
- setup.py: author_email
- pyproject.toml: email
- LICENSE: copyright holder (optional)

---

## 📦 Step 2: Build & Test (5 min)

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Test locally
pip install dist/lixplore-1.0.0-py3-none-any.whl
lixplore --help
lixplore -P -q "test" -m 2
```

---

## 🌐 Step 3: GitHub Setup (2 min)

```bash
# Push to GitHub
git add .
git commit -m "Initial release v1.0.0"
git remote add origin https://github.com/YOUR_USERNAME/lixplore.git
git branch -M main
git push -u origin main
```

---

## 🔑 Step 4: PyPI Setup (5 min)

1. Create account: https://pypi.org/account/register/
2. Create API token: https://pypi.org/manage/account/token/
3. Add to GitHub Secrets:
   - Go to: Settings → Secrets and variables → Actions
   - Name: `PYPI_API_TOKEN`
   - Value: (paste your token)

---

## 🎉 Step 5: Release (2 min)

1. Go to: https://github.com/YOUR_USERNAME/lixplore/releases
2. Click: "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Lixplore v1.0.0 - Initial Release`
5. Description: Copy from CHANGELOG.md
6. Click: "Publish release"

**GitHub Actions will automatically publish to PyPI!**

---

## ✅ Verify Installation

```bash
# Wait 2-3 minutes for PyPI to process
pip install lixplore

# Test
lixplore --help
lixplore --examples
```

---

## 🎯 That's It!

Users can now install with:
```bash
pip install lixplore
```

Package is live at:
- PyPI: https://pypi.org/project/lixplore/
- GitHub: https://github.com/YOUR_USERNAME/lixplore

---

## 📚 For More Details

- **DEPLOYMENT_GUIDE.md** - Complete step-by-step guide
- **PACKAGE_DEPLOYMENT_SUMMARY.md** - Full summary
- **README.md** - User documentation

---

**Total Time: ~20 minutes**  
**Status: Ready to Deploy!** 🚀
