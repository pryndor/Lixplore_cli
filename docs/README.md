# Lixplore Documentation

This directory contains documentation files for Lixplore.

## Files

### Man Page
- **lixplore.1** - Unix man page in groff format
- **install_man_page.sh** - Installation script for the man page

### TLDR Page
- **lixplore.md** - TLDR-style quick reference page

## Installing the Man Page

### Option 1: Using the install script (Recommended)
```bash
cd docs/
./install_man_page.sh
```

### Option 2: Manual installation
```bash
# Copy to user-local man directory
mkdir -p ~/.local/share/man/man1
cp docs/lixplore.1 ~/.local/share/man/man1/
mandb -q

# Or system-wide (requires sudo)
sudo cp docs/lixplore.1 /usr/local/share/man/man1/
sudo mandb -q
```

### Viewing the man page
```bash
man lixplore
```

## Using the TLDR Page

The TLDR page (lixplore.md) follows the [tldr-pages](https://github.com/tldr-pages/tldr) format.

### View with tldr client
If you have `tldr` installed:
```bash
# Copy to tldr cache
mkdir -p ~/.local/share/tldr/pages/common/
cp docs/lixplore.md ~/.local/share/tldr/pages/common/
tldr lixplore
```

### View directly
```bash
cat docs/lixplore.md
```

Or use any markdown viewer:
```bash
glow docs/lixplore.md  # If you have glow installed
mdless docs/lixplore.md  # If you have mdless installed
```

## Man Page vs TLDR

- **Man Page (lixplore.1)** - Comprehensive reference with all options and details
- **TLDR Page (lixplore.md)** - Quick examples for common use cases

Use `man lixplore` for complete documentation or `tldr lixplore` for quick examples.
