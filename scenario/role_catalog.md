# Enterprise Role Catalog

**Project**: Northstar Financial Services IAM Governance  
**Governance Framework**: Role-Based Access Control (RBAC) & Principle of Least Privilege  
**Review Cadence**: Semi-Annual Baseline Review

This catalog defines the standardized enterprise role profiles, permitted application scopes, privilege classifications, approval authorities, and Segregation of Duties (SoD) constraints across Northstar Financial Services.

---

## 1. Role Definitions & Access Profiles

### 1.1. Finance Department Roles

| Role Identifier | Role Name | Permitted Applications | Standard Access Level | Privileged | Approval Authority | SoD Restrictions |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **`ROLE-FIN-ANALYST`** | Financial Analyst | `APP-FIN` | Read / Write (General Ledger, Journals) | No | Finance Manager | Mutually exclusive with `ROLE-FIN-APPROVER` |
| **`ROLE-FIN-MANAGER`** | Finance Manager | `APP-FIN` | Read / Write / Reporting | No | Finance Director | Incompatible with direct payment initiation |
| **`ROLE-FIN-INITIATOR`**| Payment Initiator | `APP-FIN` (Wire Module) | Execute (Create Wire/Batch) | Yes (Sensitive) | Finance Director | **Toxic Combination**: Incompatible with `ROLE-FIN-APPROVER` |
| **`ROLE-FIN-APPROVER`** | Payment Approver | `APP-FIN` (Wire Module) | Authorize (Release Wire/Batch) | Yes (Sensitive) | Finance Director + CISO | **Toxic Combination**: Incompatible with `ROLE-FIN-INITIATOR` |

---

### 1.2. Engineering & Technology Roles

| Role Identifier | Role Name | Permitted Applications | Standard Access Level | Privileged | Approval Authority | SoD Restrictions |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **`ROLE-DEV-ENGINEER`** | Backend/Frontend Dev | `APP-DEV` | Read / Write (Code Repos, Dev Pipelines) | No | Engineering Manager | Incompatible with production deployer & IAM admin |
| **`ROLE-DEV-MANAGER`**  | Engineering Director | `APP-DEV`, `APP-OPS` | Read / Approve (PRs, Releases) | No | VP Technology | Cannot hold production infrastructure keys |
| **`ROLE-DEV-CONTRACTOR`**| Engineering Contractor | `APP-DEV` (Restricted) | Read / Write (Branch Scoped Repos) | No | Sponsor Manager + SecOps | Time-bound to contract end date; zero production access |

---

### 1.3. IT & Security Operations Roles (Privileged)

| Role Identifier | Role Name | Permitted Applications | Standard Access Level | Privileged | Approval Authority | SoD Restrictions |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **`ROLE-IT-ADMIN`** | IT Support Admin | `APP-IDP`, `APP-OPS` | User Provisioning, Password Reset | **Yes** | IT Lead + SecOps | Cannot approve own access requests; no financial app access |
| **`ROLE-IT-GLOBALADMIN`**| Global / Domain Admin | `APP-IDP`, Infrastructure | Full Administrative Control | **Yes (Critical)** | CISO Approval Required | **Must be time-bound/PAM vaulted**; zero standing 24/7 access |
| **`ROLE-SEC-ADMIN`** | Security Administrator | `APP-IDP`, All Audit Trails | Read / Audit / Security Governance | **Yes** | CISO Approval Required | Independent audit role; cannot perform operational finance workflows |

---

### 1.4. Business Operations & HR Roles

| Role Identifier | Role Name | Permitted Applications | Standard Access Level | Privileged | Approval Authority | SoD Restrictions |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **`ROLE-HR-SPECIALIST`**| HR Operations Specialist| `APP-HR` | Employee Records, Status Changes | No | HR Director | Cannot modify own employment record or payroll |
| **`ROLE-OPS-SPECIALIST`**| Operations Specialist | `APP-OPS` | Customer CRM, Loan Case Handling | No | Operations Manager | Incompatible with `ROLE-FIN-ANALYST` (Mover risk) |
| **`ROLE-OPS-MANAGER`** | Operations Manager | `APP-OPS` | Case Escalations, Operational Reporting | No | Operations Director | Independent from technical platform administration |

---

### 1.5. Service / Non-Human Identities

| Role Identifier | Role Name | Permitted Applications | Standard Access Level | Privileged | Approval Authority | Governance Requirement |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **`ROLE-SVC-BACKUP`** | Automated Backup Daemon | Infrastructure, Storage | Automated Read/Snapshot | **Yes** | Cloud Lead | Named technical owner + 90-day key rotation |
| **`ROLE-SVC-ETL`** | Batch Reconciliation Daemon| `APP-FIN` | Automated Ledger Synchronization | No | Finance Business Owner | Named technical + business owner required |
| **`ROLE-SVC-REPORTING`**| Reporting Collector | `APP-OPS` | Read-only Metrics Extraction | No | Operations Manager | Decommission upon system retirement |

---

## 2. Core Governance Rules

1. **Explicit Role Authorization**: No user may be granted application access without an assigned role registered in this catalog.
2. **Toxic Combinations**: Combining initiation and approval permissions within financial modules (e.g. `ROLE-FIN-INITIATOR` + `ROLE-FIN-APPROVER`) is strictly prohibited without a formal, board-notified risk exception.
3. **Privilege Segregation**: Privileged roles (`ROLE-IT-GLOBALADMIN`, `ROLE-IT-ADMIN`) must be assigned to dedicated administrative accounts (`adm_*`) separate from routine daily email/browsing accounts.
