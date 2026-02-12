# Networking Role

This role manages network configuration, firewalls, and connectivity.

## Sub-Components

* **physical**: Physical interface configuration.
* **virtual**: Virtual networking (bridges, taps).
* **firewall**: UFW/NFTables configuration.
* **services**: Network services (DNS, etc.).
* **container_networks**: CNI/Netavark configuration for containers.
* **vpn_mesh**: VPN and Mesh networking setup.
* **desktop**: Desktop-specific networking (NetworkManager).

## Usage

```yaml
- name: Configure Networking
  hosts: all
  roles:
    - networking
```
