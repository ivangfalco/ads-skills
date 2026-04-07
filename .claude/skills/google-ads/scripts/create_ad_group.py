"""
Create an ad group within a campaign.

Usage:
    python create_ad_group.py --campaign-id 123456 --name "Brand Keywords"
    python create_ad_group.py --campaign-id 123456 --name "High Intent" --cpc-bid 3.50
"""

import argparse
from client import get_client, get_customer_id


def create_ad_group(campaign_id: int, name: str, cpc_bid: float = 2.0):
    client = get_client()
    customer_id = get_customer_id()

    campaign_service = client.get_service("CampaignService")
    ad_group_service = client.get_service("AdGroupService")

    operation = client.get_type("AdGroupOperation")
    ad_group = operation.create

    ad_group.name = name
    ad_group.campaign = campaign_service.campaign_path(customer_id, campaign_id)
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ad_group.cpc_bid_micros = int(cpc_bid * 1_000_000)

    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[operation],
    )

    ad_group_resource = response.results[0].resource_name
    ad_group_id = ad_group_resource.split("/")[-1]

    print(f"Created ad group: '{name}'")
    print(f"  ID: {ad_group_id}")
    print(f"  Campaign: {campaign_id}")
    print(f"  CPC Bid: ${cpc_bid:.2f}")
    print(f"\nNext steps:")
    print(f"  1. Add keywords: python add_keywords.py --ad-group-id {ad_group_id} --keywords 'keyword1, keyword2'")
    print(f"  2. Create ads:   python create_ad.py --ad-group-id {ad_group_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Google Ads ad group")
    parser.add_argument("--campaign-id", required=True, type=int, help="Parent campaign ID")
    parser.add_argument("--name", required=True, help="Ad group name")
    parser.add_argument("--cpc-bid", type=float, default=2.0, help="Max CPC bid in dollars (default: $2)")
    args = parser.parse_args()

    create_ad_group(args.campaign_id, args.name, args.cpc_bid)
