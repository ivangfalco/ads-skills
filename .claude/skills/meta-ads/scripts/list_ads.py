#!/usr/bin/env python3
"""
List ALL Meta ads with ID, name, status, campaign, ad set, and performance metrics.

Unlike get_active_ads_copy.py (which only fetches active ads with creative details),
this script lists ALL ads with their performance data.

Usage:
    python list_ads.py                                      # All ads
    python list_ads.py --status ACTIVE                      # Only active
    python list_ads.py --campaign-id 12345                  # Filter by campaign
    python list_ads.py --ad-set-id 67890                    # Filter by ad set
    python list_ads.py --campaign-id 12345 --status ACTIVE  # Combined filters
"""

import argparse
import sys
from tabulate import tabulate
from client import api_get, get_account_id


def fetch_ads(account_id, campaign_id=None, ad_set_id=None, status_filter=None):
    """Fetch ads with fields and inline insights."""
    fields = (
        "name,status,effective_status,"
        "campaign_id,adset_id,"
        "insights.fields(impressions,clicks,spend,ctr,cpc,actions)"
        ".date_preset(last_30d)"
    )
    params = {"fields": fields, "limit": 200}

    if status_filter:
        params["effective_status"] = f'["{status_filter}"]'

    # Determine endpoint based on filters
    if ad_set_id:
        endpoint = f"{ad_set_id}/ads"
    elif campaign_id:
        endpoint = f"{campaign_id}/ads"
    else:
        endpoint = f"{account_id}/ads"

    return api_get(endpoint, params)


def extract_conversions(insight):
    """Extract lead/conversion count from actions."""
    actions = insight.get("actions", [])
    conversion_types = [
        "lead", "offsite_conversion", "offsite_conversion.fb_pixel_lead",
        "onsite_conversion.lead_grouped",
    ]
    total = 0
    for action in actions:
        if action.get("action_type") in conversion_types:
            total += int(action.get("value", 0))
    return total


def main():
    parser = argparse.ArgumentParser(description="List all Meta ads with performance metrics")
    parser.add_argument("--campaign-id", help="Filter by campaign ID")
    parser.add_argument("--ad-set-id", help="Filter by ad set ID")
    parser.add_argument("--status", choices=["ACTIVE", "PAUSED", "ARCHIVED", "DELETED",
                                              "PENDING_REVIEW", "DISAPPROVED", "WITH_ISSUES"],
                        help="Filter by effective status")
    parser.add_argument("--account-id", help="Meta ad account ID (default: from .env)")
    args = parser.parse_args()

    account_id = args.account_id or get_account_id()

    print(f"Fetching ads for {account_id}...")
    ads = fetch_ads(account_id, args.campaign_id, args.ad_set_id, args.status)

    if ads is None:
        print("Failed to fetch ads.")
        sys.exit(1)

    if not ads:
        print("No ads found.")
        return

    # Build rows
    rows = []
    for ad in ads:
        insights_data = ad.get("insights", {}).get("data", [])
        insight = insights_data[0] if insights_data else {}

        spend = float(insight.get("spend", 0))
        conversions = extract_conversions(insight)

        rows.append({
            "name": ad.get("name", ""),
            "id": ad.get("id", ""),
            "status": ad.get("effective_status", ad.get("status", "")),
            "campaign_id": ad.get("campaign_id", ""),
            "adset_id": ad.get("adset_id", ""),
            "spend": spend,
            "impressions": int(insight.get("impressions", 0)),
            "clicks": int(insight.get("clicks", 0)),
            "ctr": float(insight.get("ctr", 0)),
            "cpc": float(insight.get("cpc", 0)),
            "conversions": conversions,
        })

    # Sort by spend DESC
    rows.sort(key=lambda r: r["spend"], reverse=True)

    # Format table
    table = []
    for r in rows:
        table.append([
            r["name"][:35],
            r["id"],
            r["status"],
            r["campaign_id"],
            r["adset_id"],
            f"${r['spend']:,.2f}",
            f"{r['impressions']:,}",
            f"{r['clicks']:,}",
            f"{r['ctr']:.2f}%",
            f"${r['cpc']:.2f}",
            r["conversions"],
        ])

    headers = ["Ad Name", "Ad ID", "Status", "Campaign ID", "Ad Set ID",
               "Spend (30d)", "Impr", "Clicks", "CTR", "CPC", "Conv"]

    print(f"\nFound {len(rows)} ad(s) (last 30 days metrics):\n")
    print(tabulate(table, headers=headers, tablefmt="simple"))

    # Summary
    total_spend = sum(r["spend"] for r in rows)
    total_clicks = sum(r["clicks"] for r in rows)
    total_conversions = sum(r["conversions"] for r in rows)
    active_count = sum(1 for r in rows if r["status"] == "ACTIVE")
    paused_count = sum(1 for r in rows if r["status"] == "PAUSED")

    print(f"\nTotal: {len(rows)} ads ({active_count} active, {paused_count} paused)")
    print(f"Total spend (30d): ${total_spend:,.2f} | Clicks: {total_clicks:,} | Conversions: {total_conversions}")


if __name__ == "__main__":
    main()
