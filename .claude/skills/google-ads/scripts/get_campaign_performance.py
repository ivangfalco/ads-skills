"""
Get detailed performance metrics for a specific campaign or all campaigns.

Usage:
    python get_campaign_performance.py --campaign-id 123456789
    python get_campaign_performance.py --date-range last_7d
    python get_campaign_performance.py --start-date 2026-01-01 --end-date 2026-01-31
    python get_campaign_performance.py --campaign-id 123456789 --by-day
"""

import argparse
from datetime import datetime, timedelta
from client import get_client, get_customer_id
from tabulate import tabulate


DATE_RANGES = {
    "today": 0,
    "yesterday": 1,
    "last_7d": 7,
    "last_14d": 14,
    "last_30d": 30,
    "last_90d": 90,
}


def get_date_clause(args) -> str:
    if args.start_date and args.end_date:
        return f"segments.date BETWEEN '{args.start_date}' AND '{args.end_date}'"

    days = DATE_RANGES.get(args.date_range, 30)
    if days == 0:
        today = datetime.now().strftime("%Y-%m-%d")
        return f"segments.date = '{today}'"

    end = datetime.now()
    start = end - timedelta(days=days)
    return f"segments.date BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"


def get_performance(args):
    client = get_client()
    customer_id = get_customer_id()
    ga_service = client.get_service("GoogleAdsService")

    date_clause = get_date_clause(args)

    if args.by_day:
        query = f"""
            SELECT
                segments.date,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.all_conversions,
                metrics.interactions,
                metrics.average_cpc
            FROM campaign
            WHERE {date_clause}
                AND campaign.status != 'REMOVED'
        """
        if args.campaign_id:
            query += f" AND campaign.id = {args.campaign_id}"
        query += " ORDER BY segments.date DESC"
    else:
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.conversions_value,
                metrics.all_conversions,
                metrics.average_cpc,
                metrics.cost_per_conversion,
                metrics.search_impression_share
            FROM campaign
            WHERE {date_clause}
                AND campaign.status != 'REMOVED'
        """
        if args.campaign_id:
            query += f" AND campaign.id = {args.campaign_id}"
        query += " ORDER BY metrics.cost_micros DESC"

    response = ga_service.search(customer_id=customer_id, query=query)

    rows = []
    total_cost = 0
    total_conversions = 0
    total_conv_value = 0

    for row in response:
        m = row.metrics
        cost = m.cost_micros / 1_000_000 if m.cost_micros else 0
        ctr = (m.clicks / m.impressions * 100) if m.impressions > 0 else 0
        conv_rate = (m.conversions / m.clicks * 100) if m.clicks > 0 else 0
        roas = (m.conversions_value / cost) if cost > 0 else 0

        total_cost += cost
        total_conversions += m.conversions
        total_conv_value += m.conversions_value

        if args.by_day:
            rows.append([
                row.segments.date,
                row.campaign.name[:30],
                f"{m.impressions:,}",
                f"{m.clicks:,}",
                f"{ctr:.2f}%",
                f"${cost:,.2f}",
                f"{m.conversions:.1f}",
                f"{conv_rate:.2f}%",
                f"${m.conversions_value:,.2f}",
                f"{roas:.2f}x",
            ])
        else:
            search_is = f"{m.search_impression_share:.1%}" if m.search_impression_share else "-"
            rows.append([
                row.campaign.id,
                row.campaign.name[:30],
                row.campaign.status.name,
                f"{m.impressions:,}",
                f"{m.clicks:,}",
                f"{ctr:.2f}%",
                f"${cost:,.2f}",
                f"{m.conversions:.1f}",
                f"{conv_rate:.2f}%",
                f"${m.conversions_value:,.2f}",
                f"{roas:.2f}x",
                search_is,
            ])

    if not rows:
        print("No data found for the specified criteria.")
        return

    if args.by_day:
        headers = ["Date", "Campaign", "Impr", "Clicks", "CTR", "Cost", "Conv", "Conv%", "Value", "ROAS"]
    else:
        headers = ["ID", "Campaign", "Status", "Impr", "Clicks", "CTR", "Cost", "Conv", "Conv%", "Value", "ROAS", "Search IS"]

    total_roas = (total_conv_value / total_cost) if total_cost > 0 else 0

    print(f"\nCampaign Performance")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\n  Total Spend: ${total_cost:,.2f} | Conversions: {total_conversions:.1f} | "
          f"Conv Value: ${total_conv_value:,.2f} | ROAS: {total_roas:.2f}x")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get campaign performance metrics")
    parser.add_argument("--campaign-id", type=int, help="Specific campaign ID")
    parser.add_argument("--date-range", default="last_30d",
                        choices=list(DATE_RANGES.keys()), help="Preset date range")
    parser.add_argument("--start-date", help="Custom start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="Custom end date (YYYY-MM-DD)")
    parser.add_argument("--by-day", action="store_true", help="Show daily breakdown")
    args = parser.parse_args()
    get_performance(args)
