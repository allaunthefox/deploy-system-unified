#!/usr/bin/env bash
# Run detect-secrets with the same options used by CI.  This allows
# developers to reproduce the scan locally and understand failures.

set -euo pipefail

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade detect-secrets

# compute baseline path if present
if [ -f ".secrets.baseline" ]; then
  BASELINE=".secrets.baseline"
else
  BASELINE=""
fi

EXCLUDES=(
  --exclude-files 'ci-artifacts/.*'
  --exclude-files '\.secrets_scan\..*'
  --exclude-files 'Offline_Research/.*'
  --exclude-files '(^|/)\.secrets\.baseline$'
  --exclude-files '\.ansible/collections/.*'
  --exclude-files '\.ansible/galaxy_cache/.*'
  --exclude-files '\.collections/.*'
  --exclude-files 'projects/.*/\.collections/.*'
  --exclude-files 'dev_tools/ci/.*'
  --exclude-files '\.git/.*'
  --exclude-files 'inventory/group_vars/.*/secrets.*'
  --exclude-files 'charts/.*/values.*\.ya?ml'
  --exclude-files '.*\.sops\.ya?ml'
)

if [ -n "$BASELINE" ]; then
  echo "Using baseline: $BASELINE"
  base_dir="$(dirname "$BASELINE")"
  tmp_baseline="$(mktemp)"
  cp "$BASELINE" "$tmp_baseline"
  (
    cd "$base_dir"
    detect-secrets scan "${EXCLUDES[@]}" --baseline "$tmp_baseline" 1>/dev/null 2>&1
  )
  echo "Baseline scan completed"
else
  echo "No baseline found, running fresh scan..."
  detect-secrets scan --all-files "${EXCLUDES[@]}" > .secrets_scan.json 2> .secrets_scan.err
fi

echo "Done.  Review .secrets_scan.json and .secrets_scan.err if needed."
