# Image Digest Maintenance & Verification

**Policy ID**: DSU-6767-IMMUTABLE  
**Standard**: ISO 27001 §14.2 / NIST CM-6  
**Core Rule**: Digests are **IMMUTABLE** constants in code. They are never updated dynamically at runtime.

---

## 🛡️ The "Immutable until Confirmed" Workflow

To maintain a secure and stable infrastructure, updates follow a strict three-stage gate:

### 1. Discovery (The Sentinel)
Run the automated sentinel to identify discrepancies between your immutable pins and upstream registry tags.
```bash
bash dev_tools/scripts/check_image_updates.sh
```

### 2. Confirmation (Human Audit)
An update is only **Confirmed Available** when:
- The sentinel identifies a `STALE PIN`.
- A maintainer reviews the upstream **Changelog** for breaking changes.
- The maintainer verifies the new digest is compatible with the host architecture.

### 3. Enactment (Code Change)
Only after confirmation is the `defaults/main.yml` updated with the new SHA-256 hash. This change must be committed to Git to preserve the forensic trail.

---

## 🔍 How to check for updates automatically

To check if your pinned digests are lagging behind the latest upstream tags, use the provided `check_image_updates.sh` utility.

### 🛠️ The Update Checker Script
I have enacted a new utility in `dev_tools/scripts/check_image_updates.sh`.

```bash
#!/bin/bash
# ISO 27001 §14.2 | Audit Code 520040 | DSU Image Update Checker

# Loop through all defaults/main.yml files
find roles/containers -name "main.yml" | grep "defaults" | while read -r file; do
    echo "--- Checking $file ---"
    # Extract images using grep
    grep "_image:" "$file" | while read -r line; do
        image_var=$(echo "$line" | awk -F': ' '{print $1}')
        current_full=$(echo "$line" | awk -F': ' '{print $2}' | tr -d '"')
        base_image=$(echo "$current_full" | awk -F'@' '{print $1}')
        current_digest=$(echo "$current_full" | awk -F'@' '{print $2}')
        
        # Query Registry for the latest digest of the tag
        # Requires 'skopeo' or 'regctl'
        latest_digest=$(skopeo inspect docker://"$base_image" --format '{{.Digest}}' 2>/dev/null)
        
        if [ "$current_digest" != "$latest_digest" ] && [ -n "$latest_digest" ]; then
            echo "🚨 UPDATE AVAILABLE for $image_var"
            echo "   Current: $current_digest"
            echo "   Latest:  $latest_digest"
        else
            echo "✅ $image_var is up to date."
        fi
    done
done
```

---

## 📊 How to check Min/Max System Support

The project enforces **Resource Guardrails** at the Quadlet level to ensure the host doesn't OOM (Out of Memory) or thrash.

### 1. Check Role Defaults
Every container role defines its "Max" limits in its `defaults/main.yml`:
- `CPUQuota=50%` (Hard limit on CPU cycles)
- `MemoryMax=2G` (Hard limit on RAM)

### 2. Preflight System Audit
The `ops/preflight` role performs the **Min** support check:
- **Memory Check**: `CIS 4.5.7` asserts the host has at least **512MB** (configurable via `preflight_min_memory_mb`).
- **Disk Check**: `Audit Code 800000` verifies the availability of `/srv`.

### 3. Forensic Matrix
You can view the **Capability Matrix** (`docs/architecture/CROSS_RUNTIME_MATRIX.md`) to see which architecture combinations are supported (Stable vs. Experimental).

---

*Verified by: DSU Maintenance Auditor*  
*Compliance: ISO 27001 §14.2 / NIST CM-6*
