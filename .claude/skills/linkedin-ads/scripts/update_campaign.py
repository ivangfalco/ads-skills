#!/usr/bin/env python3
"""
Update an existing LinkedIn Ads campaign.

Usage:
    python update_campaign.py --campaign-id 123456 --status ACTIVE
    python update_campaign.py --campaign-id 123456 --status PAUSED
    python update_campaign.py --campaign-id 123456 --daily-budget 7500
    python update_campaign.py --campaign-id 123456 --name "New Name" --daily-budget 5000
    python update_campaign.py --campaign-id 123456 --bid-strategy MANUAL_CPC --bid-amount 500

Budget and bid amounts are in CENTS (e.g., 5000 = $50.00).
"""

import argparse
import sys
from client import get_session, get_account_id, BASE_URL


def update_campaign(args):
    session = get_session()
    account_id = get_account_id()

    # Build patch payload -- only include fields that are being changed
    patch = {}
    changes_made = []

    if args.status:
        patch["status"] = args.status.upper()
        changes_made.append(f"Status -> {args.status.upper()}")

    if args.name:
        patch["name"] = args.name
        changes_made.append(f"Name -> '{args.name}'")

    if args.daily_budget is not None:
        patch["dailyBudget"] = {
            "amount": str(args.daily_budget),
            "currencyCode": "USD",
        }
        changes_made.append(f"Daily Budget -> ${args.daily_budget / 100:,.2f}")

    if args.bid_amount is not None:
        patch["unitCost"] = {
            "amount": str(args.bid_amount),
            "currencyCode": "USD",
        }
        changes_made.append(f"Bid Amount -> ${args.bid_amount / 100:,.2f}")

    if args.bid_strategy:
        if args.bid_strategy == "AUTO":
            patch["bidStrategy"] = "MAXIMUM_DELIVERY"
        elif args.bid_strategy == "MANUAL_CPC":
            patch["bidStrategy"] = "MANUAL_BIDDING"
            patch["costType"] = "CPC"
        elif args.bid_strategy == "MANUAL_CPM":
            patch["bidStrategy"] = "MANUAL_BIDDING"
            patch["costType"] = "CPM"
        changes_made.append(f"Bid Strategy -> {args.bid_strategy}")

    if not changes_made:
        print("No changes specified. Use --status, --daily-budget, --bid-amount, --bid-strategy, or --name.")
        return

    # LinkedIn REST API uses POST with partial update for campaigns
    patch["account"] = f"urn:li:sponsoredAccount:{account_id}"

    resp = session.post(
        f"{BASE_URL}/adAccounts/{account_id}/adCampaigns/{args.campaign_id}",
        json=patch,
        headers={**session.headers, "X-Restli-Method": "PARTIAL_UPDATE"},
    )

    if resp.status_code in (200, 204):
        print(f"\nUpdated campaign {args.campaign_id}:")
        for change in changes_made:
            print(f"  - {change}")
    else:
        print(f"ERROR: Failed to update campaign: {resp.status_code}")
        print(resp.text)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a LinkedIn Ads campaign")
    parser.add_argument("--campaign-id", required=True, type=int, help="Campaign ID to update")
    parser.add_argument("--status", choices=["ACTIVE", "PAUSED", "ARCHIVED"],
                        help="New campaign status")
    parser.add_argument("--name", help="New campaign name")
    parser.add_argument("--daily-budget", type=int,
                        help="New daily budget in cents (e.g., 5000 = $50.00)")
    parser.add_argument("--bid-amount", type=int,
                        help="New bid amount in cents")
    parser.add_argument("--bid-strategy", choices=["AUTO", "MANUAL_CPC", "MANUAL_CPM"],
                        help="New bidding strategy")
    args = parser.parse_args()
    update_campaign(args)
