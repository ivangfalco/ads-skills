#!/usr/bin/env python3
"""
Detailed Meta Ads campaign performance analytics.

Usage:
    python get_campaign_performance.py                                    # All campaigns, last 30 days
    python get_campaign_performance.py --campaign-id 12345               # Specific campaign
    python get_campaign_performance.py --date-range last_7d              # Last 7 days
    python get_campaign_performance.py --start-date 2026-01-01 --end-date 2026-01-31
    python get_campaign_performance.py --campaign-id 12345 --by-day      # Daily breakdown
"""

import argparse
import sys
from datetime import datetime, timedelta
from tabulate import tabulate
from client import api_get, get_account_id


DATE_PRESETS = {
    "last_7d": "last_7d",
    "last_14d": "last_14d",
    "last_30d": "last_30d",
    "last_90d": "last_90d",
}


def build_time_params(args):
    """Build time_range or date_preset params."""
    if args.start_date and args.end_date:
        return {
            "time_range": f'{{"since":"{args.start_date}","until":"{args.end_date}"}}',
        }
    preset = args.date_range or "last_30d"
    if preset in DATE_PRESETS:
        return {"date_preset": DATE_PRESETS[preset]}
    print(f"Unknown date range: {preset}. Using last_30d.")
    return {"date_preset": "last_30d"}


def extract_conversions(actions):
    """Extract lead/conversion count from actions list."""
    if not actions:
        return 0
    conversion_types = [
        "lead", "offsite_conversion", "offsite_conversion.fb_pixel_lead",
        "onsite_conversion.lead_grouped", "complete_registration",
    ]
    total = 0
    for action in actions:
        if action.get("action_type") in conversion_types:
            total += int(action.get("value", 0))
    return total


def extract_cpl(cost_per_action):
    """Extract cost per lead from cost_per_action_type."""
    if not cost_per_action:
        return 0.0
    conversion_types = [
        "lead", "offsite_conversion", "offsite_conversion.fb_pixel_lead",
        "onsite_conversion.lead_grouped",
    ]
    for cpa in cost_per_action:
        if cpa.get("action_type") in conversion_types:
            return float(cpa.get("value", 0))
    return 0.0


def fetch_campaign_insights(account_id, campaign_id, time_params, by_day=False):
    """Fetch insights at campaign level."""
    fields = (
        "campaign_id,campaign_name,"
        "impressions,clicks,ctr,spend,reach,frequency,"
        "cpm,cpc,actions,cost_per_action_type"
    )
    params = {"fields": fields, "limit": 500}
    params.update(time_params)

    if by_day:
        params["time_increment"] = 1

    if campaign_id:
        # Use campaign-level insights endpoint
        endpoint = f"{campaign_id}/insights"
    else:
        # Use account-level with campaign breakdown
        endpoint = f"{account_id}/insights"
        params["level"] = "campaign"

    return api_get(endpoint, params)


def format_row(insight):
    """Format a single insight into a display row."""
    actions = insight.get("actions", [])
    cost_per_action = insight.get("cost_per_action_type", [])

    conversions = extract_conversions(actions)
    cpl = extract_cpl(cost_per_action)
    spend = float(insight.get("spend", 0))

    row = {
        "campaign_name": insight.get("campaign_name", "N/A"),
        "date": insight.get("date_start", ""),
        "impressions": int(insight.get("impressions", 0)),
        "clicks": int(insight.get("clicks", 0)),
        "ctr": float(insight.get("ctr", 0)),
        "spend": spend,
        "reach": int(insight.get("reach", 0)),
        "frequency": float(insight.get("frequency", 0)),
        "cpm": float(insight.get("cpm", 0)),
        "cpc": float(insight.get("cpc", 0)),
        "conversions": conversions,
        "cpl": cpl,
    }
    return row


def main():
    parser = argparse.ArgumentParser(description="Meta Ads campaign performance analytics")
    parser.add_argument("--campaign-id", help="Specific campaign ID (omit for all campaigns)")
    parser.add_argument("--date-range", choices=["last_7d", "last_14d", "last_30d", "last_90d"],
                        help="Date preset (default: last_30d)")
    parser.add_argument("--start-date", help="Custom start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Custom end date (YYYY-MM-DD)")
    parser.add_argument("--by-day", action="store_true", help="Show daily breakdown")
    parser.add_argument("--account-id", help="Meta ad account ID (default: from .env)")
    args = parser.parse_args()

    account_id = args.account_id or get_account_id()
    time_params = build_time_params(args)

    campaign_label = args.campaign_id or "All campaigns"
    print(f"Account:  {account_id}")
    print(f"Campaign: {campaign_label}")
    print(f"Params:   {time_params}")
    print("=" * 70)

    insights = fetch_campaign_insights(account_id, args.campaign_id, time_params, args.by_day)

    if insights is None:
        print("Failed to fetch insights.")
        sys.exit(1)

    if not insights:
        print("No data for this period.")
        return

    rows = [format_row(i) for i in insights]

    # Sort by spend DESC (or date for daily)
    if args.by_day:
        rows.sort(key=lambda r: r["date"])
    else:
        rows.sort(key=lambda r: r["spend"], reverse=True)

    # Build table
    if args.by_day:
        headers = ["Date", "Impr", "Clicks", "CTR", "Spend", "Reach",
                    "Freq", "CPM", "CPC", "Conv", "CPL"]
        table = []
        for r in rows:
            table.append([
                r["date"],
                f"{r['impressions']:,}",
                f"{r['clicks']:,}",
                f"{r['ctr']:.2f}%",
                f"${r['spend']:,.2f}",
                f"{r['reach']:,}",
                f"{r['frequency']:.2f}",
                f"${r['cpm']:.2f}",
                f"${r['cpc']:.2f}",
                r["conversions"],
                f"${r['cpl']:.2f}" if r["cpl"] > 0 else "-",
            ])
    else:
        headers = ["Campaign", "Impr", "Clicks", "CTR", "Spend", "Reach",
                    "Freq", "CPM", "CPC", "Conv", "CPL"]
        table = []
        for r in rows:
            table.append([
                r["campaign_name"][:35],
                f"{r['impressions']:,}",
                f"{r['clicks']:,}",
                f"{r['ctr']:.2f}%",
                f"${r['spend']:,.2f}",
                f"{r['reach']:,}",
                f"{r['frequency']:.2f}",
                f"${r['cpm']:.2f}",
                f"${r['cpc']:.2f}",
                r["conversions"],
                f"${r['cpl']:.2f}" if r["cpl"] > 0 else "-",
            ])

    print(tabulate(table, headers=headers, tablefmt="simple"))

    # Totals
    total_spend = sum(r["spend"] for r in rows)
    total_clicks = sum(r["clicks"] for r in rows)
    total_impressions = sum(r["impressions"] for r in rows)
    total_conversions = sum(r["conversions"] for r in rows)
    avg_cpl = total_spend / total_conversions if total_conversions > 0 else 0

    print(f"\nTotals: {total_impressions:,} impr | {total_clicks:,} clicks | "
          f"${total_spend:,.2f} spend | {total_conversions} conv | "
          f"${avg_cpl:.2f} CPL")


if __name__ == "__main__":
    main()
