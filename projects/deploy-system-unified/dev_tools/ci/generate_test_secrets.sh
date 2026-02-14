#!/usr/bin/env bash
set -euo pipefail

OUT=${OUT:-dev_tools/ci/test_secrets.yml}
PRINT_JSON=false
ENCRYPT=false

usage(){
  cat <<EOF
Usage: $0 [--output path] [--print-extra-vars] [--encrypt]

Generates a test secrets YAML file (never committed) containing safe mock values
for use in local CI / idempotence runs. If --encrypt is used and
ANSIBLE_VAULT_PASSWORD_FILE is set, the file will be encrypted with
ansible-vault.

Examples:
  $0                       # writes dev_tools/ci/test_secrets.yml
  $0 --print-extra-vars     # prints JSON suitable for --extra-vars
  $0 --output /tmp/s.yml    # write to custom path
  $0 --encrypt              # encrypts output (requires ANSIBLE_VAULT_PASSWORD_FILE)

EOF
}

while [[ ${1:-} != "" ]]; do
  case "$1" in
    -o|--output) OUT="$2"; shift 2;;
    --print-extra-vars) PRINT_JSON=true; shift;;
    --encrypt) ENCRYPT=true; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 2;;
  esac
done

rand() { head -c 24 /dev/urandom | base64 | tr -d '\n' ; }

cat > "$OUT" <<YML
# test-only secrets (auto-generated) - do NOT commit
restic_password: "$(rand)"
monitoring_grafana_admin_password: "$(rand)"
vaultwarden_admin_token: "$(rand)"
crowdsec_firewall_bouncer_key: "$(rand)"
# extra placeholders (optional)
# porkbun_api_key: "$(rand)"
# porkbun_secret_api_key: "$(rand)"
YML
chmod 600 "$OUT"

echo "Wrote test secrets -> $OUT"

if [ "$ENCRYPT" = true ]; then
  if command -v ansible-vault >/dev/null 2>&1 && [ -n "${ANSIBLE_VAULT_PASSWORD_FILE:-}" ]; then
    ansible-vault encrypt --vault-password-file "$ANSIBLE_VAULT_PASSWORD_FILE" "$OUT"
    echo "Encrypted $OUT with ansible-vault"
  else
    echo "Cannot encrypt: ansible-vault missing or ANSIBLE_VAULT_PASSWORD_FILE unset" >&2
    exit 2
  fi
fi

if [ "$PRINT_JSON" = true ]; then
  python - <<PY
import yaml, json, sys
print(json.dumps(yaml.safe_load(open('$OUT'))))
PY
fi
