# IAM Governance & Identity Lifecycle Operations Audit Report

**Organization**: Northstar Financial Services (Simulated)  
**Assessment Period**: Q3 Baseline Identity Governance Review  
**Assessor**: Francisco Elroy Afonso, Information Security & Access Governance  
**Audit Lead Reviewer**: Alex Wong, Chief Information Security Officer  
**Document Tracking**: `SEC-2026-IAM-RPT-01`  
**Classification**: Internal / Audit-Ready Evidence

---

## 1. Executive Summary

During Q3 2026, Northstar Financial Services conducted an enterprise **Identity and Access Management (IAM) Governance & Lifecycle Operations Audit**. The engagement evaluated the operational health, compliance alignment, and risk posture of Northstar's identity architecture across 20 representative human and non-human identities spanning five critical business applications.

While Northstar maintains baseline directory services and functional departmental silos, the audit revealed significant operational gaps at identity transition points:
- **Joiner-Mover-Leaver (JML) breakdown**: A terminated employee retained active access to financial ledger systems 34 days post-termination and logged in after their departure date.
- **Contractor lifecycle oversight**: An external engineering contractor remained active 27 days after contract expiration, retaining code repository access.
- **Privilege creep during internal transfers**: An employee transferring from Finance to Customer Operations received new operational roles while retaining write access to general ledger systems.
- **Toxic Segregation of Duties (SoD)**: A finance manager held both wire initiation and wire approval entitlements, creating an unmitigated SOX ITGC control failure.
- **Ungoverned service identities**: An active automated batch ledger daemon had no documented technical or business owner, preventing credential rotation or accountability.
- **Excessive standing privilege**: A senior engineer held permanent 24/7 Global Administrator access without time-bounding or Privileged Access Management (PAM) vault checkouts.

Through manual review and automated Python audit scripts (`automation/iam_review.py`), six formal findings were logged, risk-scored, and assigned actionable remediation milestones. Immediate corrective actions (account revocations and toxic role stripping) have been completed, establishing a defensible baseline for upcoming **SOC 2 Type II** and **SOX ITGC** examinations.

---

## 2. Assessment Scope

The audit covered all identity categories and core enterprise applications within Northstar Financial Services:

| Primary Identity Category | Population | Sampled Principals | Target Applications Evaluated |
| :--- | :---: | :---: | :--- |
| **Permanent Full-Time Employees** | 14 | `USR-1001` through `USR-1014` | `APP-FIN`, `APP-HR`, `APP-DEV`, `APP-OPS`, `APP-IDP` |
| **External Contractors** | 3 | `CTR-2001` through `CTR-2003` | `APP-DEV`, `APP-HR` |
| **Non-Human / Service Accounts** | 3 | `SVC-3001` through `SVC-3003` | `APP-FIN`, `APP-OPS`, Infrastructure Storage |
| **Total Distinct Identities** | **20** | **100% of Sampled Estate** | **5 Core Enterprise Systems** |
| *Privileged Identities (Subset)* | *4* | *`USR-1004`, `USR-1005`, `USR-1012`, `SVC-3001`* | *Authorization attribute (3 employees + 1 service account)* |

---

## 3. IAM Operating Model & ITSM Alignment

Northstar's identity operations follow an **ITSM-aligned operating model** mapped across ITIL 4 service disciplines:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                         ITSM-Aligned IAM Operating Model                               │
│                                                                                        │
│   Request Management      Change Enablement       Incident Management                  │
│   ┌────────────────────┐  ┌────────────────────┐  ┌────────────────────────────────┐   │
│   │ Role-based access  │  │ Emergency access   │  │ Account compromise lockouts,   │   │
│   │ requests via ITSM  │  │ approvals & policy │  │ unauthorized logon triage via  │   │
│   │ with dual sign-off │  │ updates (CAB/Sec)  │  │ SIEM alert integration         │   │
│   └────────────────────┘  └────────────────────┘  └────────────────────────────────┘   │
│             │                       │                             │                    │
│             └───────────────────────┼─────────────────────────────┘                    │
│                                     ▼                                                  │
│                        [Centralized Identity Hub]                                      │
│                                     │                                                  │
│             ┌───────────────────────┴─────────────────────────────┐                    │
│             ▼                                                     ▼                    │
│   Problem Management                              Knowledge Management                 │
│   ┌────────────────────────────────┐              ┌────────────────────────────────┐   │
│   │ Root-cause analysis on stale   │              │ Standardized role definitions, │   │
│   │ accounts & deprovision lag     │              │ access matrices, and SOPs      │   │
│   └────────────────────────────────┘              └────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

* **Request Management**: Standardized catalog requests with documented managerial and application owner approvals.
* **Change Enablement**: Pre-scheduled maintenance windows for infrastructure role mapping changes, with security review for privileged permission sets.
* **Incident Management**: Security Operations handles unauthorized authentication alerts (`EVT-2026-8014`) and enforces immediate credential revocation.
* **Problem Management**: Identifies recurring JML bottlenecks between HR status changes and Service Desk deprovisioning tickets.
* **Knowledge Management**: Maintains the authoritative Enterprise Role Catalog (`scenario/role_catalog.md`) and Approval Matrix.

---

## 4. Identity Lifecycle Management (JML Review)

### 4.1. Joiner Lifecycle
The Joiner process functions reliably for standard full-time employees. HR generates onboarding requests (`JRN-2026-001`), establishing baseline roles (`ROLE-DEV-ENGINEER`) linked to departmental manager approvals. No unauthorized access was discovered on newly onboarded full-time staff.

### 4.2. Mover Lifecycle (Privilege Creep)
The internal transfer process demonstrated an **additive-only flaw**. When Elena Rostova (`USR-1008`) moved from Finance to Customer Operations on 2026-07-01:
- Service Desk fulfilled request `REQ-2026-1004`, granting `ROLE-OPS-SPECIALIST` on `APP-OPS`.
- Service Desk failed to dispatch or execute a deprovisioning ticket for `ROLE-FIN-ANALYST` on `APP-FIN`.
- **Result**: The user accumulated dual-department entitlements for nearly three months until flagged during the Q3 access certification (`REV-2026-010`).

### 4.3. Leaver Lifecycle (Deprovisioning Lag)
The Leaver process exhibited significant control variance:
- **Clean Baseline**: Robert Hayes (`USR-1013`) and contractor Chloe Bennett (`CTR-2003`) had their accounts disabled on the exact date of termination, fulfilling SLA requirements.
- **Control Breakdown (Employees)**: Marcus Vance (`USR-1014`) separated on 2026-08-15. HR closed the offboarding ticket without verifying IT fulfillment. His account remained Active in directory services, and event logs show he logged into `APP-FIN` on 2026-09-18 (`EVT-2026-8008`).
- **Control Breakdown (Contractors)**: Liam Gallagher (`CTR-2002`) had an employment contract that expired on 2026-08-31. No automated trigger notified IT, leaving the account active. The contractor accessed repository systems on 2026-09-22 (`EVT-2026-8012`).

---

## 5. Access Request & Approval Workflow Analysis

An audit of simulated access requests (`access-management/access_requests.csv`) confirmed that standard low-risk requests follow appropriate managerial review. However, two critical governance weaknesses were identified:

1. **Self-Requested Conflicting Access**: David Chen (`USR-1003`) requested wire initiation rights (`REQ-2026-1002`) for himself to provide "urgent backup coverage." The Finance Director approved the request without evaluating existing role assignments, directly introducing a toxic SoD combination.
2. **Positive Control Gate Execution**: Request `REQ-2026-1005` (Contractor requesting sensitive financial ledger access) was correctly rejected by the Finance Director due to lack of business justification. Similarly, `REQ-2026-1006` (Request for permanent standing Global Admin) was placed on hold for security review, demonstrating that supervisory controls function when escalations occur.

---

## 6. Access Recertification (User Access Review)

The Q3 User Access Review evaluated 20 discrete access entitlements across the organization (`governance/access_review.csv`):

```text
┌────────────────────────────────────────────────────────────────────────┐
│                  Q3 2026 Access Review Decision Breakdown              │
│                                                                        │
│   Decision Category    Count    Percentage    Governance Implication   │
│   ─────────────────    ─────    ──────────    ──────────────────────   │
│   APPROVE               13        65.0%       Legitimate business need │
│   REVOKE                 3        15.0%       Terminated / Mover / Exp │
│   MODIFY                 2        10.0%       SoD conflict & Dormant   │
│   ESCALATE               2        10.0%       Unowned SVC & Standing   │
│   ─────────────────    ─────    ──────────    ──────────────────────   │
│   Total Evaluated       20       100.0%       Full Audit Coverage      │
└────────────────────────────────────────────────────────────────────────┘
```

* **Revocations (3)**: 
  - `REV-2026-010`: Revoked legacy finance access for moved employee Elena Rostova.
  - `REV-2026-016`: Revoked all access for terminated employee Marcus Vance.
  - `REV-2026-018`: Revoked repository access for expired contractor Liam Gallagher.
* **Modifications (2)**:
  - `REV-2026-004`: Stripped wire initiation entitlement from David Chen to resolve SoD.
  - `REV-2026-013`: Suspended dormant account for Sophia Martinez (extended leave).
* **Escalations (2)**:
  - `REV-2026-006`: Escalated Rachel Adams' standing Global Admin to CISO for PAM migration.
  - `REV-2026-020`: Escalated unowned service account `svc_legacy_etl_sync` to application owner.

---

## 7. Privileged Access Management (PAM) Review

The privileged access assessment (`governance/privileged_access_review.csv`) reviewed four standing privileged accounts and one emergency break-glass event:

### Standing Administrative Access
- `USR-1004` (Tom Bradley, `ROLE-IT-ADMIN`) holds standing provisioning access to `APP-IDP`. MFA is enforced, but separation between daily email account and `adm_tbradley` is currently manual.
- `USR-1005` (Rachel Adams, `ROLE-IT-GLOBALADMIN`) holds **permanent, 24/7 standing Domain/Global Administrator rights**. This creates a catastrophic blast radius if her endpoint is compromised.

### Emergency / Break-Glass Event Analysis
- **Incident Reference**: `INC-4491` (Production payment gateway deadlock, 2026-09-12).
- **Workflow**: James Wilson (`USR-1006`) requested temporary elevated staging database access.
- **Controls Executed**: Approved by CISO Alex Wong; checked out via PAM vault for a 4-hour window (`EVT-2026-8005`); automatically expired and revoked by system daemon at 06:15 UTC (`EVT-2026-8006`).
- **Post-Incident Review**: Session logs reviewed by SecOps; queries verified limited to deadlocked thread termination. No unauthorized alterations occurred. This serves as a model for time-bound access.

---

## 8. Segregation of Duties (SoD) Analysis

The audit confirmed one active critical toxic combination and one cross-departmental mover conflict:

1. **David Chen (`USR-1003`)**: Possessed both `ROLE-FIN-INITIATOR` (batch wire creation) and `ROLE-FIN-APPROVER` (batch wire release) within `APP-FIN`. While treasury log analysis confirmed David Chen did not execute dual transactions, the technical capability existed, representing a severe SOX ITGC control failure.
2. **Elena Rostova (`USR-1008`)**: Possessed `ROLE-OPS-SPECIALIST` (loan case processing) and `ROLE-FIN-ANALYST` (general ledger adjustments). The ability to alter customer account balances while handling customer service disputes violates organizational internal controls.

---

## 9. Non-Human Identity Governance (Service Accounts)

Evaluation of service accounts (`scenario/identity_inventory.csv`) identified substantial governance disparities:

* **Well-Governed Benchmark**: `SVC-3001` (`svc_backup_automation`) has an assigned technical owner (`Rachel Adams`), an assigned business owner, automated 90-day credential rotation, and restricted storage snapshot scope.
* **Orphaned / Unowned Risk**: `SVC-3002` (`svc_legacy_etl_sync`) operates with `service_account_owner: None` and `business_owner: None`. It ran automated batch jobs as recently as 2026-09-14 (`EVT-2026-8007`). No team claims responsibility for its credential rotation or runtime integrity.
* **Decommissioning Check**: `SVC-3003` (`svc_decom_reporting`) was properly disabled on 2026-03-31 following deprecation of the legacy reporting pipeline.

---

## 10. IAM Monitoring & Threat Detection

Analysis of operational logs (`monitoring/iam_events.csv`) confirmed that while routine events log properly, automated alerting was insufficient:

* **Control Failure**: Marcus Vance (`USR-1014`) logged into `APP-FIN` on 2026-09-18 from external IP `198.51.100.42` (`EVT-2026-8008`). The event generated a log entry but did not trigger an automated security alert because HR termination status had not synchronized to SIEM identity watchlists.
* **Privileged Brute Force**: Event `EVT-2026-8015` recorded multiple failed console authentications against privileged account `adm_radams` on 2026-09-25. While MFA prevented unauthorized entry, the account was not temporarily locked out.

---

## 11. Security Findings & Risk Register

```text
┌────────────────────────────────────────────────────────────────────────┐
│                       Audit Findings Scorecard                         │
│                                                                        │
│   Finding ID   Title                                      Severity     │
│   ──────────   ────────────────────────────────────────   ────────     │
│   IAM-01       Terminated User Retaining Active Access    HIGH         │
│   IAM-02       Access Not Removed Following Role Change   MEDIUM       │
│   IAM-03       Segregation-of-Duties Conflict             HIGH         │
│   IAM-04       Unowned / Poorly Governed Service Account  MEDIUM       │
│   IAM-05       Excessive Standing Privileged Access       HIGH         │
│   IAM-06       Expired Contractor Account Remaining Active MEDIUM      │
└────────────────────────────────────────────────────────────────────────┘
```

### Finding Details

#### IAM-01: Terminated User Retaining Active Access
* **Severity**: **HIGH** (CVSS: 8.5)
* **Affected Identity**: Marcus Vance (`USR-1014`, former Financial Analyst)
* **Description**: Employee was terminated on 2026-08-15. HR closed the offboarding ticket (`HR-OFF-914`), but IT deprovisioning was never completed. User retained active directory and `APP-FIN` access, logging in on 2026-09-18.
* **Evidence**: `scenario/identity_inventory.csv` (account active), `lifecycle/leaver_events.csv` (`Pending_Failed`), `monitoring/iam_events.csv` (`EVT-2026-8008`).
* **Risk**: Former employee retains access to sensitive financial ledger data; potential for corporate espionage or unapproved transaction entries.
* **Remediation**: Immediately disabled account and revoked all application sessions. Implement automated webhook between HRIS offboarding and directory deprovisioning.
* **Owner**: IT Service Desk Lead (`Tom Bradley`)
* **Target Date**: Completed (Immediate) / Automated integration by Day 30.
* **Status**: **Remediated (Account Disabled)**

#### IAM-02: Access Not Removed Following Role Change
* **Severity**: **MEDIUM** (CVSS: 6.8)
* **Affected Identity**: Elena Rostova (`USR-1008`, Operations Specialist)
* **Description**: User transferred from Finance to Customer Operations on 2026-07-01. Customer Operations access was granted, but Finance ledger write access was not revoked.
* **Evidence**: `lifecycle/mover_events.csv` (`MVR-2026-001`), `governance/access_review.csv` (`REV-2026-010`).
* **Risk**: Cross-departmental privilege accumulation; violation of the principle of least privilege.
* **Remediation**: Revoked `ROLE-FIN-ANALYST` access in `APP-FIN`. Update ITSM Mover workflows to require dual confirmation of legacy access removal before ticket closure.
* **Owner**: IT Service Desk Lead (`Tom Bradley`)
* **Target Date**: Completed (Access Revoked) / Workflow lock by Day 30.
* **Status**: **Remediated**

#### IAM-03: Segregation-of-Duties Conflict
* **Severity**: **HIGH** (CVSS: 8.1)
* **Affected Identity**: David Chen (`USR-1003`, Finance Operations Manager)
* **Description**: User possessed both `ROLE-FIN-INITIATOR` (create wire batches) and `ROLE-FIN-APPROVER` (release wire batches) in `APP-FIN`.
* **Evidence**: `access-management/access_requests.csv` (`REQ-2026-1002`), `governance/segregation_of_duties.md`.
* **Risk**: Unilateral financial disbursement capability bypassing dual-authorization controls; major SOX ITGC control deficiency.
* **Remediation**: Stripped `ROLE-FIN-INITIATOR` from user profile (`REV-2026-004`). Treasury confirmed zero unauthorized dual-transactions occurred. Configured automated SoD conflict rules in request management.
* **Owner**: Finance Director (`Elena Vasquez`) & SecOps
* **Target Date**: Completed (Role Stripped) / Ticketing validation rule by Day 15.
* **Status**: **Remediated**

#### IAM-04: Unowned / Poorly Governed Service Account
* **Severity**: **MEDIUM** (CVSS: 6.2)
* **Affected Identity**: `SVC-3002` (`svc_legacy_etl_sync`)
* **Description**: Active service account running automated ledger batch synchronizations lacks a documented technical or business owner.
* **Evidence**: `scenario/identity_inventory.csv` (`service_account_owner: None`), `monitoring/iam_events.csv` (`EVT-2026-8007`).
* **Risk**: Programmatic credentials cannot be rotated safely; impossible to determine if account is compromised or abandoned.
* **Remediation**: Assigned primary technical ownership to Cloud Infrastructure Lead Rachel Adams and business ownership to Finance Operations. Enrolled account in 90-day secret rotation schedule.
* **Owner**: Cloud Infrastructure Lead (`Rachel Adams`)
* **Target Date**: Day 30.
* **Status**: **In Progress (Owner Assigned, Rotation Scheduled)**

#### IAM-05: Excessive Standing Privileged Access
* **Severity**: **HIGH** (CVSS: 7.8)
* **Affected Identity**: Rachel Adams (`USR-1005`, Lead Systems Engineer)
* **Description**: User holds permanent, 24/7 standing Global Administrator privileges (`ROLE-IT-GLOBALADMIN`) in directory services.
* **Evidence**: `scenario/identity_inventory.csv`, `governance/privileged_access_review.csv` (`PAM-REV-002`).
* **Risk**: Credential theft or session hijacking on engineer's workstation grants full enterprise takeover.
* **Remediation**: Remove standing Global Admin assignment. Migrate privileged activities to Just-In-Time (JIT) checkout via the PAM vault with a 4-hour hard expiry and mandatory ticket linkage.
* **Owner**: CISO (`Alex Wong`) & SecOps
* **Target Date**: Day 60.
* **Status**: **In Progress (Policy Drafted, PAM Vault Integration Underway)**

#### IAM-06: Expired Contractor Account Remaining Active
* **Severity**: **MEDIUM** (CVSS: 6.5)
* **Affected Identity**: Liam Gallagher (`CTR-2002`, Data Integration Contractor)
* **Description**: Contractor contract expired on 2026-08-31. Account remained active and was used to authenticate to code repositories on 2026-09-22.
* **Evidence**: `scenario/identity_inventory.csv`, `lifecycle/leaver_events.csv` (`LVR-2026-003`), `monitoring/iam_events.csv` (`EVT-2026-8012`).
* **Risk**: Unauthorized access by non-employees without active non-disclosure or service contracts.
* **Remediation**: Disabled contractor account and revoked all repository tokens (`REV-2026-018`). Configured automated expiration dates in directory services matching contract end dates.
* **Owner**: Engineering Director (`Maya Lin`) & IT Service Desk
* **Target Date**: Completed (Account Disabled) / Automated directory expiration by Day 30.
* **Status**: **Remediated**

---

## 12. Phased Remediation Plan

```text
Phase 1: Immediate Containment (Days 1–5) — [COMPLETED]
├── Disable USR-1014 (Marcus Vance) in directory and all applications
├── Disable CTR-2002 (Liam Gallagher) and revoke code repo keys
├── Strip ROLE-FIN-INITIATOR from USR-1003 (David Chen)
├── Revoke legacy APP-FIN access from USR-1008 (Elena Rostova)
└── Suspend dormant account USR-1011 (Sophia Martinez) pending return to work

Phase 2: Operational Process & Tooling Hardening (Days 6–30)
├── Implement automated HRIS-to-Directory SCIM provisioning/deprovisioning connector
├── Configure mandatory contract end dates in directory accounts for all contractors
├── Assign formal technical and business owners to all service accounts
└── Deploy ticketing pre-validation rules to block incompatible SoD role requests

Phase 3: Privileged Access & PAM Vaulting (Days 31–60)
├── Remove standing 24/7 Global Admin roles from all human engineers
├── Enforce time-bound JIT checkout (max 4-hour window) via PAM vault for administrative tasks
└── Implement hardware MFA (FIDO2) requirement for all privileged console access

Phase 4: Continuous Governance & Automated Audit (Days 61–90)
├── Schedule weekly automated runs of automation/iam_review.py via CI/CD runner
├── Export findings directly to Security Operations Slack channel and SIEM
└── Institutionalize quarterly manager access certifications across all business applications
```

---

## 13. Mathematically Derived IAM Operational Metrics

All metrics below are calculated directly from the simulated identity population and review records:

| Metric Identifier | Value | Derivation Formula / Source |
| :--- | :---: | :--- |
| **Total Identity Population** | **20** | Total records in `identity_inventory.csv` |
| **Active Identity Accounts** | **16 (80.0%)** | Accounts with `account_status == 'Active'` (12 employees, 2 contractors, 2 service accounts) |
| **Disabled / Decommissioned Accounts** | **4 (20.0%)** | Accounts with `account_status == 'Disabled'` (`USR-1013`, `CTR-2003`, `SVC-3003`, etc.) |
| **Terminated Users Retaining Access** | **1 (5.0%)** | `USR-1014` (Terminated 2026-08-15; still marked Active) |
| **Expired Contractors Retaining Access**| **1 (5.0%)** | `CTR-2002` (Contract expired 2026-08-31; still marked Active) |
| **Dormant Accounts (>90 Days Inactive)**| **1 (5.0%)** | `USR-1011` (Last login: 2026-05-10; 140 days inactive) |
| **Privileged Identities** | **4 (20.0%)** | Identities with `privileged == True` (`USR-1004`, `USR-1005`, `USR-1012`, `SVC-3001`) |
| **Standing Global Admin Accounts** | **1 (5.0%)** | `USR-1005` (Permanent 24/7 administrative assignment) |
| **Unowned Service Accounts** | **1 (5.0%)** | `SVC-3002` (`service_account_owner: None`) |
| **SoD Incompatible Assignments** | **1 (5.0%)** | `USR-1003` (Wire Initiator + Wire Approver) |
| **Mover Privilege Creep Instances** | **1 (5.0%)** | `USR-1008` (Retained legacy finance role post-transfer) |
| **Open Access Exceptions** | **3** | Records in `exceptions_register.csv` (2 Active, 1 Expired) |
| **Expired Policy Exceptions** | **1 (33.3%)** | `EXC-2026-002` (Expired on 2026-09-15) |
| **Access Certification Coverage** | **100.0%** | 20 of 20 entitlements formally reviewed in Q3 UAR |
| **Immediate Remediation Completion Rate**| **83.3%** | 5 of 6 findings addressed with immediate operational mitigations |

> **Automation Detection Reconciliation Note**: The automated audit script (`automation/iam_review.py`) executes **7 discrete control rules**, generating **8 finding instances** across **6 unique affected identities**. The difference between 7 rules and 8 output instances arises because contractor Liam Gallagher (`CTR-2002`) triggered three separate control checks: unfulfilled leaver ticket (Rule 1), expired contract end date (Rule 2), and an unrevoked expired policy exception (Rule 7).

---

## 14. Audit Evidence Retention Package

To support external SOC 2 Type II and SOX ITGC auditors, the following simulated artifacts are packaged and archived:

1. **Access Request & Approval Records**: Stored in `access-management/access_requests.csv` containing timestamps, business justifications, and approving managers.
2. **Provisioning & Fulfillment Logs**: Mapped in `access-management/provisioning_matrix.csv` cross-referenced with `monitoring/iam_events.csv`.
3. **Formal Access Certification Sheets**: Stored in `governance/access_review.csv` with explicit reviewer sign-offs and decisions.
4. **Privileged Access Session Logs**: Stored in `governance/privileged_access_review.csv` documenting the 4-hour break-glass checkout for `INC-4491`.
5. **Remediation Verification Output**: Generated via `automation/iam_review.py` and exported to `automation/iam_review_results.csv`.

---

## 15. Zero Trust Architecture (ZTA) Alignment

While Northstar currently operates a perimeter-assisted model, the governance remediation aligns directly with **NIST SP 800-207 Zero Trust Architecture** tenets:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Zero Trust Tenets Alignment                     │
│                                                                        │
│   Tenet 1: Verify Explicitly                                           │
│   • Always authenticate and authorize based on all available data     │
│     points (user identity, device posture, location, resource).        │
│   • Action: Mandate hardware MFA for all administrative access.        │
│                                                                        │
│   Tenet 2: Use Least-Privilege Access                                  │
│   • Limit user access with Just-In-Time and Just-Enough-Access (JIT/JEA).│
│   • Action: Eliminate standing admin roles; migrate to PAM checkout.   │
│                                                                        │
│   Tenet 3: Assume Breach                                               │
│   • Minimize blast radius and segment access.                          │
│   • Action: Isolate application permissions using granular RBAC;       │
│     continuously audit for dormant accounts and unauthorized access.   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 16. Cloud Identity Mapping (Conceptual Architecture)

The simulated operating model translates directly to major enterprise cloud identity platforms:

* **Microsoft Entra ID (Azure AD)**:
  - Role catalog maps to **Entra ID Security Groups** and **Administrative Units**.
  - PAM workflows map to **Microsoft Entra Privileged Identity Management (PIM)** for time-bound role activation.
  - Quarterly recertifications map to **Entra Access Reviews**.
  - Dynamic user disablement maps to **Entra ID Lifecycle Workflows**.
* **AWS IAM & Identity Center (SSO)**:
  - Role catalog maps to **Permission Sets** assigned to AWS Organizations accounts.
  - Break-glass access maps to **Temporary Elevated Access (TEA)** or temporary assume-role policies with session duration limits.
  - Inactive account checks map to **IAM Credential Reports** and **AWS IAM Access Analyzer**.
* **SailPoint / Governance Platforms**:
  - Identity inventory maps to authoritative identity profiles.
  - JML events map to **Lifecycle States** (`prehire`, `active`, `leave`, `terminated`).
  - SoD matrices map to **IdentityIQ / IdentityNow Separation of Duties Policies**.

---

## 17. Conclusion & Governance Sign-Off

The Q3 IAM Governance Operations Audit successfully identified and neutralized critical access vulnerabilities across Northstar Financial Services. By combining structured operational processes, automated Python governance evaluation, and strict segregation of duties, Northstar has established a defensible, auditable identity operating model.

Continued execution of the 90-day remediation roadmap will ensure complete readiness for upcoming SOC 2 Type II examinations and protect corporate assets from unauthorized access.

---

**Report Prepared By**:  
`Francisco Elroy Afonso`  
Information Security & Access Governance Analyst  

**Report Reviewed & Approved By**:  
`Alex Wong`  
Chief Information Security Officer (CISO), Northstar Financial Services  
Date: September 27, 2026
