# Quadlets Role

## Overview
This role manages **Podman Quadlets**, which are Systemd generator files for containers. It ensures that container networks and services are managed natively by Systemd, providing robustness and auto-start capabilities.

## Standards Compliance

### 1. Network Naming
*   **Bridge Name**: Defaults to `deploy-net` (via `quadlet_network_name`).
*   **File Name**: `/etc/containers/systemd/{{ quadlet_network_name }}.network`.
*   **Variable**: `quadlet_network_name` can be overridden in `defaults/main.yml` or inventory.

### 2. Identity & Auditing
*   **UUID Generation**: Uses `core/identity` to assign a high-entropy UUID to the networking object during deployment.
*   **Compliance**: Matches the `networking/virtual` standard for object tracking.

### 3. Checkpoints
*   **Status**: Writes completion status to `/var/lib/deploy-system/checkpoints/quadlets_checkpoint.json`.
*   **Persistence**: Ensures that the network deployment ID and state are preserved across runs.

## Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `quadlet_network_name` | `deploy-net` | The name of the Podman bridge network. |
| `quadlet_network_subnet` | `10.89.0.0/24` | Subnet CIDR. |
| `quadlet_create_network` | `true` | Whether to create the base network. |

## Usage
included automatically by the `containers` meta-role.
