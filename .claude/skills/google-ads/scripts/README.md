# Google Ads Scripts

Python scripts for the Google Ads API using the official `google-ads` library.

## Files

| Script | Purpose |
|--------|---------|
| `client.py` | Shared auth wrapper -- all scripts import from here |
| `config.py` | Config loader (reads .env) |
| `account_overview.py` | High-level account snapshot with period comparison |
| `list_campaigns.py` | List all campaigns with metrics |
| `create_campaign.py` | Create new campaigns (Search, Display, PMax, etc.) |
| `create_ad_group.py` | Create ad groups within campaigns |
| `create_ad.py` | Create Responsive Search Ads |
| `add_keywords.py` | Add positive or negative keywords |
| `list_ads.py` | List ads with performance data |
| `get_campaign_performance.py` | Detailed campaign metrics with daily breakdown |
| `get_keyword_performance.py` | Keyword-level performance with Quality Score |
| `search_terms_report.py` | Search terms analysis and wasted spend finder |
| `update_campaign.py` | Update campaign status, budget, or name |

## Setup

1. Create a Google Ads developer account and get a developer token
2. Create OAuth2 credentials in Google Cloud Console
3. Add credentials to `.env` (see root `.env.example`)

## Requirements

```
pip install google-ads python-dotenv tabulate
```

## Quick Examples

```bash
# Account snapshot
python account_overview.py --compare

# Find wasted spend
python search_terms_report.py --no-conversions --min-clicks 3

# Create a full campaign
python create_campaign.py --name "Brand - Search" --type SEARCH --budget 50
python create_ad_group.py --campaign-id 123456 --name "Brand Terms"
python add_keywords.py --ad-group-id 789 --keywords "your brand" "your product" --match-type EXACT
python create_ad.py --ad-group-id 789 \
    --headlines "Your Brand" "Official Site" "Get Started Free" \
    --descriptions "The leading platform for X. Start your free trial today." "Trusted by 1000+ teams." \
    --final-url "https://yourdomain.com"
```

## Notes

- All campaigns are created as PAUSED for safety
- Google Ads uses micros for money (1,000,000 micros = $1)
- Quality Score is 1-10 (higher is better, reduces CPC)
- Always check search terms weekly for negative keyword opportunities
