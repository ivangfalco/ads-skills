"""
Create a Responsive Search Ad (RSA) in an ad group.

Usage:
    python create_ad.py --ad-group-id 123456 \
        --headlines "Headline 1" "Headline 2" "Headline 3" \
        --descriptions "Description 1" "Description 2" \
        --final-url "https://example.com" \
        --path1 "products" --path2 "demo"

Notes:
    - Minimum 3 headlines, maximum 15
    - Minimum 2 descriptions, maximum 4
    - Each headline max 30 chars, each description max 90 chars
"""

import argparse
import sys
from client import get_client, get_customer_id


def create_responsive_search_ad(
    ad_group_id: int,
    headlines: list[str],
    descriptions: list[str],
    final_url: str,
    path1: str = "",
    path2: str = "",
):
    if len(headlines) < 3:
        print("ERROR: Need at least 3 headlines (max 15).")
        sys.exit(1)
    if len(descriptions) < 2:
        print("ERROR: Need at least 2 descriptions (max 4).")
        sys.exit(1)

    for i, h in enumerate(headlines):
        if len(h) > 30:
            print(f"WARNING: Headline {i+1} is {len(h)} chars (max 30): '{h}'")

    for i, d in enumerate(descriptions):
        if len(d) > 90:
            print(f"WARNING: Description {i+1} is {len(d)} chars (max 90): '{d}'")

    client = get_client()
    customer_id = get_customer_id()

    ad_group_service = client.get_service("AdGroupAdService")

    operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = operation.create

    ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = ad_group_ad.ad
    ad.final_urls.append(final_url)

    if path1:
        ad.responsive_search_ad.path1 = path1
    if path2:
        ad.responsive_search_ad.path2 = path2

    for i, headline_text in enumerate(headlines):
        headline = client.get_type("AdTextAsset")
        headline.text = headline_text
        if i == 0:
            headline.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        ad.responsive_search_ad.headlines.append(headline)

    for description_text in descriptions:
        description = client.get_type("AdTextAsset")
        description.text = description_text
        ad.responsive_search_ad.descriptions.append(description)

    response = ad_group_service.mutate_ad_group_ads(
        customer_id=customer_id,
        operations=[operation],
    )

    ad_resource = response.results[0].resource_name

    print(f"Created Responsive Search Ad")
    print(f"  Ad Group: {ad_group_id}")
    print(f"  URL: {final_url}")
    print(f"  Headlines ({len(headlines)}):")
    for h in headlines:
        print(f"    - {h} ({len(h)}/30 chars)")
    print(f"  Descriptions ({len(descriptions)}):")
    for d in descriptions:
        print(f"    - {d} ({len(d)}/90 chars)")
    if path1:
        print(f"  Display URL: example.com/{path1}/{path2}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Responsive Search Ad")
    parser.add_argument("--ad-group-id", required=True, type=int, help="Ad group ID")
    parser.add_argument("--headlines", required=True, nargs="+", help="Headlines (3-15, max 30 chars each)")
    parser.add_argument("--descriptions", required=True, nargs="+", help="Descriptions (2-4, max 90 chars each)")
    parser.add_argument("--final-url", required=True, help="Landing page URL")
    parser.add_argument("--path1", default="", help="Display URL path 1")
    parser.add_argument("--path2", default="", help="Display URL path 2")
    args = parser.parse_args()

    create_responsive_search_ad(
        ad_group_id=args.ad_group_id,
        headlines=args.headlines,
        descriptions=args.descriptions,
        final_url=args.final_url,
        path1=args.path1,
        path2=args.path2,
    )
