#!/usr/bin/env python3
"""
Get detailed performance metrics for LinkedIn Ads campaigns.

Usage:
    python get_campaign_performance.py                              # All campaigns, last 30 days
    python get_campaign_performance.py --campaign-id 123456789
    python get_campaign_performance.py --date-range last_7d
    python get_campaign_performance.py --start-date 2026-01-01 --end-date 2026-01-31
    python get_campaign_performance.py --campaign-id 123456789 --by-day
"""

import argparse
import sys
from datetime import datetime, timedelta
from client import get_session, get_account_id, BASE_URL
from tabulate import tabulate


DATE_RANGES = {
    "last_7d": 7,
    "last_14d": 14,
    "last_30d": 30,
    "last_90d": 90,
}


def parse_dates(args):
    """Return (start_dict, end_dict) from args."""
    if args.start_date and args.end_date:
        s = datetime.strptime(args.start_date, "%Y-%m-%d")
        e = datetime.strptime(args.end_date, "%Y-%m-%d")
    else:
        days = DATE_RANGES.get(args.date_range, 30)
        e = datetime.now()
        s = e - timedelta(days=days)

    return (
        {"year": s.year, "month": s.month, "day": s.day},
        {"year": e.year, "month": e.month, "day": e.day},
    )


def date_label(d: dict) -> str:
    return f"{d['year']}-{d['month']:02d}-{d['day']:02d}"


def get_performance(args):
    session = get_session()
    account_id = get_account_id()
    start, end = parse_dates(args)

    granularity = "DAILY" if args.by_day else "ALL"

    params = {
        "q": "analytics",
        "pivot": "CAMPAIGN",
        "dateRange.start.year": start["year"],
        "dateRange.start.month": start["month"],
        "dateRange.start.day": start["day"],
        "dateRange.end.year": end["year"],
        "dateRange.end.month": end["month"],
        "dateRange.end.day": end["day"],
        "timeGranularity": granularity,
        "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
    }

    if args.campaign_id:
        params["campaigns[0]"] = f"urn:li:sponsoredCampaign:{args.campaign_id}"

    resp = session.get(f"{BASE_URL}/adAnalytics", params=params)
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch analytics: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    elements = data.get("elements", [])

    if not elements:
        print("No data found for the specified criteria.")
        return

    rows = []
    total_spend = 0
    total_conversions = 0
    total_clicks = 0
    total_impressions = 0

    for el in elements:
        impressions = el.get("impressions", 0)
        clicks = el.get("clicks", 0)
        spend = float(el.get("costInLocalCurrency", "0"))
        ext_conv = el.get("externalWebsiteConversions", 0)
        leads = el.get("oneClickLeads", 0)
        conversions = ext_conv + leads
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0
        cpl = (spend / conversions) if conversions > 0 else 0

        total_spend += spend
        total_conversions += conversions
        total_clicks += clicks
        total_impressions += impressions

        pivot = el.get("pivotValue", "")
        campaign_id = pivot.split(":")[-1] if pivot else "?"

        if args.by_day:
            date_range_info = el.get("dateRange", {})
            ds = date_range_info.get("start", {})
            date_str = f"{ds.get('year', '')}-{ds.get('month', 1):02d}-{ds.get('day', 1):02d}"
            rows.append([
                date_str,
                campaign_id,
                f"{impressions:,}",
                f"{clicks:,}",
                f"{ctr:.2f}%",
                f"${spend:,.2f}",
                f"{conversions:,}",
                f"${cpc:.2f}" if cpc > 0 else "-",
                f"${cpl:.2f}" if cpl > 0 else "-",
            ])
        else:
            rows.append([
                campaign_id,
                f"{impressions:,}",
                f"{clicks:,}",
                f"{ctr:.2f}%",
                f"${spend:,.2f}",
                f"{conversions:,}",
                f"${cpc:.2f}" if cpc > 0 else "-",
                f"${cpl:.2f}" if cpl > 0 else "-",
            ])

    # Sort by spend descending
    if args.by_day:
        rows.sort(key=lambda r: r[0], reverse=True)  # Sort by date
        headers = ["Date", "Campaign ID", "Impr", "Clicks", "CTR", "Spend", "Conv", "CPC", "CPL"]
    else:
        rows.sort(key=lambda r: float(r[4].replace("$", "").replace(",", "")), reverse=True)
        headers = ["Campaign ID", "Impr", "Clicks", "CTR", "Spend", "Conv", "CPC", "CPL"]

    total_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    total_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
    total_cpl = (total_spend / total_conversions) if total_conversions > 0 else 0

    print(f"\n  Campaign Performance: {date_label(start)} to {date_label(end)}")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\n  Totals: Spend ${total_spend:,.2f} | Clicks {total_clicks:,} | "
          f"CTR {total_ctr:.2f}% | Conv {total_conversions:,} | "
          f"CPC ${total_cpc:.2f} | CPL ${total_cpl:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get LinkedIn Ads campaign performance")
    parser.add_argument("--campaign-id", type=int, help="Specific campaign ID")
    parser.add_argument("--date-range", default="last_30d",
                        choices=list(DATE_RANGES.keys()), help="Preset date range (default: last_30d)")
    parser.add_argument("--start-date", help="Custom start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Custom end date (YYYY-MM-DD)")
    parser.add_argument("--by-day", action="store_true", help="Show daily breakdown")
    args = parser.parse_args()
    get_performance(args)
