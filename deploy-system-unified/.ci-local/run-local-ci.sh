#!/usr/bin/env bash
set -euo pipefail

# Local CI runner script
# Usage: run-local-ci.sh [all|style|detect-secrets]

JOB=${1:-all}
ROOT="$(pwd)"
ARTIFACT_DIR="projects/deploy-system-unified/ci-artifacts"
mkdir -p "$ARTIFACT_DIR"

log() { echo "[local-ci] $*"; }

run_style() {
  log "Running style enforcement script (report)"
  chmod +x dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh
  ./dev_tools/tools/style-guide-enforcement/enforce_style_guide.sh --report || true
  # copy latest report into artifacts
  cp -v $(ls -t dev_tools/tools/style-guide-enforcement/compliance_report_*.md 2>/dev/null | head -n1) "$ARTIFACT_DIR/" || true
}

run_detect_secrets() {
  log "Running detect-secrets scan (v1.3.0)"
  # run with default output (JSON)
  detect-secrets scan --all-files --exclude-files "ci-artifacts/.*" --exclude-files "ansible.log" > .secrets_scan.json 2> detect_secrets.err || true

  # produce a human-readable findings file (matches CI behaviour)
  findings_file=".detect-secrets-findings.md"
  echo "# Detect Secrets findings" > "$findings_file" || true
  if [ -s .secrets_scan.json ] && command -v jq >/dev/null 2>&1; then
    if jq -e '.results' .secrets_scan.json >/dev/null 2>&1; then
      count=$(jq '.results | keys | length' .secrets_scan.json)
      if [ "$count" -gt 0 ]; then
        jq -r '.results | to_entries[] | "\(.key)\t\(.value[]?.type // \"unknown\")\t\(.value[]?.line_number // -1)\t\(.value[]?.is_verified)"' .secrets_scan.json | while IFS=$'\t' read -r filepath type line verified; do
          echo "- **${filepath}:${line}** — ${type} — verified: ${verified}" >> "$findings_file" || true
          if [ "${line}" -ge 1 ] 2>/dev/null; then
            start=$((line > 3 ? line - 3 : 1)) || true
            end=$((line + 3)) || true
            echo '\n```\n' >> "$findings_file" || true
            sed -n "${start},${end}p" "${filepath}" 2>/dev/null | sed -n '1,200p' >> "$findings_file" || echo "(file snippet unavailable)" >> "$findings_file"
            echo '\n```\n' >> "$findings_file" || true
          fi
        done
      fi
    fi
  fi

  if [ -s .secrets_scan.json ]; then
    cp .secrets_scan.json .secrets_scan.txt
  else
    log "JSON output empty; check error log"
  fi
  mv -v .secrets_scan.json .secrets_scan.txt detect_secrets.err .detect-secrets-findings.md "$ARTIFACT_DIR/" || true
}

case "$JOB" in
  all)
    run_style
    run_detect_secrets
    ;;
  style)
    run_style
    ;;
  detect-secrets)
    run_detect_secrets
    ;;
  *)
    echo "Unknown job: $JOB"
    exit 2
    ;;
esac

log "Local CI done. Artifacts under $ARTIFACT_DIR"
exit 0
