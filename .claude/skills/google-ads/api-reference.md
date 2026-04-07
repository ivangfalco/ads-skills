# Google Ads Bot - Claude Code Integration

Scripts that let Claude Code manage your Google Ads account programmatically.
Location: `scripts/google/` in this repository.

## Quick Start (for Claude Code)

**Everything is configured and working.** To run any script:

```bash
cd "scripts/google"
.venv/bin/python3 <script>.py [args]
```

### Configuration
- **MCC (Manager):** Set `GOOGLE_ADS_LOGIN_CUSTOMER_ID` in `.env`
- **Active Client:** Set `GOOGLE_ADS_CUSTOMER_ID` in `.env`
- To switch clients: change `GOOGLE_ADS_CUSTOMER_ID` in `.env`

### Known Gotchas
1. **Always use `.venv/bin/python3`** - system Python lacks the packages
2. **`use_proto_plus: True`** is required in the client config or it throws `ValueError`
3. **The OOB OAuth flow is deprecated** - use `InstalledAppFlow.run_local_server()` (port 8080)
4. **Suppress warnings** with `2>&1 | grep -v "FutureWarning\|warnings.warn\|NotOpenSSLWarning\|non-supported"` - Python 3.9 triggers noisy deprecation warnings
5. **All new campaigns start PAUSED** - safety measure, enable explicitly
6. **Explorer access** = 15,000 ops/day, own accounts only - plenty for management

## Setup

### Google Cloud Project
- Enable the **Google Ads API** in your Google Cloud project
- Create an **OAuth Desktop App** client
- Set OAuth consent to **Internal** (for workspace accounts)

### All Credentials
- Developer token: from Google Ads API Center (Explorer access)
- Client ID + Secret: from Google Cloud Console
- Refresh token: generated via `setup_oauth.py` with localhost redirect on port 8080
- Customer ID: your 10-digit account number (no dashes)

### Generate Refresh Token

```bash
cd scripts/google
pip3 install -r requirements.txt
python3 setup_oauth.py
```

This will give you a URL to open in your browser, authorize, paste the code, and get a refresh token. Add it to `.env`:
```
GOOGLE_ADS_REFRESH_TOKEN=your-refresh-token-here
```

### Add Customer ID

Find your Google Ads customer ID (10-digit number, top-right of Google Ads UI). Add to `.env` without dashes:
```
GOOGLE_ADS_CUSTOMER_ID=1234567890
```

If using a Manager (MCC) account:
```
GOOGLE_ADS_LOGIN_CUSTOMER_ID=your-mcc-id-here
```

### Test the Connection

```bash
python3 account_overview.py
```

---

## Available Scripts

### Account & Reporting
| Script | What it does |
|--------|-------------|
| `account_overview.py` | Full account snapshot - metrics + top campaigns |
| `get_campaign_performance.py` | Detailed campaign metrics (daily breakdown, date ranges) |
| `search_terms_report.py` | What people actually searched - find waste & opportunities |
| `get_keyword_performance.py` | Keyword-level metrics, quality scores, impression share |

### Campaign Management
| Script | What it does |
|--------|-------------|
| `list_campaigns.py` | List all campaigns with status and metrics |
| `create_campaign.py` | Create new campaign (Search, Display, PMax, etc.) |
| `update_campaign.py` | Change status, budget, name of existing campaigns |

### Ad Groups
| Script | What it does |
|--------|-------------|
| `list_ad_groups.py` | List ad groups with metrics |
| `create_ad_group.py` | Create new ad group in a campaign |

### Ads
| Script | What it does |
|--------|-------------|
| `list_ads.py` | List all ads with metrics and approval status |
| `create_ad.py` | Create Responsive Search Ads (RSA) |

### Keywords
| Script | What it does |
|--------|-------------|
| `add_keywords.py` | Add keywords (broad/phrase/exact) or negatives |
| `get_keyword_performance.py` | Keyword metrics, quality scores, impression share |

---

## How Claude Code Uses This

Once `.env` is configured, you can ask Claude Code things like:

- **"Show me account performance for the last 7 days"**
  -> Runs `python account_overview.py --date-range last_7d --compare`

- **"What search terms are wasting budget?"**
  -> Runs `python search_terms_report.py --no-conversions --min-clicks 3`

- **"Create a search campaign for brand keywords"**
  -> Runs `python create_campaign.py --name "Brand - Search" --type SEARCH --budget 50`

- **"Pause the underperforming campaign"**
  -> Runs `python update_campaign.py --campaign-id 12345 --status PAUSED`

- **"Add negative keywords to block irrelevant traffic"**
  -> Runs `python add_keywords.py --ad-group-id 12345 --keywords "free" "cheap" --negative`

---

## Explorer Access Limits

With Explorer access you have:
- **15,000 operations/day** (more than enough for management)
- Access to **your own accounts only**
- All read/write operations work

To upgrade to Basic or Standard access (for higher limits or managing client accounts), apply through the Google Ads API Center.

---

## Managing Multiple Accounts

If you have an MCC (Manager account) that manages multiple client accounts, just change `GOOGLE_ADS_CUSTOMER_ID` in `.env` to switch between them. Use `list_accounts.py` to see all accounts under your MCC.

## Google Tag Manager

GTM bot scripts are at `scripts/google-tag-manager/`. Same Google Cloud project, same OAuth client, separate refresh token with GTM scopes.
