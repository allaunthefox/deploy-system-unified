#!/bin/sh
# Helper script to perform the same steps executed by the CI workflows
# so that developers can run the check locally and be confident the
# actions runner will see the same behavior.

set -euo pipefail

# Determine project root (checkout sometimes nests repository directory)
PROJECT_ROOT="$PWD"
if [ -d "$PWD/deploy-system-unified" ]; then
  PROJECT_ROOT="$PWD/deploy-system-unified"
fi

# Build ANSIBLE_ROLES_PATH from any 'roles' directories inside the project root
ROLES_PATHS=$(find "$PROJECT_ROOT" -type d -name roles -print | paste -sd ':' -)
if [ -z "$ROLES_PATHS" ]; then
  echo "ERROR: no 'roles' directories found in project root ($PROJECT_ROOT)"
  find "$PROJECT_ROOT" -maxdepth 6 -type d -name roles -print || true
  exit 2
fi
export ANSIBLE_ROLES_PATH="$ROLES_PATHS:$PROJECT_ROOT"

# override ansible config to avoid vault password lookups
cat <<'EOF' >"$PROJECT_ROOT/ci-ansible.cfg"
[defaults]
# vault_password_file disabled for CI
EOF
export ANSIBLE_CONFIG="$PROJECT_ROOT/ci-ansible.cfg"

# install minimal dependencies on the host
if ! command -v ansible-playbook >/dev/null 2>&1; then
  echo "ansible-playbook not found; installing via pip"
  python3 -m pip install --upgrade pip
  python3 -m pip install --upgrade "ansible-core>=2.15,<2.16"
fi

# Locate the idempotence playbook anywhere under the workspace
PLAYBOOK=$(find "$PROJECT_ROOT" -path '*/roles/security/sshd/tests/idempotence.yml' -print -quit)
if [ -z "$PLAYBOOK" ]; then
  echo "ERROR: idempotence playbook not found in project root"
  find "$PROJECT_ROOT" -maxdepth 4 -type f -name idempotence.yml -print || true
  exit 2
fi

echo "Using playbook: $PLAYBOOK"
ansible-playbook "$PLAYBOOK" --connection=local
