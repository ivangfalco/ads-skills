"""
Shared Google Ads API client.
All scripts import get_client() from here.
"""

import sys
from google.ads.googleads.client import GoogleAdsClient
from config import get_config, validate_config


def get_client() -> GoogleAdsClient:
    """Authenticate and return a GoogleAdsClient instance."""
    config = get_config()

    missing = validate_config(config)
    if missing:
        print(f"ERROR: Missing credentials in .env: {', '.join(missing)}")
        print("Run: python setup_oauth.py  — to generate OAuth2 tokens.")
        print("See README.md for full setup instructions.")
        sys.exit(1)

    credentials = {
        "developer_token": config["developer_token"],
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "refresh_token": config["refresh_token"],
        "use_proto_plus": True,
    }

    if config["login_customer_id"]:
        credentials["login_customer_id"] = config["login_customer_id"]

    return GoogleAdsClient.load_from_dict(credentials)


def get_customer_id() -> str:
    """Return the customer ID from config (no dashes)."""
    config = get_config()
    return config["customer_id"].replace("-", "")
