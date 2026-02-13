#!/usr/bin/env python3
import subprocess
import json
import sys
import re

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

def get_pci_devices():
    """Run lspci and return raw output with full domains (-D)."""
    try:
        # Class 0300 (VGA), 0302 (3D), 0380 (Display)
        # -D includes the PCI domain (e.g., 0000:)
        result = subprocess.run(
            ["lspci", "-Dnn", "-d", "::0300"], capture_output=True, text=True, check=True
        )
        vga = result.stdout
        result = subprocess.run(
            ["lspci", "-Dnn", "-d", "::0302"], capture_output=True, text=True, check=True
        )
        controller_3d = result.stdout
        result = subprocess.run(
            ["lspci", "-Dnn", "-d", "::0380"], capture_output=True, text=True, check=True
        )
        display = result.stdout
        return vga + controller_3d + display
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        return ""

def parse_lspci(output):
    """Parse lspci output into structured data."""
    devices = []
    # Pattern to match: 0000:00:02.0 VGA compatible controller [0300]: Intel Corporation UHD Graphics 620 [8086:3ea0] (rev 07)
    pattern = re.compile(r"([0-9a-f]{4}:[0-9a-f]{2}:[0-9a-f]{2}\.[0-9a-f])\s+([^\[]+)\s+\[([0-9a-f]+)\]:\s+(.+)\s+\[([0-9a-f]{4}):([0-9a-f]{4})\]")
    
    for line in output.splitlines():
        match = pattern.search(line)
        if match:
            pci_id, class_name, class_id, device_name, vendor_id, device_id = match.groups()
            vendor_name = VENDORS.get(vendor_id, "unknown")
            devices.append({
                "pci_id": pci_id,
                "vendor_id": vendor_id,
                "device_id": device_id,
                "vendor_name": vendor_name,
                "model": device_name.strip()
            })
    return devices

def main():
    raw_output = get_pci_devices()
    devices = parse_lspci(raw_output)
    
    vendor_list = sorted(list(set(d["vendor_name"] for d in devices)))
    
    # Filter out unknown if we have others, or map to generic if nothing found
    if not vendor_list:
        vendor_list = ["generic"]
    elif "unknown" in vendor_list and len(vendor_list) > 1:
        vendor_list.remove("unknown")
    
    # Primary vendor logic: Prefer NVIDIA or AMD, then Intel, then generic
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
        "is_multi_gpu": len(devices) > 1,
        "is_multi_vendor": len(vendor_list) > 1
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
