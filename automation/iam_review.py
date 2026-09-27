#!/usr/bin/env python3
"""
IAM Lifecycle & Access Governance Audit Script
-----------------------------------------------
Author: Francisco Elroy Afonso
Project: IAM Lifecycle & Access Governance Operations Lab
Description: Evaluates simulated enterprise identity data to identify governance
             exceptions, dormant accounts, lifecycle defects, and SoD conflicts.
"""

import csv
import os
import sys
from datetime import datetime

# Reference audit date for the simulated review
AUDIT_DATE = datetime.strptime("2026-09-27", "%Y-%m-%d")
DORMANT_THRESHOLD_DAYS = 90


def get_project_root():
    """Returns the root directory of the IAM governance project."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def load_csv(filepath):
    """Loads a CSV file and returns a list of row dictionaries."""
    if not os.path.exists(filepath):
        print(f"[ERROR] Required file not found: {filepath}", file=sys.stderr)
        return []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def check_terminated_active_users(identities, leavers):
    """
    Control Check 1: Terminated users who still retain active accounts.
    Cross-references HR leaver records with the identity inventory.
    """
    findings = []
    # Build dictionary of terminated user IDs from HR leaver events
    terminated_leaver_ids = {
        row["identity_id"]: row for row in leavers 
        if row.get("termination_date") and row.get("termination_date") != "None"
    }

    for identity in identities:
        ident_id = identity["identity_id"]
        # Check if user is marked as terminated by HR but account is still Active in IT systems
        is_terminated_hr = (
            identity["employment_status"].lower() == "terminated" or 
            ident_id in terminated_leaver_ids
        )
        is_account_active = identity["account_status"].lower() == "active"

        if is_terminated_hr and is_account_active:
            term_date = identity.get("end_date") or terminated_leaver_ids.get(ident_id, {}).get("termination_date", "Unknown")
            findings.append({
                "category": "Terminated User Retaining Active Access",
                "severity": "HIGH",
                "identity_id": ident_id,
                "name": identity["name"],
                "details": f"Terminated on {term_date}, but account status is still Active in directory. Last login: {identity['last_login']}",
                "remediation": "Immediately disable account and revoke all application entitlements."
            })
    return findings


def check_expired_contractors(identities):
    """
    Control Check 2: Contractors whose contract end_date has passed but account is active.
    """
    findings = []
    for identity in identities:
        if identity["identity_type"].lower() == "contractor" and identity["account_status"].lower() == "active":
            end_date_str = identity.get("end_date", "").strip()
            if end_date_str:
                try:
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                    if end_date < AUDIT_DATE:
                        days_expired = (AUDIT_DATE - end_date).days
                        findings.append({
                            "category": "Expired Contractor Account Active",
                            "severity": "MEDIUM",
                            "identity_id": identity["identity_id"],
                            "name": identity["name"],
                            "details": f"Contract expired {days_expired} days ago ({end_date_str}), but account is still Active. Last login: {identity['last_login']}",
                            "remediation": "Disable contractor account and require formal contract extension before re-enabling."
                        })
                except ValueError:
                    pass
    return findings


def check_dormant_accounts(identities):
    """
    Control Check 3: Active accounts that have not logged in for over 90 days.
    """
    findings = []
    for identity in identities:
        if identity["account_status"].lower() == "active":
            last_login_str = identity.get("last_login", "").strip()
            if last_login_str:
                try:
                    last_login = datetime.strptime(last_login_str, "%Y-%m-%d")
                    days_inactive = (AUDIT_DATE - last_login).days
                    if days_inactive > DORMANT_THRESHOLD_DAYS:
                        findings.append({
                            "category": "Dormant Account (>90 Days Inactive)",
                            "severity": "MEDIUM",
                            "identity_id": identity["identity_id"],
                            "name": identity["name"],
                            "details": f"Last login was {days_inactive} days ago ({last_login_str}). Status: {identity['employment_status']}",
                            "remediation": "Temporarily suspend account pending verification of active employment status."
                        })
                except ValueError:
                    pass
    return findings


def check_unowned_service_accounts(identities):
    """
    Control Check 4: Service accounts lacking a designated technical or business owner.
    """
    findings = []
    for identity in identities:
        if identity["identity_type"].lower() == "service account" and identity["account_status"].lower() == "active":
            tech_owner = identity.get("service_account_owner", "").strip()
            biz_owner = identity.get("business_owner", "").strip()

            unassigned_values = ["", "none", "n/a", "unassigned"]
            if tech_owner.lower() in unassigned_values or biz_owner.lower() in unassigned_values:
                findings.append({
                    "category": "Unowned Service Account",
                    "severity": "MEDIUM",
                    "identity_id": identity["identity_id"],
                    "name": identity["name"],
                    "details": f"Active service account lacks designated ownership (Tech: '{tech_owner}', Biz: '{biz_owner}').",
                    "remediation": "Identify business application dependency, assign primary/secondary owners, or decommission."
                })
    return findings


def check_standing_privileged_access(identities, pam_reviews):
    """
    Control Check 5: Identities with permanent, standing 24/7 privileged administrative rights.
    """
    findings = []
    for pam in pam_reviews:
        if pam.get("standing_access_flag", "").lower() == "true":
            role = pam.get("privileged_role", "")
            if "globaladmin" in role.lower() or "superadmin" in role.lower():
                findings.append({
                    "category": "Excessive Standing Privileged Access",
                    "severity": "HIGH",
                    "identity_id": pam.get("identity_id", "N/A"),
                    "name": pam.get("account_name", "N/A"),
                    "details": f"Holds permanent 24/7 standing privilege ({role}) without time-bound JIT checkout in PAM vault.",
                    "remediation": "Revoke standing administrative assignment; enforce ephemeral 4-hour checkout via PAM vault."
                })
    return findings


def check_sod_conflicts(access_reviews):
    """
    Control Check 6: Segregation of Duties (SoD) conflicts discovered during access review.
    """
    findings = []
    # Track roles held per identity in the access review
    identity_roles = {}
    for row in access_reviews:
        ident_id = row["identity_id"]
        role = row["role_held"]
        decision = row["decision"]
        if ident_id not in identity_roles:
            identity_roles[ident_id] = {"name": row["name"], "roles": set(), "decisions": []}
        identity_roles[ident_id]["roles"].add(role)
        identity_roles[ident_id]["decisions"].append(row)

    for ident_id, data in identity_roles.items():
        roles = data["roles"]
        # Incompatible pair: Wire Initiation and Wire Approval
        has_initiator = any("initiator" in r.lower() for r in roles)
        has_approver = any("approver" in r.lower() or "fin-manager" in r.lower() for r in roles)
        if has_initiator and has_approver:
            findings.append({
                "category": "Segregation of Duties (SoD) Toxic Combination",
                "severity": "HIGH",
                "identity_id": ident_id,
                "name": data["name"],
                "details": f"User possesses both payment initiation and payment approval entitlements ({', '.join(roles)}).",
                "remediation": "Revoke payment initiator entitlement immediately to restore dual-authorization controls."
            })
    return findings


def check_expired_exceptions(exceptions):
    """
    Control Check 7: Policy exceptions whose approved expiry date has passed.
    """
    findings = []
    for exc in exceptions:
        expiry_str = exc.get("expiry_date", "").strip()
        status = exc.get("review_status", "").lower()
        if expiry_str:
            try:
                expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
                if expiry < AUDIT_DATE and "expired" in status:
                    findings.append({
                        "category": "Expired Access Policy Exception",
                        "severity": "MEDIUM",
                        "identity_id": exc["identity_id"],
                        "name": exc["name"],
                        "details": f"Exception {exc['exception_id']} ({exc['access_granted']}) expired on {expiry_str} and remains unremediated.",
                        "remediation": "Revoke the exceptional access grant or submit formal extension request with CISO approval."
                    })
            except ValueError:
                pass
    return findings


def main():
    root_dir = get_project_root()
    print("=" * 76)
    print("  NORTHSTAR FINANCIAL SERVICES — IAM OPERATIONS & GOVERNANCE AUDIT")
    print(f"  Audit Baseline Reference Date: {AUDIT_DATE.strftime('%Y-%m-%d')}")
    print("=" * 76)

    # 1. Load source CSV datasets
    inv_path = os.path.join(root_dir, "scenario", "identity_inventory.csv")
    leavers_path = os.path.join(root_dir, "lifecycle", "leaver_events.csv")
    review_path = os.path.join(root_dir, "governance", "access_review.csv")
    pam_path = os.path.join(root_dir, "governance", "privileged_access_review.csv")
    exc_path = os.path.join(root_dir, "governance", "exceptions_register.csv")

    identities = load_csv(inv_path)
    leavers = load_csv(leavers_path)
    access_reviews = load_csv(review_path)
    pam_reviews = load_csv(pam_path)
    exceptions = load_csv(exc_path)

    print(f"\n[+] Loaded {len(identities)} identities from inventory.")
    print(f"[+] Loaded {len(leavers)} HR leaver lifecycle events.")
    print(f"[+] Loaded {len(access_reviews)} quarterly access certification records.")
    print(f"[+] Loaded {len(pam_reviews)} privileged access review records.")
    print(f"[+] Loaded {len(exceptions)} access policy exceptions.")

    # 2. Execute automated governance checks
    all_findings = []
    all_findings.extend(check_terminated_active_users(identities, leavers))
    all_findings.extend(check_expired_contractors(identities))
    all_findings.extend(check_dormant_accounts(identities))
    all_findings.extend(check_unowned_service_accounts(identities))
    all_findings.extend(check_standing_privileged_access(identities, pam_reviews))
    all_findings.extend(check_sod_conflicts(access_reviews))
    all_findings.extend(check_expired_exceptions(exceptions))

    # 3. Print Console Report
    print("\n" + "-" * 76)
    print(f"  IDENTIFIED GOVERNANCE DEFECTS & CONTROL EXCEPTIONS ({len(all_findings)} TOTAL)")
    print("-" * 76)

    for i, item in enumerate(all_findings, 1):
        sev_tag = f"[{item['severity']}]"
        print(f"{i:2d}. {sev_tag:<8} {item['category']}")
        print(f"    Target   : {item['name']} ({item['identity_id']})")
        print(f"    Evidence : {item['details']}")
        print(f"    Action   : {item['remediation']}\n")

    # 4. Export findings to CSV
    output_path = os.path.join(root_dir, "automation", "iam_review_results.csv")
    with open(output_path, mode="w", newline="", encoding="utf-8") as out_file:
        fieldnames = ["category", "severity", "identity_id", "name", "details", "remediation"]
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_findings)

    print(f"[+] Audit complete. Exported structured findings to: {os.path.basename(output_path)}")
    print("=" * 76)


if __name__ == "__main__":
    main()
