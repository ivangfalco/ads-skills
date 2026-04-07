#!/usr/bin/env python3
"""
Update a Meta Ads campaign (status, budget, name).

Usage:
    python update_campaign.py --campaign-id 12345 --status ACTIVE
    python update_campaign.py --campaign-id 12345 --status PAUSED
    python update_campaign.py --campaign-id 12345 --daily-budget 10000
    python update_campaign.py --campaign-id 12345 --name "New Name" --status PAUSED
"""

import argparse
import sys
from client import api_post, get_account_id

VALID_STATUSES = ["ACTIVE", "PAUSED", "ARCHIVED"]


def main():
    parser = argparse.ArgumentParser(description="Update a Meta Ads campaign")
    parser.add_argument("--campaign-id", required=True, help="Campaign ID to update")
    parser.add_argument("--status", choices=VALID_STATUSES,
                        help="New status (ACTIVE, PAUSED, ARCHIVED)")
    parser.add_argument("--daily-budget", type=int,
                        help="New daily budget in cents (e.g., 5000 = $50.00)")
    parser.add_argument("--lifetime-budget", type=int,
                        help="New lifetime budget in cents")
    parser.add_argument("--name", help="New campaign name")
    parser.add_argument("--account-id", help="Meta ad account ID (default: from .env)")
    args = parser.parse_args()

    # Check that at least one update field is provided
    if not any([args.status, args.daily_budget, args.lifetime_budget, args.name]):
        print("Error: Provide at least one field to update (--status, --daily-budget, --lifetime-budget, --name).")
        sys.exit(1)

    # Build update data
    data = {}
    changes = []

    if args.status:
        data["status"] = args.status
        changes.append(f"Status -> {args.status}")

    if args.daily_budget:
        data["daily_budget"] = args.daily_budget
        changes.append(f"Daily budget -> ${args.daily_budget / 100:,.2f}")

    if args.lifetime_budget:
        data["lifetime_budget"] = args.lifetime_budget
        changes.append(f"Lifetime budget -> ${args.lifetime_budget / 100:,.2f}")

    if args.name:
        data["name"] = args.name
        changes.append(f"Name -> {args.name}")

    print(f"Updating campaign {args.campaign_id}:")
    for change in changes:
        print(f"  {change}")
    print()

    result = api_post(args.campaign_id, data)

    if result is None:
        print("Failed to update campaign.")
        sys.exit(1)

    if result.get("success"):
        print("Campaign updated successfully.")
    else:
        print(f"Response: {result}")


if __name__ == "__main__":
    main()
