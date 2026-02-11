# networking/physical

**Role Path**: `roles/networking/physical`

## Description
**Networking Physical Role (`networking/physical`)**
This role manages physical network interface optimizations, specifically identifying interface speeds (1G, 2.5G, 10G, 25G, 40G, 100G) and identifying physical media types (Twisted Pair vs Fiber/DAC).

## Key Tasks
- Install networking tools
- Disable IRQBalance in Virtualized Environments
- Detect physical interfaces
- Gather ethtool facts for physical interfaces
- Parse Interface Types and Capabilities
- Debug Interface Capabilities
- Determine Max Interface Speed
- Select Performance Profile
- Apply High-Speed Kernel Tuning (Sysctl)
- Apply Jumbo Frames to High Speed/Fiber Interfaces
- Tune Ring Buffers (Adaptive per Interface Speed)
- Apply Offload Settings (TSO/GSO)

## Default Variables
- `interface_capabilities`
- `networking_physical_install_tools`
- `networking_physical_manage_mtu`
- `networking_physical_jumbo_frames_enabled`
- `networking_physical_jumbo_mtu`
- `networking_physical_ring_tuning_enabled`
- `networking_physical_rx_ring_size`
- `networking_physical_tx_ring_size`
- `networking_physical_offload_tuning_enabled`
- `networking_physical_enable_tso`
- `networking_physical_enable_gso`
- `networking_physical_enable_lro`
- `networking_physical_profiles`
- `networking_physical_default_profile`

---
*This page was automatically generated from role source code.*