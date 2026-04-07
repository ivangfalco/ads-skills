"""
Configuration loader for LinkedIn Marketing API.
Reads credentials from .env file in this directory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the same directory as this file
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)


def get_config() -> dict:
    """Return LinkedIn Marketing API configuration dict."""
    config = {
        "access_token": os.getenv("LINKEDIN_ACCESS_TOKEN", ""),
        "account_id": os.getenv("LINKEDIN_ACCOUNT_ID", ""),
        "client_id": os.getenv("LINKEDIN_CLIENT_ID", ""),
        "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET", ""),
    }
    return config


def validate_config(config: dict) -> list[str]:
    """Check which required fields are missing. Returns list of missing field names."""
    required = ["access_token", "account_id"]
    missing = [f for f in required if not config.get(f)]
    return missing
