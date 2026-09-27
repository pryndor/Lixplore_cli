#!/bin/bash

# Installation script for lixplore man page

set -e

echo "Installing lixplore man page..."

# Determine man page directory
if [ -d "/usr/local/share/man/man1" ]; then
    MAN_DIR="/usr/local/share/man/man1"
elif [ -d "/usr/share/man/man1" ]; then
    MAN_DIR="/usr/share/man/man1"
elif [ -d "$HOME/.local/share/man/man1" ]; then
    MAN_DIR="$HOME/.local/share/man/man1"
else
    # Create user-local man directory
    MAN_DIR="$HOME/.local/share/man/man1"
    mkdir -p "$MAN_DIR"
    echo "Created directory: $MAN_DIR"
fi

# Copy man page
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAN_SOURCE="$SCRIPT_DIR/lixplore.1"

if [ ! -f "$MAN_SOURCE" ]; then
    echo "Error: Man page file not found at $MAN_SOURCE"
    exit 1
fi

# Check if we need sudo
if [ ! -w "$MAN_DIR" ]; then
    echo "Installing to $MAN_DIR (requires sudo)..."
    sudo cp "$MAN_SOURCE" "$MAN_DIR/lixplore.1"
    sudo chmod 644 "$MAN_DIR/lixplore.1"
    
    # Update man database
    if command -v mandb >/dev/null 2>&1; then
        sudo mandb -q
    fi
else
    echo "Installing to $MAN_DIR..."
    cp "$MAN_SOURCE" "$MAN_DIR/lixplore.1"
    chmod 644 "$MAN_DIR/lixplore.1"
    
    # Update man database
    if command -v mandb >/dev/null 2>&1; then
        mandb -q
    fi
fi

echo "✓ Man page installed successfully!"
echo ""
echo "You can now view the man page with:"
echo "  man lixplore"
echo ""
echo "To uninstall, run:"
echo "  sudo rm $MAN_DIR/lixplore.1"
