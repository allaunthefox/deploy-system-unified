# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Networking**: Standardized K3s networking for restricted kernels using `host-gw` backend and `nftables` proxy mode.
- **Networking**: Automated **K3s API Gateway** systemd service to resolve ClusterIP (`172.17.0.1`) connectivity issues on restricted VPS hosts.
- **Benchmarking**: Initial resource overhead benchmarks for Podman vs. K3s, establishing a ~950MB memory baseline for K3s control plane.
- **Benchmarking**: New `docs/benchmarks/BASELINE_REFERENCE_GRAPH.md` consolidating virtualization and database performance targets.
- **Forensic**: Added new Audit Codes (810302-810304) for network gateway and proxy operations to `DSU_AUDIT_EVENT_IDENTIFIERS.md` (v1.3.0).

### Changed
- **Terminology**: Standardized on **"Audit Code"** (from "Action Code") across all roles, playbooks, and documentation to align with industry forensic standards.
- **Forensic**: Updated `roles/core/systemd`, `roles/core/logging`, `roles/core/memory`, and `roles/core/grub` with comprehensive Audit Code mapping.
- **K3s**: Refactored `roles/kubernetes/master` to support automated, idempotent deployment of the API gateway and standard 172.x CIDR ranges.
- **Testing**: Implemented 100-run benchmark aggregator for Host, Podman, and LXC runtimes to achieve statistical baseline averages.

### Changed
- **Handlers**: Resolved merge conflicts that prevented Ansible runs; removed legacy handler-name aliases and standardized handler names (see PR #127).
- **ansiblelint**: Hardened in-repo shim (`ansiblelint/__init__.py`) — activation is now gated, audit-tagged, and prevents import-time side effects.
- **Docs**: Documented `DSU004` in `docs/development/STYLE_GUIDE.md` and added guidance for shim updates.
- **CI**: Enforce DSU004 via an additional `ansible-lint` check on the shim during PR CI runs.
- **Security**: SSH service now uses non-blocking start to prevent deadlocks.
- **Security**: Audit integrity now supports custom vault IDs and output directories.
- **Core**: Refactored `core/logging` to use configurable variables for retention and rate limiting.
- **Docs**: Flattened repository structure and synced Wiki.

### Fixed
- Fixed idempotent issues in `core` roles (benchmark passed 12/12).
- Fixed `audit_integrity` vault encryption on newer Ansible versions.
- Fixed `hardening` role `pipefail` syntax errors.
- **Benchmarking**: Resolved LXC `iptables-nft` conflicts during container provisioning on modern kernels.
- **Benchmarking**: Fixed Podman volume mount path mismatches for shared benchmark scripts.
- **Resilience**: Mitigated K3s API server stability issues under high I/O load by implementing node-affinity gating for benchmark pods.

## [0.1.0] - 2026-01-15
### Added
- Initial release of Deploy-System-Unified.
- Basic role structure and hardening roles.
- Contabo and Local inventory support.
