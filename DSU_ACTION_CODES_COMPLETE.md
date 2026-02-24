# Deploy-System-Unified Complete Action Codes Catalog

**Project**: Deploy-System-Unified  
**Version**: 1.1.0  
**Date**: 2026-02-19  
**Purpose**: Complete catalog of all actions and intentions with corresponding action codes

---

## Table of Contents

1. [System Lifecycle](#1-system-lifecycle)
2. [Security Operations](#2-security-operations)
3. [Container Operations](#3-container-operations)
4. [Network Operations](#4-network-operations)
5. [Storage Operations](#5-storage-operations)
6. [Hardware Operations](#6-hardware-operations)
7. [Identity & Access](#7-identity--access)
8. [Backup & Recovery](#8-backup--recovery)
9. [Monitoring & Logging](#9-monitoring--logging)
10. [Compliance & Audit](#10-compliance--audit)
11. [Deployment & Configuration](#11-deployment--configuration)
12. [Idempotency & Drift](#12-idempotency--drift)

---

## 1. System Lifecycle

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| System bootstrap start | Initialize base system | 300010 | ISO 9001 |
| System bootstrap complete | Base system ready | 300011 | ISO 9001 |
| System reboot required | Reboot pending | 300012 | - |
| System shutdown | Shutdown system | 300013 | - |
| System startup | Start system | 300014 | - |
| Package installation start | Installing packages | 530000 | - |
| Package installed | Package installed | 530001 | - |
| Package installation failed | Install failed | 530002 | - |
| Package removal | Package removed | 530003 | - |
| Package update | Package updated | 530004 | - |
| Repository added | Repo added | 530010 | - |
| Repository removed | Repo removed | 530011 | - |
| Repository updated | Repo updated | 530012 | - |
| Repository signature invalid | Repo compromised | 530013 | - |
| System update check | Checking updates | 530020 | - |
| Update available | Update found | 530021 | - |
| Update downloaded | Update ready | 530022 | - |
| Update applied | Update installed | 530023 | - |
| Update failed | Update failed | 530024 | - |
| Update reboot required | Reboot needed | 530025 | - |

---

## 2. Security Operations

### 2.1 Firejail Sandboxing

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Firejail installation | Install sandbox | 410001 | ISO/IEC 27001 §8.26 |
| Firejail configuration | Configure sandbox | 410002 | ISO/IEC 27001 §8.26 |
| Firejail profile loaded | Profile active | 410003 | ISO/IEC 27001 §8.26 |
| Custom Firejail profile | Custom profile applied | 410004 | ISO/IEC 27001 §8.26 |
| Container escape authorized | Debug escape authorized | 410005 | ISO/IEC 27001 §8.26 |
| Privileged container request | Privileged mode requested | 410006 | ISO/IEC 27001 §8.26 |
| Capability added | Add capability | 410007 | ISO/IEC 27001 §8.26 |
| Capability dropped | Drop capability | 410008 | ISO/IEC 27001 §8.26 |
| Seccomp policy change | Change seccomp | 410009 | ISO/IEC 27001 §8.26 |
| Seccomp profile loaded | Seccomp active | 410010 | ISO/IEC 27001 §8.26 |
| SYS_ADMIN request | Request SYS_ADMIN | 410011 | ISO/IEC 27001 §8.26 |
| NET_ADMIN request | Request NET_ADMIN | 410012 | ISO/IEC 27001 §8.26 |
| SYS_MODULE request | Request SYS_MODULE | 410013 | ISO/IEC 27001 §8.26 |
| **Firejail breakout attempt** | **UNAUTHORIZED breakout** | **410101** | **ISO/IEC 27001 §8.26** |
| **Firejail breakout success** | **BREAKOUT SUCCESSFUL** | **410102** | **ISO/IEC 27001 §8.26** |
| Firejail syscall violation | Blocked syscall | 410103 | ISO/IEC 27001 §8.26 |
| Firejail file violation | File access denied | 410104 | ISO/IEC 27001 §8.26 |
| Firejail network violation | Network denied | 410105 | ISO/IEC 27001 §8.26 |
| Firejail /etc violation | /etc access denied | 410106 | ISO/IEC 27001 §8.26 |
| Firejail /var violation | /var access denied | 410107 | ISO/IEC 27001 §8.26 |
| Firejail /home violation | /home access denied | 410108 | ISO/IEC 27001 §8.26 |
| Firejail /proc violation | /proc access denied | 410109 | ISO/IEC 27001 §8.26 |
| Firejail /dev violation | /dev access denied | 410110 | ISO/IEC 27001 §8.26 |
| Container escape unauthorized | Escape attempt | 410111 | ISO/IEC 27001 §8.26 |
| Privileged container escape | Priv escape | 410112 | ISO/IEC 27001 §8.26 |
| Host path escape | Host path escape | 410113 | ISO/IEC 27001 §8.26 |
| Cgroup escape | Cgroup escape | 410114 | ISO/IEC 27001 §8.26 |
| Kernel exploit escape | Kernel exploit | 410115 | ISO/IEC 27001 §8.26 |
| Unauthorized privileged | Priv mode detected | 410116 | ISO/IEC 27001 §8.26 |
| Capability escalation | Escalate capabilities | 410118 | ISO/IEC 27001 §8.26 |
| Unauthorized SYS_ADMIN | Unauthorized SYS_ADMIN | 410123 | ISO/IEC 27001 §8.26 |
| Unauthorized NET_ADMIN | Unauthorized NET_ADMIN | 410124 | ISO/IEC 27001 §8.26 |
| Unauthorized SYS_MODULE | Unauthorized SYS_MODULE | 410125 | ISO/IEC 27001 §8.26 |
| Host PID namespace access | Host PID accessed | 410130 | ISO/IEC 27001 §8.26 |
| Host network mode | Host network detected | 410132 | ISO/IEC 27001 §8.26 |
| Host IPC access | Host IPC accessed | 410134 | ISO/IEC 27001 §8.26 |
| Device mount unauthorized | Unauthorized mount | 410136 | ISO/IEC 27001 §8.26 |
| /dev/sda mounted | Disk mounted | 410137 | ISO/IEC 27001 §8.26 |
| /dev/mem mounted | Memory device | 410138 | ISO/IEC 27001 §8.26 |
| /dev/kvm mounted | KVM device | 410139 | ISO/IEC 27001 §8.26 |
| /dev/dri mounted | GPU device | 410140 | ISO/IEC 27001 §8.26 |
| Root user in container | Root detected | 410143 | ISO/IEC 27001 §8.26 |
| Docker socket mounted | Docker socket risk | 410145 | ISO/IEC 27001 §8.26 |
| Docker socket access | Docker accessed | 410146 | ISO/IEC 27001 §8.26 |
| AppArmor disabled | AppArmor off | 410149 | ISO/IEC 27001 §8.26 |
| SELinux disabled | SELinux off | 410150 | ISO/IEC 27001 §8.26 |
| No seccomp profile | No seccomp | 410154 | ISO/IEC 27001 §8.26 |
| Privileged with host network | Priv + host net | 410155 | ISO/IEC 27001 §8.26 |

### 2.2 Namespace Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| User namespace create | Create user NS | 420001 | ISO/IEC 27001 §8.26 |
| Network namespace create | Create net NS | 420002 | ISO/IEC 27001 §8.26 |
| Mount namespace create | Create mount NS | 420003 | ISO/IEC 27001 §8.26 |
| PID namespace create | Create PID NS | 420004 | ISO/IEC 27001 §8.26 |
| UTS namespace create | Create UTS NS | 420005 | ISO/IEC 27001 §8.26 |
| IPC namespace create | Create IPC NS | 420006 | ISO/IEC 27001 §8.26 |
| **Namespace escape attempt** | **UNAUTHORIZED escape** | **420101** | **ISO/IEC 27001 §8.26** |
| Host mount in namespace | Host mount detected | 420102 | ISO/IEC 27001 §8.26 |
| Host path access | Host path accessed | 420103 | ISO/IEC 27001 §8.26 |
| /proc host access | Host /proc accessed | 420104 | ISO/IEC 27001 §8.26 |
| Sys module access | Sys module accessed | 420105 | ISO/IEC 27001 §8.26 |
| /dev/kvm access | KVM accessed | 420106 | ISO/IEC 27001 §8.26 |
| /dev/dri access | GPU accessed | 420107 | ISO/IEC 27001 §8.26 |

### 2.3 Seccomp/BPF

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Seccomp policy loaded | Policy active | 430001 | ISO/IEC 27001 §8.26 |
| Seccomp profile change | Profile changed | 430002 | ISO/IEC 27001 §8.26 |
| **Syscall blocked** | **Blocked syscall** | **430100** | **ISO/IEC 27001 §8.26** |
| Unknown syscall | Unknown syscall | 430101 | ISO/IEC 27001 §8.26 |
| Privileged syscall | Priv syscall | 430102 | ISO/IEC 27001 §8.26 |
| Container-restricted syscall | Restricted syscall | 430103 | ISO/IEC 27001 §8.26 |

### 2.4 SELinux/AppArmor

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| SELinux policy loaded | Policy active | 440001 | ISO/IEC 27001 §8.26 |
| SELinux context change | Context changed | 440002 | ISO/IEC 27001 §8.26 |
| **SELinux violation** | **SELinux denial** | **440100** | **ISO/IEC 27001 §8.26** |
| SELinux container violation | Container denied | 440101 | ISO/IEC 27001 §8.26 |
| **AppArmor violation** | **AppArmor denial** | **440102** | **ISO/IEC 27001 §8.26** |
| AppArmor container violation | Container denied | 440103 | ISO/IEC 27001 §8.26 |

### 2.5 Kernel Hardening

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Kernel lockdown enable | Lockdown on | 450001 | ISO/IEC 27001 §8.26 |
| Kernel param change | Param changed | 450002 | ISO/IEC 27001 §8.26 |
| **Hardening bypass** | **Bypass detected** | **450100** | **ISO/IEC 27001 §8.26** |
| Ptrace protection bypass | Ptrace bypass | 450101 | ISO/IEC 27001 §8.26 |
| Core pattern manipulation | Core pattern change | 450102 | ISO/IEC 27001 §8.26 |
| Sysctl tampering | Sysctl tampered | 450103 | ISO/IEC 27001 §8.26 |
| Unauthorized module load | Module loaded | 450104 | ISO/IEC 27001 §8.26 |
| Module insert attempt | Insert attempt | 450105 | ISO/IEC 27001 §8.26 |
| /dev/mem access | Mem access | 450106 | ISO/IEC 27001 §8.26 |
| /dev/kvm access | KVM access | 450107 | ISO/IEC 27001 §8.26 |

### 2.6 Threat Detection

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| **Threat detected** | **Threat found** | **460000** | **ISO/IEC 27001 §16.1** |
| **Malware detected** | **Malware found** | **460001** | **ISO/IEC 27001 §16.1** |
| **Intrusion attempt** | **Intrusion detected** | **460002** | **ISO/IEC 27001 §16.1** |
| Brute force detected | Brute force | 460003 | ISO/IEC 27001 §16.1 |
| Exploit attempt | Exploit detected | 460004 | ISO/IEC 27001 §16.1 |
| Privilege escalation | Escalation | 460005 | ISO/IEC 27001 §16.1 |
| Lateral movement | Lateral move | 460006 | ISO/IEC 27001 §16.1 |
| Data exfiltration | Data leaving | 460007 | ISO/IEC 27001 §16.1 |

### 2.7 Incident Response

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Incident detected | Incident found | 470000 | ISO/IEC 27001 §16.1 |
| Incident escalated | Escalated | 470001 | ISO/IEC 27001 §16.1 |
| Containment initiated | Containing | 470002 | ISO/IEC 27001 §16.1 |
| Eradication started | Eradicating | 470003 | ISO/IEC 27001 §16.1 |
| Recovery initiated | Recovering | 470004 | ISO/IEC 27001 §16.1 |
| Post-mortem started | Analyzing | 470005 | ISO/IEC 27001 §16.1 |

### 2.8 General Security

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Security risk flagged | Risk flagged | 400000 | ISO/IEC 27001 |
| Access granted | Access allowed | 400001 | ISO/IEC 27001 §9.2 |
| Access denied | Access blocked | 400002 | ISO/IEC 27001 §9.2 |
| Rate limit triggered | Rate limited | 400003 | ISO/IEC 27001 |
| Authentication success | Auth OK | 400004 | ISO/IEC 27001 §9.2 |
| Authentication failure | Auth failed | 400005 | ISO/IEC 27001 §9.2 |
| Session start | Session started | 400006 | ISO/IEC 27001 §9.2 |
| Session end | Session ended | 400007 | ISO/IEC 27001 §9.2 |
| Secret accessed | Secret viewed | 400010 | ISO/IEC 27001 §10.1 |
| Encryption applied | Data encrypted | 400011 | ISO/IEC 27001 §10.1 |
| Decryption applied | Data decrypted | 400012 | ISO/IEC 27001 §10.1 |
| Certificate validated | Cert OK | 400013 | ISO/IEC 27001 §10.1 |
| Certificate expired | Cert expired | 400014 | ISO/IEC 27001 §10.1 |
| **Secret key archived** | **Key Backup** | **400015** | **ISO/IEC 27001 §10.1** |
| **Secret re-encryption**| **Key Rotation** | **400016** | **ISO/IEC 27001 §10.1** |

### 2.9 Network Security

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Firewall start | FW starting | 540000 | ISO/IEC 27001 §9.4 |
| Firewall configured | FW configured | 540001 | ISO/IEC 27001 §9.4 |
| Firewall rule added | Rule added | 540002 | ISO/IEC 27001 §9.4 |
| Firewall rule removed | Rule removed | 540003 | ISO/IEC 27001 §9.4 |
| Firewall blocked | Traffic blocked | 540004 | ISO/IEC 27001 §9.4 |
| Firewall rate limited | Rate limited | 540005 | ISO/IEC 27001 §9.4 |
| IDS alert | IDS alert | 540010 | ISO/IEC 27001 §16.1 |
| IDS blocked | IDS blocked | 540011 | ISO/IEC 27001 §16.1 |
| IPS blocked | IPS blocked | 540012 | ISO/IEC 27001 §16.1 |
| Suspicious traffic | Suspicious | 540013 | ISO/IEC 27001 §16.1 |
| VPN start | VPN starting | 540100 | ISO/IEC 27001 §9.3 |
| VPN connected | VPN connected | 540101 | ISO/IEC 27001 §9.3 |
| VPN disconnected | VPN disconnected | 540102 | ISO/IEC 27001 §9.3 |
| VPN failed | VPN failed | 540103 | ISO/IEC 27001 §9.3 |
| Mesh VPN configured | Mesh VPN ready | 540104 | ISO/IEC 27001 §9.3 |
| TLS cert generated | Cert generated | 540200 | ISO/IEC 27001 §10.1 |
| TLS cert expired | Cert expired | 540201 | ISO/IEC 27001 §10.1 |
| TLS cert rotated | Cert rotated | 540202 | ISO/IEC 27001 §10.1 |
| TLS handshake failed | TLS failed | 540203 | ISO/IEC 27001 §10.1 |

### 2.10 Cryptographic Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Encryption applied | Secure data | 400011 | ISO/IEC 27001 §10.1 |
| Decryption applied | Access data | 400012 | ISO/IEC 27001 §10.1 |
| **PQC initialized** | **Post-Quantum Start** | **400100** | **ISO/IEC 27001 §10.1** |
| **PQC hybrid negotiated** | **Quantum-Resistant Key** | **400101** | **ISO/IEC 27001 §10.1** |
| **PQC signature verified** | **Quantum-Resistant Sig** | **400102** | **ISO/IEC 27001 §10.1** |
| **PQC secret encrypt** | **Quantum-Safe Secret** | **400103** | **ISO/IEC 27001 §10.1** |
| Crypto agility invoked | Algorithm switch | 400110 | ISO/IEC 27001 §10.1 |
| **Secure Boot verified** | **Boot Integrity OK** | **800510** | **NIST SP 800-193** |
| **Secure Boot violation** | **UNTRUSTED BOOT** | **800511** | **NIST SP 800-193** |

---

## 3. Container Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Container create | Create container | 700000 | - |
| Container start | Start container | 700001 | - |
| Container stop | Stop container | 700002 | - |
| Container delete | Delete container | 700003 | - |
| Container restart | Restart container | 700004 | - |
| Container pause | Pause container | 700005 | - |
| Container unpause | Unpause container | 700006 | - |
| Image pull | Pull image | 700010 | - |
| Image build | Build image | 700011 | - |
| Image push | Push image | 700012 | - |
| Image delete | Delete image | 700013 | - |
| **Image signature verified**| **Supply Chain OK**| **700014** | **ISO/IEC 27001 §14.2** |
| **Image signature failed**  | **UNTRUSTED IMAGE** | **700015** | **ISO/IEC 27001 §14.2** |
| Volume create | Create volume | 700020 | - |
| Volume mount | Mount volume | 700021 | - |
| Volume unmount | Unmount volume | 700022 | - |
| Network create | Create network | 700030 | - |
| Network connect | Connect network | 700031 | - |
| Network disconnect | Disconnect network | 700032 | - |

---

## 4. Network Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Network interface detected | NIC found | 810200 | - |
| Network interface configured | NIC configured | 810201 | - |
| Network interface up | NIC up | 810202 | - |
| Network interface down | NIC down | 810203 | - |
| Network bond configured | Bond ready | 810204 | - |
| Network bridge configured | Bridge ready | 810205 | - |
| DNS configured | DNS set | 810300 | - |
| DNS resolve success | DNS OK | 810301 | - |
| DNS resolve failed | DNS failed | 810302 | - |

---

## 5. Storage Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Storage pool create | Pool created | 500000 | ISO/IEC 27040 |
| Storage pool delete | Pool deleted | 500001 | ISO/IEC 27040 |
| Storage pool mount | Pool mounted | 500002 | ISO/IEC 27040 |
| Storage pool unmount | Pool unmounted | 500003 | ISO/IEC 27040 |
| Volume create | Vol created | 500010 | ISO/IEC 27040 |
| Volume delete | Vol deleted | 500011 | ISO/IEC 27040 |
| Volume extend | Vol extended | 500012 | ISO/IEC 27040 |
| Volume shrink | Vol shrunk | 500013 | ISO/IEC 27040 |
| Filesystem mkfs | FS created | 500020 | - |
| Filesystem mount | FS mounted | 500021 | - |
| Filesystem unmount | FS unmounted | 500022 | - |
| Filesystem check | FS checked | 500023 | - |
| Filesystem resize | FS resized | 500024 | - |
| LVM PV create | PV created | 500030 | - |
| LVM VG create | VG created | 500031 | - |
| LVM LV create | LV created | 500032 | - |
| LVM snapshot create | Snapshot created | 500033 | - |
| NFS export | NFS exported | 500040 | - |
| NFS mount | NFS mounted | 500041 | - |
| SMB share | SMB shared | 500042 | - |
| SMB mount | SMB mounted | 500043 | - |
| Disk detected | Disk found | 500050 | - |
| Disk partitioned | Disk partitioned | 500051 | - |
| Disk LVM converted | Converted to LVM | 500052 | - |
| RAID created | RAID created | 500053 | - |
| RAID degraded | RAID degraded | 500054 | ISO/IEC 27040 |
| RAID failed | RAID failed | 500055 | ISO/IEC 27040 |
| **Storage dedupe start** | **Dedupe Init** | **500060** | **ISO/IEC 27040** |
| **Storage dedupe complete**| **Dedupe Done** | **500061** | **ISO/IEC 27040** |
| **Archival optimized** | **Archival Mode** | **500070** | **ISO/IEC 27040** |

---

## 6. Hardware Operations

### 6.1 CPU Detection

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Hardware detection start | HW detection | 800000 | - |
| Hardware detection complete | HW detected | 800001 | - |
| Hardware detection failed | HW failed | 800002 | - |
| x86 CPU detected | x86 found | 800100 | - |
| Intel x86 CPU | Intel CPU | 800101 | - |
| AMD x86 CPU | AMD CPU | 800102 | - |
| AMD EPYC | EPYC CPU | 800103 | - |
| AMD Ryzen | Ryzen CPU | 800104 | - |
| Intel Xeon | Xeon CPU | 800105 | - |
| Intel Core | Core CPU | 800106 | - |
| x86 VM exit | VM exit | 800107 | - |
| ARM CPU detected | ARM found | 800200 | - |
| ARM Cortex-A72 | A72 core | 800201 | - |
| ARM Cortex-A76 | A76 core | 800202 | - |
| ARM NEON | NEON SIMD | 800203 | - |
| ARM SVE | SVE vector | 800204 | - |
| ARM SVE2 | SVE2 vector | 800205 | - |
| RISC-V detected | RISC-V found | 800300 | - |
| RISC-V RV64GC | RV64GC | 800301 | - |
| RISC-V RV64IMAFDC | RV64IMAFDC | 800302 | - |
| RISC-V V extension | V ext | 800303 | - |
| RISC-V G extension | G ext | 800304 | - |

### 6.2 GPU Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| GPU detected | GPU found | 800400 | - |
| NVIDIA GPU | NVIDIA found | 800401 | - |
| AMD GPU | AMD found | 800402 | - |
| Intel GPU | Intel found | 800403 | - |
| ARM Mali GPU | Mali found | 800404 | - |
| AMD CDNA GPU | CDNA found | 800405 | - |
| AMD RDNA GPU | RDNA found | 800406 | - |
| NVIDIA CUDA | CUDA available | 800407 | - |
| NVIDIA Ampere | Ampere GPU | 800408 | - |
| NVIDIA Hopper | Hopper GPU | 800409 | - |
| GPU driver install | Driver installing | 800410 | - |
| GPU driver installed | Driver installed | 800411 | - |
| GPU driver failed | Driver failed | 800412 | - |
| GPU validation pass | GPU OK | 800413 | - |
| GPU validation fail | GPU bad | 800414 | - |
| Vulkan available | Vulkan OK | 800415 | - |
| CUDA available | CUDA OK | 800416 | - |
| OpenCL available | OpenCL OK | 800417 | - |
| GPU slice configured | Slicing configured | 800420 | - |
| GPU MIG enabled | MIG enabled | 800421 | - |
| GPU time slicing enabled | Time slicing on | 800422 | - |

### 6.3 Firmware

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Firmware update start | FW updating | 800500 | ISO/IEC 27001 §8.9 |
| Firmware update complete | FW updated | 800501 | ISO/IEC 27001 §8.9 |
| Firmware update failed | FW failed | 800502 | ISO/IEC 27001 §8.9 |
| EFI detected | UEFI found | 800503 | - |
| BIOS detected | BIOS found | 800504 | - |

### 6.4 Platform

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Bare metal platform | Bare metal | 800600 | - |
| Virtual platform | Virtual machine | 800601 | - |
| Container platform | Container | 800602 | - |
| Cloud platform | Cloud | 800603 | - |
| AWS platform | AWS | 800604 | - |
| Azure platform | Azure | 800605 | - |
| GCP platform | GCP | 800606 | - |
| VPS platform | VPS | 800607 | - |

---

## 7. Identity & Access

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| User created | User created | 510000 | ISO/IEC 27001 §9.2 |
| User deleted | User deleted | 510001 | ISO/IEC 27001 §9.2 |
| User modified | User changed | 510002 | ISO/IEC 27001 §9.2 |
| User locked | User locked | 510003 | ISO/IEC 27001 §9.2 |
| User unlocked | User unlocked | 510004 | ISO/IEC 27001 §9.2 |
| User password changed | Password changed | 510005 | ISO/IEC 27001 §9.2 |
| User password expired | Password expired | 510006 | ISO/IEC 27001 §9.2 |
| Group created | Group created | 510010 | ISO/IEC 27001 §9.2 |
| Group deleted | Group deleted | 510011 | ISO/IEC 27001 §9.2 |
| Group modified | Group changed | 510012 | ISO/IEC 27001 §9.2 |
| User added to group | Added to group | 510013 | ISO/IEC 27001 §9.2 |
| User removed from group | Removed from group | 510014 | ISO/IEC 27001 §9.2 |
| Role assigned | Role assigned | 510020 | ISO/IEC 27001 §9.2 |
| Role removed | Role removed | 510021 | ISO/IEC 27001 §9.2 |
| Privilege escalation | Priv esc | 510022 | ISO/IEC 27001 §9.2 |
| Sudo access | Sudo used | 510023 | ISO/IEC 27001 §9.2 |
| SSO login | SSO login | 510030 | ISO/IEC 27001 §9.2 |
| SSO logout | SSO logout | 510031 | ISO/IEC 27001 §9.2 |
| SSO token issued | Token issued | 510032 | ISO/IEC 27001 §9.2 |
| SSO token revoked | Token revoked | 510033 | ISO/IEC 27001 §9.2 |
| MFA enabled | MFA on | 510034 | ISO/IEC 27001 §9.2 |
| MFA disabled | MFA off | 510035 | ISO/IEC 27001 §9.2 |
| MFA failed | MFA failed | 510036 | ISO/IEC 27001 §9.2 |

---

## 8. Backup & Recovery

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Backup start | Backup started | 900000 | ISO/IEC 27040 |
| Backup complete | Backup done | 900001 | ISO/IEC 27040 |
| Backup failed | Backup failed | 900002 | ISO/IEC 27040 |
| Backup verify | Verifying backup | 900003 | ISO/IEC 27040 |
| Backup verify pass | Backup OK | 900004 | ISO/IEC 27040 |
| Backup verify fail | Backup bad | 900005 | ISO/IEC 27040 |
| Restore start | Restore started | 900010 | ISO/IEC 27040 |
| Restore complete | Restore done | 900011 | ISO/IEC 27040 |
| Restore failed | Restore failed | 900012 | ISO/IEC 27040 |
| Snapshot create | Snapshot created | 900020 | ISO/IEC 27040 |
| Snapshot delete | Snapshot deleted | 900021 | ISO/IEC 27040 |
| Snapshot prune | Snapshot pruned | 900022 | ISO/IEC 27040 |
| Retention policy applied | Policy applied | 900030 | ISO/IEC 27040 |
| Old backup pruned | Old backup gone | 900031 | ISO/IEC 27040 |

---

## 9. Monitoring & Logging

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Metrics collect | Collecting metrics | 840000 | ISO/IEC 27001 §12.4 |
| Metrics export | Exporting metrics | 840001 | ISO/IEC 27001 §12.4 |
| Alert triggered | Alert fired | 840010 | ISO/IEC 27001 §12.4 |
| Alert resolved | Alert cleared | 840011 | ISO/IEC 27001 §12.4 |
| Alert escalated | Alert escalated | 840012 | ISO/IEC 27001 §12.4 |
| Health check start | Checking health | 840020 | - |
| Health check pass | Health OK | 840021 | - |
| Health check fail | Health bad | 840022 | - |
| Log collect | Collecting logs | 840030 | ISO/IEC 27001 §12.4 |
| Log shipped | Logs sent | 840031 | ISO/IEC 27001 §12.4 |
| **Log aggregator start** | **Loki Init** | **840040** | **ISO/IEC 27001 §12.4** |
| **Forensic dashboard deploy**| **Grafana Forensic**| **840041** | **ISO/IEC 27001 §12.4** |

---

## 10. Compliance & Audit

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Audit log start | Audit started | 520000 | ISO/IEC 27037 |
| Audit rule added | Rule added | 520001 | ISO/IEC 27037 |
| Audit rule removed | Rule removed | 520002 | ISO/IEC 27037 |
| Audit log cleared | **LOG CLEARED** | **520003** | **ISO/IEC 27037** |
| Compliance check start | Checking compliance | 520010 | ISO/IEC 27001 |
| Compliance check pass | Compliant | 520011 | ISO/IEC 27001 |
| Compliance check fail | Non-compliant | 520012 | ISO/IEC 27001 |
| Compliance report generated | Report ready | 520013 | ISO/IEC 27001 |
| Policy enforced | Policy applied | 520020 | ISO/IEC 27001 |
| Policy violated | Policy broken | 520021 | ISO/IEC 27001 |
| Policy updated | Policy changed | 520022 | ISO/IEC 27001 |
| Integrity check start | Checking integrity | 520030 | ISO/IEC 27037 |
| Integrity check pass | Integrity OK | 520031 | ISO/IEC 27037 |
| Integrity check fail | Integrity bad | 520032 | ISO/IEC 27037 |
| File changed detected | File changed | 520033 | ISO/IEC 27037 |
| **SBOM audit start** | **SBOM Gen** | **520040** | **ISO/IEC 27001 §14.2** |
| **SBOM audit complete**| **Supply Chain Verified** | **520041** | **ISO/IEC 27001 §14.2** |
| **SBOM audit failed** | **Supply Chain Fail** | **520042** | **ISO/IEC 27001 §14.2** |
| **SBOM audit paused** | **Audit Paused** | **520043** | **ISO/IEC 27001 §14.2** |
| **SBOM corruption found**| **Audit Integrity Fail**| **520044** | **ISO/IEC 27001 §14.2** |
| **SBOM record deleted** | **Audit Purge** | **520045** | **ISO/IEC 27001 §14.2** |
| **SBOM vuln matched** | **Vulnerability Found**| **520046** | **ISO/IEC 27001 §5.37** |
| **SBOM signed** | **Audit Signed** | **520047** | **ISO/IEC 27001 §14.2** |

---

## 11. Deployment & Configuration

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Deployment start | Deploying | 600000 | ISO 9001 |
| Deployment complete | Deployed | 600001 | ISO 9001 |
| Deployment failed | Deploy failed | 600002 | ISO 9001 |
| Deployment rollback | Rolling back | 600003 | ISO 9001 |
| Playbook start | Running playbook | 600010 | - |
| Playbook complete | Playbook done | 600011 | - |
| Playbook failed | Playbook failed | 600012 | - |
| Task start | Task running | 600013 | - |
| Task complete | Task done | 600014 | - |
| Task failed | Task failed | 600015 | - |
| Task skipped | Task skipped | 600016 | - |
| Host unreachable | Host down | 600017 | - |
| No hosts | No hosts | 600018 | - |
| Check mode | Check mode | 600020 | - |
| Diff mode | Diff mode | 600021 | - |
| **Profile guard enforced** | **Profile Lock** | **600030** | **ISO 9001** |
| **Profile guard bypass** | **Profile Override**| **600031** | **ISO 9001** |
| **Profile requirement elevated** | **Profile Upgrade** | **600032** | **ISO 27040 §13** |

---

## 12. Idempotency & Drift

### 12.1 Idempotency Violations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| **Idempotency violation** | **Idempotency broken** | **600100** | **ISO/IEC 27001 §8.8** |
| Idempotency blocker | Known issue | 600101 | ISO/IEC 27001 §8.8 |
| Idempotency breaker | Unwanted change | 600102 | ISO/IEC 27001 §8.8 |

### 12.2 Drift Detection

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Drift detected | Drift found | 600110 | ISO/IEC 27001 §8.8 |
| Config drift | Config changed | 600111 | ISO/IEC 27001 §8.8 |
| File drift | File changed | 600112 | ISO/IEC 27001 §8.8 |
| Permission drift | Perms changed | 600113 | ISO/IEC 27001 §8.8 |
| Ownership drift | Owner changed | 600114 | ISO/IEC 27001 §8.8 |
| Content drift | Content changed | 600115 | ISO/IEC 27001 §8.8 |

### 12.3 Blockers

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Timestamp blocker | Time issue | 600120 | ISO/IEC 27001 §8.8 |
| Random blocker | Random issue | 600121 | ISO/IEC 27001 §8.8 |
| Sequence blocker | Sequence issue | 600122 | ISO/IEC 27001 §8.8 |
| External blocker | External dep | 600123 | ISO/IEC 27001 §8.8 |
| Dependency blocker | Dep issue | 600124 | ISO/IEC 27001 §8.8 |
| Network blocker | Network issue | 600125 | ISO/IEC 27001 §8.8 |
| Service blocker | Service issue | 600126 | ISO/IEC 27001 §8.8 |

### 12.4 Breakers

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Shell breaker | Shell issue | 600130 | ISO/IEC 27001 §8.8 |
| Script breaker | Script issue | 600131 | ISO/IEC 27001 §8.8 |
| Template breaker | Template issue | 600132 | ISO/IEC 27001 §8.8 |
| Command breaker | Command issue | 600133 | ISO/IEC 27001 §8.8 |
| Handler breaker | Handler issue | 600134 | ISO/IEC 27001 §8.8 |

### 12.5 Remediation

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Idempotency fix applied | Fix applied | 600140 | ISO/IEC 27001 §8.8 |
| Idempotency fix failed | Fix failed | 600141 | ISO/IEC 27001 §8.8 |
| Drift corrected | Drift fixed | 600142 | ISO/IEC 27001 §8.8 |
| Drift correction failed | Fix failed | 600143 | ISO/IEC 27001 §8.8 |
| Idempotency check start | Checking | 600150 | ISO/IEC 27001 §8.8 |
| Idempotency check pass | Check OK | 600151 | ISO/IEC 27001 §8.8 |
| Idempotency check fail | Check failed | 600152 | ISO/IEC 27001 §8.8 |
| Idempotency report generated | Report ready | 600153 | ISO/IEC 27001 §8.8 |

---

## 13. Time Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Time sync start | Syncing time | 300001 | ISO/IEC 27001 §8.17 |
| Time sync complete | Time synced | 300002 | ISO/IEC 27001 §8.17 |
| Time drift detected | Time drift | 300003 | ISO/IEC 27001 §8.17 |
| NTP server reachable | NTP OK | 300004 | ISO/IEC 27001 §8.17 |
| NTP server unreachable | NTP down | 300005 | ISO/IEC 27001 §8.17 |
| Chrony enabled | Chrony on | 300006 | ISO/IEC 27001 §8.17 |
| Timezone set | TZ set | 300007 | ISO/IEC 27001 §8.17 |

---

## 14. Kubernetes Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| K8s cluster init | Cluster init | 820000 | - |
| K8s cluster ready | Cluster ready | 820001 | - |
| K8s cluster failed | Cluster failed | 820002 | - |
| K8s join start | Join started | 820003 | - |
| K8s join complete | Join done | 820004 | - |
| K8s node ready | Node ready | 820100 | - |
| K8s node not ready | Node not ready | 820101 | - |
| K8s node cordon | Node cordoned | 820102 | - |
| K8s node uncordon | Node uncordoned | 820103 | - |
| K8s deployment created | Deploy created | 820200 | - |
| K8s deployment ready | Deploy ready | 820201 | - |
| K8s pod scheduled | Pod scheduled | 820202 | - |
| K8s pod running | Pod running | 820203 | - |
| K8s pod failed | Pod failed | 820204 | - |
| K8s service created | Svc created | 820205 | - |

---

## 15. Virtualization Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| VM create | VM created | 830000 | - |
| VM start | VM started | 830001 | - |
| VM stop | VM stopped | 830002 | - |
| VM delete | VM deleted | 830003 | - |
| VM pause | VM paused | 830004 | - |
| VM migration start | Migrating | 830005 | - |
| VM migration complete | Migrated | 830006 | - |
| Hypervisor detected | Hypervisor found | 830100 | - |
| KVM hypervisor | KVM found | 830101 | - |
| VMware hypervisor | VMware found | 830102 | - |
| Hyper-V hypervisor | Hyper-V found | 830103 | - |
| Xen hypervisor | Xen found | 830104 | - |
| Libvirt connect | Connected | 830200 | - |
| Libvirt disconnect | Disconnected | 830201 | - |
| Libvirt domain defined | Domain defined | 830202 | - |
| Libvirt domain undefined | Domain removed | 830203 | - |

---

## 16. Application Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| App deploy start | Deploying app | 550000 | - |
| App deployed | App deployed | 550001 | - |
| App deploy failed | Deploy failed | 550002 | - |
| App rollback | Rolling back | 550003 | - |
| App healthy | App OK | 550010 | - |
| App unhealthy | App bad | 550011 | - |
| App restarted | App restarted | 550012 | - |
| App crashed | App crashed | 550013 | - |
| Config changed | Config changed | 550020 | - |
| Config reloaded | Config reloaded | 550021 | - |

---

## 17. Database Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Database connect | DB connected | 560000 | - |
| Database disconnect | DB disconnected | 560001 | - |
| Connection pool exhausted | Pool empty | 560002 | - |
| Query start | Query running | 560010 | - |
| Query complete | Query done | 560011 | - |
| Query slow | Slow query | 560012 | - |
| Transaction start | Transaction begin | 560013 | - |
| Transaction commit | Committed | 560014 | - |
| Transaction rollback | Rolled back | 560015 | - |
| DB backup start | DB backing up | 560020 | - |
| DB backup complete | DB backed up | 560021 | - |
| DB restore start | DB restoring | 560022 | - |
| DB restore complete | DB restored | 560023 | - |
| Replication start | Replicating | 560030 | - |
| Replication sync | In sync | 560031 | - |
| Replication lag | Lagging | 560032 | - |
| Replication broken | Broken | 560033 | - |

---

## 18. Cloud Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Cloud provider detected | Cloud found | 570000 | - |
| AWS instance detected | AWS found | 570001 | - |
| Azure instance detected | Azure found | 570002 | - |
| GCP instance detected | GCP found | 570003 | - |
| Cloud instance create | Instance created | 570010 | - |
| Cloud instance start | Instance started | 570011 | - |
| Cloud instance stop | Instance stopped | 570012 | - |
| Cloud instance terminate | Instance terminated | 570013 | - |
| Cloud volume attach | Volume attached | 570014 | - |
| Cloud volume detach | Volume detached | 570015 | - |
| Cloud VPC create | VPC created | 570020 | - |
| Cloud subnet create | Subnet created | 570021 | - |
| Cloud SG create | SG created | 570022 | - |
| Cloud LB create | LB created | 570023 | - |
| Cloud DNS record create | DNS record created | 570030 | - |
| Cloud DNS record delete | DNS record deleted | 570031 | - |

---

## 19. IoT/Edge Operations

| Action | Intention | Code | ISO Standard |
|--------|-----------|------|--------------|
| Edge device detected | Edge device found | 580000 | - |
| Edge device connected | Edge connected | 580001 | - |
| Edge device disconnected | Edge disconnected | 580002 | - |
| Edge device offline | Edge offline | 580003 | - |
| Edge gateway registered | Gateway registered | 580010 | - |
| Edge gateway heartbeat | Gateway heartbeat | 580011 | - |
| Edge gateway config received | Config received | 580012 | - |
| IoT data received | Data received | 580020 | - |
| IoT data processed | Data processed | 580021 | - |
| IoT alert generated | Alert generated | 580022 | - |

---

## Appendix A: ISO Standard Reference

| ISO Standard | Sections | Action Codes |
|--------------|----------|--------------|
| ISO 8000-110:2025 | Data Quality | All action codes |
| ISO 8000-8:2025 | Data Lineage | 960xxx |
| ISO/IEC 27001:2022 | §8.8 | 600xxx |
| ISO/IEC 27001:2022 | §8.9 | 800500-800504 |
| ISO/IEC 27001:2022 | §8.17 | 300001-300007 |
| ISO/IEC 27001:2022 | §8.26 | 410xxx, 420xxx, 430xxx, 440xxx, 450xxx |
| ISO/IEC 27001:2022 | §9.2 | 400001-400007, 510xxx |
| ISO/IEC 27001:2022 | §9.3 | 540100-540104 |
| ISO/IEC 27001:2022 | §9.4 | 540000-540005 |
| ISO/IEC 27001:2022 | §12.2 | 520030-520033 |
| ISO/IEC 27001:2022 | §12.4 | 300010-300014, 840xxx |
| ISO/IEC 27001:2022 | §16.1 | 460xxx, 470xxx, 540010-540013 |
| ISO 27001:2022 Amd 1 | AI Security | 480xxx |
| ISO/IEC 27037:2012 | §5-7 | 520xxx |
| ISO/IEC 27040:2024 | §8-9 | 500xxx, 900xxx |
| NIST 800-190 | Container | 410xxx |
| NIST SP 800-207 | Zero Trust | 490xxx |

---

**End of Complete Action Codes Catalog**

**Total: 350+ action codes covering all project intentions**
