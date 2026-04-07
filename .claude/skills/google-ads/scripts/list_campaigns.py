"""
List all campaigns in the Google Ads account.

Usage:
    python list_campaigns.py                     # All campaigns
    python list_campaigns.py --status ENABLED    # Only active campaigns
    python list_campaigns.py --status PAUSED     # Only paused campaigns
"""

import argparse
from client import get_client, get_customer_id
from tabulate import tabulate


def list_campaigns(status_filter: str = None):
    client = get_client()
    customer_id = get_customer_id()
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            campaign.bidding_strategy_type,
            campaign_budget.amount_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion
        FROM campaign
        WHERE campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """

    if status_filter:
        query = query.replace(
            "WHERE campaign.status != 'REMOVED'",
            f"WHERE campaign.status = '{status_filter.upper()}'"
        )

    response = ga_service.search(customer_id=customer_id, query=query)

    rows = []
    for row in response:
        c = row.campaign
        m = row.metrics
        budget = row.campaign_budget

        budget_daily = budget.amount_micros / 1_000_000 if budget.amount_micros else 0
        cost = m.cost_micros / 1_000_000 if m.cost_micros else 0
        ctr = (m.clicks / m.impressions * 100) if m.impressions > 0 else 0
        cpc = (cost / m.clicks) if m.clicks > 0 else 0
        cost_per_conv = m.cost_per_conversion if m.cost_per_conversion else 0

        rows.append([
            c.id,
            c.name,
            c.status.name,
            c.advertising_channel_type.name,
            c.bidding_strategy_type.name,
            f"${budget_daily:,.2f}",
            f"{m.impressions:,}",
            f"{m.clicks:,}",
            f"{ctr:.2f}%",
            f"${cost:,.2f}",
            f"${cpc:.2f}",
            f"{m.conversions:.1f}",
            f"${cost_per_conv:.2f}",
        ])

    if not rows:
        print("No campaigns found.")
        return

    headers = [
        "ID", "Name", "Status", "Type", "Bidding",
        "Daily Budget", "Impr", "Clicks", "CTR",
        "Cost", "CPC", "Conv", "Cost/Conv"
    ]

    print(f"\nCampaigns for account {customer_id}")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(rows)} campaigns")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Google Ads campaigns")
    parser.add_argument("--status", choices=["ENABLED", "PAUSED"], help="Filter by status")
    args = parser.parse_args()
    list_campaigns(args.status)
