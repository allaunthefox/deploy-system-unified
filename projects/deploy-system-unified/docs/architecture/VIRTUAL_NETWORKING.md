# Virtualization Networking: VLANs vs. VXLANs
This project handles virtualization networking through modular L2 and L3 isolation strategies. By separating these concerns into `networking/virtual`, we ensure that physical network logic never comingles with virtual overlay logic.

## 🏷 VLANs (Standard L2 Isolation)
VLANs are used for **Local Segmentation**. They are ideal when the hypervisor and the physical switch support 802.1Q tagging.
### Implementation Strategy
- **Interface Naming**: Standardized as `eth0.<vlan_id>` or `bond0.<vlan_id>`.
- **Bridge Mapping**: Each VLAN interface is typically attached to its own Linux Bridge (e.g., `br10` for VLAN 10).
- **Scope**: Restricted to the local physical broadcast domain.

## 🌉 VXLANs (L3 Overlay Isolation)
VXLANs (Virtual Extensible LAN) are used for **Multi-Node Segmentation**. They allow virtual L2 networks to span across different physical L3 subnets by encapsulating frames in UDP packets.
### How to deal with VXLANs
In a modular "Secure Base" setting, VXLANs are preferred for cross-node K8s or distributed VM workloads.

1. **Explicit VTEP (VXLAN Tunnel End Point)**:
   - Every node must have a VTEP interface defined.
   - Example: `vxlan10` with a specific VNI (Virtual Network Identifier).
2. **Encapsulation**:
   - Frames are encapsulated in UDP (default port 4789).
   - **Mandatory Security**: Because VXLAN packets are plain L3 traffic, they **MUST** be paired with the `networking/vpn_mesh` (IPSec/Wireguard) role if they traverse untrusted networks.
3. **Control Plane**:
   - For simple deployments: Static unicast remote IPs.
   - For scalable deployments: Multicast or BGP/EVPN (handled by specialized SDN roles).
## 🛠 Role Logic Separation
To avoid comingling, the `networking/virtual` role is divided into:
- `tasks/vlan.yml`: Local interface tagging.
- `tasks/vxlan.yml`: Tunnel interface and VNI management.
- `tasks/bridges.yml`: Virtual switch configuration.

