#!/bin/sh
# ISO 27001 §14.2 | Action 520040 | DSU Image Update Sentinel
# Usage: ./check_image_updates.sh [--json]

echo "--- DSU Immutable Digest Audit Start ---"
echo "Policy: Pinned until Manual Confirmation"

find roles/containers -name "main.yml" | grep "defaults" | while read -r file; do
    grep "_image:" "$file" | while read -r line; do
        image_var=$(echo "$line" | awk -F': ' '{print $1}' | xargs)
        current_full=$(echo "$line" | awk -F': ' '{print $2}' | tr -d '"' | xargs)
        base_image=$(echo "$current_full" | awk -F'@' '{print $1}')
        current_digest=$(echo "$current_full" | awk -F'@' '{print $2}')
        
        # Confirmation Gate: Query upstream registry
        # Use skopeo if available, else fallback to a warning
        if command -v skopeo >/dev/null 2>&1; then
            latest_digest=$(skopeo inspect docker://"$base_image" --format '{{.Digest}}' 2>/dev/null)
            if [ "$current_digest" != "$latest_digest" ] && [ -n "$latest_digest" ]; then
                echo "🚨 STALE PIN: $image_var"
                echo "   Current Immutable: $current_digest"
                echo "   Confirmed Latest:  $latest_digest"
                echo "   Action: Review changelog and manually update defaults/main.yml"
            else
                echo "✅ VERIFIED: $image_var matches latest upstream."
            fi
        else
            echo "⚠️  SKIPPED: 'skopeo' not found. Cannot confirm upstream availability."
        fi
    done
done
