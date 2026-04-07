#!/usr/bin/env python3
"""
Fetch ALL active ads in a Meta ad account with full creative/copy details.

Retrieves: ad name, ad ID, body text, headline, description, destination URL,
creative type (image/video/carousel), and CTA type.

Handles link_data, video_data, and asset_feed_spec creative formats.

Usage:
    python get_active_ads_copy.py                              # Uses META_AD_ACCOUNT_ID from .env
    python get_active_ads_copy.py --account-id act_XXXXXXXXX   # Specify account
"""

import argparse
import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_VERSION = 'v22.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'


def get_token():
    token = os.getenv('META_ACCESS_TOKEN')
    if not token:
        print('Error: META_ACCESS_TOKEN not found in .env')
        sys.exit(1)
    return token


def get_account_id():
    account_id = os.getenv('META_AD_ACCOUNT_ID')
    if not account_id:
        print('Error: META_AD_ACCOUNT_ID not found in .env')
        sys.exit(1)
    return account_id


def api_get(endpoint, params, token):
    """Make a GET request to the Meta API with pagination support."""
    params['access_token'] = token
    all_data = []
    url = f'{BASE_URL}/{endpoint}'

    while url:
        resp = requests.get(url, params=params)
        data = resp.json()

        if 'error' in data:
            print(f"API Error: {data['error']}")
            return None

        all_data.extend(data.get('data', []))

        # Pagination
        paging = data.get('paging', {})
        url = paging.get('next')
        params = {}  # next URL already contains params

    return all_data


def get_active_ads(account_id, token):
    """Get all active ads in the account."""
    endpoint = f'{account_id}/ads'
    params = {
        'effective_status': '["ACTIVE"]',
        'fields': 'id,name,creative{id}',
        'limit': 100,
    }
    return api_get(endpoint, params, token)


def get_creative_details(creative_id, token):
    """Get full creative details including ad copy."""
    endpoint = creative_id
    params = {
        'fields': (
            'id,name,body,title,link_url,call_to_action_type,'
            'object_story_spec,asset_feed_spec,'
            'effective_object_story_id,thumbnail_url'
        ),
    }
    params['access_token'] = token
    url = f'{BASE_URL}/{endpoint}'

    resp = requests.get(url, params=params)
    data = resp.json()

    if 'error' in data:
        print(f"  Error fetching creative {creative_id}: {data['error'].get('message', data['error'])}")
        return None

    return data


def extract_copy_from_link_data(link_data):
    """Extract copy fields from link_data (single image/link ads)."""
    return {
        'body': link_data.get('message', ''),
        'headline': link_data.get('name', ''),
        'description': link_data.get('description', ''),
        'url': link_data.get('link', ''),
        'cta': link_data.get('call_to_action', {}).get('type', ''),
        'type': 'IMAGE',
    }


def extract_copy_from_video_data(video_data, message=''):
    """Extract copy fields from video_data."""
    return {
        'body': message or video_data.get('message', ''),
        'headline': video_data.get('title', ''),
        'description': video_data.get('link_description', ''),
        'url': video_data.get('link', '') or video_data.get('call_to_action', {}).get('value', {}).get('link', ''),
        'cta': video_data.get('call_to_action', {}).get('type', ''),
        'type': 'VIDEO',
    }


def extract_copy_from_asset_feed(asset_feed_spec):
    """Extract copy fields from asset_feed_spec (dynamic creative / multiple assets)."""
    bodies = asset_feed_spec.get('bodies', [])
    titles = asset_feed_spec.get('titles', [])
    descriptions = asset_feed_spec.get('descriptions', [])
    link_urls = asset_feed_spec.get('link_urls', [])
    call_to_action_types = asset_feed_spec.get('call_to_action_types', [])
    videos = asset_feed_spec.get('videos', [])
    images = asset_feed_spec.get('images', [])

    # Determine type
    if videos:
        ad_type = 'VIDEO (Dynamic Creative)'
    elif images:
        ad_type = 'IMAGE (Dynamic Creative)'
    else:
        ad_type = 'DYNAMIC CREATIVE'

    # Collect all body variants
    body_texts = [b.get('text', '') for b in bodies] if bodies else []
    headline_texts = [t.get('text', '') for t in titles] if titles else []
    desc_texts = [d.get('text', '') for d in descriptions] if descriptions else []
    urls = [u.get('website_url', '') for u in link_urls] if link_urls else []

    # Get CTAs
    cta_list = []
    if call_to_action_types:
        cta_list = [c.get('value', '') if isinstance(c, dict) else c for c in call_to_action_types]
    ctas_alt = asset_feed_spec.get('call_to_actions', [])
    if ctas_alt:
        for cta_obj in ctas_alt:
            cta_type = cta_obj.get('type', '')
            if cta_type and cta_type not in cta_list:
                cta_list.append(cta_type)

    return {
        'body': '\n---\n'.join(body_texts) if body_texts else '',
        'headline': '\n---\n'.join(headline_texts) if headline_texts else '',
        'description': '\n---\n'.join(desc_texts) if desc_texts else '',
        'url': '\n'.join(urls) if urls else '',
        'cta': ', '.join(cta_list) if cta_list else '',
        'type': ad_type,
        'body_count': len(body_texts),
        'headline_count': len(headline_texts),
    }


def extract_copy_from_creative(creative):
    """Parse creative data and extract copy regardless of format."""
    result = {
        'body': '',
        'headline': '',
        'description': '',
        'url': '',
        'cta': '',
        'type': 'UNKNOWN',
    }

    # Check object_story_spec first (most common)
    oss = creative.get('object_story_spec', {})

    if oss:
        link_data = oss.get('link_data', {})
        if link_data:
            if link_data.get('child_attachments'):
                children = link_data['child_attachments']
                result['type'] = 'CAROUSEL'
                result['body'] = link_data.get('message', '')
                result['url'] = link_data.get('link', '')
                result['cta'] = link_data.get('call_to_action', {}).get('type', '')

                cards = []
                for i, child in enumerate(children, 1):
                    card = {
                        'headline': child.get('name', ''),
                        'description': child.get('description', ''),
                        'url': child.get('link', ''),
                        'cta': child.get('call_to_action', {}).get('type', ''),
                    }
                    cards.append(card)

                result['carousel_cards'] = cards
                if cards:
                    result['headline'] = cards[0].get('headline', '')
                    result['description'] = cards[0].get('description', '')
                return result
            else:
                return extract_copy_from_link_data(link_data)

        video_data = oss.get('video_data', {})
        if video_data:
            return extract_copy_from_video_data(video_data, video_data.get('message', ''))

    # Check for asset_feed_spec (dynamic creative)
    afs = creative.get('asset_feed_spec', {})
    if afs:
        return extract_copy_from_asset_feed(afs)

    # Fallback: use top-level fields
    result['body'] = creative.get('body', '')
    result['headline'] = creative.get('title', '')
    result['url'] = creative.get('link_url', '')
    result['cta'] = creative.get('call_to_action_type', '')

    if creative.get('thumbnail_url'):
        result['type'] = 'IMAGE or VIDEO (from top-level fields)'

    return result


def print_ad_details(ad, copy_data):
    """Print formatted ad details."""
    print('=' * 80)
    print(f"AD NAME: {ad['name']}")
    print(f"AD ID:   {ad['id']}")
    print(f"TYPE:    {copy_data['type']}")
    print('-' * 80)

    if copy_data.get('body'):
        print(f"\nBODY TEXT:")
        print(copy_data['body'])

    if copy_data.get('headline'):
        label = 'HEADLINES' if copy_data.get('headline_count', 1) > 1 else 'HEADLINE'
        print(f"\n{label}:")
        print(copy_data['headline'])

    if copy_data.get('description'):
        print(f"\nDESCRIPTION:")
        print(copy_data['description'])

    if copy_data.get('url'):
        print(f"\nDESTINATION URL:")
        print(copy_data['url'])

    if copy_data.get('cta'):
        print(f"\nCTA TYPE: {copy_data['cta']}")

    if copy_data.get('carousel_cards'):
        print(f"\nCAROUSEL CARDS ({len(copy_data['carousel_cards'])}):")
        for i, card in enumerate(copy_data['carousel_cards'], 1):
            print(f"\n  Card {i}:")
            if card.get('headline'):
                print(f"    Headline:    {card['headline']}")
            if card.get('description'):
                print(f"    Description: {card['description']}")
            if card.get('url'):
                print(f"    URL:         {card['url']}")
            if card.get('cta'):
                print(f"    CTA:         {card['cta']}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Fetch active ads with full creative details")
    parser.add_argument("--account-id", help="Meta ad account ID (e.g. act_XXXXXXXXX)")
    args = parser.parse_args()

    token = get_token()
    account_id = args.account_id or get_account_id()

    print(f'Fetching active ads for account {account_id}...\n')

    ads = get_active_ads(account_id, token)
    if ads is None:
        print('Failed to fetch ads.')
        sys.exit(1)

    if not ads:
        print('No active ads found.')
        return

    print(f'Found {len(ads)} active ad(s). Fetching creative details...\n')

    results = []
    for ad in ads:
        creative_ref = ad.get('creative', {})
        creative_id = creative_ref.get('id')

        if not creative_id:
            print(f"  Skipping ad '{ad['name']}' - no creative ID found")
            continue

        creative = get_creative_details(creative_id, token)
        if not creative:
            continue

        copy_data = extract_copy_from_creative(creative)
        results.append((ad, copy_data))

    print(f'\n{"=" * 80}')
    print(f'ACTIVE ADS REPORT - {account_id}')
    print(f'Total: {len(results)} ad(s)')
    print(f'{"=" * 80}\n')

    type_counts = {}
    for ad, copy_data in results:
        ad_type = copy_data['type']
        type_counts[ad_type] = type_counts.get(ad_type, 0) + 1
        print_ad_details(ad, copy_data)

    print('=' * 80)
    print('SUMMARY')
    print('-' * 80)
    print(f'Total active ads: {len(results)}')
    for ad_type, count in sorted(type_counts.items()):
        print(f'  {ad_type}: {count}')
    print('=' * 80)


if __name__ == '__main__':
    main()
