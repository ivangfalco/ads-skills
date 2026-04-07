"""
Get keyword-level performance metrics.

Usage:
    python get_keyword_performance.py                            # All keywords
    python get_keyword_performance.py --campaign-id 123456       # Keywords in campaign
    python get_keyword_performance.py --ad-group-id 789012       # Keywords in ad group
    python get_keyword_performance.py --date-range last_7d       # Last 7 days
    python get_keyword_performance.py --top 20                   # Top 20 by spend
"""

import argparse
from datetime import datetime, timedelta
from client import get_client, get_customer_id
from tabulate import tabulate


DATE_RANGES = {"last_7d": 7, "last_14d": 14, "last_30d": 30, "last_90d": 90}


def get_keyword_performance(campaign_id: int = None, ad_group_id: int = None,
                            date_range: str = "last_30d", top: int = 50):
    client = get_client()
    customer_id = get_customer_id()
    ga_service = client.get_service("GoogleAdsService")

    days = DATE_RANGES.get(date_range, 30)
    end = datetime.now()
    start = end - timedelta(days=days)
    date_clause = f"segments.date BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"

    conditions = [
        date_clause,
        "ad_group_criterion.status != 'REMOVED'",
        "ad_group_criterion.negative = FALSE",
    ]
    if campaign_id:
        conditions.append(f"campaign.id = {campaign_id}")
    if ad_group_id:
        conditions.append(f"ad_group.id = {ad_group_id}")

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.quality_info.quality_score,
            ad_group.name,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.cost_per_conversion,
            metrics.search_impression_share,
            metrics.top_impression_percentage,
            metrics.absolute_top_impression_percentage
        FROM keyword_view
        WHERE {where_clause}
        ORDER BY metrics.cost_micros DESC
        LIMIT {top}
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    rows = []
    total_cost = 0
    total_conversions = 0

    for row in response:
        kw = row.ad_group_criterion
        m = row.metrics
        cost = m.cost_micros / 1_000_000 if m.cost_micros else 0
        ctr = (m.clicks / m.impressions * 100) if m.impressions > 0 else 0
        qs = kw.quality_info.quality_score if kw.quality_info.quality_score else "-"
        search_is = f"{m.search_impression_share:.0%}" if m.search_impression_share else "-"
        top_is = f"{m.top_impression_percentage:.0%}" if m.top_impression_percentage else "-"

        total_cost += cost
        total_conversions += m.conversions

        match_abbr = {"BROAD": "B", "PHRASE": "P", "EXACT": "E"}.get(kw.keyword.match_type.name, "?")

        rows.append([
            kw.keyword.text[:35],
            match_abbr,
            qs,
            f"{m.impressions:,}",
            f"{m.clicks:,}",
            f"{ctr:.1f}%",
            f"${cost:,.2f}",
            f"{m.conversions:.1f}",
            f"${m.cost_per_conversion:.2f}" if m.cost_per_conversion else "-",
            search_is,
            top_is,
        ])

    if not rows:
        print("No keyword data found.")
        return

    headers = ["Keyword", "M", "QS", "Impr", "Clicks", "CTR", "Cost", "Conv", "CPA", "Search IS", "Top IS"]

    print(f"\nKeyword Performance ({date_range})")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\nShowing top {len(rows)} keywords | Total Spend: ${total_cost:,.2f} | Conversions: {total_conversions:.1f}")
    print(f"  Match types: B=Broad, P=Phrase, E=Exact | QS=Quality Score | IS=Impression Share")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get keyword performance metrics")
    parser.add_argument("--campaign-id", type=int, help="Filter by campaign")
    parser.add_argument("--ad-group-id", type=int, help="Filter by ad group")
    parser.add_argument("--date-range", default="last_30d", choices=list(DATE_RANGES.keys()))
    parser.add_argument("--top", type=int, default=50, help="Top N keywords by spend")
    args = parser.parse_args()

    get_keyword_performance(args.campaign_id, args.ad_group_id, args.date_range, args.top)
