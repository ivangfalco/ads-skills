"""
Configuration loader for Google Ads API.
Reads credentials from .env file in this directory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)


def get_config() -> dict:
    """Return Google Ads API configuration dict."""
    config = {
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", ""),
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET", ""),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN", ""),
        "customer_id": os.getenv("GOOGLE_ADS_CUSTOMER_ID", ""),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", ""),
    }
    return config


def validate_config(config: dict) -> list[str]:
    """Check which required fields are missing. Returns list of missing field names."""
    required = ["developer_token", "client_id", "client_secret", "refresh_token", "customer_id"]
    missing = [f for f in required if not config.get(f)]
    return missing
