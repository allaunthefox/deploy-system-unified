#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500068
# Last Updated: 2026-03-01
# =============================================================================
"""
Mock lspci for GPU Hardware Simulation
Used by Molecule to verify discovery logic without physical GPUs.
"""
import os
import sys

# Simulation Data
MOCK_OUTPUTS = {
    "NVIDIA": "0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA102 [GeForce RTX 3090] [10de:2204] (rev a1)",
    "INTEL": "0000:00:02.0 VGA compatible controller [0300]: Intel Corporation Alder Lake-S GT1 [UHD Graphics 770] [8086:4680] (rev 0c)",
    "AMD": "0000:03:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Navi 21 [Radeon RX 6800/6800 XT / 6900 XT] [1002:73bf] (rev c1)",
    "MULTI": "0000:01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA102 [10de:2204]
0000:00:02.0 VGA compatible controller [0300]: Intel Corporation Alder Lake [8086:4680]"
}

def main():
    gpu_type = os.environ.get("DSU_MOCK_GPU", "NONE")
    
    # If lspci is called with specific filter flags, return filtered mock data
    if "-d" in sys.argv:
        if gpu_type == "NONE":
            sys.exit(0)
        print(MOCK_OUTPUTS.get(gpu_type, ""))
    else:
        # Default behavior: pass through to real lspci if available, or return nothing
        try:
            import subprocess
            subprocess.run(["/usr/bin/lspci"] + sys.argv[1:])
        except FileNotFoundError:
            sys.exit(0)

if __name__ == "__main__":
    main()
