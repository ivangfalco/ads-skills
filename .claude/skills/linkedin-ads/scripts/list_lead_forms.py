#!/usr/bin/env python3
"""
List all lead gen forms on the LinkedIn Ads account.

Usage:
    python list_lead_forms.py
"""

import argparse
import sys
from client import get_session, get_account_id, BASE_URL
from tabulate import tabulate


def list_lead_forms():
    session = get_session()
    account_id = get_account_id()

    params = {"q": "search", "count": 100}

    resp = session.get(f"{BASE_URL}/adAccounts/{account_id}/adForms", params=params)
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch lead forms: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    forms = data.get("elements", [])

    if not forms:
        print("No lead gen forms found.")
        return

    rows = []
    for form in forms:
        form_id = form.get("id", "N/A")
        name = form.get("name", "N/A")
        status = form.get("status", "UNKNOWN")
        headline = form.get("headline", "-")
        description = form.get("description", "-")
        cta = form.get("callToAction", "-")

        # Count questions
        questions = form.get("questions", [])
        hidden_fields = form.get("hiddenFields", [])
        num_questions = len(questions)
        num_hidden = len(hidden_fields)

        rows.append([
            form_id,
            name[:35],
            status,
            headline[:30] if headline else "-",
            description[:30] if description else "-",
            cta[:15] if cta else "-",
            num_questions,
            num_hidden,
        ])

    headers = ["Form ID", "Name", "Status", "Headline", "Description", "CTA", "Questions", "Hidden Fields"]

    print(f"\nLead Gen Forms for account {account_id}")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(rows)} forms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List LinkedIn Ads lead gen forms")
    args = parser.parse_args()
    list_lead_forms()
