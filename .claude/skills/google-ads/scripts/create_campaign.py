"""
Create a new Google Ads campaign.

Usage:
    python create_campaign.py --name "Brand - Search" --type SEARCH --budget 50
    python create_campaign.py --name "Retargeting - Display" --type DISPLAY --budget 30 --bidding MAXIMIZE_CONVERSIONS
    python create_campaign.py --name "PMax - All Products" --type PERFORMANCE_MAX --budget 100

Campaign types: SEARCH, DISPLAY, SHOPPING, PERFORMANCE_MAX, VIDEO, DISCOVERY
Bidding strategies: MAXIMIZE_CONVERSIONS, MAXIMIZE_CONVERSION_VALUE, TARGET_CPA, TARGET_ROAS, MANUAL_CPC
"""

import argparse
import sys
from client import get_client, get_customer_id


CHANNEL_TYPES = {
    "SEARCH": "SEARCH",
    "DISPLAY": "DISPLAY",
    "SHOPPING": "SHOPPING",
    "PERFORMANCE_MAX": "PERFORMANCE_MAX",
    "VIDEO": "VIDEO",
    "DISCOVERY": "DISCOVERY",
}

BIDDING_STRATEGIES = {
    "MAXIMIZE_CONVERSIONS": "maximize_conversions",
    "MAXIMIZE_CONVERSION_VALUE": "maximize_conversion_value",
    "TARGET_CPA": "target_cpa",
    "TARGET_ROAS": "target_roas",
    "MANUAL_CPC": "manual_cpc",
}


def create_campaign(name: str, campaign_type: str, daily_budget: float,
                    bidding: str = "MAXIMIZE_CONVERSIONS",
                    target_cpa: float = None, target_roas: float = None,
                    paused: bool = False):
    client = get_client()
    customer_id = get_customer_id()

    # Step 1: Create campaign budget
    budget_service = client.get_service("CampaignBudgetService")
    budget_operation = client.get_type("CampaignBudgetOperation")
    budget = budget_operation.create

    budget.name = f"{name} Budget"
    budget.amount_micros = int(daily_budget * 1_000_000)
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD

    if campaign_type == "PERFORMANCE_MAX":
        budget.explicitly_shared = False

    budget_response = budget_service.mutate_campaign_budgets(
        customer_id=customer_id,
        operations=[budget_operation],
    )
    budget_resource = budget_response.results[0].resource_name
    print(f"Created budget: ${daily_budget}/day")

    # Step 2: Create campaign
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create

    campaign.name = name
    campaign.campaign_budget = budget_resource
    campaign.advertising_channel_type = getattr(
        client.enums.AdvertisingChannelTypeEnum, campaign_type
    )

    # Always start paused for safety
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    print("  (Starting as PAUSED for safety -- enable when ready)")

    # Bidding strategy
    if bidding == "MAXIMIZE_CONVERSIONS":
        campaign.maximize_conversions.target_cpa_micros = (
            int(target_cpa * 1_000_000) if target_cpa else 0
        )
    elif bidding == "MAXIMIZE_CONVERSION_VALUE":
        campaign.maximize_conversion_value.target_roas = target_roas or 0
    elif bidding == "TARGET_CPA":
        if not target_cpa:
            print("ERROR: --target-cpa is required for TARGET_CPA bidding")
            sys.exit(1)
        campaign.target_cpa.target_cpa_micros = int(target_cpa * 1_000_000)
    elif bidding == "TARGET_ROAS":
        if not target_roas:
            print("ERROR: --target-roas is required for TARGET_ROAS bidding")
            sys.exit(1)
        campaign.target_roas.target_roas = target_roas
    elif bidding == "MANUAL_CPC":
        campaign.manual_cpc.enhanced_cpc_enabled = True

    # Network settings (for Search campaigns)
    if campaign_type == "SEARCH":
        campaign.network_settings.target_google_search = True
        campaign.network_settings.target_search_network = False
        campaign.network_settings.target_content_network = False

    campaign_response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[campaign_operation],
    )
    campaign_resource = campaign_response.results[0].resource_name
    campaign_id = campaign_resource.split("/")[-1]

    print(f"Created campaign: '{name}'")
    print(f"  ID: {campaign_id}")
    print(f"  Type: {campaign_type}")
    print(f"  Bidding: {bidding}")
    print(f"  Budget: ${daily_budget}/day")
    print(f"\nNext steps:")
    print(f"  1. Create ad groups: python create_ad_group.py --campaign-id {campaign_id} --name 'My Ad Group'")
    print(f"  2. Add keywords:     python add_keywords.py --ad-group-id <id> --keywords 'keyword1, keyword2'")
    print(f"  3. Create ads:       python create_ad.py --ad-group-id <id>")
    print(f"  4. Enable campaign:  python update_campaign.py --campaign-id {campaign_id} --status ENABLED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Google Ads campaign")
    parser.add_argument("--name", required=True, help="Campaign name")
    parser.add_argument("--type", required=True, choices=list(CHANNEL_TYPES.keys()),
                        dest="campaign_type", help="Campaign type")
    parser.add_argument("--budget", required=True, type=float, help="Daily budget in dollars")
    parser.add_argument("--bidding", default="MAXIMIZE_CONVERSIONS",
                        choices=list(BIDDING_STRATEGIES.keys()), help="Bidding strategy")
    parser.add_argument("--target-cpa", type=float, help="Target CPA in dollars")
    parser.add_argument("--target-roas", type=float, help="Target ROAS (e.g., 3.0 = 300%)")
    parser.add_argument("--paused", action="store_true", help="Create in paused state")
    args = parser.parse_args()

    create_campaign(
        name=args.name,
        campaign_type=args.campaign_type,
        daily_budget=args.budget,
        bidding=args.bidding,
        target_cpa=args.target_cpa,
        target_roas=args.target_roas,
        paused=args.paused,
    )
