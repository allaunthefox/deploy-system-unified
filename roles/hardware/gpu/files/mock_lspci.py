#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500068
# Last Updated: 2026-03-01
# =============================================================================
"""
Mock lspci for GPU Hardware Simulation
Used by Molecule to verify discovery logic without physical GPUs.
Standardized using real-world data from RTX 4090, RX 7900 XTX, and Arc A770.
"""
import os
import sys

# Real-world PCI Simulation Data
MOCK_OUTPUTS = {
    "NVIDIA_RTX_4090": "0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation AD102 [GeForce RTX 4090] [10de:2684] (rev a1)",
    "AMD_RX_7900_XTX": "0000:03:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Navi 31 [Radeon RX 7900 XT/7900 XTX] [1002:744c] (rev c8)",
    "INTEL_ARC_A770": "0000:03:00.0 VGA compatible controller [0300]: Intel Corporation DG2 [Arc A770] [8086:56a0] (rev 08)",
    "INTEL_BATTLEMAGE": "0000:03:00.0 VGA compatible controller [0300]: Intel Corporation [8086:e20b] (rev 01)", # Simulated Battlemage
    "MULTI_NV_INTEL": "0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation AD102 [GeForce RTX 4090] [10de:2684] (rev a1)\n0000:00:02.0 VGA compatible controller [0300]: Intel Corporation [8086:56a0]",
    "LEGACY_NVIDIA": "0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA102 [GeForce RTX 3090] [10de:2204] (rev a1)"
}

def main():
    gpu_type = os.environ.get("DSU_MOCK_GPU", "NONE")
    
    # If lspci is called with specific filter flags, return filtered mock data
    if "-d" in sys.argv:
        if gpu_type == "NONE":
            sys.exit(0)
        # Use first match or default to GA102 if not found
        print(MOCK_OUTPUTS.get(gpu_type, MOCK_OUTPUTS["LEGACY_NVIDIA"]))
    else:
        # Default behavior: pass through to real lspci if available, or return nothing
        try:
            import subprocess
            # Look for real lspci in common paths
            real_lspci = "/usr/bin/lspci"
            if not os.path.exists(real_lspci):
                real_lspci = "lspci"
            subprocess.run([real_lspci] + sys.argv[1:])
        except (FileNotFoundError, PermissionError):
            sys.exit(0)

if __name__ == "__main__":
    main()
