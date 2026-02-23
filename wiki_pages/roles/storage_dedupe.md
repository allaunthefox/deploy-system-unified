# Role: storage/dedupe (Archival Deduplication)

**Classification:** WI-CONT (Work Instruction)  
**Standard:** ISO 27040  
**Action Codes:** 500060 - 500070

## Overview
The `storage/dedupe` role implements NoDupeLabs archival standards for block-level deduplication. It focuses on optimizing long-term storage while ensuring data integrity via forensic auditing.

## Key Features
- **Offline Btrfs Deduplication**: Scheduled `duperemove` scans for cold data.
- **Forensic Audit mandatory**: Hardened profiles require a deduplication potential audit.
- **Ephemeral Guard**: Automatically disabled in short-lived environments to save resources.

## Configuration
| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `storage_dedupe_btrfs_enable` | bool | `false` | Enable deduplication |
| `storage_dedupe_btrfs_paths` | list | `["/srv/media"]` | Paths to scan |

## Compliance Mapping
- **ISO 27040**: Storage security standards.
- **Action 500061**: Deduplication complete.
- **Profile 600032**: Requirement elevated (Hardened mandatory check).
