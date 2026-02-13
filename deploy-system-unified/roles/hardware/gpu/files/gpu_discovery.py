#!/usr/bin/env python3
"""
GPU Discovery Script with Vendor Validation and Container Runtime Support
Enhanced for Phase 1 GPU Backlog
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
    try:
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
    try:
        result = subprocess.run(
            ["nvidia-smi"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # Parse driver version
            match = re.search(r"Driver Version:\s*(\S+)", result.stdout)
            driver_version = match.group(1) if match else "unknown"
            
            # Parse CUDA version
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
    try:
        result = subprocess.run(
            ["timeout", "5", "intel_gpu_top", "-l", "1"], 
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return {"available": True}
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check for i915 module
    if os.path.exists("/sys/class/drm/card0/device/driver"):
        driver_link = os.readlink("/sys/class/drm/card0/device/driver")
        if "i915" in driver_link:
            return {"available": True, "driver": "i915"}
    
    return {"available": False}

def check_egpu_hot_swap():
    """Check for eGPU hot-swap capability via Thunderbolt/USB4."""
    egpu_info = {
        "thunderbolt_detected": False,
        "usb4_detected": False,
        "oculink_detected": False,
        "hot_swap_capable": False,
        "connected_devices": []
    }
    
    # Check Thunderbolt
    try:
        result = subprocess.run(
            ["boltctl", "list"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            egpu_info["thunderbolt_detected"] = True
            egpu_info["hot_swap_capable"] = True
            # Parse connected devices
            for line in result.stdout.splitlines():
                if line.strip():
                    egpu_info["connected_devices"].append({
                        "type": "thunderbolt",
                        "info": line.strip()
                    })
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check USB4 (via Thunderbolt system)
    try:
        # USB4 devices appear in thunderbolt list
        result = subprocess.run(
            ["lssysfs", "list"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            egpu_info["usb4_detected"] = True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check OCuLink (PCIe hot-plug)
    try:
        # Check if pciehp is available
        if os.path.exists("/sys/bus/pci/hotplug"):
            egpu_info["oculink_detected"] = True
            egpu_info["hot_swap_capable"] = True
    except Exception:
        pass
    
    # Check for recently added GPU devices (hot-swap detection)
    try:
        # Check dmesg for recent GPU additions
        result = subprocess.run(
            ["dmesg"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            recent_gpus = []
            for line in result.stdout.splitlines():
                if any(x in line.lower() for x in ["gpu added", "nvidia", "radeon", "intel"]):
                    if "hotplug" in line.lower() or "hot-add" in line.lower():
                        recent_gpus.append(line.strip()[:100])
            if recent_gpus:
                egpu_info["recent_hot_adds"] = recent_gpus[-5:]  # Last 5
    except Exception:
        pass
    
    return egpu_info

def check_dp_alt_mode():
    """Check DisplayPort Alt Mode via USB-C."""
    dp_info = {
        "usb_c_ports": [],
        "dp_alt_mode_available": False,
        "connected_displays": [],
        "thunderbolt_ports": [],
        "usb4_ports": []
    }
    
    # Check for USB-C ports with DP capability
    try:
        result = subprocess.run(
            ["lsusb", "-t"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "DP" in line or "DisplayPort" in line:
                    dp_info["dp_alt_mode_available"] = True
                    dp_info["connected_displays"].append(line.strip())
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check via sysfs for DP capable USB-C
    try:
        for port in os.listdir("/sys/bus/usb/devices"):
            if "usb" in port:
                # Check for downstream ports with display capability
                path = f"/sys/bus/usb/devices/{port}/power/control"
                if os.path.exists(path):
                    dp_info["usb_c_ports"].append(port)
    except Exception:
        pass
    
    # Check Thunderbolt ports
    try:
        result = subprocess.run(
            ["boltctl", "list"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            dp_info["thunderbolt_ports"] = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Check USB4 ports via sysfs
    try:
        if os.path.exists("/sys/bus/thunderbolt"):
            dp_info["usb4_ports"] = [d for d in os.listdir("/sys/bus/thunderbolt/devices") if d]
    except Exception:
        pass
    
    # Check connected displays via wayland/X
    try:
        if os.environ.get("WAYLAND_DISPLAY") or os.environ.get("DISPLAY"):
            result = subprocess.run(
                ["wlr-randr"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.strip():
                        dp_info["connected_displays"].append(line.strip()[:80])
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    return dp_info

def check_rdma_support():
    """Check RDMA (Remote Direct Memory Access) support."""
    rdma_info = {
        "rdma_available": False,
        "rdma_devices": [],
        "ib_devices": [],
        "rdma_modules_loaded": [],
        "roce_supported": False,
        "iwarp_supported": False
    }
    
    # Check for RDMA devices
    try:
        if os.path.exists("/sys/class/infiniband"):
            rdma_info["rdma_available"] = True
            rdma_info["ib_devices"] = [d for d in os.listdir("/sys/class/infiniband") if d]
    except Exception:
        pass
    
    # Check RDMA kernel modules
    rdma_modules = ["ib_core", "ib_uverbs", "rdma_cm", "mlx5_ib", "i40iw", "bnxt_re"]
    try:
        with open("/proc/modules", "r") as f:
            loaded = [line.split()[0] for line in f]
            rdma_info["rdma_modules_loaded"] = [m for m in rdma_modules if m in loaded]
    except Exception:
        pass
    
    # Check RoCE (RDMA over Converged Ethernet)
    try:
        if os.path.exists("/sys/class/net"):
            for net in os.listdir("/sys/class/net"):
                roce_path = f"/sys/class/net/{net}/device/rdma_roce_state"
                if os.path.exists(roce_path):
                    rdma_info["roce_supported"] = True
                    break
    except Exception:
        pass
    
    # Check iWARP
    try:
        result = subprocess.run(
            ["rdma", "link"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout:
            rdma_info["rdma_devices"] = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    return rdma_info

def check_egpu_rdma_integration():
    """Check eGPU + RDMA integration capability."""
    integration = {
        "egpu_rdma_capable": False,
        "thunderbolt_rdma": False,
        "pcie_rdma": False,
        "bandwidth_gbps": 0,
        "notes": []
    }
    
    egpu = check_egpu_hot_swap()
    rdma = check_rdma_support()
    
    # Check for Thunderbolt + RDMA (via Thunderbolt to PCIe)
    if egpu["thunderbolt_detected"] and rdma["rdma_available"]:
        integration["thunderbolt_rdma"] = True
        integration["egpu_rdma_capable"] = True
        integration["notes"].append("Thunderbolt eGPU with RDMA detected")
        integration["bandwidth_gbps"] = 40  # Thunderbolt 3/4
    
    # Check for direct PCIe + RDMA
    if not egpu["thunderbolt_detected"] and rdma["rdma_available"]:
        integration["pcie_rdma"] = True
        integration["egpu_rdma_capable"] = True
        integration["notes"].append("Direct PCIe GPU with RDMA detected")
        integration["bandwidth_gbps"] = 32  # PCIe 3.0 x16
    
    return integration

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
            has_nvidia = "nvidia" in result.stdout.lower()
            has_fuse = "fuse" in result.stdout.lower() or "fuse3" in result.stdout.lower()
            runtime_info["podman"] = {
                "available": True,
                "nvidia_support": has_nvidia,
                "fuse_support": has_fuse,
                "version": info.get("version", {}).get("version", "unknown")
            }
        else:
            runtime_info["podman"] = {"available": False}
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        runtime_info["podman"] = {"available": False}
    
    # Check Docker
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "json"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            info = json.loads(result.stdout)
            runtime_info["docker"] = {
                "available": True,
                "nvidia_support": "nvidia" in result.stdout.lower(),
                "version": info.get("ServerVersion", "unknown")
            }
        else:
            runtime_info["docker"] = {"available": False}
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        runtime_info["docker"] = {"available": False}
    
    # Check for GPU device nodes
    gpu_devices = []
    for dev in os.listdir("/dev"):
        if dev.startswith(("nvidia", " render", "card")):
            gpu_devices.append(f"/dev/{dev}")
    
    runtime_info["device_nodes"] = gpu_devices
    
    return runtime_info

def validate_vendor_configuration(configured_vendor, detected_vendors):
    """Compare configured vendor against detected hardware."""
    if not configured_vendor or configured_vendor == "generic":
        return {
            "valid": True,
            "warning": "No specific vendor configured, using auto-detection"
        }
    
    # Handle list of vendors
    if isinstance(configured_vendor, list):
        configured = configured_vendor
    else:
        configured = [configured_vendor]
    
    # Check if any configured vendor matches detected
    matches = [v for v in configured if v in detected_vendors]
    
    if matches:
        return {
            "valid": True,
            "matches": matches,
            "message": f"Configuration matches detected hardware: {matches}"
        }
    else:
        return {
            "valid": False,
            "configured": configured,
            "detected": detected_vendors,
            "warning": f"Mismatch: configured {configured} but detected {detected_vendors}"
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="GPU Discovery and Validation")
    parser.add_argument("--configured-vendor", "-c", help="Configured vendor to validate against")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON format")
    parser.add_argument("--validation-only", "-v", action="store_true", help="Only run validation")
    parser.add_argument("--container-check", action="store_true", help="Check container runtime GPU support")
    parser.add_argument("--egpu-check", action="store_true", help="Check eGPU hot-swap capability")
    parser.add_argument("--dp-alt-mode", action="store_true", help="Check DisplayPort Alt Mode")
    parser.add_argument("--rdma", action="store_true", help="Check RDMA support")
    parser.add_argument("--egpu-rdma", action="store_true", help="Check eGPU + RDMA integration")
    args = parser.parse_args()
    
    raw_output = get_pci_devices()
    devices = parse_lspci(raw_output)
    
    vendor_list = sorted(list(set(d["vendor_name"] for d in devices)))
    
    if not vendor_list:
        vendor_list = ["generic"]
    elif "unknown" in vendor_list and len(vendor_list) > 1:
        vendor_list.remove("unknown")
    
    # Primary vendor logic
    primary = "generic"
    for v in ["nvidia", "amd", "intel"]:
        if v in vendor_list:
            primary = v
            break
    
    # Check drivers
    nvidia_info = check_nvidia_driver()
    amdgpu_info = check_amdgpu_driver()
    intel_info = check_intel_driver()
    
    result = {
        "detected_devices": devices,
        "detected_vendor_list": vendor_list,
        "primary_detected_vendor": primary,
        "gpu_count": len(devices),
        "is_multi_gpu": len(devices) > 1,
        "is_multi_vendor": len(vendor_list) > 1,
        "drivers": {
            "nvidia": nvidia_info,
            "amdgpu": amdgpu_info,
            "intel": intel_info
        }
    }
    
    # Vendor validation if requested
    if args.configured_vendor:
        validation = validate_vendor_configuration(args.configured_vendor, vendor_list)
        result["vendor_validation"] = validation
    
    # Container runtime check if requested
    if args.container_check:
        result["container_runtime"] = check_container_runtime_gpu()
    
    # Enhanced multi-GPU reporting
    if len(devices) > 1:
        result["multi_gpu_details"] = {
            "total_devices": len(devices),
            "by_vendor": {},
            "identical_cards": len(set(d["model"] for d in devices)) == 1,
            "pci_slots": [d["pci_id"] for d in devices]
        }
        
        # Group by vendor
        for d in devices:
            vendor = d["vendor_name"]
            if vendor not in result["multi_gpu_details"]["by_vendor"]:
                result["multi_gpu_details"]["by_vendor"][vendor] = []
            result["multi_gpu_details"]["by_vendor"][vendor].append(d["model"])
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("=== GPU Detection Summary ===")
        print(f"Total GPUs: {len(devices)}")
        print(f"Detected Vendors: {', '.join(vendor_list)}")
        print(f"Primary Vendor: {primary}")
        print(f"Multi-GPU: {result['is_multi_gpu']}")
        print(f"Multi-Vendor: {result['is_multi_vendor']}")
        
        if nvidia_info["available"]:
            print(f"\nNVIDIA Driver: {nvidia_info.get('driver_version', 'N/A')}")
            print(f"  CUDA: {nvidia_info.get('cuda_version', 'N/A')}")
        
        if amdgpu_info["available"]:
            print(f"\nAMDGPU Driver: {amdgpu_info.get('driver_version', 'N/A')}")
        
        if intel_info["available"]:
            print(f"\nIntel GPU: Driver loaded")
        
        if args.configured_vendor and "vendor_validation" in result:
            print(f"\n=== Vendor Validation ===")
            v = result["vendor_validation"]
            if v["valid"]:
                print(f"✓ {v.get('message', 'Valid')}")
            else:
                print(f"✗ {v.get('warning', 'Invalid')}")
        
        if args.container_check and "container_runtime" in result:
            print(f"\n=== Container Runtime ===")
            for runtime, info in result["container_runtime"].items():
                if isinstance(info, dict) and info.get("available"):
                    print(f"{runtime}: {'✓' if info.get('nvidia_support') or info.get('fuse_support') else 'basic'}")
        
        # eGPU hot-swap check
        if args.egpu_check:
            egpu_info = check_egpu_hot_swap()
            result["egpu"] = egpu_info
            print(f"\n=== eGPU Hot-Swap ===")
            print(f"Thunderbolt: {'✓' if egpu_info['thunderbolt_detected'] else '✗'}")
            print(f"USB4: {'✓' if egpu_info['usb4_detected'] else '✗'}")
            print(f"OCuLink: {'✓' if egpu_info['oculink_detected'] else '✗'}")
            print(f"Hot-Swap Capable: {'✓' if egpu_info['hot_swap_capable'] else '✗'}")
            if egpu_info['connected_devices']:
                print("Connected Devices:")
                for dev in egpu_info['connected_devices']:
                    print(f"  - {dev['type']}: {dev['info']}")
        
        # DP Alt Mode check
        if args.dp_alt_mode:
            dp_info = check_dp_alt_mode()
            result["dp_alt_mode"] = dp_info
            print(f"\n=== DisplayPort Alt Mode ===")
            print(f"DP Alt Mode Available: {'✓' if dp_info['dp_alt_mode_available'] else '✗'}")
            if dp_info['usb_c_ports']:
                print(f"USB-C Ports: {len(dp_info['usb_c_ports'])}")
            if dp_info['thunderbolt_ports']:
                print(f"Thunderbolt Ports: {len(dp_info['thunderbolt_ports'])}")
            if dp_info['usb4_ports']:
                print(f"USB4 Ports: {len(dp_info['usb4_ports'])}")
            if dp_info['connected_displays']:
                print("Connected Displays:")
                for disp in dp_info['connected_displays'][:3]:
                    print(f"  - {disp[:60]}")
        
        # RDMA check
        if args.rdma:
            rdma_info = check_rdma_support()
            result["rdma"] = rdma_info
            print(f"\n=== RDMA Support ===")
            print(f"RDMA Available: {'✓' if rdma_info['rdma_available'] else '✗'}")
            if rdma_info['ib_devices']:
                print(f"InfiniBand Devices: {', '.join(rdma_info['ib_devices'])}")
            if rdma_info['rdma_modules_loaded']:
                print(f"Loaded Modules: {', '.join(rdma_info['rdma_modules_loaded'])}")
            print(f"RoCE Supported: {'✓' if rdma_info['roce_supported'] else '✗'}")
        
        # eGPU + RDMA integration check
        if args.egpu_rdma:
            integration = check_egpu_rdma_integration()
            result["egpu_rdma_integration"] = integration
            print(f"\n=== eGPU + RDMA Integration ===")
            print(f"eGPU+RDMA Capable: {'✓' if integration['egpu_rdma_capable'] else '✗'}")
            print(f"Thunderbolt+RDMA: {'✓' if integration['thunderbolt_rdma'] else '✗'}")
            print(f"PCIe+RDMA: {'✓' if integration['pcie_rdma'] else '✗'}")
            if integration['bandwidth_gbps']:
                print(f"Max Bandwidth: {integration['bandwidth_gbps']} Gbps")
            if integration['notes']:
                for note in integration['notes']:
                    print(f"  - {note}")

if __name__ == "__main__":
    main()
