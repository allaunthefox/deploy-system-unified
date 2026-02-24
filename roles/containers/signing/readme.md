# Cosign Container Image Signing Role

This role provides Cosign container image signing and verification for the deploy-system-unified project.

## Features

- **Key-based Signing**: Traditional key pair signing
- **Keyless Signing**: Sigstore Fulcio-based keyless signing
- **Verification Policies**: Custom policies for image verification
- **OCI Registry Support**: Integration with OCI registries
- **Transparency Log**: Rekor transparency log integration

## Requirements

- Ansible 2.15+
- Supported OS: Ubuntu, Debian, Fedora, CentOS

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `cosign_version` | `2.3.0` | Cosign version to install |
| `cosign_key_mode` | `keypair` | Signing mode: keypair, keyless |
| `cosign_keyless_mode` | `false` | Enable keyless signing |
| `cosign_enable_verification` | `false` | Enable image verification |
| `cosign_policy_name` | `default-policy` | Policy name |

## Example Playbook - Key-based Signing

```yaml
- hosts: container_hosts
  roles:
    - role: containers.signing
      vars:
        cosign_version: "2.3.0"
        cosign_key_mode: keypair
```

## Example Playbook - Keyless Signing

```yaml
- hosts: container_hosts
  roles:
    - role: containers.signing
      vars:
        cosign_key_mode: keyless
        cosign_keyless_mode: true
        cosign_fulcio_url: "https://fulcio.sigstore.dev"
        cosign_rekor_url: "https://rekor.sigstore.dev"
```

## Image Signing

```bash
# Sign an image
cosign sign --key /etc/cosign/keys/cosign.key your-registry/image:tag

# Verify an image
cosign verify --key /etc/cosign/keys/cosign.pub your-registry/image:tag
```

## Verification Policies

Create custom policies in `/etc/cosign/policies/`:

```yaml
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: my-policy
spec:
  images:
  - glob: "my-registry/**/*"
  authorities:
  - keyless:
      url: https://fulcio.sigstore.dev
```

## Tags

- `security`
- `signing`
- `containers`
- `cosign`
- `sigstore`

## Compliance

- ISO 27001 §8.26 (Information security review)
- NIST 800-53 SC-8 (Transmission confidentiality and integrity)
- NIST 800-53 SI-7 (Software and information integrity)
