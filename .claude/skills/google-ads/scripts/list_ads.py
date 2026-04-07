"""
List ads with performance metrics.

Usage:
    python list_ads.py                              # All ads
    python list_ads.py --campaign-id 123456         # Ads in a campaign
    python list_ads.py --ad-group-id 789012         # Ads in an ad group
"""

import argparse
from client import get_client, get_customer_id
from tabulate import tabulate


def list_ads(campaign_id: int = None, ad_group_id: int = None):
    client = get_client()
    customer_id = get_customer_id()
    ga_service = client.get_service("GoogleAdsService")

    conditions = ["ad_group_ad.status != 'REMOVED'"]
    if campaign_id:
        conditions.append(f"campaign.id = {campaign_id}")
    if ad_group_id:
        conditions.append(f"ad_group.id = {ad_group_id}")

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            ad_group_ad.ad.id,
            ad_group_ad.ad.type,
            ad_group_ad.status,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.final_urls,
            ad_group.name,
            campaign.name,
            ad_group_ad.policy_summary.approval_status,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.all_conversions
        FROM ad_group_ad
        WHERE {where_clause}
        ORDER BY metrics.cost_micros DESC
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    rows = []
    for row in response:
        ad = row.ad_group_ad
        m = row.metrics
        cost = m.cost_micros / 1_000_000 if m.cost_micros else 0
        ctr = (m.clicks / m.impressions * 100) if m.impressions > 0 else 0

        headlines = ad.ad.responsive_search_ad.headlines
        first_headline = headlines[0].text if headlines else "-"

        final_urls = list(ad.ad.final_urls)
        url = final_urls[0][:40] if final_urls else "-"

        rows.append([
            ad.ad.id,
            ad.ad.type_.name[:12],
            ad.status.name,
            ad.policy_summary.approval_status.name[:10],
            first_headline[:25],
            url,
            row.ad_group.name[:20],
            f"{m.impressions:,}",
            f"{m.clicks:,}",
            f"{ctr:.2f}%",
            f"${cost:,.2f}",
            f"{m.conversions:.1f}",
        ])

    if not rows:
        print("No ads found.")
        return

    headers = ["Ad ID", "Type", "Status", "Approval", "Headline", "URL", "Ad Group", "Impr", "Clicks", "CTR", "Cost", "Conv"]
    print(f"\nAds")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\nTotal: {len(rows)} ads")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Google Ads")
    parser.add_argument("--campaign-id", type=int, help="Filter by campaign ID")
    parser.add_argument("--ad-group-id", type=int, help="Filter by ad group ID")
    args = parser.parse_args()
    list_ads(args.campaign_id, args.ad_group_id)
