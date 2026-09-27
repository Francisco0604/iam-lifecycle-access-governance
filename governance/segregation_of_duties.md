# Segregation of Duties (SoD) & Toxic Combination Analysis

**Project**: Northstar Financial Services IAM Governance  
**Governance Scope**: Financial Controls (SOX ITGC), Fraud Prevention, and Identity Integrity  
**Review Period**: Q3 Baseline Review

Segregation of Duties (SoD) ensures that no single individual possesses end-to-end authorization to execute, approve, and verify sensitive business or technical transactions without independent checks and balances.

---

## 1. Enterprise Incompatible Roles Matrix

The following role combinations represent **inherent toxic combinations** across Northstar's operational environment:

```text
┌───────────────────────────┬───────────────────────────┬────────────────────────────────────────────────────────┐
│ Role A (Initiation/Action)│ Role B (Approval/Audit)   │ Incompatibility Rationale & Risk                       │
├───────────────────────────┼───────────────────────────┼────────────────────────────────────────────────────────┤
│ ROLE-FIN-INITIATOR        │ ROLE-FIN-APPROVER         │ Fraud Risk: Single user creates and releases corporate │
│ (Create Wire / Batch)     │ (Authorize Disbursement)  │ wire transfers without secondary authorization.        │
├───────────────────────────┼───────────────────────────┼────────────────────────────────────────────────────────┤
│ ROLE-IT-ADMIN             │ Business Access Approver  │ Governance Risk: Service Desk tech approves their own  │
│ (User Provisioner)        │ (Department Head)         │ access requests or fulfills unapproved entitlements.   │
├───────────────────────────┼───────────────────────────┼────────────────────────────────────────────────────────┤
│ ROLE-DEV-ENGINEER         │ ROLE-IT-GLOBALADMIN       │ Change Risk: Developer deploys untested code directly  │
│ (Application Code Author) │ (Directory Administrator) │ to production or modifies security baseline policies.  │
├───────────────────────────┼───────────────────────────┼────────────────────────────────────────────────────────┤
│ ROLE-OPS-SPECIALIST       │ ROLE-FIN-ANALYST          │ Business Risk: Customer loan processor can modify loan │
│ (Loan / Case Handler)     │ (Financial Ledger Writer) │ ledger records and alter customer balance histories.   │
└───────────────────────────┴───────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 2. Identified Toxic Combinations & Remediation Actions

### 2.1. Toxic Combination 1: Financial Disbursement Self-Approval
* **Affected Principal**: `USR-1003` (David Chen, Finance Operations Manager)
* **Target System**: `APP-FIN` (Northstar Financial Ledger)
* **Conflicting Entitlements**:
  - `ROLE-FIN-INITIATOR` (Granted via `REQ-2026-1002` on 2026-07-11 for "urgent backup coverage")
  - `ROLE-FIN-APPROVER` (Held as primary duty under `ROLE-FIN-MANAGER`)
* **Technical Risk & Impact**:
  David Chen has the technical capability to enter a wire transaction into the payment queue and subsequently log in as manager to approve and release the funds to an external bank account. This completely circumvents the two-person rule mandated by SOX ITGC and corporate treasury policies.
* **Root Cause**:
  The access request was approved by the Finance Director during an emergency staffing shortage under the assumption that "he is a trusted manager." The ticketing system lacked an automated SoD blocking rule.
* **Remediation Action**:
  - **Immediate**: Revoke `ROLE-FIN-INITIATOR` from `USR-1003` immediately (`REV-2026-004`).
  - **Audit**: Pull transaction history for the past 90 days to verify whether `USR-1003` both initiated and approved any single wire transaction (Treasury audit confirmed zero dual-transactions occurred).
  - **Preventive**: Implement a hard pre-provisioning SoD validation rule in the ticketing system that halts any request combining these two role IDs.

---

### 2.2. Toxic Combination 2: Cross-Departmental Mover Privilege Creep
* **Affected Principal**: `USR-1008` (Elena Rostova, Operations Specialist)
* **Target Systems**: `APP-OPS` (ClientPulse CRM) and `APP-FIN` (Northstar Financial Ledger)
* **Conflicting Entitlements**:
  - `ROLE-OPS-SPECIALIST` (Assigned 2026-07-02 for customer case handling)
  - `ROLE-FIN-ANALYST` (Retained from previous role in Finance)
* **Technical Risk & Impact**:
  A customer operations specialist can adjust loan status notes in `APP-OPS` while retaining read/write ledger privileges in `APP-FIN` to alter debit/credit journal entries. This introduces risk of fraudulent debt reconciliation or improper credit adjustments.
* **Root Cause**:
  Northstar's mover process is "additive only." The Service Desk fulfilled the onboarding ticket for Operations but had no automated trigger to deprovision legacy department roles.
* **Remediation Action**:
  - **Immediate**: Revoke `ROLE-FIN-ANALYST` access in `APP-FIN` (`REV-2026-010`).
  - **Preventive**: Update Mover workflows in ITSM so that new department role provisioning requires a signed closure receipt confirming legacy entitlement revocation.

---

### 2.3. Toxic Combination 3: IT Support Requesting Unconstrained Global Admin
* **Affected Principal**: `USR-1004` (Tom Bradley, IT Support Supervisor)
* **Target System**: `APP-IDP` (Northstar Identity Hub)
* **Potential Conflict**:
  Request `REQ-2026-1006` requested assigning permanent `ROLE-IT-GLOBALADMIN` to an IT technician who routinely fulfills day-to-day user tickets.
* **Technical Risk & Impact**:
  An IT technician with standing Global Admin access can create backdoor user accounts, assign them enterprise administrative privileges, and delete identity event logs without detection.
* **Remediation Action**:
  - **Action**: Request flagged as `Pending_Security_Review` and rejected by CISO.
  - **Alternative**: Implemented a Privileged Access Management (PAM) vault policy. If Tom Bradley requires elevated permissions for weekend infrastructure maintenance, he must request a time-bound, 4-hour checked-out session requiring manager sign-off.
