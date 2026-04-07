#!/usr/bin/env python3
"""
Create a Meta Ads campaign.

Usage:
    python create_campaign.py --name "Q2 Leads" --objective OUTCOME_LEADS --daily-budget 5000
    python create_campaign.py --name "Brand" --objective OUTCOME_AWARENESS --lifetime-budget 100000 --status ACTIVE
    python create_campaign.py --name "Housing Leads" --objective OUTCOME_LEADS --daily-budget 3000 \
        --special-ad-categories HOUSING
"""

import argparse
import sys
from client import api_post, get_account_id

VALID_OBJECTIVES = [
    "OUTCOME_LEADS",
    "OUTCOME_TRAFFIC",
    "OUTCOME_AWARENESS",
    "OUTCOME_ENGAGEMENT",
    "OUTCOME_SALES",
]

VALID_STATUSES = ["ACTIVE", "PAUSED"]

VALID_SPECIAL_CATEGORIES = [
    "CREDIT",
    "EMPLOYMENT",
    "HOUSING",
    "SOCIAL_ISSUES_ELECTIONS_POLITICS",
]


def main():
    parser = argparse.ArgumentParser(description="Create a Meta Ads campaign")
    parser.add_argument("--name", required=True, help="Campaign name")
    parser.add_argument("--objective", required=True, choices=VALID_OBJECTIVES,
                        help="Campaign objective")
    parser.add_argument("--daily-budget", type=int,
                        help="Daily budget in cents (e.g., 5000 = $50.00)")
    parser.add_argument("--lifetime-budget", type=int,
                        help="Lifetime budget in cents (e.g., 100000 = $1,000.00)")
    parser.add_argument("--status", choices=VALID_STATUSES, default="PAUSED",
                        help="Campaign status (default: PAUSED)")
    parser.add_argument("--special-ad-categories", nargs="*", choices=VALID_SPECIAL_CATEGORIES,
                        help="Special ad categories (if applicable)")
    parser.add_argument("--account-id", help="Meta ad account ID (default: from .env)")
    args = parser.parse_args()

    if not args.daily_budget and not args.lifetime_budget:
        print("Error: Provide either --daily-budget or --lifetime-budget (in cents).")
        sys.exit(1)

    if args.daily_budget and args.lifetime_budget:
        print("Error: Provide only one of --daily-budget or --lifetime-budget, not both.")
        sys.exit(1)

    account_id = args.account_id or get_account_id()

    # Build campaign data
    data = {
        "name": args.name,
        "objective": args.objective,
        "status": args.status,
        "special_ad_categories": "[]",
    }

    if args.daily_budget:
        data["daily_budget"] = args.daily_budget

    if args.lifetime_budget:
        data["lifetime_budget"] = args.lifetime_budget

    if args.special_ad_categories:
        import json
        data["special_ad_categories"] = json.dumps(args.special_ad_categories)

    # Confirm before creating
    budget_str = (f"${args.daily_budget / 100:,.2f}/day" if args.daily_budget
                  else f"${args.lifetime_budget / 100:,.2f} lifetime")

    print(f"Creating campaign:")
    print(f"  Account:    {account_id}")
    print(f"  Name:       {args.name}")
    print(f"  Objective:  {args.objective}")
    print(f"  Budget:     {budget_str}")
    print(f"  Status:     {args.status}")
    if args.special_ad_categories:
        print(f"  Special:    {', '.join(args.special_ad_categories)}")
    print()

    result = api_post(f"{account_id}/campaigns", data)

    if result is None:
        print("Failed to create campaign.")
        sys.exit(1)

    campaign_id = result.get("id")
    print(f"Campaign created successfully!")
    print(f"  Campaign ID: {campaign_id}")
    print()
    print("Next steps:")
    print(f"  1. Create an ad set under this campaign (campaign_id={campaign_id})")
    print(f"  2. Define targeting, placement, and optimization goal in the ad set")
    print(f"  3. Create ads with creative under the ad set")
    print(f"  4. Set campaign status to ACTIVE when ready:")
    print(f"     python update_campaign.py --campaign-id {campaign_id} --status ACTIVE")


if __name__ == "__main__":
    main()
