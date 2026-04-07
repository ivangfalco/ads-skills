"""
High-level account performance overview.

Usage:
    python account_overview.py                  # Last 30 days
    python account_overview.py --date-range last_7d
    python account_overview.py --compare        # Compare to previous period
"""

import argparse
from datetime import datetime, timedelta
from client import get_client, get_customer_id
from tabulate import tabulate


DATE_RANGES = {"last_7d": 7, "last_14d": 14, "last_30d": 30, "last_90d": 90}


def get_date_range(days: int, offset: int = 0):
    end = datetime.now() - timedelta(days=offset)
    start = end - timedelta(days=days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def fetch_account_metrics(ga_service, customer_id, start_date, end_date):
    query = f"""
        SELECT
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.all_conversions,
            metrics.interactions
        FROM customer
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """
    response = ga_service.search(customer_id=customer_id, query=query)

    totals = {"impressions": 0, "clicks": 0, "cost": 0, "conversions": 0, "conv_value": 0}
    for row in response:
        m = row.metrics
        totals["impressions"] += m.impressions
        totals["clicks"] += m.clicks
        totals["cost"] += m.cost_micros / 1_000_000
        totals["conversions"] += m.conversions
        totals["conv_value"] += m.conversions_value

    totals["ctr"] = (totals["clicks"] / totals["impressions"] * 100) if totals["impressions"] > 0 else 0
    totals["cpc"] = (totals["cost"] / totals["clicks"]) if totals["clicks"] > 0 else 0
    totals["cpa"] = (totals["cost"] / totals["conversions"]) if totals["conversions"] > 0 else 0
    totals["roas"] = (totals["conv_value"] / totals["cost"]) if totals["cost"] > 0 else 0
    totals["conv_rate"] = (totals["conversions"] / totals["clicks"] * 100) if totals["clicks"] > 0 else 0

    return totals


def fetch_campaign_breakdown(ga_service, customer_id, start_date, end_date):
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
            AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
        LIMIT 15
    """
    response = ga_service.search(customer_id=customer_id, query=query)
    campaigns = []
    for row in response:
        c = row.campaign
        m = row.metrics
        cost = m.cost_micros / 1_000_000 if m.cost_micros else 0
        ctr = (m.clicks / m.impressions * 100) if m.impressions > 0 else 0
        roas = (m.conversions_value / cost) if cost > 0 else 0
        campaigns.append({
            "name": c.name, "status": c.status.name, "type": c.advertising_channel_type.name,
            "impressions": m.impressions, "clicks": m.clicks, "cost": cost,
            "conversions": m.conversions, "conv_value": m.conversions_value,
            "ctr": ctr, "roas": roas,
        })
    return campaigns


def account_overview(date_range: str = "last_30d", compare: bool = False):
    client = get_client()
    customer_id = get_customer_id()
    ga_service = client.get_service("GoogleAdsService")

    days = DATE_RANGES.get(date_range, 30)
    start, end = get_date_range(days)

    print(f"\n{'='*60}")
    print(f"  GOOGLE ADS ACCOUNT OVERVIEW")
    print(f"  Account: {customer_id}")
    print(f"  Period: {start} to {end} ({date_range})")
    print(f"{'='*60}")

    current = fetch_account_metrics(ga_service, customer_id, start, end)

    metrics_table = [
        ["Impressions", f"{current['impressions']:,}"],
        ["Clicks", f"{current['clicks']:,}"],
        ["CTR", f"{current['ctr']:.2f}%"],
        ["Avg CPC", f"${current['cpc']:.2f}"],
        ["Total Spend", f"${current['cost']:,.2f}"],
        ["Conversions", f"{current['conversions']:.1f}"],
        ["Conv Rate", f"{current['conv_rate']:.2f}%"],
        ["Cost/Conv", f"${current['cpa']:.2f}"],
        ["Conv Value", f"${current['conv_value']:,.2f}"],
        ["ROAS", f"{current['roas']:.2f}x"],
    ]

    if compare:
        prev_start, prev_end = get_date_range(days, offset=days)
        previous = fetch_account_metrics(ga_service, customer_id, prev_start, prev_end)

        def delta(curr, prev):
            if prev == 0:
                return "n/a"
            change = ((curr - prev) / prev) * 100
            arrow = "+" if change > 0 else "" if change < 0 else ""
            return f"{arrow}{change:.1f}%"

        metrics_table[0].append(delta(current["impressions"], previous["impressions"]))
        metrics_table[1].append(delta(current["clicks"], previous["clicks"]))
        metrics_table[2].append(delta(current["ctr"], previous["ctr"]))
        metrics_table[3].append(delta(current["cpc"], previous["cpc"]))
        metrics_table[4].append(delta(current["cost"], previous["cost"]))
        metrics_table[5].append(delta(current["conversions"], previous["conversions"]))
        metrics_table[6].append(delta(current["conv_rate"], previous["conv_rate"]))
        metrics_table[7].append(delta(current["cpa"], previous["cpa"]))
        metrics_table[8].append(delta(current["conv_value"], previous["conv_value"]))
        metrics_table[9].append(delta(current["roas"], previous["roas"]))

        headers = ["Metric", "Current", f"vs Previous {days}d"]
    else:
        headers = ["Metric", "Value"]

    print(f"\n  ACCOUNT METRICS")
    print(tabulate(metrics_table, headers=headers, tablefmt="simple"))

    campaigns = fetch_campaign_breakdown(ga_service, customer_id, start, end)

    if campaigns:
        camp_rows = []
        for c in campaigns:
            camp_rows.append([
                c["name"][:30],
                c["status"],
                c["type"][:8],
                f"{c['impressions']:,}",
                f"{c['clicks']:,}",
                f"${c['cost']:,.2f}",
                f"{c['conversions']:.1f}",
                f"{c['roas']:.2f}x",
            ])

        print(f"\n  TOP CAMPAIGNS BY SPEND")
        camp_headers = ["Campaign", "Status", "Type", "Impr", "Clicks", "Cost", "Conv", "ROAS"]
        print(tabulate(camp_rows, headers=camp_headers, tablefmt="simple"))

    print(f"\n{'='*60}")
    print(f"  Run 'python get_campaign_performance.py' for detailed breakdowns")
    print(f"  Run 'python search_terms_report.py' for search term analysis")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Ads account overview")
    parser.add_argument("--date-range", default="last_30d", choices=list(DATE_RANGES.keys()))
    parser.add_argument("--compare", action="store_true", help="Compare to previous period")
    args = parser.parse_args()

    account_overview(args.date_range, args.compare)
