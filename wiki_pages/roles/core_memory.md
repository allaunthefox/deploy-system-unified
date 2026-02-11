# core/memory

**Role Path**: `roles/core/memory`

## Description
Tasks for core/memory - Intelligent Memory Compression

## Key Tasks
- Detect Physical Swap
- Detect Shared Video Memory (UMA)
- Determine Memory Strategy (Auto-Selection)
- Report Selected Strategy
- Resolve Configuration Conflicts (Intelligent Resolution)
- Validate Final Configuration
- Configure ZRAM (zram-generator)
- Configure ZSwap (Kernel Modules)
- Tune Virtual Memory for Compression
- Configure Transparent Huge Pages (THP)

## Default Variables
- `core_memory_compression_strategy`
- `core_memory_shared_vram`
- `core_memory_workload_profile`
- `core_memory_thp_state`
- `core_memory_zram_size_percent`
- `core_memory_zram_algorithm`
- `core_memory_zram_priority`
- `core_memory_zswap_compressor`
- `core_memory_zswap_zpool`
- `core_memory_zswap_max_pool_percent`
- `core_memory_swappiness`
- `core_memory_cache_pressure`
- `core_memory_dirty_bytes`
- `core_memory_dirty_background_bytes`

---
*This page was automatically generated from role source code.*