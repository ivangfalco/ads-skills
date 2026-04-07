"""
Search terms report -- see what people actually searched before clicking your ads.
Critical for finding negative keyword opportunities and new keyword ideas.

Usage:
    python search_terms_report.py                          # Last 30 days, all campaigns
    python search_terms_report.py --campaign-id 123456     # Specific campaign
    python search_terms_report.py --date-range last_7d     # Last 7 days
    python search_terms_report.py --min-clicks 5           # Only terms with 5+ clicks
    python search_terms_report.py --no-conversions         # Wasted spend: clicks but no conversions
    python search_terms_report.py --top 100                # Top 100 terms by spend
"""

import argparse
from datetime import datetime, timedelta
from client import get_client, get_customer_id
from tabulate import tabulate


DATE_RANGES = {"last_7d": 7, "last_14d": 14, "last_30d": 30, "last_90d": 90}


def search_terms_report(campaign_id: int = None, date_range: str = "last_30d",
                        min_clicks: int = 1, no_conversions: bool = False, top: int = 50):
    client = get_client()
    customer_id = get_customer_id()
    ga_service = client.get_service("GoogleAdsService")

    days = DATE_RANGES.get(date_range, 30)
    end = datetime.now()
    start = end - timedelta(days=days)
    date_clause = f"segments.date BETWEEN '{start.strftime('%Y-%m-%d')}' AND '{end.strftime('%Y-%m-%d')}'"

    conditions = [date_clause]
    if campaign_id:
        conditions.append(f"campaign.id = {campaign_id}")

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT
            search_term_view.search_term,
            search_term_view.status,
            campaign.name,
            ad_group.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.cost_per_conversion
        FROM search_term_view
        WHERE {where_clause}
        ORDER BY metrics.cost_micros DESC
        LIMIT {top * 2}
    """

    response = ga_service.search(customer_id=customer_id, query=query)

    rows = []
    wasted_spend = 0
    total_cost = 0

    for row in response:
        st = row.search_term_view
        m = row.metrics
        cost = m.cost_micros / 1_000_000 if m.cost_micros else 0
        ctr = (m.clicks / m.impressions * 100) if m.impressions > 0 else 0

        total_cost += cost

        if m.clicks < min_clicks:
            continue

        if no_conversions and m.conversions > 0:
            continue

        if m.conversions == 0:
            wasted_spend += cost

        status_icon = "+" if st.status.name == "ADDED" else "o" if st.status.name == "NONE" else "x"

        rows.append([
            st.search_term[:45],
            status_icon,
            row.campaign.name[:20],
            f"{m.impressions:,}",
            f"{m.clicks:,}",
            f"{ctr:.1f}%",
            f"${cost:,.2f}",
            f"{m.conversions:.1f}",
            f"${m.cost_per_conversion:.2f}" if m.cost_per_conversion else "-",
        ])

        if len(rows) >= top:
            break

    if not rows:
        print("No search term data found.")
        return

    headers = ["Search Term", "S", "Campaign", "Impr", "Clicks", "CTR", "Cost", "Conv", "CPA"]

    title = "WASTED SPEND -- Search Terms (clicks, no conversions)" if no_conversions else "Search Terms Report"
    print(f"\n{title} ({date_range})")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print(f"\nShowing {len(rows)} search terms | Total Spend: ${total_cost:,.2f}")
    print(f"Status: +=Added as keyword  o=Not added  x=Excluded")
    if wasted_spend > 0 and not no_conversions:
        print(f"\nWasted spend (clicks with 0 conversions): ${wasted_spend:,.2f}")
        print(f"   Run with --no-conversions to see only wasted-spend terms")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Ads search terms report")
    parser.add_argument("--campaign-id", type=int, help="Filter by campaign")
    parser.add_argument("--date-range", default="last_30d", choices=list(DATE_RANGES.keys()))
    parser.add_argument("--min-clicks", type=int, default=1, help="Minimum clicks to show")
    parser.add_argument("--no-conversions", action="store_true",
                        help="Only show terms with clicks but no conversions (wasted spend)")
    parser.add_argument("--top", type=int, default=50, help="Top N terms by spend")
    args = parser.parse_args()

    search_terms_report(args.campaign_id, args.date_range, args.min_clicks, args.no_conversions, args.top)
