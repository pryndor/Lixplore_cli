# Installation

## Requirements

- **Python**: 3.8 or higher
- **pip**: Python package manager (usually comes with Python)
- **Operating System**: Linux, macOS, or Windows

## Installation Methods

### Method 1: Install from PyPI (Recommended)

This is the simplest and recommended method:

```bash
pip install lixplore
```

Verify the installation:

```bash
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
pipx install lixplore
```

## Dependencies

Lixplore automatically installs these dependencies:

- `requests` - HTTP library for API calls
- `beautifulsoup4` - HTML parsing
- `openpyxl` - Excel file generation
- `rich` - Terminal formatting
- `prompt_toolkit` - Interactive TUI

**Note**: Lixplore has NO machine learning dependencies. It's lightweight and fast!

## Upgrade

To upgrade to the latest version:

```bash
pip install --upgrade lixplore
```

## Uninstall

To remove Lixplore:

```bash
pip uninstall lixplore
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

### Command not found

If you get "command not found", ensure pip's bin directory is in your PATH:

```bash
# On Linux/macOS
export PATH=$PATH:~/.local/bin

# Or add to ~/.bashrc or ~/.zshrc
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
```

### Permission denied

If you get permission errors, try installing for your user only:

```bash
pip install --user lixplore
```

### Python version too old

Check your Python version:

```bash
python3 --version
```

If it's below 3.8, upgrade Python first.

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Basic Usage](basic-usage.md)
- [First Search](first-search.md)
