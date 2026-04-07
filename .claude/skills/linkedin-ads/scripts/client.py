"""
Shared LinkedIn Marketing API client.
All scripts import get_session() and get_account_id() from here.
"""

import sys
import requests
from config import get_config, validate_config

BASE_URL = "https://api.linkedin.com/rest"


def get_session() -> requests.Session:
    """Authenticate and return a requests.Session with LinkedIn API headers."""
    config = get_config()

    missing = validate_config(config)
    if missing:
        print(f"ERROR: Missing credentials in .env: {', '.join(missing)}")
        print("Run: python oauth_server.py  -- to generate an access token.")
        print("See README.md for full setup instructions.")
        sys.exit(1)

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {config['access_token']}",
        "LinkedIn-Version": "202601",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    })
    return session


def get_account_id() -> str:
    """Return the LinkedIn ad account ID from config."""
    config = get_config()
    return config["account_id"]
