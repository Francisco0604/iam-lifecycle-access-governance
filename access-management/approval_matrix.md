# Access Approval & Governance Matrix

**Project**: Northstar Financial Services IAM Governance  
**Policy Reference**: `POL-IAM-003` (Access Request, Authorization & Segregation of Duties)  
**ITSM Alignment**: ITIL 4 Service Request Management & Change Enablement

This document defines the formal approval authority matrix governing access requests across Northstar Financial Services. It enforces segregation between **Requester**, **Approver**, and **Fulfiller** to ensure that no individual can grant themselves access to corporate data or infrastructure.

---

## 1. Approval Authority Matrix

| Access Category | Target System / Role | Primary Approver | Secondary / Security Approver | Mandatory Pre-Fulfillment Checks |
| :--- | :--- | :--- | :--- | :--- |
| **Standard Business Access** | `APP-OPS`, `APP-HR` standard user roles | Target User's Direct Manager | Application Business Owner | Verify active employment status |
| **Financial Ledger Access** | `APP-FIN` (`ROLE-FIN-ANALYST`, `ROLE-FIN-MANAGER`) | Direct Manager (Finance) | Finance Director (`Elena Vasquez`) | SoD conflict check against disbursement roles |
| **Sensitive Financial Execution** | `APP-FIN` Wire / Payment Initiation (`ROLE-FIN-INITIATOR`) | Finance Director | CISO / SecOps | **Hard SoD Block**: Automatic rejection if user holds `ROLE-FIN-APPROVER` |
| **Sensitive Financial Approval** | `APP-FIN` Wire / Payment Release (`ROLE-FIN-APPROVER`) | Finance Director | CISO / SecOps | **Hard SoD Block**: Automatic rejection if user holds `ROLE-FIN-INITIATOR` |
| **Developer Repositories** | `APP-DEV` (`ROLE-DEV-ENGINEER`) | Engineering Director (`Maya Lin`) | N/A (Standard) | Branch permission scoping; no production deploy rights |
| **Privileged IT Administration** | `APP-IDP` (`ROLE-IT-ADMIN`) | IT Support Lead | SecOps Lead (`Francisco Afonso`) | Background check verification; dedicated admin account (`adm_*`) |
| **Global / Domain Admin** | `APP-IDP` (`ROLE-IT-GLOBALADMIN`) | IT Lead (`Rachel Adams`) | **CISO Approval Required** | Standing access prohibited; PAM checkout & MFA required |
| **Emergency / Break-Glass** | All Production Platforms | Incident Commander | **CISO Verbal + Digital Sign-off** | 4-hour hard ceiling; automated session recording enabled |
| **Third-Party Contractor** | All Permitted Applications | Northstar Sponsor Manager | Information Security | Contract end-date verification; max 6-month validity |

---

## 2. Segregation of Operational Duties (Requester vs Approver vs Fulfiller)

To prevent self-authorization and collusion:

```text
┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
│     1. REQUEST        │       │     2. APPROVAL       │       │    3. FULFILLMENT     │
│                       │       │                       │       │                       │
│ • End User or Manager │──────▶│ • Business Owner      │──────▶│ • IT Service Desk or  │
│ • Documents business  │       │ • Security Review     │       │   Automated SCIM      │
│   justification       │       │ • SoD verification   │       │ • Zero approval power │
└───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

1. **Self-Approval Prohibition**: No user may approve their own access request under any circumstance. Requests submitted by managers for themselves must escalate to the next management level.
2. **Fulfillment Isolation**: IT Service Desk technicians (`ROLE-IT-ADMIN`) possess the technical capability to provision accounts but are procedurally and auditorily prohibited from fulfilling any request that lacks documented, cryptographic/ITSM manager and owner approvals.
3. **Escalation Rules**: If an access request involves crossing departmental boundaries (e.g. an operations employee requesting financial ledger access), both the current department head and the target department head must provide documented sign-off.
