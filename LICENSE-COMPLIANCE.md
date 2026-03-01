# License Compliance Policy

## Overview

Deploy-System-Unified is licensed under **GPL-3.0**. All dependencies must use GPL-3.0 compatible licenses.

## Allowed Licenses

✅ **Permitted without review:**
- MIT
- Apache-2.0
- BSD-2-Clause, BSD-3-Clause
- ISC
- GPL-3.0, LGPL-3.0
- MPL-2.0

⚠️ **Requires legal review:**
- AGPL-3.0 (network copyleft)
- MPL-2.0 (file-level copyleft)

❌ **Not permitted:**
- SSPL (service restriction)
- Proprietary/Commercial licenses
- GPL-2.0 only (not "or later")

## Source Code Availability (GPL-3.0 Compliance)

In accordance with Section 6 of the GNU General Public License v3.0, the "Corresponding Source" for this project is available at:
- **Repository**: `https://github.com/deploy-system-unified/deploy-system-unified`
- **Archive**: Contact the maintainers for a formal source archive if required for offline use.

## Preservation of Legal Notices

To comply with Apache License 2.0 (Section 4d) and other attribution-based licenses:
- All `NOTICE` and `ACKNOWLEDGEMENT` files from third-party distributions must be preserved.
- These notices are consolidated in `docs/security/THIRD_PARTY_LICENSES.md` for easy reference.

## Automated Checks

License compliance is enforced via CI:
- **Workflow:** `.github/workflows/license-compliance.yml`
- **Runs:** Every PR + weekly scheduled scan
- **Tool:** `pip-licenses` for Python dependencies

## Adding New Dependencies

Before adding a new dependency:

1. Check the license: `pip show <package> | grep License`
2. Verify compatibility with GPL-3.0
3. Add to `docs/security/THIRD_PARTY_LICENSES.md`
4. Update `requirements.txt` or `requirements.yml`

## Reporting Issues

Found a license compliance issue? Open an issue with:
- Package name and version
- License type
- Where it's used

---

See [docs/security/THIRD_PARTY_LICENSES.md](./docs/security/THIRD_PARTY_LICENSES.md) for full third-party license acknowledgments.
Full license texts are available in the [THIRD_PARTY_LICENSES/](./THIRD_PARTY_LICENSES/) directory.
