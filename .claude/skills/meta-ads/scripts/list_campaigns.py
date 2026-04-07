#!/usr/bin/env python3
"""
List all Meta Ads campaigns with status, objective, budget, and metrics.

Usage:
    python list_campaigns.py                    # All campaigns
    python list_campaigns.py --status ACTIVE    # Only active
    python list_campaigns.py --status PAUSED    # Only paused
"""

import argparse
import sys
from tabulate import tabulate
from client import api_get, get_account_id


def fetch_campaigns(account_id, status_filter=None):
    """Fetch campaigns with fields and insights."""
    fields = (
        "name,objective,status,effective_status,"
        "daily_budget,lifetime_budget,"
        "insights.fields(impressions,clicks,spend,ctr,cpc,cpm,reach,actions)"
        ".date_preset(last_30d)"
    )
    params = {"fields": fields, "limit": 100}

    if status_filter:
        params["effective_status"] = f'["{status_filter}"]'

    return api_get(f"{account_id}/campaigns", params)


def extract_lead_conversions(insights):
    """Extract lead/conversion count from insights actions."""
    if not insights:
        return 0
    actions = insights.get("actions", [])
    conversion_types = [
        "lead", "offsite_conversion", "offsite_conversion.fb_pixel_lead",
        "onsite_conversion.lead_grouped",
    ]
    total = 0
    for action in actions:
        if action.get("action_type") in conversion_types:
            total += int(action.get("value", 0))
    return total


def format_budget(campaign):
    """Format budget display."""
    daily = campaign.get("daily_budget")
    lifetime = campaign.get("lifetime_budget")
    if daily:
        return f"${int(daily) / 100:,.2f}/day"
    if lifetime:
        return f"${int(lifetime) / 100:,.2f} lifetime"
    return "CBO/No budget"


def main():
    parser = argparse.ArgumentParser(description="List Meta Ads campaigns")
    parser.add_argument("--status", choices=["ACTIVE", "PAUSED", "ARCHIVED", "DELETED"],
                        help="Filter by effective status")
    parser.add_argument("--account-id", help="Meta ad account ID (default: from .env)")
    args = parser.parse_args()

    account_id = args.account_id or get_account_id()

    print(f"Fetching campaigns for {account_id}...")
    campaigns = fetch_campaigns(account_id, args.status)

    if campaigns is None:
        print("Failed to fetch campaigns.")
        sys.exit(1)

    if not campaigns:
        print("No campaigns found.")
        return

    # Build rows
    rows = []
    for c in campaigns:
        insights_data = c.get("insights", {}).get("data", [])
        insight = insights_data[0] if insights_data else {}

        spend = float(insight.get("spend", 0))
        conversions = extract_lead_conversions(insight)

        rows.append({
            "name": c.get("name", ""),
            "id": c.get("id", ""),
            "status": c.get("effective_status", c.get("status", "")),
            "objective": c.get("objective", ""),
            "budget": format_budget(c),
            "spend": spend,
            "impressions": int(insight.get("impressions", 0)),
            "clicks": int(insight.get("clicks", 0)),
            "ctr": float(insight.get("ctr", 0)),
            "cpc": float(insight.get("cpc", 0)),
            "conversions": conversions,
        })

    # Sort by spend DESC
    rows.sort(key=lambda r: r["spend"], reverse=True)

    # Format for display
    table = []
    for r in rows:
        table.append([
            r["name"][:40],
            r["id"],
            r["status"],
            r["objective"],
            r["budget"],
            f"${r['spend']:,.2f}",
            f"{r['impressions']:,}",
            f"{r['clicks']:,}",
            f"{r['ctr']:.2f}%",
            f"${r['cpc']:.2f}",
            r["conversions"],
        ])

    headers = ["Campaign", "ID", "Status", "Objective", "Budget",
               "Spend (30d)", "Impr", "Clicks", "CTR", "CPC", "Conv"]

    print(f"\nFound {len(rows)} campaign(s) (last 30 days metrics):\n")
    print(tabulate(table, headers=headers, tablefmt="simple"))

    # Summary
    total_spend = sum(r["spend"] for r in rows)
    total_conversions = sum(r["conversions"] for r in rows)
    print(f"\nTotal spend (30d): ${total_spend:,.2f}")
    print(f"Total conversions: {total_conversions}")


if __name__ == "__main__":
    main()
