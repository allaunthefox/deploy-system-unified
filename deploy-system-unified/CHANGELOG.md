# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Observability**: New `roles/ops/health_check` for post-deploy verification.
- **Observability**: Log retention policies (`docs/architecture/LOGGING_POLICY.md`) and enforcement.
- **Resilience**: Disaster recovery runbook (`RESTORE_RUNBOOK.md`) and helper script (`scripts/restore_data.sh`).
- **Secrets**: SOPS/Age integration for secure secret management.
- **Community**: Standard community files (`CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `ROADMAP.md`).
- **Inventory**: Production profile added to Contabo inventory.

### Changed
- **Security**: SSH service now uses non-blocking start to prevent deadlocks.
- **Security**: Audit integrity now supports custom vault IDs and output directories.
- **Core**: Refactored `core/logging` to use configurable variables for retention and rate limiting.
- **Docs**: Flattened repository structure and synced Wiki.

### Fixed
- Fixed idempotent issues in `core` roles (benchmark passed 12/12).
- Fixed `audit_integrity` vault encryption on newer Ansible versions.
- Fixed `hardening` role `pipefail` syntax errors.

## [0.1.0] - 2026-01-15
### Added
- Initial release of Deploy-System-Unified.
- Basic role structure and hardening roles.
- Contabo and Local inventory support.
