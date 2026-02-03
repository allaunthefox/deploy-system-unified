# Multiple Instance Strategy Review

## Current Limitations (Singleton Architecture)
The module currently enforces a **Singleton Pattern** per host. It cannot support multiple isolated media stacks (e.g., "Kids" vs. "Adults" or "Tenant A" vs. "Tenant B") on the same physical server.

### 1. Static Filenames
*   **The Issue**: The Ansible role writes to hardcoded paths:
    *   `/etc/containers/systemd/jellyfin.container`
    *   `/srv/containers/caddy/conf.d/media_stack.caddy`
*   **The Check**: Running the playbook a second time with different variables will simply **overwrite** the existing stack, treating it as a configuration update rather than a new deployment.

### 2. Static Container Names
*   **The Issue**: The Quadlet files define `ContainerName=jellyfin` directly.
*   **The Consequence**: Podman cannot run two containers with the same name. Attempting to start a second stack would result in Systemd unit failure or the previous container being killed.

### 3. Port Allocation
*   **The Issue**: While ports are variable (e.g., `jellyfin_port_http`), the defaults are fixed. Support for dynamic port assignment or "internal-only" socket binding is present but requires manual variable management for every new instance to avoid collision.

---

## Gaming Out Scenarios

### Scenario A: Multi-Domain Collaboration (Same Host)
**Goal**: Host `family.tv` (Stack A) and `personal.tv` (Stack B) on one server.
**Result**: **FAILURE** (Collision).
*   Both stacks try to write `media_stack.caddy`.
*   The last one to run wins.
*   The Caddy Gatekeeper is robust (it imports `*.caddy`), but since both roles write to the same filename, only one configuration survives.

### Scenario B: Dedicated Subdomains (Distributed)
**Goal**: `nyc.media.com` (Host A), `lon.media.com` (Host B).
**Result**: **SUCCESS**.
*   The Singleton pattern works perfectly across distributed infrastructure.
*   Each host has its own IP and independent Caddy instance.
*   Standard DNS A records direct traffic appropriately.

### Scenario C: Single Domain, Split Backend
**Goal**: `jellyfin.domain.com` routing to *two* balanced containers.
**Result**: **FAILURE**.
*   The role logic assumes a 1:1 mapping of Service -> Container.
*   No load balancing logic exists in the generated Caddyfile fragment.

## Recommendations for Multi-Tenancy

To support "Collaboration" or "Multiple Copies" on one host:

1.  **Variable-Based Namespacing**:
    replace `ContainerName=jellyfin` with `ContainerName=jellyfin-{{ media_instance_id }}`.
2.  **Dynamic File Paths**:
    replace `dest: .../jellyfin.container` with `dest: .../jellyfin-{{ media_instance_id }}.container`.
3.  **Config Isolation**:
    The Caddy configuration file must be unique per instance: `dest: .../{{ media_instance_id }}_stack.caddy`.

**Verdict**: The current profile is production-ready for **Dedicated Single-Tenant Hosts**, but requires refactoring for **Multi-Tenant/High-Density** consolidation.
