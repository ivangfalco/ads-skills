#!/usr/bin/env python3
"""
List all campaigns in the LinkedIn Ads account.

Usage:
    python list_campaigns.py                       # All campaigns
    python list_campaigns.py --status ACTIVE       # Only active campaigns
    python list_campaigns.py --status PAUSED       # Only paused campaigns
"""

import argparse
import sys
from datetime import datetime, timedelta
from client import get_session, get_account_id, BASE_URL
from tabulate import tabulate


def list_campaigns(status_filter: str = None):
    session = get_session()
    account_id = get_account_id()

    # Fetch campaigns
    params = {"q": "search", "count": 100}
    if status_filter:
        params["search"] = f"(status:(values:List({status_filter.upper()})))"

    resp = session.get(f"{BASE_URL}/adAccounts/{account_id}/adCampaigns", params=params)
    if resp.status_code != 200:
        print(f"ERROR: Failed to fetch campaigns: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    data = resp.json()
    campaigns = data.get("elements", [])

    if not campaigns:
        print("No campaigns found.")
        return

    # Fetch analytics for all campaigns (last 30 days)
    end = datetime.now()
    start = end - timedelta(days=30)
    campaign_ids = [str(c.get("id", "")) for c in campaigns if c.get("id")]

    analytics_map = {}
    if campaign_ids:
        analytics_params = {
            "q": "analytics",
            "pivot": "CAMPAIGN",
            "dateRange.start.year": start.year,
            "dateRange.start.month": start.month,
            "dateRange.start.day": start.day,
            "dateRange.end.year": end.year,
            "dateRange.end.month": end.month,
            "dateRange.end.day": end.day,
            "timeGranularity": "ALL",
            "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
        }
        for i, cid in enumerate(campaign_ids):
            analytics_params[f"campaigns[{i}]"] = f"urn:li:sponsoredCampaign:{cid}"

        a_resp = session.get(f"{BASE_URL}/adAnalytics", params=analytics_params)
        if a_resp.status_code == 200:
            for el in a_resp.json().get("elements", []):
                pivot = el.get("pivotValue", "")
                cid = pivot.split(":")[-1] if pivot else ""
                analytics_map[cid] = el

    rows = []
    for c in campaigns:
        cid = str(c.get("id", ""))
        name = c.get("name", "N/A")
        status = c.get("status", "UNKNOWN")
        campaign_type = c.get("type", "N/A")
        objective = c.get("objectiveType", "N/A")

        # Budget
        daily_budget = c.get("dailyBudget", {})
        budget_amount = daily_budget.get("amount", "0")
        budget_currency = daily_budget.get("currencyCode", "USD")
        budget_display = f"${float(budget_amount):,.2f}" if budget_amount else "-"

        # Analytics
        a = analytics_map.get(cid, {})
        impressions = a.get("impressions", 0)
        clicks = a.get("clicks", 0)
        spend = float(a.get("costInLocalCurrency", "0"))
        conversions = a.get("externalWebsiteConversions", 0) + a.get("oneClickLeads", 0)
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0

        rows.append([
            cid,
            name[:35],
            status,
            campaign_type[:15],
            objective[:20],
            budget_display,
            f"{impressions:,}",
            f"{clicks:,}",
            f"{ctr:.2f}%",
            f"${spend:,.2f}",
            f"${cpc:.2f}" if cpc > 0 else "-",
            f"{conversions:,}",
        ])

    # Sort by spend (column index 9) descending
    rows.sort(key=lambda r: float(r[9].replace("$", "").replace(",", "")), reverse=True)

    headers = [
        "ID", "Name", "Status", "Type", "Objective",
        "Daily Budget", "Impr", "Clicks", "CTR",
        "Spend (30d)", "CPC", "Conv"
    ]

    print(f"\nCampaigns for account {account_id}")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(rows)} campaigns")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List LinkedIn Ads campaigns")
    parser.add_argument("--status", choices=["ACTIVE", "PAUSED", "ARCHIVED"],
                        help="Filter by campaign status")
    args = parser.parse_args()
    list_campaigns(args.status)
