#!/bin/bash
# Quick Documentation Setup for Lixplore

echo "======================================"
echo "Lixplore Quick Documentation Setup"
echo "======================================"
echo

# Install dependencies
echo "[1/3] Installing MkDocs..."
pip install -q mkdocs mkdocs-material

# Build docs
echo "[2/3] Building documentation..."
cd /home/bala/Lixplore_cli
mkdocs build -q

# Start server
echo "[3/3] Starting documentation server..."
echo
echo "✓ Documentation server starting at:"
echo "  http://127.0.0.1:8000"
echo
echo "Press Ctrl+C to stop the server"
echo

mkdocs serve
