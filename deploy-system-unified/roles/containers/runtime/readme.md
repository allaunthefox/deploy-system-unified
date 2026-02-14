# Container Runtime Role

This role handles the installation and configuration of the container runtime environment (Podman/Docker) and associated hardware support (GPU).

## Configuration

### Image Pull Reliability

To avoid being rate-limited or banned by image registries (specifically Docker Hub, which has a 100 pull/6hr limit for anonymous users), this role implements a "Safe Retry" strategy.

| Variable | Default | Description |
|----------|---------|-------------|
| `containers_pull_retries` | `5` | Number of times to retry a failed image pull. |
| `containers_pull_delay` | `30` | Seconds to wait between retries. High defaults prevent "Hammering" bans. |

### Hardware Acceleration

| Variable | Default | Description |
|----------|---------|-------------|
| `containers_enable_gpu_support` | `false` | Enable GPU drivers and hooks. |
| `containers_gpu_vendor` | `nvidia` | Vendor (`nvidia`, `amd`, `intel`). |
