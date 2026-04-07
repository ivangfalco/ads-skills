#!/usr/bin/env python3
"""
List all creatives in the LinkedIn Ads account.

Usage:
    python list_creatives.py                          # All creatives
    python list_creatives.py --campaign-id 123456     # Creatives for a specific campaign
"""

import argparse
import sys
from client import get_session, get_account_id, BASE_URL
from tabulate import tabulate


def list_creatives(campaign_id: int = None):
    session = get_session()
    account_id = get_account_id()

    params = {"q": "search", "count": 100}
    if campaign_id:
        params["search"] = f"(campaign:(values:List(urn:li:sponsoredCampaign:{campaign_id})))"

    resp = session.get(f"{BASE_URL}/adAccounts/{account_id}/adCreatives", params=params)
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch creatives: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    creatives = data.get("elements", [])

    if not creatives:
        print("No creatives found.")
        return

    rows = []
    for cr in creatives:
        creative_id = cr.get("id", "N/A")
        status = cr.get("status", "UNKNOWN")
        creative_type = cr.get("type", "N/A")

        # Extract campaign ID from the campaign URN
        campaign_urn = cr.get("campaign", "")
        camp_id = campaign_urn.split(":")[-1] if campaign_urn else "-"

        # Get the reference (content reference / share URN)
        reference = cr.get("reference", "")
        if not reference:
            # Try to get from content
            content = cr.get("content", {})
            reference = content.get("reference", "")

        # Truncate reference for display
        ref_display = reference[:50] if reference else "-"

        rows.append([
            creative_id,
            camp_id,
            creative_type[:20],
            status,
            ref_display,
        ])

    headers = ["Creative ID", "Campaign ID", "Type", "Status", "Reference"]

    print(f"\nCreatives for account {account_id}")
    if campaign_id:
        print(f"  Filtered by campaign: {campaign_id}")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(rows)} creatives")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List LinkedIn Ads creatives")
    parser.add_argument("--campaign-id", type=int, help="Filter by campaign ID")
    args = parser.parse_args()
    list_creatives(args.campaign_id)
