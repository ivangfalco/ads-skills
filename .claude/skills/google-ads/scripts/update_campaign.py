"""
Update an existing campaign (status, budget, name, bidding).

Usage:
    python update_campaign.py --campaign-id 123456 --status ENABLED
    python update_campaign.py --campaign-id 123456 --status PAUSED
    python update_campaign.py --campaign-id 123456 --budget 75
    python update_campaign.py --campaign-id 123456 --name "New Campaign Name"
    python update_campaign.py --campaign-id 123456 --status ENABLED --budget 100
"""

import argparse
from google.api_core import protobuf_helpers
from client import get_client, get_customer_id


def update_campaign(campaign_id: int, status: str = None, budget: float = None, name: str = None):
    client = get_client()
    customer_id = get_customer_id()

    changes_made = []

    if status or name:
        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.update

        campaign.resource_name = campaign_service.campaign_path(customer_id, campaign_id)

        field_mask_paths = []

        if status:
            campaign.status = getattr(client.enums.CampaignStatusEnum, status.upper())
            field_mask_paths.append("status")
            changes_made.append(f"Status -> {status.upper()}")

        if name:
            campaign.name = name
            field_mask_paths.append("name")
            changes_made.append(f"Name -> '{name}'")

        client.copy_from(campaign_operation.update_mask, protobuf_helpers.field_mask(None, campaign, field_mask_paths))

        campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation],
        )

    if budget is not None:
        ga_service = client.get_service("GoogleAdsService")
        query = f"""
            SELECT campaign.campaign_budget
            FROM campaign
            WHERE campaign.id = {campaign_id}
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        budget_resource = None
        for row in response:
            budget_resource = row.campaign.campaign_budget
            break

        if budget_resource:
            budget_service = client.get_service("CampaignBudgetService")
            budget_operation = client.get_type("CampaignBudgetOperation")
            budget_obj = budget_operation.update

            budget_obj.resource_name = budget_resource
            budget_obj.amount_micros = int(budget * 1_000_000)

            client.copy_from(
                budget_operation.update_mask,
                protobuf_helpers.field_mask(None, budget_obj, ["amount_micros"])
            )

            budget_service.mutate_campaign_budgets(
                customer_id=customer_id,
                operations=[budget_operation],
            )
            changes_made.append(f"Budget -> ${budget:.2f}/day")

    if changes_made:
        print(f"Updated campaign {campaign_id}:")
        for change in changes_made:
            print(f"  - {change}")
    else:
        print("No changes specified. Use --status, --budget, or --name.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Google Ads campaign")
    parser.add_argument("--campaign-id", required=True, type=int, help="Campaign ID to update")
    parser.add_argument("--status", choices=["ENABLED", "PAUSED"], help="New status")
    parser.add_argument("--budget", type=float, help="New daily budget in dollars")
    parser.add_argument("--name", help="New campaign name")
    args = parser.parse_args()

    update_campaign(args.campaign_id, args.status, args.budget, args.name)
