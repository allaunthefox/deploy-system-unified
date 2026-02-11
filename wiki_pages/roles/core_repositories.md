# core/repositories

**Role Path**: `roles/core/repositories`

## Description
**Repository Management**
Ensures secure repository configuration and management of third-party sources (RPMFusion, etc.).

## Key Tasks
- Ensure repository management tools (Debian/Ubuntu)
- Check for legacy sources.list
- Enable Contrib and Non-Free repositories (Legacy Debian)
- Enable Ubuntu Universe/Multiverse
- Check if RPMFusion is installed (RedHat/Fedora)
- Securely download RPMFusion Free Release (Fedora)
- Securely download RPMFusion NonFree Release (Fedora)
- Install RPMFusion Free/NonFree from verified local files (Fedora)
- Enable Community Repository (Alpine)
- Update package cache (Debian/Ubuntu)
- Update package cache (RedHat/Fedora)
- Update package cache (Arch)
- Update package cache (Alpine)

## Default Variables
- `rpmfusion_free_url`
- `rpmfusion_nonfree_url`
- `rpmfusion_free_sha256`
- `rpmfusion_nonfree_sha256`
- `rpmfusion_verify_checksum`

---
*This page was automatically generated from role source code.*