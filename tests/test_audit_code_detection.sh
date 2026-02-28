#!/bin/bash
# =============================================================================
# Audit Event Identifier: DSU-TST-1000110
# Script Type: Audit Code Validation Test
# Description: Validates that audit codes are present and detectable across all files
# Usage: ./test_audit_code_detection.sh [--verbose] [--json]
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
# Audit Code Detection Test Script
# Scans the repository for audit code patterns and validates coverage

set -eu

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL_FILES=0
FILES_WITH_CODES=0
FILES_WITHOUT_CODES=0
INVALID_CODES=0

# Arrays for tracking
declare -a MISSING_FILES=()
declare -a INVALID_FILES=()
declare -a VALID_FILES=()

# Output format (text/json)
OUTPUT_FORMAT="text"
VERBOSE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --json|-j)
            OUTPUT_FORMAT="json"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--verbose] [--json]"
            echo ""
            echo "Options:"
            echo "  --verbose, -v    Show detailed output for each file"
            echo "  --json, -j       Output results in JSON format"
            echo "  --help, -h       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# ============================================================================
# Test Functions
# ============================================================================

echo "=== Deploy-System-Unified Audit Code Detection Test ==="
echo "Project: $PROJECT_DIR"
echo "Date: $(date -Iseconds)"
echo ""

# Test 1: Check for audit code pattern in files
echo "[Test 1/5] Scanning for 'Audit Event Identifier' pattern..."

# Define file patterns to check (used for documentation)
# Actual scanning uses find directly for better reliability

# Scan files by category
scan_category() {
    local category="$1"
    local pattern="$2"
    
    echo ""
    echo "  Category: $category"
    echo "  Pattern: $pattern"
    
    local found=0
    local missing=0
    
    # Find files matching pattern
    while IFS= read -r -d '' file; do
        TOTAL_FILES=$((TOTAL_FILES + 1))
        
        if grep -q "Audit Event Identifier" "$file" 2>/dev/null; then
            FILES_WITH_CODES=$((FILES_WITH_CODES + 1))
            found=$((found + 1))
            
            # Validate code format
            if grep -qE "DSU-[A-Z]{3}-[0-9]{6}" "$file" 2>/dev/null; then
                VALID_FILES+=("$file")
                if [ "$VERBOSE" = true ]; then
                    code=$(grep -oE "DSU-[A-Z]{3}-[0-9]{6}" "$file" | head -1)
                    echo -e "    ${GREEN}✓${NC} $file -> $code"
                fi
            else
                INVALID_CODES=$((INVALID_CODES + 1))
                INVALID_FILES+=("$file")
                if [ "$VERBOSE" = true ]; then
                    echo -e "    ${YELLOW}⚠${NC} $file (invalid format)"
                fi
            fi
        else
            FILES_WITHOUT_CODES=$((FILES_WITHOUT_CODES + 1))
            missing=$((missing + 1))
            MISSING_FILES+=("$file")
            if [ "$VERBOSE" = true ]; then
                echo -e "    ${RED}✗${NC} $file (missing)"
            fi
        fi
    done < <(find "$PROJECT_DIR" -path "*/.ansible/collections" -prune -o -path "*/.git" -prune -o -path "*/node_modules" -prune -o -type f -name "${pattern%%:*}" -print0 2>/dev/null)
    
    if [ $found -gt 0 ]; then
        echo -e "  Result: ${GREEN}PASS${NC} - $found/$((found + missing)) files have audit codes"
    else
        echo -e "  Result: ${RED}FAIL${NC} - 0 files found or all missing"
    fi
}

# Run scans for each category
echo ""
echo "Scanning file categories..."
echo "=========================================="

# YAML files (playbooks, roles, inventory)
scan_category "Playbooks & Roles (YAML)" "*.yml" 300

# Python files
scan_category "Python Scripts" "*.py" 20

# Shell scripts
scan_category "Shell Scripts" "*.sh" 30

# Jinja2 templates
scan_category "Jinja2 Templates" "*.j2" 40

# Markdown documentation
scan_category "Markdown Documentation" "*.md" 30

# Container files
scan_category "Container Files" "Containerfile" 1

# Test 2: Validate code format
echo ""
echo "[Test 2/5] Validating audit code format..."

VALID_FORMAT_COUNT=0
INVALID_FORMAT_COUNT=0

while IFS= read -r -d '' file; do
    if grep -q "Audit Event Identifier" "$file" 2>/dev/null; then
        code=$(grep -oE "DSU-[A-Z]{3}-[0-9]{6}" "$file" 2>/dev/null | head -1)
        if [ -n "$code" ]; then
            VALID_FORMAT_COUNT=$((VALID_FORMAT_COUNT + 1))
        else
            INVALID_FORMAT_COUNT=$((INVALID_FORMAT_COUNT + 1))
            if [ "$VERBOSE" = true ]; then
                echo -e "  ${YELLOW}⚠${NC} Invalid format in: $file"
            fi
        fi
    fi
done < <(find "$PROJECT_DIR" \( -name "*.yml" -o -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.j2" -o -name "*.ini" -o -name "*.yaml" -o -name "Containerfile" \) -type f -not -path "*/.ansible/*" -not -path "*/.git/*" -not -path "*/node_modules/*" -print0 2>/dev/null)

if [ $INVALID_FORMAT_COUNT -eq 0 ]; then
    echo -e "  Result: ${GREEN}PASS${NC} - All $VALID_FORMAT_COUNT codes have valid format (DSU-XXX-NNNNNN)"
else
    echo -e "  Result: ${YELLOW}WARN${NC} - $INVALID_FORMAT_COUNT codes have invalid format"
fi

# Test 3: Check registry files exist
echo ""
echo "[Test 3/5] Checking registry files..."

REGISTRY_FILES=(
    "AUDIT_CODE_SYSTEM_INDEX.md"
    "DOCUMENT_AUDIT_REGISTRY.md"
    "CODE_CONFIG_AUDIT_REGISTRY.md"
    "docs/deployment/mermaid/VERSION_CONTROL.md"
    "AUDIT_CODE_IMPLEMENTATION_GUIDE.md"
    "AUDIT_CODE_SUMMARY.md"
)

REGISTRY_FOUND=0
REGISTRY_MISSING=0

for registry in "${REGISTRY_FILES[@]}"; do
    if [ -f "$PROJECT_DIR/$registry" ]; then
        REGISTRY_FOUND=$((REGISTRY_FOUND + 1))
        if [ "$VERBOSE" = true ]; then
            echo -e "  ${GREEN}✓${NC} $registry"
        fi
    else
        REGISTRY_MISSING=$((REGISTRY_MISSING + 1))
        echo -e "  ${RED}✗${NC} $registry (missing)"
    fi
done

if [ $REGISTRY_MISSING -eq 0 ]; then
    echo -e "  Result: ${GREEN}PASS${NC} - All $REGISTRY_FOUND registry files present"
else
    echo -e "  Result: ${RED}FAIL${NC} - $REGISTRY_MISSING registry files missing"
fi

# Test 4: Verify code uniqueness
echo ""
echo "[Test 4/5] Checking for duplicate audit codes..."

DUPLICATE_COUNT=0
ALL_CODES=$(find "$PROJECT_DIR" \( -name "*.yml" -o -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.j2" -o -name "*.ini" -o -name "*.yaml" -o -name "Containerfile" \) -type f -not -path "*/.ansible/*" -not -path "*/.git/*" -not -path "*/node_modules/*" -exec grep -ohE "DSU-[A-Z]{3}-[0-9]{6}" {} \; 2>/dev/null | sort)

UNIQUE_CODES=$(echo "$ALL_CODES" | sort -u)

TOTAL_UNIQUE=$(echo "$UNIQUE_CODES" | wc -l)
TOTAL_ALL=$(echo "$ALL_CODES" | wc -l)

if [ "$TOTAL_UNIQUE" -eq "$TOTAL_ALL" ]; then
    echo -e "  Result: ${GREEN}PASS${NC} - All $TOTAL_UNIQUE codes are unique"
else
    DUPLICATE_COUNT=$((TOTAL_ALL - TOTAL_UNIQUE))
    echo -e "  Result: ${YELLOW}WARN${NC} - Found $DUPLICATE_COUNT duplicate codes"
    
    if [ "$VERBOSE" = true ]; then
        echo "  Duplicates:"
        echo "$ALL_CODES" | sort | uniq -d | while read -r dup; do
            echo "    - $dup"
        done
    fi
fi

# Test 5: Coverage calculation
echo ""
echo "[Test 5/5] Calculating coverage..."

# Count expected files (excluding vendor/external)
EXPECTED_YAML=$(find "$PROJECT_DIR" -path "*/.ansible/*" -prune -o -path "*/.git/*" -prune -o -path "*/node_modules/*" -prune -o \( -name "*.yml" -o -name "*.yaml" \) -type f -print 2>/dev/null | grep -cv ".ansible")
EXPECTED_PY=$(find "$PROJECT_DIR" -path "*/.ansible/*" -prune -o -path "*/.git/*" -prune -o -path "*/node_modules/*" -prune -o -name "*.py" -type f -print 2>/dev/null | wc -l)
EXPECTED_SH=$(find "$PROJECT_DIR" -path "*/.ansible/*" -prune -o -path "*/.git/*" -prune -o -path "*/node_modules/*" -prune -o -name "*.sh" -type f -print 2>/dev/null | wc -l)
EXPECTED_MD=$(find "$PROJECT_DIR" -path "*/.ansible/*" -prune -o -path "*/.git/*" -prune -o -path "*/node_modules/*" -prune -o -name "*.md" -type f -print 2>/dev/null | grep -cE "(docs|wiki_pages|roles)")

TOTAL_EXPECTED=$((EXPECTED_YAML + EXPECTED_PY + EXPECTED_SH + EXPECTED_MD))

# Calculate percentage
if [ $TOTAL_EXPECTED -gt 0 ]; then
    COVERAGE_PCT=$((FILES_WITH_CODES * 100 / TOTAL_EXPECTED))
else
    COVERAGE_PCT=0
fi

echo "  Expected files: $TOTAL_EXPECTED"
echo "  Files with codes: $FILES_WITH_CODES"
echo "  Files without codes: $FILES_WITHOUT_CODES"

if [ $COVERAGE_PCT -ge 95 ]; then
    echo -e "  Result: ${GREEN}PASS${NC} - Coverage: ${COVERAGE_PCT}%"
elif [ $COVERAGE_PCT -ge 80 ]; then
    echo -e "  Result: ${YELLOW}WARN${NC} - Coverage: ${COVERAGE_PCT}%"
else
    echo -e "  Result: ${RED}FAIL${NC} - Coverage: ${COVERAGE_PCT}%"
fi

# ============================================================================
# Generate Report
# ============================================================================

echo ""
echo "=========================================="
echo "           TEST SUMMARY"
echo "=========================================="
echo ""

if [ "$OUTPUT_FORMAT" = "json" ]; then
    # JSON output
    cat << EOF
{
  "test_date": "$(date -Iseconds)",
  "project": "$PROJECT_DIR",
  "results": {
    "total_files_scanned": $TOTAL_FILES,
    "files_with_codes": $FILES_WITH_CODES,
    "files_without_codes": $FILES_WITHOUT_CODES,
    "valid_codes": $VALID_FORMAT_COUNT,
    "invalid_codes": $INVALID_CODES,
    "duplicate_codes": $DUPLICATE_COUNT,
    "registry_files_present": $REGISTRY_FOUND,
    "registry_files_missing": $REGISTRY_MISSING,
    "coverage_percentage": $COVERAGE_PCT
  },
  "status": "$([ $COVERAGE_PCT -ge 95 ] && echo "PASS" || echo "FAIL")",
  "unique_codes_count": $TOTAL_UNIQUE
}
EOF
else
    # Text output
    echo "Test Results:"
    echo "  Total files scanned:     $TOTAL_FILES"
    echo "  Files with codes:        $FILES_WITH_CODES"
    echo "  Files without codes:     $FILES_WITHOUT_CODES"
    echo "  Valid code format:       $VALID_FORMAT_COUNT"
    echo "  Invalid code format:     $INVALID_CODES"
    echo "  Duplicate codes:         $DUPLICATE_COUNT"
    echo "  Registry files present:  $REGISTRY_FOUND"
    echo "  Registry files missing:  $REGISTRY_MISSING"
    echo ""
    echo "  Coverage:                  ${COVERAGE_PCT}%"
    echo ""
    
    if [ $COVERAGE_PCT -ge 95 ] && [ $REGISTRY_MISSING -eq 0 ] && [ $INVALID_CODES -eq 0 ]; then
        echo -e "Overall Status: ${GREEN}✓ PASS${NC}"
        echo ""
        echo "All audit codes are properly implemented and detectable!"
        exit 0
    else
        echo -e "Overall Status: ${RED}✗ FAIL${NC}"
        echo ""
        
        if [ $COVERAGE_PCT -lt 95 ]; then
            echo "  - Coverage below 95% threshold"
        fi
        if [ $REGISTRY_MISSING -gt 0 ]; then
            echo "  - Missing registry files"
        fi
        if [ $INVALID_CODES -gt 0 ]; then
            echo "  - Invalid code formats detected"
        fi
        if [ $DUPLICATE_COUNT -gt 0 ]; then
            echo "  - Duplicate codes found"
        fi
        
        exit 1
    fi
fi
