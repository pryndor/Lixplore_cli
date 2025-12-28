#!/bin/bash
# Lixplore Documentation Deployment Script

set -e  # Exit on error

echo "=============================================="
echo "Lixplore Documentation Deployment"
echo "=============================================="
echo

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "mkdocs.yml" ]; then
    echo -e "${RED}Error: mkdocs.yml not found. Please run from Lixplore_cli root directory.${NC}"
    exit 1
fi

echo -e "${BLUE}[1/5] Checking dependencies...${NC}"
# Check if mkdocs is installed
if ! command -v mkdocs &> /dev/null; then
    echo -e "${YELLOW}MkDocs not found. Installing...${NC}"
    pip install mkdocs mkdocs-material
else
    echo -e "${GREEN}MkDocs is installed${NC}"
fi

echo
echo -e "${BLUE}[2/5] Validating documentation structure...${NC}"
# Count markdown files
MD_COUNT=$(find docs -name "*.md" -type f | wc -l)
echo -e "${GREEN}Found $MD_COUNT documentation files${NC}"

# Check key files exist
KEY_FILES=(
    "docs/index.md"
    "docs/getting-started/installation.md"
    "docs/getting-started/quickstart.md"
    "docs/reference/flags-overview.md"
    "mkdocs.yml"
)

for file in "${KEY_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file (missing)"
    fi
done

echo
echo -e "${BLUE}[3/5] Building documentation site...${NC}"
mkdocs build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Documentation built successfully in site/ directory${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

echo
echo -e "${BLUE}[4/5] Testing documentation locally...${NC}"
echo -e "${YELLOW}Starting local server on http://127.0.0.1:8000${NC}"
echo -e "${YELLOW}Press Ctrl+C when done reviewing, then you can deploy.${NC}"
echo
mkdocs serve

echo
echo -e "${BLUE}[5/5] Ready to deploy!${NC}"
echo
echo -e "${YELLOW}To deploy to GitHub Pages, run:${NC}"
echo -e "${GREEN}    mkdocs gh-deploy${NC}"
echo
echo -e "${YELLOW}Or run this script with --deploy flag:${NC}"
echo -e "${GREEN}    ./deploy_docs.sh --deploy${NC}"

# Handle --deploy flag
if [ "$1" == "--deploy" ]; then
    echo
    echo -e "${BLUE}[DEPLOY] Deploying to GitHub Pages...${NC}"
    echo -e "${YELLOW}This will push to the gh-pages branch.${NC}"
    echo -e "${YELLOW}Your documentation will be live at:${NC}"
    echo -e "${GREEN}    https://pryndor.github.io/Lixplore_cli/${NC}"
    echo
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mkdocs gh-deploy --force
        if [ $? -eq 0 ]; then
            echo
            echo -e "${GREEN}=============================================="
            echo "✓ Documentation deployed successfully!"
            echo "=============================================="
            echo
            echo "Your documentation is live at:"
            echo "https://pryndor.github.io/Lixplore_cli/"
            echo
            echo "Note: It may take a few minutes for GitHub Pages to update."
            echo -e "${NC}"
        else
            echo -e "${RED}✗ Deployment failed${NC}"
            exit 1
        fi
    else
        echo "Deployment cancelled."
    fi
fi

echo
echo -e "${GREEN}=============================================="
echo "Documentation setup complete!"
echo "=============================================="
echo -e "${NC}"
