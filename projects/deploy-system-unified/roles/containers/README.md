# Containers Role

This role manages container runtimes and orchestration tools.

## Sub-Components

*   **runtime**: Installs and configures Podman/Docker runtimes.
*   **config**: General container configuration (registries, storage).
*   **caddy**: Caddy web server setup (often used as a reverse proxy for containers).
*   **memcached**: Distributed memory object caching system (Podman Quadlet).
*   **quadlets**: Systemd generator for Podman containers.
*   **anubis**: Specific containerized service configuration.
*   **lxc**: LXC (Linux Containers) setup and configuration.

## Usage

```yaml
- name: Setup Container Environment
  hosts: container_nodes
  roles:
    - containers
```
