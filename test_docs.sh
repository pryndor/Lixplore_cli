#!/bin/bash
# Documentation Testing and Verification Script

echo "=============================================="
echo "Lixplore Documentation Testing"
echo "=============================================="
echo

PASS=0
FAIL=0
WARN=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

test_file() {
    local file="$1"
    local required="$2"
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file"
        ((PASS++))
        return 0
    else
        if [ "$required" = "required" ]; then
            echo -e "${RED}✗${NC} $file (MISSING - REQUIRED)"
            ((FAIL++))
        else
            echo -e "${YELLOW}⚠${NC} $file (missing - optional)"
            ((WARN++))
        fi
        return 1
    fi
}

echo -e "${BLUE}=== Core Configuration ===${NC}"
test_file "mkdocs.yml" "required"
test_file ".github/workflows/docs.yml" "required"

echo
echo -e "${BLUE}=== Homepage ===${NC}"
test_file "docs/index.md" "required"

echo
echo -e "${BLUE}=== Getting Started (4 files) ===${NC}"
test_file "docs/getting-started/installation.md" "required"
test_file "docs/getting-started/quickstart.md" "required"
test_file "docs/getting-started/basic-usage.md" "required"
test_file "docs/getting-started/first-search.md" "required"

echo
echo -e "${BLUE}=== User Guide (6 files) ===${NC}"
test_file "docs/guide/search-sources.md" "required"
test_file "docs/guide/filtering.md" "required"
test_file "docs/guide/export.md" "required"
test_file "docs/guide/annotations.md" "required"
test_file "docs/guide/interactive.md" "required"
test_file "docs/guide/pdf.md" "required"

echo
echo -e "${BLUE}=== Advanced Features (5 files) ===${NC}"
test_file "docs/advanced/automation.md" "required"
test_file "docs/advanced/ai-integration.md" "required"
test_file "docs/advanced/profiles.md" "required"
test_file "docs/advanced/custom-apis.md" "required"
test_file "docs/advanced/zotero.md" "required"

echo
echo -e "${BLUE}=== Command Reference (9 files) ===${NC}"
test_file "docs/reference/flags-overview.md" "required"
test_file "docs/reference/source-flags.md" "required"
test_file "docs/reference/search-flags.md" "required"
test_file "docs/reference/filter-flags.md" "required"
test_file "docs/reference/display-flags.md" "required"
test_file "docs/reference/export-flags.md" "required"
test_file "docs/reference/annotation-flags.md" "required"
test_file "docs/reference/interactive-flags.md" "required"
test_file "docs/reference/utility-flags.md" "required"

echo
echo -e "${BLUE}=== Examples (4 files) ===${NC}"
test_file "docs/examples/workflows.md" "required"
test_file "docs/examples/use-cases.md" "required"
test_file "docs/examples/integrations.md" "required"
test_file "docs/examples/automation-examples.md" "required"

echo
echo -e "${BLUE}=== About Section (4 files) ===${NC}"
test_file "docs/about/changelog.md" "required"
test_file "docs/about/contributing.md" "required"
test_file "docs/about/license.md" "required"
test_file "docs/about/faq.md" "required"

echo
echo -e "${BLUE}=== Deployment Scripts ===${NC}"
test_file "deploy_docs.sh" "required"
test_file "quick_docs_setup.sh" "required"

echo
echo "=============================================="
echo -e "${BLUE}Testing MkDocs Build...${NC}"
echo "=============================================="

cd /home/bala/Lixplore_cli
if mkdocs build -q 2>/dev/null; then
    echo -e "${GREEN}✓ MkDocs build successful${NC}"
    ((PASS++))
    
    # Check site directory
    if [ -d "site" ]; then
        SITE_FILES=$(find site -type f | wc -l)
        echo -e "${GREEN}✓ Generated $SITE_FILES files in site/ directory${NC}"
        ((PASS++))
    fi
else
    echo -e "${RED}✗ MkDocs build failed${NC}"
    echo "Run 'mkdocs build' for details"
    ((FAIL++))
fi

echo
echo "=============================================="
echo "RESULTS"
echo "=============================================="
echo -e "${GREEN}Passed:  $PASS${NC}"
if [ $FAIL -gt 0 ]; then
    echo -e "${RED}Failed:  $FAIL${NC}"
fi
if [ $WARN -gt 0 ]; then
    echo -e "${YELLOW}Warnings: $WARN${NC}"
fi

echo
if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}=============================================="
    echo "✓ ALL TESTS PASSED - READY TO DEPLOY!"
    echo "=============================================="
    echo
    echo "Next steps:"
    echo "  1. Preview locally:  ./quick_docs_setup.sh"
    echo "  2. Deploy:           ./deploy_docs.sh --deploy"
    echo -e "${NC}"
    exit 0
else
    echo -e "${RED}=============================================="
    echo "✗ TESTS FAILED - FIX ERRORS BEFORE DEPLOYING"
    echo "=============================================="
    echo -e "${NC}"
    exit 1
fi
