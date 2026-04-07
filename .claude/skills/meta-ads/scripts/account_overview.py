#!/usr/bin/env python3
"""
Meta Ads Account Overview - Account-level dashboard with key metrics.

Pulls impressions, clicks, spend, reach, frequency, CPM, CPC, CTR,
conversions, cost per conversion, and actions breakdown.

Usage:
    python account_overview.py                    # Last 30 days
    python account_overview.py --days 7           # Last 7 days
    python account_overview.py --compare          # Compare to previous period
    python account_overview.py --start-date 2026-01-01 --end-date 2026-01-31
"""

import argparse
import sys
from datetime import datetime, timedelta
from tabulate import tabulate
from client import api_get, get_account_id


def get_date_range(args):
    """Build date range dict from args."""
    if args.start_date and args.end_date:
        return {
            "since": args.start_date,
            "until": args.end_date,
        }
    days = args.days or 30
    end = datetime.now().date()
    start = end - timedelta(days=days)
    return {
        "since": start.isoformat(),
        "until": end.isoformat(),
    }


def get_previous_period(date_range):
    """Calculate the previous period of the same length for comparison."""
    start = datetime.strptime(date_range["since"], "%Y-%m-%d").date()
    end = datetime.strptime(date_range["until"], "%Y-%m-%d").date()
    length = (end - start).days
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=length)
    return {
        "since": prev_start.isoformat(),
        "until": prev_end.isoformat(),
    }


def fetch_insights(account_id, date_range):
    """Fetch account-level insights for a date range."""
    fields = (
        "impressions,clicks,spend,reach,frequency,"
        "cpm,cpc,ctr,actions,cost_per_action_type"
    )
    params = {
        "fields": fields,
        "time_range": f'{{"since":"{date_range["since"]}","until":"{date_range["until"]}"}}',
    }
    data = api_get(f"{account_id}/insights", params)
    if not data:
        return None
    # insights returns a list with one entry
    if isinstance(data, list) and len(data) > 0:
        return data[0]
    return data


def extract_conversions(insight):
    """Extract conversion count and cost from actions breakdown."""
    actions = insight.get("actions", [])
    cost_per_action = insight.get("cost_per_action_type", [])

    conversion_types = [
        "lead", "offsite_conversion", "offsite_conversion.fb_pixel_lead",
        "onsite_conversion.lead_grouped", "complete_registration",
        "offsite_conversion.fb_pixel_complete_registration",
    ]

    total_conversions = 0
    for action in actions:
        if action.get("action_type") in conversion_types:
            total_conversions += int(action.get("value", 0))

    cost_per_conv = 0.0
    for cpa in cost_per_action:
        if cpa.get("action_type") in conversion_types:
            cost_per_conv = float(cpa.get("value", 0))
            break  # Take the first matching cost

    return total_conversions, cost_per_conv


def format_metric(value, fmt=",.0f"):
    """Format a metric value, handling None."""
    if value is None:
        return "N/A"
    try:
        return f"{float(value):{fmt}}"
    except (ValueError, TypeError):
        return str(value)


def build_metrics_table(insight, label="Current Period"):
    """Build a formatted metrics table from an insight dict."""
    if not insight:
        return []

    conversions, cost_per_conv = extract_conversions(insight)

    rows = [
        ["Impressions", format_metric(insight.get("impressions"))],
        ["Reach", format_metric(insight.get("reach"))],
        ["Clicks", format_metric(insight.get("clicks"))],
        ["CTR", format_metric(insight.get("ctr"), ".2f") + "%"],
        ["Spend", "$" + format_metric(insight.get("spend"), ",.2f")],
        ["CPM", "$" + format_metric(insight.get("cpm"), ",.2f")],
        ["CPC", "$" + format_metric(insight.get("cpc"), ",.2f")],
        ["Frequency", format_metric(insight.get("frequency"), ".2f")],
        ["Conversions", format_metric(conversions)],
        ["Cost/Conversion", "$" + format_metric(cost_per_conv, ",.2f") if cost_per_conv > 0 else "N/A"],
    ]
    return rows


def print_actions_breakdown(insight):
    """Print a breakdown of all actions."""
    actions = insight.get("actions", [])
    if not actions:
        print("\nNo actions data available.")
        return

    rows = []
    for action in sorted(actions, key=lambda a: int(a.get("value", 0)), reverse=True):
        rows.append([
            action.get("action_type", "unknown"),
            format_metric(action.get("value")),
        ])

    print("\nActions Breakdown:")
    print(tabulate(rows, headers=["Action Type", "Count"], tablefmt="simple"))


def main():
    parser = argparse.ArgumentParser(description="Meta Ads account overview dashboard")
    parser.add_argument("--days", type=int, help="Number of days to look back (default: 30)")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--compare", action="store_true", help="Compare with previous period")
    parser.add_argument("--account-id", help="Meta ad account ID (default: from .env)")
    args = parser.parse_args()

    account_id = args.account_id or get_account_id()
    date_range = get_date_range(args)

    print(f"Account: {account_id}")
    print(f"Period:  {date_range['since']} to {date_range['until']}")
    print("=" * 60)

    # Fetch current period
    insight = fetch_insights(account_id, date_range)
    if not insight:
        print("No data returned for this period.")
        sys.exit(1)

    if args.compare:
        # Fetch previous period
        prev_range = get_previous_period(date_range)
        prev_insight = fetch_insights(account_id, prev_range)

        current_rows = build_metrics_table(insight)
        prev_rows = build_metrics_table(prev_insight) if prev_insight else []

        # Build comparison table
        headers = ["Metric", f"Current ({date_range['since']} to {date_range['until']})",
                    f"Previous ({prev_range['since']} to {prev_range['until']})"]
        combined = []
        for i, row in enumerate(current_rows):
            prev_val = prev_rows[i][1] if i < len(prev_rows) else "N/A"
            combined.append([row[0], row[1], prev_val])

        print(tabulate(combined, headers=headers, tablefmt="simple"))
    else:
        rows = build_metrics_table(insight)
        print(tabulate(rows, headers=["Metric", "Value"], tablefmt="simple"))

    # Actions breakdown
    print_actions_breakdown(insight)


if __name__ == "__main__":
    main()
