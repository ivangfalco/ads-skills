#!/usr/bin/env python3
"""
Create a new LinkedIn Ads campaign.

Usage:
    python create_campaign.py --name "Lead Gen - Decision Makers" --campaign-group-id 123456 --objective LEAD_GENERATION --daily-budget 5000
    python create_campaign.py --name "Brand - Tech Audience" --campaign-group-id 123456 --objective BRAND_AWARENESS --daily-budget 3000 --bid-strategy AUTO
    python create_campaign.py --name "Website Traffic" --campaign-group-id 123456 --objective WEBSITE_VISITS --daily-budget 2500 --bid-amount 800 --bid-strategy MANUAL_CPC

Budget and bid amounts are in CENTS (e.g., 5000 = $50.00).
Campaign always starts in PAUSED state for safety.
"""

import argparse
import sys
from client import get_session, get_account_id, BASE_URL


OBJECTIVES = [
    "LEAD_GENERATION",
    "WEBSITE_VISITS",
    "BRAND_AWARENESS",
    "VIDEO_VIEWS",
    "ENGAGEMENT",
]

BID_STRATEGIES = ["AUTO", "MANUAL_CPC", "MANUAL_CPM"]


def create_campaign(args):
    session = get_session()
    account_id = get_account_id()

    # Validate
    if args.bid_strategy in ("MANUAL_CPC", "MANUAL_CPM") and not args.bid_amount:
        print("ERROR: --bid-amount is required for MANUAL_CPC and MANUAL_CPM bid strategies.")
        sys.exit(1)

    # Build campaign payload
    payload = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "campaignGroup": f"urn:li:sponsoredCampaignGroup:{args.campaign_group_id}",
        "name": args.name,
        "objectiveType": args.objective,
        "status": "PAUSED",
        "type": "SPONSORED_UPDATES",
        "costType": "CPM",
        "dailyBudget": {
            "amount": str(args.daily_budget),
            "currencyCode": "USD",
        },
        "unitCost": {},
        "locale": {"country": "US", "language": "en"},
        "offsiteDeliveryEnabled": False,
    }

    # Bid strategy
    if args.bid_strategy == "AUTO":
        payload["bidStrategy"] = "MAXIMUM_DELIVERY"
    elif args.bid_strategy == "MANUAL_CPC":
        payload["costType"] = "CPC"
        payload["bidStrategy"] = "MANUAL_BIDDING"
        payload["unitCost"] = {
            "amount": str(args.bid_amount),
            "currencyCode": "USD",
        }
    elif args.bid_strategy == "MANUAL_CPM":
        payload["costType"] = "CPM"
        payload["bidStrategy"] = "MANUAL_BIDDING"
        payload["unitCost"] = {
            "amount": str(args.bid_amount),
            "currencyCode": "USD",
        }

    resp = session.post(f"{BASE_URL}/adAccounts/{account_id}/adCampaigns", json=payload)

    if resp.status_code == 201:
        campaign_id = resp.headers.get("x-restli-id", "unknown")
        budget_dollars = args.daily_budget / 100

        print(f"\nCampaign created successfully!")
        print(f"  ID:           {campaign_id}")
        print(f"  Name:         {args.name}")
        print(f"  Objective:    {args.objective}")
        print(f"  Daily Budget: ${budget_dollars:,.2f}")
        print(f"  Bid Strategy: {args.bid_strategy}")
        print(f"  Status:       PAUSED (starts paused for safety)")
        print(f"\nNext steps:")
        print(f"  1. Add targeting to the campaign in LinkedIn Campaign Manager")
        print(f"  2. Create creatives / ads for the campaign")
        print(f"  3. Enable: python update_campaign.py --campaign-id {campaign_id} --status ACTIVE")
        print(f"  4. Monitor:  python get_campaign_performance.py --campaign-id {campaign_id}")
    else:
        print(f"ERROR: Failed to create campaign: {resp.status_code}")
        print(resp.text)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new LinkedIn Ads campaign")
    parser.add_argument("--name", required=True, help="Campaign name")
    parser.add_argument("--campaign-group-id", required=True, type=int,
                        help="Campaign group ID to create under")
    parser.add_argument("--objective", required=True, choices=OBJECTIVES,
                        help="Campaign objective")
    parser.add_argument("--daily-budget", required=True, type=int,
                        help="Daily budget in cents (e.g., 5000 = $50.00)")
    parser.add_argument("--bid-amount", type=int,
                        help="Bid amount in cents (required for MANUAL_CPC/MANUAL_CPM)")
    parser.add_argument("--bid-strategy", default="AUTO", choices=BID_STRATEGIES,
                        help="Bidding strategy (default: AUTO)")
    args = parser.parse_args()
    create_campaign(args)
