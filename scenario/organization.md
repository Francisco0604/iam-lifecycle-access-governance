# Organization Scenario: Northstar Financial Services

**Project**: IAM Lifecycle & Access Governance Operations Lab  
**Organization Type**: Mid-Sized Financial Services Firm (Simulated)  
**Operating Model**: Centralized Identity & Access Governance with ITSM Integration  
**Scope**: Enterprise Identity Estate (Employees, Contractors, Privileged Accounts, Service Identities)

---

## 1. Enterprise Profile & Context

**Northstar Financial Services ("Northstar")** is a simulated mid-sized wealth advisory and loan servicing firm with approximately 350 staff members. The firm operates in a regulated financial environment subject to periodic external audits, including **SOC 2 Type II**, **SOX IT General Controls (ITGC)**, and **GLBA Safeguards Rule** requirements.

The firm's technical infrastructure blends internal business applications, developer platforms, and cloud-hosted administrative tools. Over the last two years, Northstar expanded its technology footprint, leading to manual handoffs between HR, hiring managers, and the IT Service Desk. As a result, identity governance gaps began to emerge:
- Access deprovisioning delays following employee departures.
- Role changes resulting in "privilege creep" (users accumulating access across departments).
- Contractor accounts persisting past contractual end dates.
- Service accounts created ad-hoc for automation projects without formal ownership or credential lifecycle management.

This project models Northstar's identity architecture, operational workflows, governance reviews, and automated anomaly detection to establish an auditable, compliant IAM operating model.

---

## 2. Core Business Applications in Scope

The identity governance framework manages access across five primary enterprise applications:

| Application ID | Application Name | Business Purpose | Criticality | Data Sensitivity |
| :--- | :--- | :--- | :---: | :--- |
| **`APP-FIN`** | Northstar Financial Ledger | General ledger, journal entries, wire approvals, and financial reporting | **High (SOX In-Scope)** | Confidential / Financial Records |
| **`APP-HR`** | PeopleCore HRIS | Employee personnel records, payroll details, onboarding/offboarding workflows | **High** | Restricted / Employee PII |
| **`APP-DEV`** | DevCloud Engineering Suite | Source code repositories, CI/CD deployment pipelines, build artifacts | **Medium** | Internal / Intellectual Property |
| **`APP-OPS`** | ClientPulse Operations CRM | Customer loan applications, account status, communication history | **Medium** | Confidential / Customer PII |
| **`APP-IDP`** | Northstar Identity Hub | Directory services, single sign-on (SSO), user provisioning, and role assignment | **Critical** | Core Infrastructure / Administrative |

---

## 3. Organizational Structure & Stakeholders

The simulated environment covers the following departments and key operational stakeholders:

```text
Northstar Financial Services — Governance Structure
│
├── Executive & Risk
│   ├── Chief Information Security Officer (CISO) — Approves policy exceptions & break-glass access
│   └── Internal Audit Lead — Reviews periodic access certifications & SoD matrices
│
├── Business Units
│   ├── Finance (Director: Elena Vasquez) — Financial accounting, reconciliation, disbursements
│   ├── Customer Operations (Manager: Marcus Reid) — Client support, loan processing
│   └── Human Resources (Lead: Karen Patel) — Authoritative source for Joiner-Mover-Leaver events
│
└── Technology & Security
    ├── IT Service Desk (Supervisor: Tom Bradley) — Manual and automated fulfillment
    ├── Cloud Infrastructure (Lead: Rachel Adams) — System engineering, service accounts
    └── Security Operations (Lead: Francisco Afonso) — IAM monitoring, access reviews, PAM governance
```

---

## 4. Identity Classifications & Population Breakdown

Northstar structures its identity population across **three primary identity categories** totaling **20 distinct identities**:

1. **Permanent Full-Time Employees (14 Identities: `USR-1001` to `USR-1014`)**: Permanent staff requiring role-based access to core business applications (e.g., HR Analyst, Finance Analyst, Customer Operations Specialist).
2. **Third-Party Contractors (3 Identities: `CTR-2001` to `CTR-2003`)**: External consultants and staff augmentation personnel subject to fixed-term contracts (maximum 6-month durations before formal renewal).
3. **Non-Human / Service Identities (3 Identities: `SVC-3001` to `SVC-3003`)**: Programmatic accounts used by automated batch scripts, backup daemons, and ETL pipelines to communicate across systems.

### Privileged Authorization Attribute (Cross-Cutting Subset)
**Privileged Access** is an authorization tier assigned to a subset of **4 identities** across the population (3 employees: `USR-1004`, `USR-1005`, `USR-1012`; and 1 service account: `SVC-3001`). These accounts hold elevated capabilities (e.g., Global Admin, System Admin, Security Admin) requiring enhanced controls such as time-bound checkout and MFA enforcement.

---

## 5. Simulation Disclaimer

This project is a **simulated educational lab** designed to demonstrate enterprise IAM lifecycle operations, governance methodologies, and audit verification. All organizations, personas, systems, and data records are entirely fictional. No real enterprise systems, commercial identity software, or production accounts were accessed or utilized.
