# Installation

## ⚠️ Prerequisites

Before installing Lixplore, ensure you have:

### 1. Python (Version 3.8 or Higher)

Check your Python version:

```bash
python --version
# or
python3 --version
```

If Python is not installed or too old:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: `brew install python3` or download from python.org
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### 2. pip (Python Package Manager)

Check if pip is installed:

```bash
pip --version
# or
pip3 --version
```

Usually comes with Python. If missing:
```bash
python -m ensurepip --upgrade
```

### 3. **Windows Only**: Microsoft C++ Build Tools

**⚠️ IMPORTANT FOR WINDOWS USERS:**

If you're on Windows, you need Microsoft C++ Build Tools to avoid installation errors:

**Option A: Build Tools Only (Recommended - ~6GB)**
1. Download: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Run the installer
3. Select **"Desktop development with C++"**
4. Click Install
5. **Restart your computer** after installation

**Option B: Full Visual Studio (~20GB)**
1. Download: [Visual Studio Community](https://visualstudio.microsoft.com/downloads/)
2. During installation, select **"Desktop development with C++"** workload
3. Restart your computer after installation

> **Why is this needed?** The `gensim` package (a dependency of `litstudy`) requires C++ compilation on Windows. This is a one-time setup.

---

## Installation Methods

### Method 1: Install from PyPI (Recommended)

This is the simplest and recommended method:

```bash
pip install lixplore-cli
```

**On Windows (after installing C++ Build Tools):**
```bash
pip install lixplore-cli
```

Verify the installation:

```bash
lixplore --version
lixplore --help
```

### Method 2: Install from Source

For the latest development version or to contribute:

```bash
# Clone the repository
git clone https://github.com/pryndor/Lixplore_cli.git
cd Lixplore_cli

# Install in development mode
pip install -e .
```

### Method 3: Using pipx (Isolated Installation)

For an isolated installation that doesn't interfere with other Python packages:

```bash
# Install pipx if you don't have it
pip install pipx
pipx ensurepath

# Install lixplore
pipx install lixplore-cli
```

## Dependencies

Lixplore automatically installs these core dependencies:

- `biopython` - PubMed/NCBI API access
- `requests` - HTTP library for API calls
- `litstudy` - Literature study framework
- `openpyxl` - Excel file generation

**Optional dependencies:**
- `rich` - Enhanced TUI mode (install with: `pip install lixplore-cli[all]`)

**Note**: Total installation size is approximately 150-200MB including all dependencies.

## Upgrade

To upgrade to the latest version:

```bash
pip install --upgrade lixplore-cli
```

## Uninstall

To remove Lixplore:

```bash
pip uninstall lixplore-cli
```

## Verify Installation

After installation, verify it works:

```bash
# Check version and help
lixplore --help

# Run a simple test search
lixplore -P -q "test" -m 5
```

## Troubleshooting

### ❌ Error: "Failed to build gensim" (Windows)

This is the most common error on Windows:

**Error Message:**
```
Building wheel for gensim (pyproject.toml) ... error
Failed to build gensim
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solution 1 (Recommended):**
1. Install Microsoft C++ Build Tools (see Prerequisites section above)
2. **Restart your terminal/PowerShell completely**
3. Try installing again:
   ```bash
   pip install lixplore-cli
   ```

**Solution 2 (Alternative):**
```bash
# Upgrade pip and try installing gensim first
pip install --upgrade pip setuptools wheel
pip install gensim --no-cache-dir
pip install lixplore-cli
```

**Solution 3 (If still failing):**
```bash
# Install from pre-built wheels
pip install --only-binary :all: gensim
pip install lixplore-cli
```

**Still having issues?** Report at: https://github.com/pryndor/Lixplore_cli/issues

---

### ❌ Error: "command 'pip' not found"

**Solution:**
```bash
# Try pip3 instead
pip3 install lixplore-cli

# Or use Python module syntax
python -m pip install lixplore-cli
# or
python3 -m pip install lixplore-cli
```

---

### ❌ Error: "command 'lixplore' not found" (After Installation)

**On Linux/macOS:**
```bash
# Add pip's bin directory to PATH
export PATH=$PATH:~/.local/bin

# Make it permanent
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

**On Windows:**
- The Scripts directory should be in PATH automatically
- If not, add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X\Scripts`

---

### ❌ Error: Permission denied

**On Linux/Mac:**
```bash
# Install for current user only (no sudo needed)
pip install --user lixplore-cli
```

**On Windows:**
- Right-click Command Prompt → "Run as administrator"
- Then run: `pip install lixplore-cli`

---

### ❌ Error: Python version too old

Check your Python version:

```bash
python3 --version
```

If it's below 3.8, you need to upgrade Python:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: `brew install python3`
- **Linux**: `sudo apt install python3.10` (or newer)

---

### ✅ Verify Installation

After successful installation:

```bash
# Check version
lixplore --version

# Should show: Lixplore v1.0.1 or higher

# Test basic functionality
lixplore --help

# Quick test search
lixplore -P -q "test" -m 5
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Basic Usage](basic-usage.md)
- [First Search](first-search.md)
