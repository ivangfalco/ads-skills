#!/usr/bin/env python3
"""
Upload a Target Account List (TAL) or contact list to LinkedIn Ads.

Usage:
    python upload_audience.py --name "Q2 Target Accounts" --file accounts.csv --type COMPANY
    python upload_audience.py --name "Email List - Prospects" --file contacts.csv --type USER

CSV format for COMPANY: One column with company names or domains.
CSV format for USER: Columns for email, firstName, lastName (email required).

Uses the LinkedIn DMP Segments API.
"""

import argparse
import sys
import os
from client import get_session, get_account_id, BASE_URL


AUDIENCE_TYPES = {
    "COMPANY": "COMPANY",
    "USER": "USER",
}


def upload_audience(args):
    session = get_session()
    account_id = get_account_id()

    # Validate file exists
    if not os.path.isfile(args.file):
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)

    file_size = os.path.getsize(args.file)
    if file_size == 0:
        print("ERROR: File is empty.")
        sys.exit(1)

    print(f"\nUploading audience list...")
    print(f"  Name: {args.name}")
    print(f"  File: {args.file} ({file_size:,} bytes)")
    print(f"  Type: {args.type}")

    # Step 1: Create DMP segment
    segment_payload = {
        "account": f"urn:li:sponsoredAccount:{account_id}",
        "name": args.name,
        "type": "DYNAMIC" if args.type == "COMPANY" else "STATIC",
        "status": "ACTIVE",
    }

    resp = session.post(f"{BASE_URL}/dmpSegments", json=segment_payload)
    if resp.status_code not in (200, 201):
        print(f"ERROR: Failed to create DMP segment: {resp.status_code}")
        print(resp.text)
        sys.exit(1)

    segment_id = resp.headers.get("x-restli-id")
    if not segment_id:
        # Try to get from response body
        resp_data = resp.json() if resp.text else {}
        segment_id = resp_data.get("id", "unknown")

    print(f"  Created segment: {segment_id}")

    # Step 2: Request upload URL
    upload_payload = {
        "segment": f"urn:li:dmpSegment:{segment_id}",
        "uploadType": args.type,
    }

    upload_resp = session.post(f"{BASE_URL}/dmpSegments/{segment_id}/uploadUrl", json=upload_payload)
    if upload_resp.status_code not in (200, 201):
        print(f"ERROR: Failed to get upload URL: {upload_resp.status_code}")
        print(upload_resp.text)
        print(f"\nSegment {segment_id} was created but file was not uploaded.")
        print("You may need to upload the file manually through Campaign Manager.")
        sys.exit(1)

    upload_data = upload_resp.json()
    upload_url = upload_data.get("value", {}).get("uploadUrl", "")

    if not upload_url:
        print("ERROR: No upload URL returned.")
        print(f"Response: {upload_data}")
        print(f"\nSegment {segment_id} was created but file was not uploaded.")
        sys.exit(1)

    # Step 3: Upload CSV file
    with open(args.file, "rb") as f:
        file_data = f.read()

    upload_headers = {
        "Content-Type": "text/csv",
        "Authorization": session.headers["Authorization"],
        "LinkedIn-Version": "202601",
    }

    file_resp = session.put(upload_url, data=file_data, headers=upload_headers)
    if file_resp.status_code in (200, 201, 204):
        print(f"\n  Upload successful!")
        print(f"  Segment ID: {segment_id}")
        print(f"  Status: Processing (may take 24-48 hours to match)")
        print(f"\nNext steps:")
        print(f"  1. Wait for LinkedIn to process and match the audience (24-48h)")
        print(f"  2. Use the segment as targeting in your campaigns")
        print(f"  3. Minimum audience size: 300 members for targeting")
    else:
        print(f"ERROR: Failed to upload file: {file_resp.status_code}")
        print(file_resp.text)
        print(f"\nSegment {segment_id} was created but file upload failed.")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload audience list to LinkedIn Ads")
    parser.add_argument("--name", required=True, help="Audience list name")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--type", required=True, choices=list(AUDIENCE_TYPES.keys()),
                        help="Audience type: COMPANY (account list) or USER (contact list)")
    args = parser.parse_args()
    upload_audience(args)
