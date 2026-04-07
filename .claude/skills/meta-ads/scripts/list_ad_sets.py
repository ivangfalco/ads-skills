#!/usr/bin/env python3
"""
List Meta Ads ad sets with campaign, status, budget, targeting summary, and metrics.

Usage:
    python list_ad_sets.py                                  # All ad sets
    python list_ad_sets.py --status ACTIVE                  # Only active
    python list_ad_sets.py --campaign-id 12345              # Filter by campaign
    python list_ad_sets.py --campaign-id 12345 --status ACTIVE
"""

import argparse
import sys
from tabulate import tabulate
from client import api_get, get_account_id


def summarize_targeting(targeting):
    """Build a short targeting summary from the targeting spec."""
    if not targeting:
        return "N/A"

    parts = []

    # Age range
    age_min = targeting.get("age_min")
    age_max = targeting.get("age_max")
    if age_min or age_max:
        parts.append(f"Age {age_min or '?'}-{age_max or '?'}")

    # Genders
    genders = targeting.get("genders", [])
    gender_map = {1: "M", 2: "F"}
    if genders:
        g_str = "+".join(gender_map.get(g, str(g)) for g in genders)
        parts.append(g_str)

    # Geo targeting
    geo = targeting.get("geo_locations", {})
    countries = geo.get("countries", [])
    if countries:
        parts.append(",".join(countries[:3]))
        if len(countries) > 3:
            parts.append(f"+{len(countries) - 3} more")

    cities = geo.get("cities", [])
    if cities:
        city_names = [c.get("name", c.get("key", "?")) for c in cities[:2]]
        parts.append(",".join(city_names))
        if len(cities) > 2:
            parts.append(f"+{len(cities) - 2} cities")

    # Custom audiences
    custom_audiences = targeting.get("custom_audiences", [])
    if custom_audiences:
        parts.append(f"{len(custom_audiences)} audiences")

    # Interests
    interests = targeting.get("flexible_spec", [])
    if interests:
        interest_count = sum(len(spec.get("interests", [])) for spec in interests)
        if interest_count:
            parts.append(f"{interest_count} interests")

    return " | ".join(parts) if parts else "Broad"


def fetch_ad_sets(account_id, campaign_id=None, status_filter=None):
    """Fetch ad sets with fields and inline insights."""
    fields = (
        "name,campaign_id,status,effective_status,"
        "daily_budget,lifetime_budget,"
        "targeting,optimization_goal,billing_event,"
        "insights.fields(impressions,clicks,spend,ctr,cpc,actions)"
        ".date_preset(last_30d)"
    )
    params = {"fields": fields, "limit": 200}

    if status_filter:
        params["effective_status"] = f'["{status_filter}"]'

    if campaign_id:
        # Fetch ad sets for a specific campaign
        endpoint = f"{campaign_id}/adsets"
    else:
        endpoint = f"{account_id}/adsets"

    return api_get(endpoint, params)


def extract_conversions(insight):
    """Extract lead/conversion count from actions."""
    actions = insight.get("actions", [])
    conversion_types = [
        "lead", "offsite_conversion", "offsite_conversion.fb_pixel_lead",
        "onsite_conversion.lead_grouped",
    ]
    total = 0
    for action in actions:
        if action.get("action_type") in conversion_types:
            total += int(action.get("value", 0))
    return total


def format_budget(ad_set):
    """Format budget display."""
    daily = ad_set.get("daily_budget")
    lifetime = ad_set.get("lifetime_budget")
    if daily:
        return f"${int(daily) / 100:,.2f}/day"
    if lifetime:
        return f"${int(lifetime) / 100:,.2f} life"
    return "Inherited"


def main():
    parser = argparse.ArgumentParser(description="List Meta Ads ad sets")
    parser.add_argument("--campaign-id", help="Filter by campaign ID")
    parser.add_argument("--status", choices=["ACTIVE", "PAUSED", "ARCHIVED", "DELETED"],
                        help="Filter by effective status")
    parser.add_argument("--account-id", help="Meta ad account ID (default: from .env)")
    args = parser.parse_args()

    account_id = args.account_id or get_account_id()

    print(f"Fetching ad sets for {account_id}...")
    ad_sets = fetch_ad_sets(account_id, args.campaign_id, args.status)

    if ad_sets is None:
        print("Failed to fetch ad sets.")
        sys.exit(1)

    if not ad_sets:
        print("No ad sets found.")
        return

    # Build rows
    rows = []
    for a in ad_sets:
        insights_data = a.get("insights", {}).get("data", [])
        insight = insights_data[0] if insights_data else {}

        spend = float(insight.get("spend", 0))
        conversions = extract_conversions(insight)
        targeting_summary = summarize_targeting(a.get("targeting", {}))

        rows.append({
            "name": a.get("name", ""),
            "id": a.get("id", ""),
            "campaign_id": a.get("campaign_id", ""),
            "status": a.get("effective_status", a.get("status", "")),
            "budget": format_budget(a),
            "optimization": a.get("optimization_goal", ""),
            "targeting": targeting_summary,
            "spend": spend,
            "impressions": int(insight.get("impressions", 0)),
            "clicks": int(insight.get("clicks", 0)),
            "ctr": float(insight.get("ctr", 0)),
            "conversions": conversions,
        })

    # Sort by spend DESC
    rows.sort(key=lambda r: r["spend"], reverse=True)

    # Format table
    table = []
    for r in rows:
        table.append([
            r["name"][:30],
            r["id"],
            r["campaign_id"],
            r["status"],
            r["budget"],
            r["optimization"][:15],
            r["targeting"][:35],
            f"${r['spend']:,.2f}",
            f"{r['impressions']:,}",
            f"{r['clicks']:,}",
            f"{r['ctr']:.2f}%",
            r["conversions"],
        ])

    headers = ["Ad Set", "ID", "Campaign ID", "Status", "Budget",
               "Opt Goal", "Targeting", "Spend (30d)", "Impr", "Clicks", "CTR", "Conv"]

    print(f"\nFound {len(rows)} ad set(s) (last 30 days metrics):\n")
    print(tabulate(table, headers=headers, tablefmt="simple"))

    total_spend = sum(r["spend"] for r in rows)
    print(f"\nTotal spend (30d): ${total_spend:,.2f}")


if __name__ == "__main__":
    main()
