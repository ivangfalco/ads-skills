#!/usr/bin/env python3
"""
View and update bids for a LinkedIn Ads campaign.

Usage:
    python manage_bids.py --campaign-id 123456 --action view
    python manage_bids.py --campaign-id 123456 --action set --bid-amount 500
    python manage_bids.py --campaign-id 123456 --action set --bid-strategy MANUAL_CPC --bid-amount 750
    python manage_bids.py --campaign-id 123456 --action set --bid-strategy AUTO

Bid amounts are in CENTS (e.g., 500 = $5.00).
"""

import argparse
import sys
from client import get_session, get_account_id, BASE_URL
from tabulate import tabulate


def view_bid(session, account_id, campaign_id):
    """View current bid info for a campaign."""
    resp = session.get(f"{BASE_URL}/adAccounts/{account_id}/adCampaigns/{campaign_id}")
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch campaign {campaign_id}: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    campaign = resp.json()

    name = campaign.get("name", "N/A")
    status = campaign.get("status", "UNKNOWN")
    cost_type = campaign.get("costType", "N/A")
    bid_strategy = campaign.get("bidStrategy", "N/A")

    unit_cost = campaign.get("unitCost", {})
    bid_amount = unit_cost.get("amount", "0")
    bid_currency = unit_cost.get("currencyCode", "USD")

    daily_budget = campaign.get("dailyBudget", {})
    budget_amount = daily_budget.get("amount", "0")
    budget_currency = daily_budget.get("currencyCode", "USD")

    bid_dollars = float(bid_amount) / 100 if bid_amount else 0
    budget_dollars = float(budget_amount) / 100 if budget_amount else 0

    rows = [
        ["Campaign ID", campaign_id],
        ["Name", name],
        ["Status", status],
        ["Cost Type", cost_type],
        ["Bid Strategy", bid_strategy],
        ["Bid Amount", f"${bid_dollars:,.2f} {bid_currency}" if bid_dollars > 0 else "Auto"],
        ["Daily Budget", f"${budget_dollars:,.2f} {budget_currency}"],
    ]

    print(f"\n  Bid Info for Campaign {campaign_id}")
    print(tabulate(rows, headers=["Field", "Value"], tablefmt="simple"))
    print()


def set_bid(session, account_id, campaign_id, bid_amount=None, bid_strategy=None):
    """Update bid for a campaign."""
    patch = {"account": f"urn:li:sponsoredAccount:{account_id}"}
    changes = []

    if bid_strategy:
        if bid_strategy == "AUTO":
            patch["bidStrategy"] = "MAXIMUM_DELIVERY"
            changes.append("Bid Strategy -> AUTO (Maximum Delivery)")
        elif bid_strategy == "MANUAL_CPC":
            patch["bidStrategy"] = "MANUAL_BIDDING"
            patch["costType"] = "CPC"
            changes.append("Bid Strategy -> MANUAL_CPC")
        elif bid_strategy == "MANUAL_CPM":
            patch["bidStrategy"] = "MANUAL_BIDDING"
            patch["costType"] = "CPM"
            changes.append("Bid Strategy -> MANUAL_CPM")

    if bid_amount is not None:
        patch["unitCost"] = {
            "amount": str(bid_amount),
            "currencyCode": "USD",
        }
        changes.append(f"Bid Amount -> ${bid_amount / 100:,.2f}")

    if not changes:
        print("ERROR: For 'set' action, provide --bid-amount and/or --bid-strategy.")
        sys.exit(1)

    resp = session.post(
        f"{BASE_URL}/adAccounts/{account_id}/adCampaigns/{campaign_id}",
        json=patch,
        headers={**session.headers, "X-Restli-Method": "PARTIAL_UPDATE"},
    )

    if resp.status_code in (200, 204):
        print(f"\nUpdated bids for campaign {campaign_id}:")
        for change in changes:
            print(f"  - {change}")
    else:
        print(f"ERROR: Failed to update bids: {resp.status_code}")
        print(resp.text)
        sys.exit(1)


def manage_bids(args):
    session = get_session()
    account_id = get_account_id()

    if args.action == "view":
        view_bid(session, account_id, args.campaign_id)
    elif args.action == "set":
        if not args.bid_amount and not args.bid_strategy:
            print("ERROR: For 'set' action, provide --bid-amount and/or --bid-strategy.")
            sys.exit(1)
        set_bid(session, account_id, args.campaign_id, args.bid_amount, args.bid_strategy)
        # Show updated state
        print("\nCurrent state after update:")
        view_bid(session, account_id, args.campaign_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View and update LinkedIn Ads campaign bids")
    parser.add_argument("--campaign-id", required=True, type=int, help="Campaign ID")
    parser.add_argument("--action", required=True, choices=["view", "set"],
                        help="Action: view current bids or set new bids")
    parser.add_argument("--bid-amount", type=int,
                        help="Bid amount in cents (e.g., 500 = $5.00)")
    parser.add_argument("--bid-strategy", choices=["AUTO", "MANUAL_CPC", "MANUAL_CPM"],
                        help="Bidding strategy")
    args = parser.parse_args()
    manage_bids(args)
