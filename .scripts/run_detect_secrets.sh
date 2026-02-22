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

# replicate identical excludes from CI workflow
EXCLUDES=(
  --exclude-files 'ci-artifacts/.*'
  --exclude-files '\.secrets_scan\..*'
  --exclude-files 'Offline_Research/.*'
  --exclude-files '(^|/)\.secrets\.baseline$'
  --exclude-files '\.ansible/collections/.*'
  --exclude-files '\.ansible/galaxy_cache/.*'
  --exclude-files 'dev_tools/ci/.*'
  --exclude-files '\.git/.*'
  --exclude-files '\.github/workflows/vault-secrets\.yml'
  --exclude-files 'inventory/group_vars/.*/secrets.*'
  --exclude-files 'charts/.*/values.*\.ya?ml'
  --exclude-files '.*\.sops\.ya?ml'
)

if [ -n "$BASELINE" ]; then
  echo "Using baseline: $BASELINE"
  base_dir="$(dirname "$BASELINE")"
  tmp_baseline="$(mktemp)"
  cp "$BASELINE" "$tmp_baseline"
  # run scan against copy and diff results exactly like CI
  (
    cd "$base_dir"
    detect-secrets scan "${EXCLUDES[@]}" --baseline "$tmp_baseline" 1>/dev/null 2> .secrets_scan.err
  )
  cp "$tmp_baseline" .secrets_scan.json

  # compare baseline and new copy
  baseline_fps="$(mktemp)"
  tmp_fps="$(mktemp)"
  jq -r '.results | to_entries[] | .key as $file | .value[]? | "\($file)|\(.type)|\(.hashed_secret)"' "$BASELINE" | sort -u > "$baseline_fps"
  jq -r '.results | to_entries[] | .key as $file | .value[]? | "\($file)|\(.type)|\(.hashed_secret)"' "$tmp_baseline" | sort -u > "$tmp_fps"

  new_secrets="$(comm -13 "$baseline_fps" "$tmp_fps" || true)"
  if [ -n "$new_secrets" ]; then
    echo "New potential secrets detected (not present in baseline):"
    echo "$new_secrets"
    exit 1
  fi
  echo "No new secrets detected."
else
  echo "No baseline found, running fresh scan..."
  detect-secrets scan --all-files "${EXCLUDES[@]}" > .secrets_scan.json 2> .secrets_scan.err
  count=$(jq '[.results | to_entries[] | select(.value | length > 0)] | length' .secrets_scan.json)
  if [ "$count" -gt 0 ]; then
    echo "Potential secrets detected! Create a baseline with: detect-secrets scan > .secrets.baseline"
    jq '.results' .secrets_scan.json
    exit 1
  fi
fi

echo "✅ No new secrets detected"
