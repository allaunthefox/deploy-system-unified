# SSH Policy (Draft)

Scope: Applies to hosts managed by `projects/deploy-system-unified` Ansible playbooks and roles.

Summary of authoritative policy decisions

- PermitRootLogin: no (root login via SSH is disabled across environments)
- PasswordAuthentication: no (only public key or certificate-based auth)
- X11Forwarding: no
- AllowAgentForwarding: no by default; allowed for specific trusted groups only
- AllowTcpForwarding: no by default; allowed for specific trusted groups only
- Host key algorithms: ed25519 and RSA (4096) generated if missing
- Strong ciphers, MACs, and KEX enforced via role `security/sshd`

Exceptions and trusted groups

- Exceptions are implemented with `Match Group` blocks in `sshd_config`.
- Variable controls (role defaults):
  - `sshd_enable_trusted_group_exceptions` (boolean) — default: false
  - `sshd_trusted_groups` (list) — default: []

Recommended next steps

- Decide on a key management approach: SSH certificates (internal CA) recommended for scalability, or continue with `authorized_keys` and an IdP-based provisioning workflow.
- Define `ssh-trusted` group membership process and audit logs for exception use.
- Add CI tests that render `sshd_config` and run `sshd -t` to validate syntax and content.

Audit and enforcement

- Use Ansible tests and Molecule scenarios for role verification in staging.
- Use gitleaks and .gitignore (already present) to prevent key material commits.

Owner: TBD (suggest operations/security team)

Notes: This is a draft. Edit or approve to make changes to the enforced policy in the repo.
