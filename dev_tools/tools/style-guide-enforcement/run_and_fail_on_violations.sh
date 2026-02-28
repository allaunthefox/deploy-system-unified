#!/bin/sh
# =============================================================================
# Audit Event Identifier: DSU-SHS-400027
# Script Type: CI Gate (Style Enforcement)
# Description: Runs style enforcement and fails on violations
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
set -eu
ENFORCE_SCRIPT="$(dirname "$0")/enforce_style_guide.sh"
REPORT_DIR="$(dirname "$0")"

if [ ! -x "$ENFORCE_SCRIPT" ]; then
  chmod +x "$ENFORCE_SCRIPT" || true
fi

# Run enforcement
"$ENFORCE_SCRIPT" "$@"

# Find latest report
# shellcheck disable=SC2012
LATEST_REPORT=$(ls -1t "$REPORT_DIR"/compliance_report_*.md 2>/dev/null | head -n1 || true)
if [ -z "$LATEST_REPORT" ]; then
  echo "Enforcement script did not produce a report in $REPORT_DIR"
  exit 2
fi

# Look for total issues == 0
if grep -q "\*\*Total Issues Found:\*\* 0" "$LATEST_REPORT"; then
  echo "No style guide violations found in $LATEST_REPORT"
  exit 0
else
  echo "Style guide violations detected — failing. See: $LATEST_REPORT"
  echo "---- Report preview (first 200 lines) ----"
  sed -n '1,200p' "$LATEST_REPORT" || true
  exit 1
fi
