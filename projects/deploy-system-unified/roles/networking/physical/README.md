# Networking Physical Role (`networking/physical`)

## Description
This role manages physical network interface optimizations, specifically identifying interface speeds (1G, 2.5G, 10G, 25G, 40G, 100G) and identifying physical media types (Twisted Pair vs Fiber/DAC).

## Capabilities
- **Hardware Detection**: Uses `ethtool` to identify port types and negotiated speeds.
- **Adaptive Performance Tuning**: Applies system-wide kernel parameters (`sysctl`) based on the *fastest* detected interface.
- **Jumbo Frames**: Automatically enables MTU 9000 for high-speed fiber links (>= 10Gbps).
- **Ring Buffers**: Tunes RX/TX ring buffers per-interface based on that interface's speed tier (512 for 1G -> 8192 for 100G).
- **Offloading**: Manages TSO/GSO offloading settings.

## Performance Profiles
The role includes predefined tuning profiles for the following speeds:
- **1 Gbps**: Standard desktop/server tuning.
- **2.5 Gbps**: Enhanced buffer sizing.
- **10 Gbps**: Standard Fiber/10GBASE-T server tuning.
- **25 Gbps**: High-throughput tuning (Tor/Leaf).
- **40 Gbps**: Datacenter Interconnect tuning.
- **100 Gbps**: Extreme performance (requires `irqbalance` and huge buffers).

## Variables
| Variable | Default | Description |
|----------|---------|-------------|
| `networking_physical_jumbo_frames_enabled` | `true` | Enable MTU 9000 for Fiber/SFP+. |
| `networking_physical_ring_tuning_enabled` | `true` | Enable adaptive ring buffer resizing. |
| `networking_physical_default_profile` | `"1000"` | Fallback profile if speed detection fails. |

## Usage
```yaml
- role: networking/physical
  vars:
    networking_physical_jumbo_frames_enabled: true
    # Force a specific profile for testing
    # networking_physical_default_profile: "10000"
```
