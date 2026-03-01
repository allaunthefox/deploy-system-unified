#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500068
# Last Updated: 2026-03-01
# =============================================================================
"""
Mock lspci for GPU Hardware Simulation (Extended Matrix)
Standardized using verified signatures from:
- NVIDIA (RTX 4090, H100, A100, RTX 3060 Mobile, vGPU A10)
- AMD (RX 7900 XTX, Instinct MI250X, SR-IOV VF S7150, Radeon Vega 8 iGPU)
- Intel (Arc A770, Flex 170, Max 1550, UHD 770, Iris Xe, GVT-g HD 610)
- Server BMC (ASPEED AST2400/2500/2600, Matrox G200e)
- Hybrid Systems (Intel + NVIDIA)
- Virtualized (VirtIO GPU)
"""
import os
import sys

# Global Mock Database (Verified Real-World Signatures)
MOCK_DATABASE = {
    # Physical Discrete GPUs
    "NVIDIA_RTX_4090": "0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation AD102 [GeForce RTX 4090] [10de:2684] (rev a1)",
    "NVIDIA_H100_SXM": "0000:b4:00.0 3D controller [0302]: NVIDIA Corporation GH100 [H100 SXM5] [10de:2321] (rev a1)",
    "NVIDIA_A100_PCIE": "0000:25:00.0 3D controller [0302]: NVIDIA Corporation GA100 [A100 PCIe 80GB] [10de:20b5] (rev a1)",
    "NVIDIA_RTX_3060_MOBILE": "0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA106M [GeForce RTX 3060 Mobile / Max-Q] [10de:2520] (rev a1)",
    
    "AMD_RX_7900_XTX": "0000:03:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Navi 31 [Radeon RX 7900 XT/7900 XTX] [1002:744c] (rev c8)",
    "AMD_INSTINCT_MI250X": "0000:03:00.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] Aldebaran [Instinct MI250X/MI250] [1002:740c] (rev 01)",
    
    "INTEL_ARC_A770": "0000:03:00.0 VGA compatible controller [0300]: Intel Corporation DG2 [Arc A770] [8086:56a0] (rev 08)",
    "INTEL_FLEX_170": "0000:b3:00.0 Display controller [0380]: Intel Corporation Device [8086:56c0] (rev 08)",
    "INTEL_MAX_1550": "0000:4d:00.0 Display controller [0380]: Intel Corporation Device [8086:0bd5] (rev 08)",
    "INTEL_UHD_770": "0000:00:02.0 VGA compatible controller [0300]: Intel Corporation Alder Lake-S GT1 [UHD Graphics 770] [8086:4680] (rev 0c)",
    "INTEL_IRIS_XE": "0000:00:02.0 VGA compatible controller [0300]: Intel Corporation TigerLake-LP GT2 [Iris Xe Graphics] [8086:9a49] (rev 01)",

    # Integrated GPUs (iGPUs)
    "AMD_VEGA_8": "0000:07:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Raven Ridge [Radeon Vega Series] [1002:15d8] (rev c3)",
    "INTEL_UHD_630": "0000:00:02.0 VGA compatible controller [0300]: Intel Corporation UHD Graphics 630 [8086:3e92] (rev 00)",

    # Server BMC / Management Video (Supermicro, etc.)
    "ASPEED_AST2500": "0000:01:00.0 VGA compatible controller [0300]: ASPEED Technology, Inc. ASPEED Graphics Family [1a03:2000] (rev 41)",
    "ASPEED_AST2600": "0000:05:00.0 VGA compatible controller [0300]: ASPEED Technology, Inc. ASPEED Graphics Family [1a03:2000] (rev 52)",
    "MATROX_G200E": "0000:06:03.0 VGA compatible controller [0300]: Matrox Electronics Systems Ltd. MGA G200eW WPCM450 [102b:0532] (rev 0a)",
    
    # Virtualized & Mediated GPUs
    "NVIDIA_VGPU_A10": "0000:00:05.0 VGA compatible controller [0300]: NVIDIA Corporation GA102GL [A10] [10de:2230] (rev a1)",
    "AMD_SRIOV_VF": "0000:00:03.0 Display controller [0380]: Advanced Micro Devices, Inc. [AMD/ATI] TongaXT GL [FirePro S7150] [1002:6929] (rev 00)",
    "INTEL_GVTG_HD610": "0000:00:02.0 VGA compatible controller [0300]: Intel Corporation HD Graphics 610 [8086:5902] (rev 04)",
    "VIRTIO_GPU": "0000:00:02.0 VGA compatible controller [0300]: Red Hat, Inc. Virtio GPU [1af4:1050] (rev 01)",
    
    # Multi-GPU & Hybrid
    "HYBRID_LAPTOP": "0000:00:02.0 VGA compatible controller [0300]: Intel Corporation Meteor Lake-P [Intel Arc Graphics] [8086:7d55] (rev 08)\n0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation AD107M [GeForce RTX 4060 Max-Q / Mobile] [10de:28a0] (rev a1)",
    "SERVER_MULTI_A100": "0000:25:00.0 3D controller [0302]: NVIDIA Corporation GA100 [10de:20b5]\n0000:26:00.0 3D controller [0302]: NVIDIA Corporation GA100 [10de:20b5]",
    "SUPERMICRO_HYBRID": "0000:01:00.0 VGA compatible controller [0300]: ASPEED Technology, Inc. ASPEED Graphics Family [1a03:2000] (rev 41)\n0000:02:00.0 3D controller [0302]: NVIDIA Corporation GA100 [A100 PCIe 80GB] [10de:20b5]",
    
    "NONE": ""
}

def main():
    # Fetch simulation type from environment
    gpu_type = os.environ.get("DSU_MOCK_GPU", "NONE")
    
    # Logic simulation: If -d is used, we are looking for filtered device IDs
    if "-d" in sys.argv:
        if gpu_type == "NONE":
            sys.exit(0)
        print(MOCK_DATABASE.get(gpu_type, ""))
    else:
        # Passthrough to real system if not in mock mode
        try:
            import subprocess
            real_lspci = "/usr/bin/lspci"
            if not os.path.exists(real_lspci):
                real_lspci = "lspci"
            subprocess.run([real_lspci] + sys.argv[1:])
        except (FileNotFoundError, PermissionError):
            sys.exit(0)

if __name__ == "__main__":
    main()
