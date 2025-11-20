#!/bin/bash
# Script to create GitHub issues using GitHub CLI (gh)
# This script reads issues_data.json and creates issues using the gh CLI tool
#
# Prerequisites:
#   - GitHub CLI (gh) must be installed and authenticated
#   - jq must be installed for JSON parsing
#
# Usage:
#   ./create_issues.sh [--dry-run]
#
# Example:
#   ./create_issues.sh           # Create issues
#   ./create_issues.sh --dry-run # Preview issues without creating

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed${NC}"
    echo "Install it with: sudo apt install jq (Ubuntu) or brew install jq (Mac)"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Parse arguments
DRY_RUN=false
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
fi

# Check if issues_data.json exists
if [ ! -f "issues_data.json" ]; then
    echo -e "${RED}Error: issues_data.json not found${NC}"
    exit 1
fi

# Count total issues
TOTAL=$(jq length issues_data.json)

echo -e "${BLUE}Loaded $TOTAL issues from issues_data.json${NC}"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}DRY RUN - Issues that would be created:${NC}"
    echo "========================================"
    
    COUNT=0
    while read -r issue; do
        COUNT=$((COUNT + 1))
        TITLE=$(echo "$issue" | jq -r '.title')
        LABELS=$(echo "$issue" | jq -r '.labels | join(", ")')
        BODY_PREVIEW=$(echo "$issue" | jq -r '.body' | head -c 100)
        
        echo ""
        echo -e "${GREEN}$COUNT. $TITLE${NC}"
        echo -e "   Labels: ${BLUE}$LABELS${NC}"
        echo "   Body preview: $BODY_PREVIEW..."
    done < <(jq -c '.[]' issues_data.json)
    
    echo ""
    echo "========================================"
    echo -e "${YELLOW}To create these issues, run without --dry-run flag${NC}"
    exit 0
fi

# Create issues
echo -e "${BLUE}Creating issues in repository...${NC}"
echo "========================================"

CREATED=0
FAILED=0
COUNT=0

while read -r issue; do
    COUNT=$((COUNT + 1))
    TITLE=$(echo "$issue" | jq -r '.title')
    BODY=$(echo "$issue" | jq -r '.body')
    LABELS=$(echo "$issue" | jq -r '.labels | join(",")')
    
    echo ""
    echo -e "${BLUE}[$COUNT/$TOTAL] Creating: $TITLE${NC}"
    
    # Create the issue
    if ISSUE_URL=$(gh issue create --title "$TITLE" --body "$BODY" --label "$LABELS" 2>&1); then
        CREATED=$((CREATED + 1))
        echo -e "${GREEN}✓ Created: $ISSUE_URL${NC}"
    else
        FAILED=$((FAILED + 1))
        echo -e "${RED}✗ Failed to create issue${NC}"
        echo -e "${RED}Error: $ISSUE_URL${NC}"
    fi
    
    # Small delay to avoid rate limiting
    sleep 1
done < <(jq -c '.[]' issues_data.json)

# Summary
echo ""
echo "========================================"
echo -e "${BLUE}Summary:${NC}"
echo "  Total issues: $TOTAL"
echo -e "  ${GREEN}Successfully created: $CREATED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "  ${RED}Failed: $FAILED${NC}"
fi

if [ $CREATED -eq $TOTAL ]; then
    echo ""
    echo -e "${GREEN}✓ All issues created successfully!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}✗ Some issues failed to create${NC}"
    exit 1
fi
