#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500002
# Script Type: Secret Validation
# Description: Verifies secrets file contains all required keys for migration
# Usage: ./validate_secrets_schema.py <path_to_secrets.yml>
# Last Updated: 2026-02-28
# Version: 1.0
# =============================================================================
"""
Secrets Schema Validator
Verifies that a secrets file contains all required keys for the migration.
Usage: ./validate_secrets_schema.py <path_to_secrets.yml>
"""

import sys
import yaml
import os

REQUIRED_KEYS = [
    "authentik_secret_key",
    "authentik_pg_password",
    "wikijs_pg_password",
    "vaultwarden_admin_token",
    "database_password"
]

def validate(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False

    try:
        with open(file_path, 'r') as f:
            secrets = yaml.safe_load(f)
    except Exception as e:
        print(f"Error parsing YAML: {e}")
        return False

    if not secrets:
        print("Error: Empty secrets file")
        return False

    missing = []
    for key in REQUIRED_KEYS:
        if key not in secrets:
            missing.append(key)

    if missing:
        print("FAIL: Missing required keys:")
        for key in missing:
            print(f"  - {key}")
        return False

    print("SUCCESS: All required secret keys present.")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <secrets_file>")
        sys.exit(1)
    
    if not validate(sys.argv[1]):
        sys.exit(1)
    sys.exit(0)
