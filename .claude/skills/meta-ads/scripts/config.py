"""
Configuration loader for Meta Marketing API.
Reads credentials from .env file in this directory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)


def get_config() -> dict:
    """Return Meta Ads API configuration dict."""
    account_id = os.getenv("META_AD_ACCOUNT_ID", "")
    # Ensure account ID has act_ prefix
    if account_id and not account_id.startswith("act_"):
        account_id = f"act_{account_id}"

    config = {
        "access_token": os.getenv("META_ACCESS_TOKEN", ""),
        "ad_account_id": account_id,
        "app_id": os.getenv("META_APP_ID", ""),
    }
    return config


def validate_config(config: dict = None) -> list[str]:
    """Check which required fields are missing. Returns list of missing field names."""
    if config is None:
        config = get_config()
    required = ["access_token", "ad_account_id"]
    missing = [f for f in required if not config.get(f)]
    return missing
