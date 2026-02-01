# OS Configuration Controls
The `os_settings.yml` file serves as the **Single Source of Truth (SSOT)** for fleet-wide operating system configurations.

**File Location:** `inventory/group_vars/all/os_settings.yml`

## Purpose
In a distributed microservice architecture, "where do we set the timezone?" or "what describes the base package list?" are common questions. This configuration file answers them by determining the baseline state for **every** managed node, regardless of its role (GPU Worker, Web Server, or Container Host).

### 1. System Identity
Controls the non-functional requirements of the server—how it identifies itself to the world and its administrators.
*   **Timezone**: Ensures consistent logging timestamps across the fleet (Default: `UTC`).
*   **Locale/Keyboard**: Ensures consistent character encoding and terminal behavior.

### 2. Administrative Access
Defines the "Break-Glass" and standard entry mechanisms.
*   **Admin User**: The standard username created on all nodes.
*   **Endlessh Integration**: If `system_enable_endlessh` is true, port 22 is trapped, and real SSH moves to 2222.
*   **SSH Port**: The listening port for SSHD. (Dynamic based on Endlessh status).
*   **Root Login**: Global security toggle to allow/deny direct root access.

### 3. Base Software (Bootstrap)
Defines the "Minimum Viable Product" for a server.
*   **Common Packages**: Installed on *all* distributions (e.g., `sudo`, `curl`).
*   **Distro-Specifics**: Maps the common intents to specific package names (e.g., `apache2` vs `httpd` is handled in mappings, but here we define *what* we want).

### 4. Hardware & Kernel Profiles
Global overrides for the physical layer.
*   **Kernel Profile**: Selects between `generic` (virtualization-safe) and `bare_metal` (hardware-optimized) tuning.
*   **IOMMU/DMA**: Toggles low-level hardware isolation features.

## Example Configuration

```yaml
# inventory/group_vars/all/os_settings.yml

system_timezone: "America/New_York"
system_admin_user: "ops_team"
system_ssh_port: 2022
system_base_packages:
  common:
    - htop
    - tmux
    - git
```

## How Roles Use These Variables
*   **`roles/core/bootstrap`**: Consumes `system_base_packages` to install software.
*   **`roles/security/sshd`**: Consumes `system_ssh_port` (via variable inheritance).
*   **`roles/security/kernel`**: Consumes `kernel_profile` to decide whether to apply Sysctl hardening.
