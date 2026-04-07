"""
LinkedIn Campaign Manager API Client

Core wrapper for the LinkedIn Marketing API (v202601).
Handles authentication, campaigns, creatives, and analytics.

Usage:
    from linkedin_api import LinkedInCampaignManager
    client = LinkedInCampaignManager()
    accounts = client.get_ad_accounts()
"""
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


class LinkedInCampaignManager:
    BASE_URL = "https://api.linkedin.com/rest"

    def __init__(self):
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("No access token found. Run oauth_server.py first.")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "LinkedIn-Version": "202601",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        }

    def _get(self, endpoint, params=None):
        resp = requests.get(f"{self.BASE_URL}{endpoint}", headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint, data):
        resp = requests.post(f"{self.BASE_URL}{endpoint}", headers=self.headers, json=data)
        return resp

    # --- Account Info ---
    def get_ad_accounts(self):
        """Get all ad accounts you have access to."""
        return self._get("/adAccounts", params={"q": "search"})

    def get_ad_account(self, account_id):
        """Get a specific ad account."""
        return self._get(f"/adAccounts/{account_id}")

    # --- Campaigns ---
    def get_campaigns(self, account_id, status=None):
        """Get all campaigns for an ad account."""
        params = {"q": "search"}
        if status:
            params["search"] = f"(status:(values:List({status})))"
        return self._get(f"/adAccounts/{account_id}/adCampaigns", params=params)

    def get_campaign(self, account_id, campaign_id):
        """Get a specific campaign."""
        return self._get(f"/adAccounts/{account_id}/adCampaigns/{campaign_id}")

    # --- Campaign Groups ---
    def get_campaign_groups(self, account_id):
        """Get all campaign groups for an ad account."""
        return self._get(f"/adAccounts/{account_id}/adCampaignGroups", params={"q": "search"})

    # --- Creatives ---
    def get_creatives(self, account_id, campaign_id=None):
        """Get creatives for an account, optionally filtered by campaign."""
        params = {"q": "search"}
        if campaign_id:
            params["search"] = f"(campaign:(values:List(urn:li:sponsoredCampaign:{campaign_id})))"
        return self._get(f"/adAccounts/{account_id}/adCreatives", params=params)

    # --- Create Campaign ---
    def create_campaign(self, account_id, campaign_data):
        """Create a new campaign under an ad account."""
        campaign_data["account"] = f"urn:li:sponsoredAccount:{account_id}"
        resp = self._post(f"/adAccounts/{account_id}/adCampaigns", campaign_data)
        if resp.status_code == 201:
            campaign_id = resp.headers.get("x-restli-id")
            return {"success": True, "campaign_id": campaign_id}
        else:
            return {"success": False, "status": resp.status_code, "error": resp.text}

    # --- Create Campaign Group ---
    def create_campaign_group(self, account_id, group_data):
        """Create a new campaign group."""
        group_data["account"] = f"urn:li:sponsoredAccount:{account_id}"
        resp = self._post(f"/adAccounts/{account_id}/adCampaignGroups", group_data)
        if resp.status_code == 201:
            group_id = resp.headers.get("x-restli-id")
            return {"success": True, "group_id": group_id}
        else:
            return {"success": False, "status": resp.status_code, "error": resp.text}

    # --- Analytics / Reporting ---
    def get_campaign_analytics(self, account_id, campaign_ids, start_date, end_date, time_granularity="DAILY"):
        """Get analytics for campaigns."""
        params = {
            "q": "analytics",
            "pivot": "CAMPAIGN",
            "dateRange.start.year": start_date["year"],
            "dateRange.start.month": start_date["month"],
            "dateRange.start.day": start_date["day"],
            "dateRange.end.year": end_date["year"],
            "dateRange.end.month": end_date["month"],
            "dateRange.end.day": end_date["day"],
            "timeGranularity": time_granularity,
        }
        for i, cid in enumerate(campaign_ids):
            params[f"campaigns[{i}]"] = f"urn:li:sponsoredCampaign:{cid}"

        return self._get(f"/adAccounts/{account_id}/adAnalytics", params=params)

    def get_account_analytics(self, account_id, start_date, end_date, time_granularity="DAILY"):
        """Get analytics at the account level."""
        params = {
            "q": "analytics",
            "pivot": "ACCOUNT",
            "dateRange.start.year": start_date["year"],
            "dateRange.start.month": start_date["month"],
            "dateRange.start.day": start_date["day"],
            "dateRange.end.year": end_date["year"],
            "dateRange.end.month": end_date["month"],
            "dateRange.end.day": end_date["day"],
            "timeGranularity": time_granularity,
            "accounts[0]": f"urn:li:sponsoredAccount:{account_id}",
        }
        return self._get(f"/adAccounts/{account_id}/adAnalytics", params=params)


def pretty_print(data):
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    client = LinkedInCampaignManager()

    print("Fetching ad accounts...")
    accounts = client.get_ad_accounts()
    pretty_print(accounts)
