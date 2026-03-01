# Hardware Verification Fidelity Matrix

**Audit Event Identifier:** DSU-DOC-180010  
**Last Updated:** 2026-03-01  
**Status:** ✅ Active Standard

This document defines the fidelity levels for hardware verification within the **Deploy-System-Unified** project, ensuring clear distinction between simulated logic and physical validation.

---

## 📊 Fidelity Levels

| Tag | Level | Description | Environment | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **`[SIM]`** | **Simulation** | Software-in-the-Loop (SiL). Uses mock data (e.g., `gpu_mock_lspci_output`) to verify Ansible logic, role dependencies, and task flow. | Molecule / CI | **Logic Only** |
| **`[HIL]`** | **Hardware-in-the-Loop** | Verification on physical hardware in a controlled test rig. Validates driver loading and basic device initialization. | Dev Lab | **Functional** |
| **`[PHYS]`** | **Physical** | Full production verification on target hardware. Validates performance, stability, and real-world interactions. | Production | **Complete** |

---

## 🛠️ Verification Scope (GPU Example)

| Feature | `[SIM]` Scope (Mock) | `[PHYS]` Scope (Real) |
| :--- | :--- | :--- |
| **Vendor Detection** | String matching against mock PCI IDs. | Real PCI bus scan via `lspci`. |
| **Role Branching** | Verifies if `nvidia` tasks run when mock ID is `10de`. | Verifies if driver correctly initializes the silicon. |
| **Slicing Strategy** | Verifies if configuration files are generated correctly. | Verifies if MIG/SR-IOV partitions are created in VRAM. |
| **Performance** | N/A | Validates compute throughput and latency. |

---

## 🛡️ Compliance Alignment

*   **ISO 26262-6**: Supports early-stage verification using SiL (Software-in-the-Loop) methods.
*   **NIST SP 800-53 SA-11**: Provides developer-side testing evidence through automated simulation.
*   **Traceability**: Every `[SIM]` result must be superseded by a `[PHYS]` result before a feature can be marked as "Production Ready" in the Deployment Matrix.
