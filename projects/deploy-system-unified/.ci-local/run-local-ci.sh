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
  # run with JSON output; fall back to plaintext if needed
  detect-secrets scan --all-files --json > .secrets_scan.json 2> detect_secrets.err || true
  if [ ! -s .secrets_scan.json ]; then
    log "JSON output empty; falling back to plaintext"
    detect-secrets scan --all-files > .secrets_scan.txt 2>> detect_secrets.err || true
  fi
  mv -v .secrets_scan.json .secrets_scan.txt detect_secrets.err "$ARTIFACT_DIR/" || true
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
