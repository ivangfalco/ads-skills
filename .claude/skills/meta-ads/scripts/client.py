"""
Shared Meta Marketing API client.
All scripts import helpers from here.
"""

import sys
import requests
from config import get_config, validate_config

API_VERSION = "v22.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def _ensure_config():
    """Validate config and exit with helpful message if missing."""
    config = get_config()
    missing = validate_config(config)
    if missing:
        print(f"ERROR: Missing credentials in .env: {', '.join(missing)}")
        print("Required env vars: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID")
        print("Optional: META_APP_ID")
        sys.exit(1)
    return config


def get_params() -> dict:
    """Return base params dict with access_token for API calls."""
    config = _ensure_config()
    return {"access_token": config["access_token"]}


def get_account_id() -> str:
    """Return the ad account ID (with act_ prefix)."""
    config = _ensure_config()
    return config["ad_account_id"]


def get_base_url() -> str:
    """Return the Meta Graph API base URL."""
    return BASE_URL


def api_get(endpoint: str, params: dict = None) -> list | dict | None:
    """
    Make a GET request to the Meta API with automatic pagination.

    For endpoints that return paginated lists (data + paging), this follows
    paging.next and returns the combined list of all items.

    For endpoints that return a single object (like insights), returns the
    raw response dict.
    """
    base_params = get_params()
    if params:
        base_params.update(params)

    url = f"{BASE_URL}/{endpoint}"
    all_data = []
    is_list = None

    while url:
        resp = requests.get(url, params=base_params)
        data = resp.json()

        if "error" in data:
            print(f"API Error: {data['error'].get('message', data['error'])}")
            return None

        # Determine if this is a paginated list or single object
        if is_list is None:
            is_list = "data" in data

        if is_list:
            all_data.extend(data.get("data", []))
            # Follow pagination
            paging = data.get("paging", {})
            url = paging.get("next")
            base_params = {}  # next URL already contains all params
        else:
            return data

    return all_data


def api_post(endpoint: str, data: dict = None) -> dict | None:
    """
    Make a POST request to the Meta API.
    Returns the response dict or None on error.
    """
    base_params = get_params()
    if data:
        base_params.update(data)

    url = f"{BASE_URL}/{endpoint}"
    resp = requests.post(url, data=base_params)
    result = resp.json()

    if "error" in result:
        print(f"API Error: {result['error'].get('message', result['error'])}")
        return None

    return result
