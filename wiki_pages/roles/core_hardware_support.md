# core_hardware_support

**Role Path**: `roles/core/hardware_support`

## Description
**Hardware Discovery & Requirements**
Discovers CPU features (AVX, AES-NI) and handles hardware acceleration requirements.

## Key Tasks
- Retrieve CPU flags
- Set Hardware Facts
- Check for Intel QAT (QuickAssist Technology)
- Set Crypto Accelerator Facts
- Report Hardware Capabilities
- Validate AVX Requirement (Generic Media/DB)
- Warn on missing AVX (Soft Check)
- Get timedatectl status
- Configure Hardware Clock (RTC) to UTC
- Enable NTP-based RTC synchronization
- Validate Crypto Acceleration (Secure Nodes)
- Warn on missing Crypto extensions

## Default Variables
- `enable_hardware_discovery`
- `require_avx`
- `require_aes_ni`
- `require_crypto_extensions`
- `warn_on_missing_avx`
- `warn_on_missing_crypto`

---
*This page was automatically generated from role source code.*