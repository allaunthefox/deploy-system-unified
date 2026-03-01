# THIRD_PARTY_LICENSES

This project incorporates third-party open source software components. This document lists the licenses of dependencies used in Deploy-System-Unified.

## Project License

**Deploy-System-Unified** is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

See [LICENSE](../LICENSE.md) for the full license text.

---

## Allowed Licenses (GPL-3.0 Compatible)

The following licenses are considered compatible with GPL-3.0 and are allowed for dependencies:

| License | SPDX Identifier | Compatible |
|---------|-----------------|------------|
| MIT License | MIT | ✅ Yes |
| Apache License 2.0 | Apache-2.0 | ✅ Yes |
| BSD 2-Clause License | BSD-2-Clause | ✅ Yes |
| BSD 3-Clause License | BSD-3-Clause | ✅ Yes |
| ISC License | ISC | ✅ Yes |
| GNU GPL v3.0 | GPL-3.0 | ✅ Yes |
| GNU LGPL v3.0 | LGPL-3.0 | ✅ Yes |
| Mozilla Public License 2.0 | MPL-2.0 | ✅ Yes (weak copyleft) |

---

## Core Dependencies

### Ansible Collections

| Collection | License | Notes | Project Site |
|------------|---------|-------|--------------|
| `ansible.posix` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Core POSIX module support | [GitHub](https://github.com/ansible-collections/ansible.posix) |
| `ansible.utils` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Ansible utility modules | [GitHub](https://github.com/ansible-collections/ansible.utils) |
| `community.general` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Community maintained modules | [GitHub](https://github.com/ansible-collections/community.general) |
| `community.crypto` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Cryptographic operations | [GitHub](https://github.com/ansible-collections/community.crypto) |
| `community.docker` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Docker engine integration | [GitHub](https://github.com/ansible-collections/community.docker) |
| `containers.podman` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Podman container support | [GitHub](https://github.com/containers/ansible-podman-collections) |
| `community.sops` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | SOPS secrets management | [GitHub](https://github.com/ansible-collections/community.sops) |
| `community.libvirt` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Virtualization management | [GitHub](https://github.com/ansible-collections/community.libvirt) |
| `community.library_inventory_filtering_v1` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Advanced inventory filtering | [GitHub](https://github.com/ansible-collections/community.library_inventory_filtering_v1) |

### Python Packages

| Package | License | Purpose | Project Site |
|---------|---------|---------|--------------|
| `ansible-core` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | Ansible runtime | [GitHub](https://github.com/ansible/ansible) |
| `ansible-lint` | [MIT](../../THIRD_PARTY_LICENSES/MIT.txt) | Linting and validation | [GitHub](https://github.com/ansible/ansible-lint) |
| `yamllint` | [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt) | YAML validation | [GitHub](https://github.com/adrienverge/yamllint) |
| `detect-secrets` | [Apache-2.0](../../THIRD_PARTY_LICENSES/Apache-2.0.txt) | Secret detection | [GitHub](https://github.com/Yelp/detect-secrets) |
| `jinja2` | [BSD-3-Clause](../../THIRD_PARTY_LICENSES/BSD-3-Clause.txt) | Template engine | [GitHub](https://github.com/pallets/jinja) |
| `pyyaml` | [MIT](../../THIRD_PARTY_LICENSES/MIT.txt) | YAML parsing | [GitHub](https://github.com/yaml/pyyaml) |
| `requests` | [Apache-2.0](../../THIRD_PARTY_LICENSES/Apache-2.0.txt) | HTTP library | [GitHub](https://github.com/psf/requests) |
| `urllib3` | [MIT](../../THIRD_PARTY_LICENSES/MIT.txt) | HTTP client | [GitHub](https://github.com/urllib3/urllib3) |
| `certifi` | [MPL-2.0](../../THIRD_PARTY_LICENSES/MPL-2.0.txt) | SSL certificates | [GitHub](https://github.com/certifi/python-certifi) |
| `idna` | [BSD-3-Clause](../../THIRD_PARTY_LICENSES/BSD-3-Clause.txt) | IDNA support | [GitHub](https://github.com/kjd/idna) |
| `charset-normalizer` | [MIT](../../THIRD_PARTY_LICENSES/MIT.txt) | Character encoding detection | [GitHub](https://github.com/Ousret/charset_normalizer) |
| `pip-licenses` | [MIT](../../THIRD_PARTY_LICENSES/MIT.txt) | License audit tool | [GitHub](https://github.com/pypa/pip-licenses) |
| `prettytable` | [BSD-3-Clause](../../THIRD_PARTY_LICENSES/BSD-3-Clause.txt) | Dependency for pip-licenses | [GitHub](https://github.com/jazzband/prettytable) |
| `openai` | [Apache-2.0](../../THIRD_PARTY_LICENSES/Apache-2.0.txt) | Qwen Sub-Agent API client | [GitHub](https://github.com/openai/openai-python) |
| `tiktoken` | [MIT](../../THIRD_PARTY_LICENSES/MIT.txt) | Qwen Sub-Agent tokenization | [GitHub](https://github.com/openai/tiktoken) |
| `pydantic` | [MIT](../../THIRD_PARTY_LICENSES/MIT.txt) | Data validation for Sub-Agents | [GitHub](https://github.com/pydantic/pydantic) |
| `python-dotenv` | [BSD-3-Clause](../../THIRD_PARTY_LICENSES/BSD-3-Clause.txt) | Environment variable management | [GitHub](https://github.com/theskumar/python-dotenv) |

---

## Flagged Dependencies (Review Required)

The following licenses require additional review before use:

| License | Concern | Action Required |
|---------|---------|-----------------|
| AGPL-3.0 | Network copyleft | Legal review for SaaS use |
| SSPL | Service restriction | Not compatible with project goals |
| Proprietary | Commercial terms | Requires purchase/agreement |

---

## Compliance Automation

License compliance is checked automatically via GitHub Actions:

- **Workflow:** `.github/workflows/license-compliance.yml`
- **Frequency:** Every PR + weekly scheduled scan
- **Tool:** `pip-licenses` for Python dependencies
- **Artifacts:** License reports uploaded to CI artifacts

---

## Reporting License Issues

If you discover a dependency with an incompatible license:

1. **Open an issue** with the dependency name and license
2. **Tag with** `license-compliance` label
3. **Suggest alternatives** if available

---

## Generating License Reports

To generate a local license report:

```bash
# Install pip-licenses
pip install pip-licenses

# Generate markdown report
pip-licenses --format=markdown --with-authors --with-urls > THIRD_PARTY_LICENSES.md

# Check for incompatible licenses
pip-licenses --format=plain | grep -iE 'AGPL|SSPL|Proprietary'
```

---

---

## Vendored Components

The following components are included directly in the repository for specific hardware or environment support:

| Component | Path | License | Origin |
|-----------|------|---------|--------|
| GPU Task Scripts | `roles/containers/lxc/tasks/vendor/` | MIT/Apache-2.0 Equivalent | Revised from Vendor Docs (AMD/Intel/NVIDIA) |
| SSHD Hardening | `roles/security/sshd/` | MIT | Derived from standard hardening patterns |

---

## Legal Notices and License Texts

Full license texts for third-party components are available in the [THIRD_PARTY_LICENSES/](../../THIRD_PARTY_LICENSES/) directory:

- [GPL-3.0](../../THIRD_PARTY_LICENSES/GPL-3.0.txt)
- [Apache-2.0](../../THIRD_PARTY_LICENSES/Apache-2.0.txt)
- [MIT](../../THIRD_PARTY_LICENSES/MIT.txt)
- [BSD-3-Clause](../../THIRD_PARTY_LICENSES/BSD-3-Clause.txt)

---

## Attribution Notices

As required by the Apache License 2.0 (Section 4d), the following attribution notices are preserved:

- **Setuptools**: This project utilizes `setuptools` which includes notices from the PSF and other contributors.
- **Other Components**: No additional `NOTICE` or `ACKNOWLEDGEMENT` files were identified in the current dependency tree.

---

**Last Updated:** 2026-03-01  
**Report Generated By:** Security Compliance Audit (Phase 13) & Legal Review (Phase 14)
