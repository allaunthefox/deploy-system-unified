# SECURITY_CROWDSEC_HYBRID

## 1. Architecture Overview

We have adopted a **Hybrid Deployment Model** for the security stack to overcome limitations in containerized network stack manipulation.

- **CrowdSec Agent**: Runs as a **Podman Container** (Quadlet). It handles log parsing, scenario detection, and API coordination.
- **Firewall Bouncer**: Runs as a **Native Host Binary** (`crowdsec-firewall-bouncer`). It interfaces directly with the host kernel (via `ipset` and `nftables/iptables`) to enforce bans.
- **Application (Caddy)**: Runs as a **Podman Container**.

### Why Hybrid?

Pure containerized bouncers require privileged access and complex volume/network capability mapping to manipulate the host's firewall tables. Running the bouncer as a native service simplifies the architecture, while keeping the main logic (Agent) containerized and portable.

---

## 2. Infrastructure & Prerequisites

### Host Dependencies

The host (Arch Linux) requires specific packages for the bouncer to function:

- **`ipset`**: Critical dependency. The bouncer uses `ipset` to manage lists of banned IPs efficiently.
- **`crowdsec-firewall-bouncer`**: The binary executable (v0.0.34 utilized).

### Directory Structure

```
/srv/containers/caddy/
├── logs/                   # Shared Volume: Caddy writes here, Agent reads here
│   └── access.log
├── crowdsec/
│   ├── config/             # Agent Configuration (acquis.yaml, etc)
│   └── data/               # Persistent DB
```

---

## 3. Ansible Configuration

The deployment is managed via the `containers/caddy` role in Ansible.

### Agent Container (`crowdsec.container`)

The agent runs with `Network=host` to simplify communication with the local API and network scanning.

- **Image**: `docker.io/crowdsecurity/crowdsec:latest`
- **Volumes**:
    - `/srv/containers/caddy/logs:/var/log/caddy:ro,Z` (Log Ingestion)
    - `/srv/containers/caddy/crowdsec/config:/etc/crowdsec:Z` (Configuration)

### Host Bouncer Setup

Ansible handles the scaffolding for the host binary:

1. Installs `ipset` (pacman).
2. Creates `/etc/crowdsec/bouncers/`.
3. Deploys the base `crowdsec-firewall-bouncer.yaml` configuration template.

---

## 4. Middleware & Glue Logic

Connecting the **Containerized Agent** to the **Host Bouncer** requires exchanging an API key. This is automated by `scripts/setup_crowdsec.py`.

### The Script Logic (`scripts/setup_crowdsec.py`)

1. **Generate Key**: Executes `cscli bouncers add firewall-bouncer-host` **inside** the Crowdsec container.
2. **Parse Output**: Handles both JSON object and raw string returns from `cscli` (robustness patch).
3. **Write Config**: Injects the API Key into the host file `/etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml`.
4. **Restart Service**: Reloads the host systemd service `crowdsec-firewall-bouncer`.

### Manual Commands (Reference)

If the script fails, the manual equivalent is:

```bash
# Inside Container
podman exec crowdsec cscli bouncers add my-bouncer

# On Host
nano /etc/crowdsec/bouncers/crowdsec-firewall-bouncer.yaml
# Update api_key: <key_from_above>
systemctl restart crowdsec-firewall-bouncer
```

---

## 5. Log Acquisition Configuration

For the Agent to see Caddy logs, a specific acquisition config is required in `/srv/containers/caddy/crowdsec/config/acquis.yaml`:

```yaml
filenames:
  - /var/log/caddy/access.log
labels:
  type: caddy
```

*Note: The path `/var/log/caddy/access.log` is the path **inside the container** (mapped from host).*

---

## 6. Verification & Troubleshooting

### 1. Verify Log Ingestion

Generate traffic and check metrics:

```bash
# Generate a log entry
curl -I http://localhost

# Check Internal Metrics
sudo podman exec crowdsec cscli metrics
```

**Success Indicator**:

- `Acquisition Metrics`: `file:/var/log/caddy/access.log` shows non-zero lines read.
- `Parser Metrics`: `crowdsecurity/caddy-logs` shows hits.

### 2. Verify Bouncer Connection

Check that the bouncer is registered:

```bash
sudo podman exec crowdsec cscli bouncers list
```

**Success Indicator**: Status `valid`, Last API Pull `< recent`.

### 3. Verify Firewall Rules (Host)

Check if `ipset` has been populated:

```bash
sudo ipset list
```

**Success Indicator**: You should see sets named `crowdsec-blacklists` or similar.

---

## 7. Known Issues & Fixes

- **`ipset` Missing**: Found in logs `unable to find ipset`. Fixed by `pacman -S ipset`.
- **Parsing Errors**: If `cscli metrics` shows "Lines parsed: 0", check `acquis.yaml` labels. `type: caddy` is mandatory.
- **API URL**: Ensure `api_url` in the bouncer config points to `http://localhost:8080` (since Agent is on host network).
