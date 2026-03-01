# Signing Role

**Audit Event Identifier:** DSU-PLY-100160  
**Mermaid Version:** 1.2  
**Renderer Support:** GitHub, GitLab, Mermaid Live  
**Last Updated:** 2026-03-01  

This role implements container image signing and verification using Cosign, ensuring supply chain integrity.

## Architecture

```mermaid
graph TD
    subgraph Supply Chain
        BUILD[Build Process] --> SIGN(Cosign Sign)
        SIGN --> REGISTRY[Container Registry]
    end
    
    subgraph Runtime Verification
        REGISTRY --> PULL[Podman Pull]
        PULL --> POLICY{Policy Check}
        POLICY -->|Verified| RUN[Container Start]
        POLICY -->|Failed| BLOCK[Block Execution]
        
        KEY[Public Key] --> POLICY
        SIG[Signature] --> POLICY
    end
    
    classDef process fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef check fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef secure fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef fail fill:#ffebee,stroke:#c62828,stroke-width:2px;
    
    class BUILD,SIGN,REGISTRY,PULL process;
    class POLICY check;
    class RUN,KEY,SIG secure;
    class BLOCK fail;
```

## Features
- **Cosign**: Industry-standard container signing tool.
- **Policy Enforcement**: Configuration of `policy.json` to reject unsigned images.
- **Key Management**: Secure distribution of public verification keys.
- **Automation**: Integration with CI/CD pipelines for automatic signing.

## Usage

```yaml
- name: Setup Image Signing
  hosts: container_nodes
  roles:
    - containers/signing
```
