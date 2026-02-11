# security_audit_integrity

**Role Path**: `roles/security/audit_integrity`

## Description
**Cryptographic Log Immutability**
Ensures the integrity and immutability of system audit logs using cryptographic signatures.

## Key Tasks
- Check if journal FSS keys are already initialized
- Initialize Forward Secure Sealing (FSS) keys
- Create secure temporary file for FSS key capture
- Store FSS verification key on controller
- Encrypt FSS key with Ansible Vault
- Move encrypted FSS key to final destination
- Ensure Seal is enabled in journald configuration

---
*This page was automatically generated from role source code.*