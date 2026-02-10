# Hardware Compatibility & Synergy Matrix

This document details supported hardware platforms, CPU-GPU pairings, and system-level capabilities for the `deploy-system-unified` project. It serves as a guide for selecting hardware for specific deployment roles (Compute, VDI, Edge, Workstation).

## 1. Platform Tier Definition

| Tier | Typical Hardware | Target Roles | Key Capabilities | Limitations |
| :--- | :--- | :--- | :--- | :--- |
| **Enterprise Server** | AMD EPYC, Intel Xeon Scalable, Ampere Altra | Cloud, K8s Node, AI Training | 128+ PCIe Lanes, ECC RAM, IPMI, SR-IOV | High noise, boot time, power consumption |
| **HEDT / Workstation** | AMD Threadripper, Intel Xeon W, Core X | AI Dev, Rendering, Engineering | 64+ PCIe Lanes, Quad-Channel RAM | Limited remote management (no IPMI) |
| **Consumer Desktop** | Intel Core i9/i7, AMD Ryzen 9/7 | Gaming, Basic Dev, Home Lab | High Single-Core Clock, QuickSync | Limited PCIe lanes (usually 20-24), No ECC |
| **Edge / Embedded** | NVIDIA Jetson, Intel NUC, Industrial PC | Robotics, Inference, Gateway | Low Power, GPIO, passive cooling | Memory constraints, non-standard boot (UEFI alternate) |
| **SBC (RISC-V/ARM)** | StarFive, Milk-V, Raspberry Pi | IoT, Lightweight Service | Ultra-low power, experimental ISA | Limited PCIe (often x1 or x4), minimal support |

## 2. CPU + GPU Synergy Matrix

Certain CPU and GPU combinations unlock specific implementation features.

| CPU Platform | GPU Vendor | Feature Enabled | Description | Requirements |
| :--- | :--- | :--- | :--- | :--- |
| **AMD Ryzen/EPYC** | **AMD Radeon/Instinct** | **Smart Access Memory (SAM) / ReBAR** | CPU accesses full GPU VRAM. Critical for gaming & large LLM loading. | BIOS: 4G Decoding enabled, ReBAR enabled. |
| **Intel Core/Xeon** | **Intel Arc/Data Center** | **Deep Link / Hyper Compute** | Simultaneous use of iGPU and dGPU for transcoding/compute. | Intel CPU with Xe iGPU + Supported Arc dGPU. |
| **Intel Xeon** | **NVIDIA** | **GPUDirect RDMA** | Direct NIC-to-GPU memory transfer (bypassing CPU). | Supported NIC (Mellanox), Root Complex support. |
| **NVIDIA ARM (Grace)** | **NVIDIA Hopper** | **NVLink C2C** | Unified Memory Architecture between CPU and GPU. | Grace Hopper Superchip hardware. |
| **Generic x86** | **NVIDIA** | **NVIDIA ReBAR** | Resizable BAR support on standard x86 platforms. | Driver 460+, Compatible Motherboard. |

## 3. Virtualization & Slicing Capabilities

Hardware requirements for advanced GPU slicing and passthrough features defined in `gpu_stack`.

| Capability | Hardware Requirement | Notes |
| :--- | :--- | :--- |
| **PCIe Passthrough** | **IOMMU (VT-d / AMD-Vi)** | Must be supported by CPU and Motherboard. Consumer boards often have poor IOMMU groups (grouping USB/SATA with GPU). |
| **SR-IOV (GPU)** | **Server-Grade GPU** | AMD FirePro/Instinct, NVIDIA A100/H100, Intel Flex/Max. Consumer cards (GeForce/Radeon) **do not** support SR-IOV. |
| **MIG (Multi-Instance GPU)** | **NVIDIA Ampere/Hopper (A100/A30/H100)** | Not available on A10/A40 or consumer cards. Requires disabling ECC on some models. |
| **Time Slicing (Software)** | **All NVIDIA Pascal+** | **Supported on Consumer GPUs**. Uses container runtime to share GPU cycles. No memory isolation, but enables sharing 1 GPU across multiple containers. |
| **GVT-g (Legacy)** | **Intel Broadwell to Comet Lake (Gen 5-9.5)** | **Deprecated**. Hardware mediation for older Intel iGPUs. Not supported on 11th Gen+ (Xe). |
| **Bitfusion / vGPU** | **Licensed Data Center GPU** | Requires NVIDIA vGPU software licensing server. |

## 4. Storage & Networking Hardware

Specialized operational roles (`hardware/sas`, `networking/physical`) optimize these hardware classes.

| Hardware Class | Recommended Controller | Driver | Optimal Configuration | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **SAS-2 (6G)** | LSI 2008 / 2308 | `mpt3sas` | Queue Depth: 64 | Legacy/Budget JBODs. |
| **SAS-3 (12G)** | LSI 3008 / 3108 | `mpt3sas` / `megaraid_sas` | Queue Depth: 128 | Standard Enterprise. |
| **SAS-4 (24G)** | LSI 9600 / 9500 (Tri-Mode) | `mpi3mr` | Queue Depth: 256 | Required for NVMe-over-SAS infrastructure. |
| **10GbE Network** | Intel X540 / X550 | `ixgbe` | MTU 9000 (Fiber/DAC) | Enable `irqbalance`. |
| **25/40GbE Network** | Mellanox ConnectX-4/5 | `mlx5_core` | Ring Buffers: 4096 | Requires PCI Gen3 x8 minimum. |
| **100GbE Network** | Mellanox ConnectX-6 / Intel E810 | `mlx5_core` / `ice` | Ring Buffers: 8192, Huge Pages | Requires specific Sysctl tuning (provided by `networking/physical`). |

## 5. Edge & Experimental Architectures (RISC-V / ARM)

Support matrix for specific non-x86 boards targeted in the restructuring plan.

| Board / Platform | Architecture | Recommended GPU | PCIe Constraints | Usage Scenario |
| :--- | :--- | :--- | :--- | :--- |
| **NVIDIA Jetson Orin** | ARM64 | **Integrated (Ampere)** | N/A (SoC) | Edge AI, Robotics. Uses `tegra` drivers. |
| **Raspberry Pi 5** | ARM64 | **Generic (AMD/NVIDIA)** | PCIe Gen 2 x1 (via hat) | Not recommended for heavy GPU loads. Bottlenecked. |
| **Ampere Altra Dev Kit** | ARM64 | **NVIDIA A100 / AMD Pro** | Full PCIe Gen4 x128 | ARM Native Cloud Native workstation. |
| **Milk-V Pioneer** | RISC-V | **AMD Radeon (RX 500/6000)** | PCIe Gen3 x16 | Native RISC-V builder. AMD `amdgpu` open driver is best supported. |
| **StarFive VisionFive 2** | RISC-V | **IMG BXE (Integrated)** | N/A | Basic display/3D. Drivers are still maturing. PCIe x4 slot available for dGPU (experimental). |

## 5. Storage & Bandwidth interactions

When designing a node, consider the PCIe lane budget.

* **Consumer CPUs (Core/Ryzen)**: typically have ~20-24 lanes directly to CPU.
    * x16 for GPU
    * x4 for primary NVMe
    * (Rest via Chipset DMI - bottleneck)
    * *Risk*: Installing a second GPU often drops the primary to x8, or forces the second GPU through the chipset (high latency, bad for P2P).

* **HEDT/Server CPUs**: typically 64-128 lanes.
    * Allows multiple x16 GPUs at full speed.
    * Allows multiple NVMe drives directly attached to CPU.
    * *Benefit*: Essential for Multi-GPU training (LLMs) to ensure fast P2P interconnect.

## 6. Known Conflicts

1. **NVIDIA Consumer + Virtualization**:
    * Older drivers (pre-465) blocked passthrough (Error 43). Modern drivers allow it, but capabilities are artificially limited (no SR-IOV).
2. **Intel Arc + Legacy BIOS**:
    * Requires ReBAR for usable performance. Without it, performance drops by ~40%.
3. **AMD APU + dGPU**:

## 7. External GPU (eGPU) Interfaces

Deploy System Unified supports both Thunderbolt/USB4 and OCuLink standards for external GPU expansion.

| Interface | Bandwidth | Protocol | Hot Plug | Recommended Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Thunderbolt 3/4** | ~32 Gbps (Data) | PCIe x4 Gen3 over USB-C | Yes (Software managed by `bolt`) | Mobile workstations, temporary docking. |
| **OCuLink (SFF-8611)** | ~64 Gbps (PCIe 4.0 x4) | Native PCIe | No (Requires Rescan/Reboot) | High-performance semi-permanent clusters. |

* **Thunderbolt**: Requires `bolt` daemon authorization (User Space).
* **OCuLink**: Requires generic PCIe Bus Rescan (Kernel Space). Use `gpu-rescan` utility provided by the role.
