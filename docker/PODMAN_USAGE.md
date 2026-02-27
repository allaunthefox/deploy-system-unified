# Podman Usage Guide

This project uses **Podman** as the default and preferred container runtime with **Docker compatibility mode** enabled.

## Why Podman?

- **Rootless by default** - No daemon required, better security
- **Systemd integration** - Native Quadlet support for service management
- **Docker-compatible** - Same CLI commands, same images via compatibility socket
- **No socket exposure** - Optional Docker socket emulation (on-demand)
- **Kubernetes-native** - Direct YAML support with `podman play kube`

---

## Docker Compatibility Mode

Podman can emulate the Docker socket for seamless compatibility with existing Docker tools.

### Enable Docker Compatibility

```bash
# Run the setup script
sudo ./docker/setup-podman-docker-compat.sh

# Or manually enable the socket
sudo systemctl enable --now podman-docker-compat.socket
```

### Use Docker Commands with Podman

Once compatibility mode is enabled:

```bash
# All Docker CLI commands work
docker ps
docker images
docker-compose up -d
docker-compose ps

# Behind the scenes, Podman handles the requests
# No Docker daemon required!
```

### Verify Compatibility

```bash
# Check if Docker socket is available
ls -la /var/run/docker.sock
# Output: srw-rw---- 1 root docker ... /var/run/docker.sock

# Test Docker CLI
docker version
# Shows Podman version with Docker API compatibility

# Test docker-compose
docker-compose ps
# Shows Quadlet-managed containers
```

---

## Quick Start

### Option 1: Podman Quadlet (Recommended)

Quadlet integrates containers with systemd for automatic management.

```bash
# 1. Build the image
podman build -t deploy-system-unified:latest -f docker/Containerfile .

# 2. Copy Quadlet files to systemd directory
sudo cp docker/deploy-system.container /etc/containers/systemd/
sudo cp docker/*.volume /etc/containers/systemd/volumes/

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Start the service
sudo systemctl start deploy-system

# 5. Enable auto-start on boot
sudo systemctl enable deploy-system

# 6. View logs
journalctl -u deploy-system -f

# 7. Check status
systemctl status deploy-system
```

### Option 2: Podman Kube YAML

```bash
# 1. Build the image
podman build -t deploy-system-unified:latest -f docker/Containerfile .

# 2. Deploy with Kubernetes YAML
podman play kube docker/deploy-system.yaml

# 3. View logs
podman logs deploy-system

# 4. Stop deployment
podman pod stop deploy-system
podman pod rm deploy-system
```

### Option 3: Direct Podman Run

```bash
# 1. Build the image
podman build -t deploy-system-unified:latest -f docker/Containerfile .

# 2. Run container
podman run -d \
  --name deploy-system \
  --restart unless-stopped \
  --user 1000:1000 \
  --memory 1024m \
  --cpus 1.0 \
  --read-only \
  --tmpfs /tmp:size=100M,mode=1777 \
  --tmpfs /var/tmp:size=50M,mode=1777 \
  --security-opt no-new-privileges:true \
  --cap-drop ALL \
  --volume deploy-config:/opt/deploy-system/config \
  --volume deploy-logs:/opt/deploy-system/logs \
  --volume deploy-data:/opt/deploy-system/data \
  --volume ./inventory:/opt/deploy-system/inventory:ro \
  --volume ./playbooks:/opt/deploy-system/playbooks:ro \
  --volume ./roles:/opt/deploy-system/roles:ro \
  deploy-system-unified:latest \
  --help

# 3. View logs
podman logs deploy-system

# 4. Execute commands in container
podman exec -it deploy-system /bin/sh
```

---

## Volume Management

### Create Named Volumes

```bash
# Create volumes for persistent data
podman volume create deploy-config
podman volume create deploy-logs
podman volume create deploy-data

# Inspect volumes
podman volume inspect deploy-config
```

### Backup Volumes

```bash
# Backup configuration
podman run --rm \
  --volume deploy-config:/source:ro \
  --volume $(pwd):/backup \
  alpine tar czf /backup/deploy-config-backup.tar.gz -C /source .

# Restore configuration
podman run --rm \
  --volume deploy-config:/target \
  --volume $(pwd):/backup \
  alpine tar xzf /backup/deploy-config-backup.tar.gz -C /target
```

---

## Security Considerations

### Rootless Execution

Podman runs containers as non-root by default:

```bash
# Verify running as non-root
podman exec deploy-system id
# Output: uid=1000(deploy) gid=1000(deploy)
```

### No Socket Exposure

Unlike Docker, Podman does NOT require socket exposure:

```bash
# ❌ Docker (security risk):
# /var/run/docker.sock mounted in container

# ✅ Podman (secure):
# No socket required - daemonless architecture
```

### Read-Only Filesystem

The container runs with a read-only root filesystem:

```bash
# Verify read-only
podman exec deploy-system touch /test-file
# Output: Read-only file system
```

---

## Troubleshooting

### Check Container Status

```bash
# Quadlet (systemd)
systemctl status deploy-system

# Direct Podman
podman ps -a --filter name=deploy-system
```

### View Logs

```bash
# Quadlet (systemd)
journalctl -u deploy-system -f

# Direct Podman
podman logs deploy-system
podman logs --tail 100 deploy-system
```

### Health Check

```bash
# Check health status
podman inspect deploy-system --format '{{.State.Health.Status}}'

# Run health check manually
podman exec deploy-system /opt/deploy-system/entrypoint.sh healthcheck
```

### Resource Usage

```bash
# View resource usage
podman stats deploy-system

# View detailed info
podman inspect deploy-system
```

---

## Migration from Docker

If you're migrating from Docker Compose:

```bash
# 1. Stop Docker container
docker-compose down

# 2. Backup volumes
docker run --rm \
  --volume deploy-system_deploy-config:/source:ro \
  --volume $(pwd):/backup \
  alpine tar czf /backup/deploy-config-backup.tar.gz -C /source .

# 3. Build Podman image
podman build -t deploy-system-unified:latest -f docker/Containerfile .

# 4. Restore volumes
podman volume create deploy-config
podman run --rm \
  --volume deploy-config:/target \
  --volume $(pwd):/backup \
  alpine tar xzf /backup/deploy-config-backup.tar.gz -C /target

# 5. Deploy with Quadlet (see Option 1 above)
```

---

## Commands Reference

| Docker Command | Podman Equivalent |
|----------------|-------------------|
| `docker build` | `podman build` |
| `docker run` | `podman run` |
| `docker exec` | `podman exec` |
| `docker logs` | `podman logs` |
| `docker ps` | `podman ps` |
| `docker-compose up` | `podman play kube` or Quadlet |
| `docker volume create` | `podman volume create` |

---

## Additional Resources

- [Podman Documentation](https://podman.io/docs)
- [Quadlet Documentation](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)
- [Podman vs Docker](https://podman.io/whatis)
- [Rootless Podman](https://github.com/containers/podman/blob/main/docs/tutorials/rootless_tutorial.md)

---

**Last Updated:** 2026-02-27  
**Podman Version:** 5.0+ recommended
