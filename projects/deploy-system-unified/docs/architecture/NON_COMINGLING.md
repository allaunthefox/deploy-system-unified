# Philosophy: Non-Comingling of Tasks
The foundational rule of this project is:
> **Complexity is not a problem, but comingling tasks is.**

## 🔍 What is Comingling?
Comingling occurs when a single Role or Task tries to manage multiple logical concerns. This creates hidden dependencies and makes the system fragile.
### ❌ Anti-Patterns (Comingled)
*   A `security` role that installs `ntp` (Comingling Security with System Services).
*   A `bootstrap` role that configures a `firewall` (Comingling Initialization with Perimeter Defense).
*   A `hardened_ssh` task that generates an encrypted report for the operator (Comingling Target Posture with Operational Reporting).

### ✅ Modular Patterns (The Unified Way)
*   **`core/time`**: Only manages NTP/Chrony.
*   **`networking/firewall`**: Only manages the L3/L4 perimeter.
*   **`ops/connection_info`**: Only manages operator reporting and encryption.
## 🛠 Why this matters
1.  **Forensic Clarity**: When a log says `core/time` failed, you know exactly what is wrong. You don't have to guess if the "Security Framework" failed due to a network error or a bad config.
2.  **Auditability**: Security auditors can review `networking/firewall` without having to parse through unrelated package installation logic.
3.  **Flexibility**: You can swap `core/time` for a different time sync method without touching any security roles.

## 🤖 Enforcement
This philosophy is enforced by:
1.  **`enforce_style_guide.sh`**: Audits role structure and nesting.
2.  **The Base Import Rule**: Workloads *never* define infrastructure; they *import* it from a verified Base Layer.

