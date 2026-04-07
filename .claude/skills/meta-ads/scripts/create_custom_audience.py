#!/usr/bin/env python3
"""
Meta Custom Audience API Upload

Creates custom audiences and uploads hashed customer data via Meta Marketing API.
Supports batched uploads (10,000 users per batch).

Usage:
    python create_custom_audience.py input.csv "My Audience Name"
    python create_custom_audience.py input.csv "My Audience Name" --account-id act_XXXXXXXXX
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_VERSION = 'v22.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

# Country mapping
COUNTRY_MAP = {
    'united states': 'us', 'usa': 'us', 'u.s.': 'us',
    'united kingdom': 'gb', 'uk': 'gb', 'england': 'gb',
    'canada': 'ca', 'australia': 'au', 'germany': 'de',
    'france': 'fr', 'netherlands': 'nl', 'spain': 'es',
    'italy': 'it', 'brazil': 'br', 'india': 'in',
    'singapore': 'sg', 'japan': 'jp', 'israel': 'il',
    'ireland': 'ie', 'switzerland': 'ch', 'sweden': 'se',
    'california': 'us', 'new york': 'us', 'texas': 'us',
    'florida': 'us', 'washington': 'us', 'oregon': 'us',
    'colorado': 'us', 'massachusetts': 'us', 'illinois': 'us',
    'georgia': 'us', 'pennsylvania': 'us', 'ohio': 'us',
}


def sha256(value):
    """SHA256 hash a normalized value."""
    if not value:
        return ''
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def normalize_email(email):
    """Normalize email: lowercase, trim."""
    if not email:
        return ''
    return email.lower().strip()


def normalize_name(name):
    """Normalize name: lowercase, trim, remove special chars."""
    if not name:
        return ''
    name = name.lower().strip()
    name = re.sub(r'\b(phd|dr|mr|mrs|ms|jr|sr|ii|iii|iv)\b\.?', '', name, flags=re.IGNORECASE)
    name = re.sub(r'[^a-z\s]', '', name)
    return ' '.join(name.split()).strip()


def extract_country(location):
    """Extract 2-letter country code from location."""
    if not location:
        return ''
    location_lower = location.lower()
    for name, code in COUNTRY_MAP.items():
        if name in location_lower:
            return code
    return ''


def create_custom_audience(account_id, name, description, token):
    """Create a custom audience and return its ID."""
    url = f'{BASE_URL}/{account_id}/customaudiences'

    payload = {
        'name': name,
        'description': description,
        'subtype': 'CUSTOM',
        'customer_file_source': 'USER_PROVIDED_ONLY',
        'access_token': token,
    }

    resp = requests.post(url, data=payload)
    data = resp.json()

    if 'error' in data:
        print(f"Error creating audience: {data['error']}")
        return None

    audience_id = data.get('id')
    print(f"Created audience '{name}' with ID: {audience_id}")
    return audience_id


def upload_users_batch(audience_id, users_batch, token):
    """Upload a batch of users to the audience."""
    url = f'{BASE_URL}/{audience_id}/users'

    payload = {
        'payload': json.dumps({
            'schema': ['EMAIL', 'FN', 'LN', 'COUNTRY'],
            'data': users_batch
        }),
        'access_token': token,
    }

    resp = requests.post(url, data=payload)
    data = resp.json()

    if 'error' in data:
        print(f"Error uploading batch: {data['error']}")
        return None

    return data


def process_and_upload(input_csv, account_id, audience_name, token, batch_size=10000):
    """Process CSV and upload to Meta audience."""

    print(f"Reading {input_csv}...")
    users = []

    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        fieldnames = reader.fieldnames
        email_col = next((k for k in fieldnames if 'email' in k.lower()), None)
        fn_col = next((k for k in fieldnames if 'first' in k.lower() and 'name' in k.lower()), None)
        ln_col = next((k for k in fieldnames if 'last' in k.lower() and 'name' in k.lower()), None)
        location_col = next((k for k in fieldnames if 'location' in k.lower()), None)

        print(f"Columns: email={email_col}, fn={fn_col}, ln={ln_col}, location={location_col}")

        for row in reader:
            email = normalize_email(row.get(email_col, ''))
            if not email:
                continue

            fn = normalize_name(row.get(fn_col, ''))
            ln = normalize_name(row.get(ln_col, ''))
            country = extract_country(row.get(location_col, ''))

            users.append([
                sha256(email),
                sha256(fn) if fn else '',
                sha256(ln) if ln else '',
                sha256(country) if country else ''
            ])

    print(f"Processed {len(users)} users with valid emails")

    description = f"Custom audience - {len(users)} contacts - Uploaded via API"
    audience_id = create_custom_audience(account_id, audience_name, description, token)

    if not audience_id:
        return None

    total_batches = (len(users) + batch_size - 1) // batch_size

    for i in range(0, len(users), batch_size):
        batch_num = (i // batch_size) + 1
        batch = users[i:i + batch_size]

        print(f"Uploading batch {batch_num}/{total_batches} ({len(batch)} users)...")
        result = upload_users_batch(audience_id, batch, token)

        if result:
            num_received = result.get('num_received', 0)
            num_invalid = result.get('num_invalid_entries', 0)
            print(f"  Received: {num_received}, Invalid: {num_invalid}")

        if batch_num < total_batches:
            time.sleep(1)

    print(f"\nAudience '{audience_name}' created and populated!")
    print(f"   Audience ID: {audience_id}")
    print(f"   View at: https://business.facebook.com/adsmanager/audiences?act={account_id.replace('act_', '')}")

    return audience_id


def main():
    parser = argparse.ArgumentParser(description="Create Meta custom audience from CSV")
    parser.add_argument("input_csv", help="Path to CSV file with contact data")
    parser.add_argument("audience_name", help="Name for the custom audience")
    parser.add_argument("--account-id", help="Meta ad account ID (default: META_AD_ACCOUNT_ID from .env)")
    args = parser.parse_args()

    token = os.getenv('META_ACCESS_TOKEN')
    if not token:
        print("Error: META_ACCESS_TOKEN not found in .env")
        sys.exit(1)

    account_id = args.account_id or os.getenv('META_AD_ACCOUNT_ID')
    if not account_id:
        print("Error: Provide --account-id or set META_AD_ACCOUNT_ID in .env")
        sys.exit(1)

    print(f"=== Meta Custom Audience Upload ===")
    print(f"Account: {account_id}")
    print(f"Audience: {args.audience_name}")
    print(f"Input: {args.input_csv}")
    print()

    process_and_upload(args.input_csv, account_id, args.audience_name, token)


if __name__ == '__main__':
    main()
