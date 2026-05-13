"""
Google Ads OAuth 2.0 Setup
Run this script to get a refresh token for the Google Ads API.
"""
import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = os.getenv("GOOGLE_ADS_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_ADS_CLIENT_SECRET", "")

if not CLIENT_ID or not CLIENT_SECRET:
    # Try loading from .env
    try:
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".env")
        load_dotenv(env_path)
        CLIENT_ID = os.getenv("GOOGLE_ADS_CLIENT_ID", "")
        CLIENT_SECRET = os.getenv("GOOGLE_ADS_CLIENT_SECRET", "")
    except ImportError:
        pass

if not CLIENT_ID or not CLIENT_SECRET:
    print("Error: GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET must be set.")
    print("Set them in your .env file first.")
    sys.exit(1)

client_config = {
    "installed": {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

SCOPES = ["https://www.googleapis.com/auth/adwords"]

print("=" * 60)
print("Google Ads OAuth 2.0 Setup")
print("=" * 60)
print("\nA browser window will open. Log in and authorize the app.\n")

flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
credentials = flow.run_local_server(port=8080)

print(f"\nYour refresh token:\n")
print(credentials.refresh_token)
print(f"\nSave this to your .env file as GOOGLE_ADS_REFRESH_TOKEN")
print("Done!")
