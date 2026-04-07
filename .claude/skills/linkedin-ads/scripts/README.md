# LinkedIn Ads Scripts

Python scripts for the LinkedIn Marketing API (v202601).

## Files

| Script | Purpose |
|--------|---------|
| `linkedin_api.py` | Core API client class — accounts, campaigns, creatives, analytics |
| `oauth_server.py` | OAuth 2.0 token flow — run once to get your access token |

## Setup

1. Create a LinkedIn Marketing App at https://www.linkedin.com/developers/
2. Add your credentials to `.env` (see root `.env.example`)
3. Run `python oauth_server.py` to get your access token
4. Use `linkedin_api.py` in your own scripts or let Claude Code call it directly

## Requirements

```
pip install requests python-dotenv
```

## Quick Start

```python
from linkedin_api import LinkedInCampaignManager

client = LinkedInCampaignManager()

# List all ad accounts
accounts = client.get_ad_accounts()

# Get campaigns for an account
campaigns = client.get_campaigns(account_id="YOUR_ACCOUNT_ID")

# Get analytics
analytics = client.get_campaign_analytics(
    account_id="YOUR_ACCOUNT_ID",
    campaign_ids=["CAMPAIGN_ID"],
    start_date={"year": 2026, "month": 1, "day": 1},
    end_date={"year": 2026, "month": 1, "day": 31},
)
```

## OAuth Token Refresh

LinkedIn tokens expire periodically. To refresh:

1. Run `python oauth_server.py`
2. Open the URL it prints in your browser
3. Authorize the app
4. Token auto-saves to `.env`
