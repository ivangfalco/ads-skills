"""
Add keywords to an ad group.

Usage:
    python add_keywords.py --ad-group-id 123456 --keywords "b2b saas" "crm software" "sales automation"
    python add_keywords.py --ad-group-id 123456 --keywords "project management tool" --match-type PHRASE
    python add_keywords.py --ad-group-id 123456 --keywords "[exact match keyword]" --match-type EXACT

Match types:
    BROAD   - Default. Matches related searches (widest reach)
    PHRASE  - Matches searches containing the phrase meaning
    EXACT   - Matches the exact search intent (tightest control)

Negative keywords:
    python add_keywords.py --ad-group-id 123456 --keywords "free" "cheap" --negative
"""

import argparse
from client import get_client, get_customer_id


def add_keywords(ad_group_id: int, keywords: list[str], match_type: str = "BROAD",
                 negative: bool = False, cpc_bid: float = None):
    client = get_client()
    customer_id = get_customer_id()

    if negative:
        _add_negative_keywords(client, customer_id, ad_group_id, keywords, match_type)
    else:
        _add_positive_keywords(client, customer_id, ad_group_id, keywords, match_type, cpc_bid)


def _add_positive_keywords(client, customer_id, ad_group_id, keywords, match_type, cpc_bid):
    ag_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_service = client.get_service("AdGroupService")

    operations = []
    for kw in keywords:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create

        criterion.ad_group = ad_group_service.ad_group_path(customer_id, ad_group_id)
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = kw.strip()
        criterion.keyword.match_type = getattr(
            client.enums.KeywordMatchTypeEnum, match_type.upper()
        )

        if cpc_bid:
            criterion.cpc_bid_micros = int(cpc_bid * 1_000_000)

        operations.append(operation)

    response = ag_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations,
    )

    print(f"Added {len(response.results)} keywords to ad group {ad_group_id}:")
    for kw in keywords:
        prefix = {"BROAD": "", "PHRASE": '"', "EXACT": "["}
        suffix = {"BROAD": "", "PHRASE": '"', "EXACT": "]"}
        display = f"{prefix[match_type]}{kw}{suffix[match_type]}"
        print(f"  - {display}  ({match_type})")


def _add_negative_keywords(client, customer_id, ad_group_id, keywords, match_type):
    ag_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_service = client.get_service("AdGroupService")

    operations = []
    for kw in keywords:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create

        criterion.ad_group = ad_group_service.ad_group_path(customer_id, ad_group_id)
        criterion.negative = True
        criterion.keyword.text = kw.strip()
        criterion.keyword.match_type = getattr(
            client.enums.KeywordMatchTypeEnum, match_type.upper()
        )

        operations.append(operation)

    response = ag_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations,
    )

    print(f"Added {len(response.results)} NEGATIVE keywords to ad group {ad_group_id}:")
    for kw in keywords:
        print(f"  - -{kw}  ({match_type})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add keywords to a Google Ads ad group")
    parser.add_argument("--ad-group-id", required=True, type=int, help="Ad group ID")
    parser.add_argument("--keywords", required=True, nargs="+", help="Keywords to add")
    parser.add_argument("--match-type", default="BROAD", choices=["BROAD", "PHRASE", "EXACT"],
                        help="Keyword match type (default: BROAD)")
    parser.add_argument("--negative", action="store_true", help="Add as negative keywords")
    parser.add_argument("--cpc-bid", type=float, help="Keyword-level CPC bid override (dollars)")
    args = parser.parse_args()

    add_keywords(args.ad_group_id, args.keywords, args.match_type, args.negative, args.cpc_bid)
