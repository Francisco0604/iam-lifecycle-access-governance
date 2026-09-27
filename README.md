# IAM Lifecycle & Access Governance Operations Lab

> **A simulated enterprise identity governance, Joiner-Mover-Leaver (JML) audit, and access operations lab featuring automated Python anomaly detection.**

[![Governance Focus](https://img.shields.io/badge/Security-IAM%20Governance-0052cc.svg)](#)
[![Compliance](https://img.shields.io/badge/Framework-SOX%20ITGC%20%7C%20SOC2-232f3e.svg)](#)
[![Automation](https://img.shields.io/badge/Automation-Python%20Auditing-success.svg)](#)
[![Status](https://img.shields.io/badge/Status-Completed%20%2F%20Remediated-brightgreen.svg)](#)

---

## 📌 Project Overview & Purpose

Managing identity security in an enterprise is not just about writing AWS JSON policies; it is about managing the **entire operational lifecycle of human and machine identities** across business applications. 

This project simulates the identity operations and governance framework of **Northstar Financial Services**, a mid-sized wealth advisory and lending firm. It evaluates the complete identity journey:
- **Joiner**: Onboarding, identity creation, baseline role assignment, and manager approval.
- **Mover**: Department transfers, role changes, and the prevention of privilege creep.
- **Leaver**: Voluntary/involuntary termination, timely deprovisioning, and access revocation.
- **Privileged Access Management (PAM)**: Managing standing administrative access versus time-bound, emergency break-glass sessions.
- **Segregation of Duties (SoD)**: Enforcing incompatible role boundaries to prevent corporate financial fraud.
- **Non-Human Identity Governance**: Ensuring service accounts have assigned technical and business ownership.

This repository complements my technical [Cloud IAM & Least-Privilege Access Review Lab](../Cloud%20IAM%20&%20Least-Privilege%20Access%20Review%20Lab/README.md) by demonstrating the **operational, managerial, and compliance controls** required for enterprise IAM and Security Operations roles.

> **Disclaimer**: This is a simulated, educational portfolio lab modeling enterprise IAM operations. All organizations, employee names, systems, event logs, and access records are entirely fictional.

---

## 🏗️ Enterprise Architecture & Operating Model

```text
Northstar Financial Services — Identity Governance Lifecycle
│
├── Identity Authoritative Sources (HR / Contractors)
│   ├── HRIS (PeopleCore) ──────▶ Authoritative source for permanent staff onboarding & terminations
│   └── Sponsor Managers ───────▶ Fixed-term contractor onboarding and contract end dates
│
├── Central Identity & Access Governance Engine
│   ├── Role-Based Access Control (RBAC) & Enterprise Role Catalog (15 standardized roles)
│   ├── Request Management (ITSM dual-approval workflows)
│   ├── Segregation of Duties (SoD) Toxic Combination Validation Engine
│   └── Quarterly User Access Reviews (UAR / Recertification)
│
└── Business Systems & Workloads Governed
    ├── APP-FIN  (Financial Ledger & Wire Disbursement Module — SOX In-Scope)
    ├── APP-HR   (HRIS Personnel & Payroll Records)
    ├── APP-DEV  (DevCloud Source Code Repositories & CI/CD Pipelines)
    ├── APP-OPS  (Customer Operations CRM & Loan Servicing)
    └── APP-IDP  (Identity Platform & Directory Infrastructure)
```

---

## 📁 Repository Structure

```text
iam-lifecycle-access-governance/
│
├── README.md                                  # You are here: project overview, metrics, and guide
│
├── scenario/
│   ├── organization.md                        # Enterprise context, in-scope applications, and stakeholders
│   ├── identity_inventory.csv                 # Authoritative identity catalog (20 human & service identities)
│   └── role_catalog.md                        # Formal RBAC definitions, permitted scopes, and SoD rules
│
├── lifecycle/
│   ├── joiner_events.csv                      # New hire onboarding records and baseline role assignments
│   ├── mover_events.csv                       # Internal transfer records documenting privilege creep defects
│   └── leaver_events.csv                      # HR termination records cross-referenced with deprovisioning SLA
│
├── access-management/
│   ├── access_requests.csv                    # Ticketed access requests (approved, rejected, and escalated)
│   ├── approval_matrix.md                     # Formal authority matrix (Requester vs Approver vs Fulfiller)
│   └── provisioning_matrix.csv                # Technical mapping: Role -> Application -> Permission Level
│
├── governance/
│   ├── access_review.csv                      # Quarterly UAR sheet (20 entitlements evaluated with decisions)
│   ├── privileged_access_review.csv           # PAM evaluation: standing admin vs break-glass event logs
│   ├── segregation_of_duties.md               # Toxic combination analysis and treasury control evaluation
│   └── exceptions_register.csv                # Policy exceptions register with compensating controls
│
├── monitoring/
│   └── iam_events.csv                         # Operational IAM audit trail (authentications, elevation, alerts)
│
├── automation/
│   ├── iam_review.py                          # Automated Python audit script evaluating governance rules
│   └── iam_review_results.csv                 # Structured defect findings exported by the script
│
└── report/
    └── IAM-Governance-Operations-Report.md    # Formal executive audit report with scorecards & remediation
```

---

## 🚨 Key Audit Findings Summary

| Finding ID | Title | Severity | Impacted Identity | Root Cause & Remediation |
| :--- | :--- | :---: | :--- | :--- |
| **IAM-01** | Terminated User Retaining Active Access | **HIGH** | Marcus Vance (`USR-1014`) | HR closed offboarding ticket without IT deprovisioning verification; user logged in post-termination. Account disabled immediately; automated SCIM connector planned. |
| **IAM-02** | Access Not Removed Following Role Change | **MEDIUM** | Elena Rostova (`USR-1008`) | Mover process was additive; user transferred to Operations but retained Finance write access. Legacy role revoked; dual-confirmation workflow enforced. |
| **IAM-03** | Segregation-of-Duties Conflict | **HIGH** | David Chen (`USR-1003`) | Finance manager held both Wire Initiation and Wire Approval rights, bypassing dual-custody. Wire initiator role stripped immediately; automated pre-request SoD checks added. |
| **IAM-04** | Unowned / Poorly Governed Service Account | **MEDIUM** | `svc_legacy_etl_sync` (`SVC-3002`) | Automated reconciliation daemon lacked technical and business owners, preventing safe rotation. Assigned to Cloud Lead; enrolled in 90-day rotation. |
| **IAM-05** | Excessive Standing Privileged Access | **HIGH** | Rachel Adams (`USR-1005`) | Lead engineer held permanent 24/7 Global Administrator access. Revoking standing rights; migrating to time-bound JIT checkout via PAM vault. |
| **IAM-06** | Expired Contractor Account Remaining Active | **MEDIUM** | Liam Gallagher (`CTR-2002`) | Contract expired on 2026-08-31, but account remained active and authenticated on 2026-09-22. Account disabled; directory expiration dates enforced. |

---

## ⚙️ Python Automation: `iam_review.py`

To demonstrate continuous identity governance and remove reliance on error-prone manual spreadsheets, I developed a lightweight audit automation script located in [`automation/iam_review.py`](automation/iam_review.py).

### Capabilities
The script evaluates source CSV datasets using standard library Python and automatically flags:
1. **Terminated users retaining active directory status** (cross-referencing HR leaver tickets).
2. **Expired contractor accounts remaining active**.
3. **Dormant accounts** (>90 days without interactive authentication).
4. **Service accounts without assigned ownership**.
5. **Excessive standing privileged accounts** (`ROLE-IT-GLOBALADMIN`).
6. **Toxic Segregation of Duties combinations**.
7. **Expired policy exceptions**.

> **Detection Rule Reconciliation**: The script implements **7 discrete audit functions** that evaluate the environment and output **8 finding instances** across **6 unique affected identities**. The difference between 7 rules and 8 output instances occurs because contractor Liam Gallagher (`CTR-2002`) triggered three separate control checks: unfulfilled leaver ticket (Rule 1), expired contract end date (Rule 2), and an unrevoked expired policy exception (Rule 7).

### Running the Script Locally
```bash
# Navigate to the project root
cd iam-lifecycle-access-governance

# Run the audit script
python automation/iam_review.py
```

### Script Execution Output
```text
============================================================================
  NORTHSTAR FINANCIAL SERVICES — IAM OPERATIONS & GOVERNANCE AUDIT
  Audit Baseline Reference Date: 2026-09-27
============================================================================

[+] Loaded 20 identities from inventory.
[+] Loaded 4 HR leaver lifecycle events.
[+] Loaded 20 quarterly access certification records.
[+] Loaded 5 privileged access review records.
[+] Loaded 3 access policy exceptions.

----------------------------------------------------------------------------
  IDENTIFIED GOVERNANCE DEFECTS & CONTROL EXCEPTIONS (8 TOTAL)
----------------------------------------------------------------------------
 1. [HIGH]   Terminated User Retaining Active Access
    Target   : Marcus Vance (USR-1014)
    Evidence : Terminated on 2026-08-15, but account status is still Active in directory. Last login: 2026-09-18
    Action   : Immediately disable account and revoke all application entitlements.

 2. [HIGH]   Terminated User Retaining Active Access
    Target   : Liam Gallagher (CTR-2002)
    Evidence : Terminated on 2026-08-31, but account status is still Active in directory. Last login: 2026-09-22
    Action   : Immediately disable account and revoke all application entitlements.

 3. [MEDIUM] Expired Contractor Account Active
    Target   : Liam Gallagher (CTR-2002)
    Evidence : Contract expired 27 days ago (2026-08-31), but account is still Active. Last login: 2026-09-22
    Action   : Disable contractor account and require formal contract extension before re-enabling.

 4. [MEDIUM] Dormant Account (>90 Days Inactive)
    Target   : Sophia Martinez (USR-1011)
    Evidence : Last login was 140 days ago (2026-05-10). Status: Extended Leave
    Action   : Temporarily suspend account pending verification of active employment status.

 5. [MEDIUM] Unowned Service Account
    Target   : svc_legacy_etl_sync (SVC-3002)
    Evidence : Active service account lacks designated ownership (Tech: 'None', Biz: 'None').
    Action   : Identify business application dependency, assign primary/secondary owners, or decommission.

 6. [HIGH]   Excessive Standing Privileged Access
    Target   : adm_radams (USR-1005)
    Evidence : Holds permanent 24/7 standing privilege (ROLE-IT-GLOBALADMIN) without time-bound JIT checkout in PAM vault.
    Action   : Revoke standing administrative assignment; enforce ephemeral 4-hour checkout via PAM vault.

 7. [HIGH]   Segregation of Duties (SoD) Toxic Combination
    Target   : David Chen (USR-1003)
    Evidence : User possesses both payment initiation and payment approval entitlements (ROLE-FIN-INITIATOR, ROLE-FIN-MANAGER).
    Action   : Revoke payment initiator entitlement immediately to restore dual-authorization controls.

 8. [MEDIUM] Expired Access Policy Exception
    Target   : Liam Gallagher (CTR-2002)
    Evidence : Exception EXC-2026-002 (Direct Customer Data Export Tool Access) expired on 2026-09-15 and remains unremediated.
    Action   : Revoke the exceptional access grant or submit formal extension request with CISO approval.

[+] Audit complete. Exported structured findings to: iam_review_results.csv
============================================================================
```

---

## 📊 Mathematically Derived IAM Metrics

Every percentage and metric in this lab is strictly derived from the underlying CSV records:

| Metric Name | Value | Calculation Basis |
| :--- | :---: | :--- |
| **Total Distinct Identities** | **20** | 14 Permanent Employees + 3 Contractors + 3 Service Accounts |
| **Active Identity Accounts** | **16 (80.0%)** | 12 employees, 2 contractors, 2 service accounts active |
| **Disabled Accounts** | **4 (20.0%)** | 2 terminated employees, 1 terminated contractor, 1 decom service account |
| **Terminated Users Retaining Active Access**| **1 (5.0%)** | `USR-1014` (Terminated 2026-08-15; still Active) |
| **Expired Contractors Retaining Access** | **1 (5.0%)** | `CTR-2002` (Contract expired 2026-08-31; still Active) |
| **Dormant Accounts (>90 Days Inactive)** | **1 (5.0%)** | `USR-1011` (140 days since last login; on leave) |
| **Privileged Identities (Subset Attribute)**| **4 (20.0%)** | Cross-cutting attribute: 3 Employees (`USR-1004`, `USR-1005`, `USR-1012`) + 1 Service Account (`SVC-3001`) |
| **Identities with Standing 24/7 Admin** | **1 (5.0%)** | `USR-1005` (Permanent Global Admin) |
| **Unowned Service Accounts** | **1 (5.0%)** | `SVC-3002` (`service_account_owner: None`) |
| **Segregation of Duties Conflicts** | **1 (5.0%)** | `USR-1003` (Holds both Wire Initiator + Approver) |
| **Access Recertification Coverage** | **100.0%** | 20 of 20 entitlements evaluated in Q3 UAR |
| **Immediate Remediation Completion Rate** | **83.3%** | 5 of 6 findings resolved immediately |

---

## 🎯 IAM Skills & Interview Talking Points

This project directly demonstrates real-world competencies required for **IAM Analysts**, **Security Governance Analysts**, and **SecOps Engineers**:

- **Identity Lifecycle Engineering (JML)**: Explaining why HR-to-IT handoffs fail, how deprovisioning lag creates attack surface, and how SCIM connectors automate joiner/leaver workflows.
- **Access Governance & Recertification**: Executing structured quarterly access certifications (User Access Reviews), understanding decision criteria (`APPROVE`, `REVOKE`, `MODIFY`, `ESCALATE`), and tracking remediation evidence for SOX and SOC 2 audits.
- **Privileged Access Management (PAM)**: Explaining the architectural difference between dangerous standing 24/7 admin access and ephemeral, time-bound Just-In-Time (JIT) access with break-glass incident logging.
- **Segregation of Duties (SoD)**: Formulating toxic combination matrices to prevent fraud in financial and change management workflows.
- **Non-Human Identity Governance**: Establishing accountability and secret rotation schedules for orphaned service accounts and daemon scripts.
- **Python Security Automation**: Building standalone, readable audit scripts to continuously detect identity governance anomalies.

---

## 📖 Navigation Guide

1. Read the organizational context in [`scenario/organization.md`](scenario/organization.md) and review the [Role Catalog](scenario/role_catalog.md).
2. Examine the [Lifecycle Events](lifecycle/) to see the raw Joiner, Mover, and Leaver tracking data.
3. Review the [Quarterly Access Review](governance/access_review.csv) and [Privileged Access Review](governance/privileged_access_review.csv).
4. Run the Python audit script in [`automation/iam_review.py`](automation/iam_review.py).
5. Read the complete [Executive Governance Report](report/IAM-Governance-Operations-Report.md).
