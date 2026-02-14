# Release Cycles & Roadmap

This document outlines the release process and public roadmap for Deploy-System-Unified.

## Release Schedule

### Versioning Scheme

We follow Semantic Versioning (SemVer):
- **MAJOR** (x.0.0) - Breaking changes, architectural updates
- **MINOR** (x.y.0) - New features, backwards compatible
- **PATCH** (x.y.z) - Bug fixes, security updates

### Release Cadence

| Type | Frequency | Examples |
|------|-----------|----------|
| Major | Annually | v1.0.0, v2.0.0 |
| Minor | Quarterly | v1.1.0, v1.2.0 |
| Patch | As needed | v1.1.1, v1.1.2 |

## Release Process

### 1. Planning (2 weeks before release)
- Review outstanding issues
- Prioritize features/fixes
- Update changelog

### 2. Development (2-4 weeks)
- Implement features
- Update tests
- Update documentation

### 3. Testing (1 week)
- Run full test suite
- Molecule tests
- Idempotency checks

### 4. Release
- Tag release
- Create GitHub release
- Update docs

## Roadmap

### 2026 Q1 (v1.2.0) - Current
- [x] GPU orchestration enhancements
- [x] Multi-node K3s support
- [x] GRUB validation improvements
- [ ] Performance metrics collection
- [ ] Enhanced monitoring dashboards

### 2026 Q2 (v1.3.0)
- [ ] Container security hardening
- [ ] SOPS secrets integration
- [ ] Enhanced CI/CD pipelines

### 2026 Q3 (v1.4.0)
- [ ] Multi-architecture support (ARM64, RISC-V)
- [ ] Advanced GPU slicing
- [ ] RDMA support

### 2026 Q4 (v2.0.0)
- [ ] Major architecture update
- [ ] New deployment patterns
- [ ] Community features

## Contributing to Roadmap

1. Open an issue with `roadmap` label
2. Discuss in community channels
3. Submit PR for documentation

## Changelog

See [CHANGELOG.md](../CHANGELOG.md) for historical releases.
