# Role: security/sbom

POL-SEC | Software Bill of Materials (SBOM) generation and supply-chain auditing.

## Compliance
- **ISO 27001 §14.2**: Supply Chain Security
- **Audit Event Identifier**: 520040 (Audit Start)
- **Audit Event Identifier**: 520047 (Audit Signed)

## Summary
Generates a signed CycloneDX SBOM for all project dependencies. Required for `hardened` and `production` profiles.
