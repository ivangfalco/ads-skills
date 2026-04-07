# Meta Ads Scripts

Python scripts for the Meta Marketing API (v22.0).

## Files

| Script | Purpose |
|--------|---------|
| `get_active_ads_copy.py` | Fetch all active ads with full creative/copy details |
| `create_custom_audience.py` | Create custom audiences and upload hashed contact lists |
| `ad_scheduler.py` | Schedule automatic ad pauses (great for webinar ads) |

## Setup

1. Create a Meta App at https://developers.facebook.com/
2. Generate a User Access Token with `ads_management` and `ads_read` permissions
3. Add credentials to `.env` (see root `.env.example`)

## Requirements

```
pip install requests python-dotenv
```

## Quick Examples

### Audit all active ad copy
```bash
python get_active_ads_copy.py
```

### Upload a custom audience
```bash
python create_custom_audience.py contacts.csv "My Target Account List"
```

### Schedule a webinar ad to pause
```bash
python ad_scheduler.py add --ad-id 123456789 --pause-at "2026-04-15 09:00" --name "Webinar Apr 15"
python ad_scheduler.py list
python ad_scheduler.py run   # Execute pending pauses (run via cron)
```

## Notes

- Always use Python for Meta API calls (never curl — token characters get mangled)
- Token expires every ~60 days. Refresh at https://developers.facebook.com/tools/explorer/
- Budgets are in cents (5000 = $50.00)
- Always create campaigns/ads as PAUSED, never ACTIVE
