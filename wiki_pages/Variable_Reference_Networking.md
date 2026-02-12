# Variable_Reference_Networking

## Networking Variables

### `networking/container_networks`
- [`container_networks_enable`](roles/networking_container_networks.md#containernetworksenable)
- [`podman_rootless_enabled`](roles/networking_container_networks.md#podmanrootlessenabled)
- [`podman_rootless_user`](roles/networking_container_networks.md#podmanrootlessuser)
- [`podman_rootless_user_home`](roles/networking_container_networks.md#podmanrootlessuserhome)
- [`containers_systemd_dir`](roles/networking_container_networks.md#containerssystemddir)
- [`containers_systemd_scope`](roles/networking_container_networks.md#containerssystemdscope)
- [`containers_systemd_owner`](roles/networking_container_networks.md#containerssystemdowner)
- [`containers_systemd_group`](roles/networking_container_networks.md#containerssystemdgroup)
- [`containers_systemd_env`](roles/networking_container_networks.md#containerssystemdenv)
- [`container_networks_list`](roles/networking_container_networks.md#containernetworkslist)

### `networking/desktop`
- [`networking_desktop_enable_wifi`](roles/networking_desktop.md#networkingdesktopenablewifi)
- [`networking_desktop_wifi_backend`](roles/networking_desktop.md#networkingdesktopwifibackend)
- [`networking_desktop_manager`](roles/networking_desktop.md#networkingdesktopmanager)
- [`networking_desktop_install_gui_tools`](roles/networking_desktop.md#networkingdesktopinstallguitools)

### `networking/firewall`
- [`firewall_enabled`](roles/networking_firewall.md#firewallenabled)
- [`firewall_allowed_tcp_ports`](roles/networking_firewall.md#firewallallowedtcpports)
- [`firewall_allow_endlessh`](roles/networking_firewall.md#firewallallowendlessh)
- [`firewall_endlessh_port`](roles/networking_firewall.md#firewallendlesshport)
- [`firewall_allowed_udp_ports`](roles/networking_firewall.md#firewallallowedudpports)
- [`firewall_additional_rules`](roles/networking_firewall.md#firewalladditionalrules)
- [`firewall_forward_policy`](roles/networking_firewall.md#firewallforwardpolicy)

### `networking/physical`
- [`interface_capabilities`](roles/networking_physical.md#interfacecapabilities)
- [`networking_physical_install_tools`](roles/networking_physical.md#networkingphysicalinstalltools)
- [`networking_physical_manage_mtu`](roles/networking_physical.md#networkingphysicalmanagemtu)
- [`networking_physical_jumbo_frames_enabled`](roles/networking_physical.md#networkingphysicaljumboframesenabled)
- [`networking_physical_jumbo_mtu`](roles/networking_physical.md#networkingphysicaljumbomtu)
- [`networking_physical_ring_tuning_enabled`](roles/networking_physical.md#networkingphysicalringtuningenabled)
- [`networking_physical_rx_ring_size`](roles/networking_physical.md#networkingphysicalrxringsize)
- [`networking_physical_tx_ring_size`](roles/networking_physical.md#networkingphysicaltxringsize)
- [`networking_physical_offload_tuning_enabled`](roles/networking_physical.md#networkingphysicaloffloadtuningenabled)
- [`networking_physical_enable_tso`](roles/networking_physical.md#networkingphysicalenabletso)
- [`networking_physical_enable_gso`](roles/networking_physical.md#networkingphysicalenablegso)
- [`networking_physical_enable_lro`](roles/networking_physical.md#networkingphysicalenablelro)
- [`networking_physical_profiles`](roles/networking_physical.md#networkingphysicalprofiles)
- [`networking_physical_default_profile`](roles/networking_physical.md#networkingphysicaldefaultprofile)

### `networking/services`
- *No variables defined in defaults/main.yml*

### `networking/virtual`
- *No variables defined in defaults/main.yml*

### `networking/vpn_mesh`
- *No variables defined in defaults/main.yml*

