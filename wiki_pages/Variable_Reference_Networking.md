# Variable_Reference_Networking

## Networking Variables

### `networking/container_networks`
- `[container_networks_enabled](roles/networking_container_networks.md#containernetworksenabled)`
- `[container_networks_bridge_name](roles/networking_container_networks.md#containernetworksbridgename)`
- `[container_networks_subnet](roles/networking_container_networks.md#containernetworkssubnet)`
- `[container_networks_gateway](roles/networking_container_networks.md#containernetworksgateway)`
- `[container_networks_driver](roles/networking_container_networks.md#containernetworksdriver)`
- `[container_networks_internal](roles/networking_container_networks.md#containernetworksinternal)`

### `networking/desktop`
- `[desktop_network_wifi_enabled](roles/networking_desktop.md#desktopnetworkwifienabled)`
- `[desktop_network_nm_backend](roles/networking_desktop.md#desktopnetworknmbackend)`
- `[desktop_network_wifi_backend](roles/networking_desktop.md#desktopnetworkwifibackend)`
- `[desktop_network_wireless_backend](roles/networking_desktop.md#desktopnetworkwirelessbackend)`

### `networking/firewall`
- `[firewall_enabled](roles/networking_firewall.md#firewallenabled)`
- `[firewall_backend](roles/networking_firewall.md#firewallbackend)`
- `[firewall_default_policy](roles/networking_firewall.md#firewalldefaultpolicy)`
- `[firewall_allowed_tcp_ports](roles/networking_firewall.md#firewallallowedtcpports)`
- `[firewall_allowed_udp_ports](roles/networking_firewall.md#firewallallowedudpports)`
- `[firewall_denied_tcp_ports](roles/networking_firewall.md#firewalldeniedtcpports)`
- `[firewall_denied_udp_ports](roles/networking_firewall.md#firewalldeniedudpports)`
- `[firewall_trusted_networks](roles/networking_firewall.md#firewalltrustednetworks)`
- `[firewall_masquerade_interfaces](roles/networking_firewall.md#firewallmasqueradeinterfaces)`
- `[firewall_zone_trusted](roles/networking_firewall.md#firewallzonetrusted)`
- `[firewall_zone_public](roles/networking_firewall.md#firewallzonepublic)`
- `[firewall_zone_internal](roles/networking_firewall.md#firewallzoneinternal)`
- `[firewall_zone_dmz](roles/networking_firewall.md#firewallzonedmz)`

### `networking/physical`
- `[physical_network_interface_speed_detection](roles/networking_physical.md#physicalnetworkinterfacespeeddetection)`
- `[physical_network_interface_speed_threshold](roles/networking_physical.md#physicalnetworkinterfacespeedthreshold)`
- `[physical_network_media_type_detection](roles/networking_physical.md#physicalnetworkmediatypedetection)`
- `[physical_network_optimization_enabled](roles/networking_physical.md#physicalnetworkoptimizationenabled)`
- `[physical_network_queue_depth](roles/networking_physical.md#physicalnetworkqueuedepth)`

### `networking/services`
- `[endlessh_enabled](roles/networking_services.md#endlesshenabled)`
- `[endlessh_port](roles/networking_services.md#endlesshport)`
- `[endlessh_banner](roles/networking_services.md#endlesshbanner)`
- `[endlessh_delay](roles/networking_services.md#endlesshdelay)`
- `[endlessh_max_clients](roles/networking_services.md#endlesshmaxclients)`
- `[endlessh_max_commands](roles/networking_services.md#endlesshmaxcommands)`
- `[endlessh_log_level](roles/networking_services.md#endlesshloglevel)`
- `[endlessh_address](roles/networking_services.md#endlesshaddress)`

### `networking/virtual`
- `[virtual_network_vlan_enabled](roles/networking_virtual.md#virtualnetworkvlanenabled)`
- `[virtual_network_vxlan_enabled](roles/networking_virtual.md#virtualnetworkvxlanenabled)`
- `[virtual_network_vlan_ids](roles/networking_virtual.md#virtualnetworkvlanids)`
- `[virtual_network_vxlan_vni](roles/networking_virtual.md#virtualnetworkvxlanvni)`
- `[virtual_network_overlay_encryption](roles/networking_virtual.md#virtualnetworkoverlayencryption)`
- `[virtual_network_sdn_controller](roles/networking_virtual.md#virtualnetworksdncontroller)`

### `networking/vpn_mesh`
- `[vpn_mesh_enabled](roles/networking_vpn_mesh.md#vpnmeshenabled)`
- `[vpn_mesh_backend](roles/networking_vpn_mesh.md#vpnmeshbackend)`
- `[vpn_mesh_wireguard_enabled](roles/networking_vpn_mesh.md#vpnmeshwireguardenabled)`
- `[vpn_mesh_tailscale_enabled](roles/networking_vpn_mesh.md#vpnmeshtailscaleenabled)`
- `[vpn_mesh_endpoint](roles/networking_vpn_mesh.md#vpnmeshendpoint)`
- `[vpn_mesh_allowed_ips](roles/networking_vpn_mesh.md#vpnmeshallowedips)`
- `[vpn_mesh_persistent_keepalive](roles/networking_vpn_mesh.md#vpnmeshpersistentkeepalive)`
- `[vpn_mesh_mtu](roles/networking_vpn_mesh.md#vpnmeshmtu)`
- `[vpn_mesh_pre_shared_key](roles/networking_vpn_mesh.md#vpnmeshpresharedkey)`
