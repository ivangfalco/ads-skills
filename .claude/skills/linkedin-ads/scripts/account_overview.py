#!/usr/bin/env python3
"""
High-level LinkedIn Ads account performance overview.

Usage:
    python account_overview.py                  # Last 30 days
    python account_overview.py --date-range last_7d
    python account_overview.py --compare        # Compare to previous period
"""

import argparse
import sys
from datetime import datetime, timedelta
from client import get_session, get_account_id, BASE_URL
from tabulate import tabulate


DATE_RANGES = {"last_7d": 7, "last_14d": 14, "last_30d": 30, "last_90d": 90}


def get_date_range(days: int, offset: int = 0):
    """Return (start_date, end_date) as dicts with year/month/day."""
    end = datetime.now() - timedelta(days=offset)
    start = end - timedelta(days=days)
    return (
        {"year": start.year, "month": start.month, "day": start.day},
        {"year": end.year, "month": end.month, "day": end.day},
    )


def date_label(d: dict) -> str:
    return f"{d['year']}-{d['month']:02d}-{d['day']:02d}"


def fetch_account_metrics(session, account_id, start, end):
    """Fetch account-level analytics for a date range."""
    params = {
        "q": "analytics",
        "pivot": "ACCOUNT",
        "dateRange.start.year": start["year"],
        "dateRange.start.month": start["month"],
        "dateRange.start.day": start["day"],
        "dateRange.end.year": end["year"],
        "dateRange.end.month": end["month"],
        "dateRange.end.day": end["day"],
        "timeGranularity": "ALL",
        "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
    }
    resp = session.get(f"{BASE_URL}/adAnalytics", params=params)
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch account analytics: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    elements = data.get("elements", [])

    totals = {"impressions": 0, "clicks": 0, "spend": 0.0, "conversions": 0,
              "externalWebsiteConversions": 0, "oneClickLeads": 0}
    for el in elements:
        totals["impressions"] += el.get("impressions", 0)
        totals["clicks"] += el.get("clicks", 0)
        totals["spend"] += float(el.get("costInLocalCurrency", "0"))
        totals["conversions"] += el.get("externalWebsiteConversions", 0)
        totals["externalWebsiteConversions"] += el.get("externalWebsiteConversions", 0)
        totals["oneClickLeads"] += el.get("oneClickLeads", 0)

    totals["ctr"] = (totals["clicks"] / totals["impressions"] * 100) if totals["impressions"] > 0 else 0
    totals["cpc"] = (totals["spend"] / totals["clicks"]) if totals["clicks"] > 0 else 0
    total_conv = totals["conversions"] + totals["oneClickLeads"]
    totals["total_conversions"] = total_conv
    totals["cpl"] = (totals["spend"] / total_conv) if total_conv > 0 else 0

    return totals


def fetch_top_campaigns(session, account_id, start, end):
    """Fetch campaign-level analytics, sorted by spend."""
    params = {
        "q": "analytics",
        "pivot": "CAMPAIGN",
        "dateRange.start.year": start["year"],
        "dateRange.start.month": start["month"],
        "dateRange.start.day": start["day"],
        "dateRange.end.year": end["year"],
        "dateRange.end.month": end["month"],
        "dateRange.end.day": end["day"],
        "timeGranularity": "ALL",
        "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
    }
    resp = session.get(f"{BASE_URL}/adAnalytics", params=params)
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch campaign analytics: {resp.status_code}")
        print(resp.text)
        return []

    data = resp.json()
    elements = data.get("elements", [])

    campaigns = []
    for el in elements:
        spend = float(el.get("costInLocalCurrency", "0"))
        impressions = el.get("impressions", 0)
        clicks = el.get("clicks", 0)
        conversions = el.get("externalWebsiteConversions", 0) + el.get("oneClickLeads", 0)
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpl = (spend / conversions) if conversions > 0 else 0

        # Extract campaign ID from pivotValue URN
        pivot = el.get("pivotValue", "")
        campaign_id = pivot.split(":")[-1] if pivot else "?"

        campaigns.append({
            "id": campaign_id,
            "impressions": impressions,
            "clicks": clicks,
            "spend": spend,
            "conversions": conversions,
            "ctr": ctr,
            "cpl": cpl,
        })

    # Sort by spend descending
    campaigns.sort(key=lambda c: c["spend"], reverse=True)
    return campaigns[:15]


def account_overview(date_range: str = "last_30d", compare: bool = False):
    session = get_session()
    account_id = get_account_id()

    days = DATE_RANGES.get(date_range, 30)
    start, end = get_date_range(days)

    print(f"\n{'='*60}")
    print(f"  LINKEDIN ADS ACCOUNT OVERVIEW")
    print(f"  Account: {account_id}")
    print(f"  Period: {date_label(start)} to {date_label(end)} ({date_range})")
    print(f"{'='*60}")

    current = fetch_account_metrics(session, account_id, start, end)

    metrics_table = [
        ["Impressions", f"{current['impressions']:,}"],
        ["Clicks", f"{current['clicks']:,}"],
        ["CTR", f"{current['ctr']:.2f}%"],
        ["Avg CPC", f"${current['cpc']:.2f}"],
        ["Total Spend", f"${current['spend']:,.2f}"],
        ["Conversions", f"{current['total_conversions']:,}"],
        ["Lead Form Fills", f"{current['oneClickLeads']:,}"],
        ["Cost per Lead", f"${current['cpl']:.2f}"],
    ]

    if compare:
        prev_start, prev_end = get_date_range(days, offset=days)
        previous = fetch_account_metrics(session, account_id, prev_start, prev_end)

        def delta(curr, prev):
            if prev == 0:
                return "n/a"
            change = ((curr - prev) / prev) * 100
            arrow = "+" if change > 0 else ""
            return f"{arrow}{change:.1f}%"

        metrics_table[0].append(delta(current["impressions"], previous["impressions"]))
        metrics_table[1].append(delta(current["clicks"], previous["clicks"]))
        metrics_table[2].append(delta(current["ctr"], previous["ctr"]))
        metrics_table[3].append(delta(current["cpc"], previous["cpc"]))
        metrics_table[4].append(delta(current["spend"], previous["spend"]))
        metrics_table[5].append(delta(current["total_conversions"], previous["total_conversions"]))
        metrics_table[6].append(delta(current["oneClickLeads"], previous["oneClickLeads"]))
        metrics_table[7].append(delta(current["cpl"], previous["cpl"]))

        headers = ["Metric", "Current", f"vs Previous {days}d"]
    else:
        headers = ["Metric", "Value"]

    print(f"\n  ACCOUNT METRICS")
    print(tabulate(metrics_table, headers=headers, tablefmt="simple"))

    # Top campaigns by spend
    campaigns = fetch_top_campaigns(session, account_id, start, end)
    if campaigns:
        camp_rows = []
        for c in campaigns:
            camp_rows.append([
                c["id"],
                f"{c['impressions']:,}",
                f"{c['clicks']:,}",
                f"{c['ctr']:.2f}%",
                f"${c['spend']:,.2f}",
                f"{c['conversions']:,}",
                f"${c['cpl']:.2f}" if c['cpl'] > 0 else "-",
            ])

        print(f"\n  TOP CAMPAIGNS BY SPEND")
        camp_headers = ["Campaign ID", "Impr", "Clicks", "CTR", "Spend", "Conv", "CPL"]
        print(tabulate(camp_rows, headers=camp_headers, tablefmt="simple"))

    print(f"\n{'='*60}")
    print(f"  Run 'python get_campaign_performance.py' for detailed breakdowns")
    print(f"  Run 'python get_demographics.py' for audience insights")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Ads account overview")
    parser.add_argument("--date-range", default="last_30d", choices=list(DATE_RANGES.keys()),
                        help="Preset date range (default: last_30d)")
    parser.add_argument("--compare", action="store_true", help="Compare to previous period")
    args = parser.parse_args()

    account_overview(args.date_range, args.compare)
