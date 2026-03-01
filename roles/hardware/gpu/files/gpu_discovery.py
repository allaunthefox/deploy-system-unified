#!/usr/bin/env python3
# =============================================================================
# Audit Event Identifier: DSU-PYS-500067
# Last Updated: 2026-03-01
# =============================================================================
"""
GPU Discovery Script with Vendor Validation and Container Runtime Support
Enhanced for Phase 1 GPU Backlog & Simulation Mode
"""
import subprocess
import json
import sys
import re
import os

# PCI Vendor IDs
VENDORS = {
    "10de": "nvidia",
    "1002": "amd",
    "8086": "intel",
    "102b": "generic",  # Matrox
    "1a03": "generic",  # Aspeed
    "1af4": "generic",  # VirtIO
    "15ad": "generic",  # VMware
    "1234": "generic",  # QEMU
}

# Intel GPU Generation Detection
INTEL_GENERATIONS = {
    "gen9": ["9bc0", "9bc4", "9bc5", "9bc6", "9bd0", "9bd1", "9bd2"],
    "gen9lp": ["9ba0", "9baa", "9bab"],
    "gen10": ["3ea0", "3ea5", "3ea6", "3ea7", "3ea8", "3ea9"],
    "gen11": ["8a70", "8a71", "8a72", "8a73", "8a74", "8a75", "8a76", "8a77"],
    "gen12": ["8a50", "8a51", "8a52", "8a53", "8a54", "8a55", "8a56", "8a57"],
    "xe": ["4c80", "4c8a", "4c90", "4c9a", "4c8b", "4c8c", "4c8d", "4c8e", "4c8f"],
    "xe_hp": ["4f00", "4f01", "4f02", "4f03", "4f04", "4f05", "4f06", "4f07", "4f08", "4f09"],
    "battlemage": ["e20b", "e20c", "e20d", "e20e", "e20f", "e21b", "e21c", "e21d", "e21e", "e21f"],
}

def get_pci_devices():
    """Run lspci and return raw output with full domains (-D)."""
    # Simulation Mode Override
    mock_output = os.environ.get("DSU_MOCK_LSPCI_OUTPUT")
    if mock_output:
        return mock_output

    outputs = []
    for class_id in ["0300", "0302", "0380"]:
        try:
            result = subprocess.run(
                ["lspci", "-Dnn", "-d", f"::{class_id}"], capture_output=True, text=True, check=True
            )
            outputs.append(result.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return "".join(outputs)

def parse_lspci(output):
    """Parse lspci output into structured data."""
    devices = []
    pattern = re.compile(r"([0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-9a-f])\s+([^\[]+)\s+\[([0-9a-f]+)\]:\s+(.+)\s+\[([0-9a-f]{4}):([0-9a-f]{4})\]")
    
    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            pci_id, class_name, class_id, device_name, vendor_id, device_id = match.groups()
            vendor_name = VENDORS.get(vendor_id, "unknown")
            
            # Detect Intel generation
            intel_gen = None
            if vendor_id == "8086":
                for gen, ids in INTEL_GENERATIONS.items():
                    if device_id in ids:
                        intel_gen = gen
                        break
            
            devices.append({
                "pci_id": pci_id,
                "vendor_id": vendor_id,
                "device_id": device_id,
                "vendor_name": vendor_name,
                "model": device_name.strip(),
                "intel_generation": intel_gen
            })
    return devices

def check_nvidia_driver():
    """Check if NVIDIA driver is loaded."""
    # Simulation Mode Override
    mock_out = os.environ.get("DSU_MOCK_NVIDIA_SMI_OUTPUT")
    if mock_out:
        match = re.search(r"Driver Version:\s*(\S+)\s*CUDA Version:\s*(\S+)", mock_out)
        return {
            "available": True,
            "driver_version": match.group(1) if match else "unknown",
            "cuda_version": match.group(2) if match else "unknown"
        }

    try:
        result = subprocess.run(
            ["nvidia-smi"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            match = re.search(r"Driver Version:\s*(\S+)", result.stdout)
            driver_version = match.group(1) if match else "unknown"
            match = re.search(r"CUDA Version:\s*(\S+)", result.stdout)
            cuda_version = match.group(1) if match else "unknown"
            return {
                "available": True,
                "driver_version": driver_version,
                "cuda_version": cuda_version
            }
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return {"available": False, "driver_version": None, "cuda_version": None}

def check_amdgpu_driver():
    """Check if AMDGPU driver is loaded."""
    # Simulation Mode Override
    mock_out = os.environ.get("DSU_MOCK_ROCM_SMI_OUTPUT")
    if mock_out:
        match = re.search(r"Version:\s*(\S+)", mock_out)
        return {
            "available": True,
            "driver_version": match.group(1) if match else "unknown"
        }

    try:
        result = subprocess.run(
            ["rocm-smi"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            match = re.search(r"GPU\s+\[.*\]\s+Version:\s*(\S+)", result.stdout)
            return {
                "available": True,
                "driver_version": match.group(1) if match else "unknown"
            }
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return {"available": False, "driver_version": None}

def check_intel_driver():
    """Check if Intel GPU driver is loaded."""
    # Simulation Mode Override
    if os.environ.get("DSU_MOCK_INTEL_GPU_TOP_OUTPUT"):
        return {"available": True}

    try:
        result = subprocess.run(
            ["timeout", "5", "intel_gpu_top", "-l", "1"], 
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return {"available": True}
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check for i915/xe module via sysfs
    if os.path.exists("/sys/class/drm/card0/device/driver"):
        driver_link = os.readlink("/sys/class/drm/card0/device/driver")
        driver_name = os.path.basename(driver_link)
        if driver_name in ["i915", "xe"]:
            return {"available": True, "driver": driver_name}
    
    return {"available": False}

def check_container_runtime_gpu():
    """Check GPU support in container runtimes."""
    runtime_info = {}
    
    # Check Podman
    try:
        result = subprocess.run(
            ["podman", "info", "--format", "json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            info = json.loads(result.stdout)
            runtime_info["podman"] = {
                "available": True,
                "nvidia_support": "nvidia" in result.stdout.lower(),
                "fuse_support": "fuse" in result.stdout.lower(),
                "version": info.get("version", {}).get("version", "unknown")
            }
        else:
            runtime_info["podman"] = {"available": False}
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        runtime_info["podman"] = {"available": False}
    
    return runtime_info

def main():
    import argparse
    parser = argparse.ArgumentParser(description="GPU Discovery and Validation")
    parser.add_argument("--configured-vendor", "-c", help="Configured vendor to validate against")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    raw_output = get_pci_devices()
    devices = parse_lspci(raw_output)
    vendor_list = sorted(list(set(d["vendor_name"] for d in devices)))
    
    if not vendor_list:
        vendor_list = ["generic"]
    elif "unknown" in vendor_list and len(vendor_list) > 1:
        vendor_list.remove("unknown")
    
    primary = "generic"
    for v in ["nvidia", "amd", "intel"]:
        if v in vendor_list:
            primary = v
            break
    
    result = {
        "detected_devices": devices,
        "detected_vendor_list": vendor_list,
        "primary_detected_vendor": primary,
        "gpu_count": len(devices),
        "drivers": {
            "nvidia": check_nvidia_driver(),
            "amdgpu": check_amdgpu_driver(),
            "intel": check_intel_driver()
        }
    }
    
    # Optional runtime check
    result["container_runtime"] = check_container_runtime_gpu()
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
