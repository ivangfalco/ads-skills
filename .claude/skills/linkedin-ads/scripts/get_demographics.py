#!/usr/bin/env python3
"""
Demographics breakdown for LinkedIn Ads campaigns.

Usage:
    python get_demographics.py                                           # All pivots, last 30 days
    python get_demographics.py --pivot JOB_FUNCTION                      # Single pivot
    python get_demographics.py --campaign-id 123456 --pivot MEMBER_SENIORITY
    python get_demographics.py --date-range last_7d --pivot MEMBER_INDUSTRY
    python get_demographics.py --pivot MEMBER_COMPANY_SIZE --pivot MEMBER_COUNTRY

Pivots: JOB_FUNCTION, MEMBER_SENIORITY, MEMBER_COMPANY_SIZE, MEMBER_INDUSTRY, MEMBER_COUNTRY
"""

import argparse
import sys
from datetime import datetime, timedelta
from client import get_session, get_account_id, BASE_URL
from tabulate import tabulate


DATE_RANGES = {"last_7d": 7, "last_14d": 14, "last_30d": 30, "last_90d": 90}

ALL_PIVOTS = [
    "MEMBER_JOB_FUNCTION",
    "MEMBER_SENIORITY",
    "MEMBER_COMPANY_SIZE",
    "MEMBER_INDUSTRY",
    "MEMBER_COUNTRY_V2",
]

PIVOT_MAP = {
    "JOB_FUNCTION": "MEMBER_JOB_FUNCTION",
    "MEMBER_SENIORITY": "MEMBER_SENIORITY",
    "MEMBER_COMPANY_SIZE": "MEMBER_COMPANY_SIZE",
    "MEMBER_INDUSTRY": "MEMBER_INDUSTRY",
    "MEMBER_COUNTRY": "MEMBER_COUNTRY_V2",
}


def parse_dates(args):
    days = DATE_RANGES.get(args.date_range, 30)
    e = datetime.now()
    s = e - timedelta(days=days)
    return (
        {"year": s.year, "month": s.month, "day": s.day},
        {"year": e.year, "month": e.month, "day": e.day},
    )


def date_label(d: dict) -> str:
    return f"{d['year']}-{d['month']:02d}-{d['day']:02d}"


def fetch_demographics(session, account_id, pivot, start, end, campaign_id=None):
    """Fetch demographics for a single pivot."""
    params = {
        "q": "analytics",
        "pivot": pivot,
        "dateRange.start.year": start["year"],
        "dateRange.start.month": start["month"],
        "dateRange.start.day": start["day"],
        "dateRange.end.year": end["year"],
        "dateRange.end.month": end["month"],
        "dateRange.end.day": end["day"],
        "timeGranularity": "ALL",
        "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
    }

    if campaign_id:
        params["campaigns[0]"] = f"urn:li:sponsoredCampaign:{campaign_id}"

    resp = session.get(f"{BASE_URL}/adAnalytics", params=params)
    if resp.status_code != 200:
        print(f"  WARNING: Failed to fetch {pivot}: {resp.status_code}")
        return []

    data = resp.json()
    elements = data.get("elements", [])

    segments = []
    for el in elements:
        pivot_value = el.get("pivotValue", "")
        # Clean up URN for display
        display_value = pivot_value.split(":")[-1] if ":" in pivot_value else pivot_value

        impressions = el.get("impressions", 0)
        clicks = el.get("clicks", 0)
        spend = float(el.get("costInLocalCurrency", "0"))
        conversions = el.get("externalWebsiteConversions", 0) + el.get("oneClickLeads", 0)
        ctr = (clicks / impressions * 100) if impressions > 0 else 0

        segments.append({
            "segment": display_value,
            "impressions": impressions,
            "clicks": clicks,
            "spend": spend,
            "conversions": conversions,
            "ctr": ctr,
        })

    # Sort by spend descending
    segments.sort(key=lambda s: s["spend"], reverse=True)
    return segments


def get_demographics(args):
    session = get_session()
    account_id = get_account_id()
    start, end = parse_dates(args)

    # Determine which pivots to run
    if args.pivot:
        pivots = [PIVOT_MAP.get(p, p) for p in args.pivot]
    else:
        pivots = ALL_PIVOTS

    print(f"\n{'='*60}")
    print(f"  LINKEDIN ADS DEMOGRAPHICS BREAKDOWN")
    print(f"  Account: {account_id}")
    if args.campaign_id:
        print(f"  Campaign: {args.campaign_id}")
    print(f"  Period: {date_label(start)} to {date_label(end)}")
    print(f"{'='*60}")

    for pivot in pivots:
        # Friendly name
        friendly = pivot.replace("MEMBER_", "").replace("_V2", "").replace("_", " ").title()

        segments = fetch_demographics(session, account_id, pivot, start, end, args.campaign_id)

        if not segments:
            print(f"\n  {friendly}: No data")
            continue

        rows = []
        for s in segments[:20]:  # Top 20 per pivot
            rows.append([
                s["segment"][:40],
                f"{s['impressions']:,}",
                f"{s['clicks']:,}",
                f"{s['ctr']:.2f}%",
                f"${s['spend']:,.2f}",
                f"{s['conversions']:,}",
            ])

        print(f"\n  {friendly.upper()}")
        headers = ["Segment", "Impr", "Clicks", "CTR", "Spend", "Conv"]
        print(tabulate(rows, headers=headers, tablefmt="simple"))

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Ads demographics breakdown")
    parser.add_argument("--campaign-id", type=int, help="Filter by campaign ID")
    parser.add_argument("--pivot", action="append",
                        choices=list(PIVOT_MAP.keys()),
                        help="Demographic pivot(s) to show (default: all)")
    parser.add_argument("--date-range", default="last_30d",
                        choices=list(DATE_RANGES.keys()),
                        help="Preset date range (default: last_30d)")
    args = parser.parse_args()
    get_demographics(args)
