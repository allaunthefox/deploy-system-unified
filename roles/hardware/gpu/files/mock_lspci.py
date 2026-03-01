#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500068
# Last Updated: 2026-03-01
# =============================================================================
"""
Mock lspci for GPU Hardware Simulation (Extended Matrix)
Standardized using verified signatures from:
- NVIDIA (RTX 4090, H100, A100, RTX 3060 Mobile)
- AMD (RX 7900 XTX, Instinct MI250X)
- Intel (Arc A770, Flex 170, Max 1550, UHD 770)
- Hybrid Systems (Intel + NVIDIA)
"""
import os
import sys

# Global Mock Database (Verified Real-World Signatures)
MOCK_DATABASE = {
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
    
    "HYBRID_LAPTOP": "0000:00:02.0 VGA compatible controller [0300]: Intel Corporation Meteor Lake-P [Intel Arc Graphics] [8086:7d55] (rev 08)\n0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation AD107M [GeForce RTX 4060 Max-Q / Mobile] [10de:28a0] (rev a1)",
    "SERVER_MULTI_A100": "0000:25:00.0 3D controller [0302]: NVIDIA Corporation GA100 [10de:20b5]\n0000:26:00.0 3D controller [0302]: NVIDIA Corporation GA100 [10de:20b5]",
    
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
