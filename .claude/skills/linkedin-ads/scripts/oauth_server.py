"""
LinkedIn OAuth 2.0 Authorization Flow
Run this script, open the URL it prints, authorize, and it will save your access token.
"""
import http.server
import urllib.parse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:3000/callback")
SCOPES = "r_ads,r_ads_reporting,r_organization_social,w_organization_social,rw_ads,w_member_social"

AUTH_URL = (
    f"https://www.linkedin.com/oauth/v2/authorization?"
    f"response_type=code&client_id={CLIENT_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&scope={urllib.parse.quote(SCOPES)}"
)


class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/callback":
            params = urllib.parse.parse_qs(parsed.query)
            if "code" in params:
                code = params["code"][0]
                token = self.exchange_code(code)
                if token:
                    self.save_token(token)
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<h1>Success! Access token saved.</h1><p>You can close this window.</p>")
                    print(f"\nAccess token obtained and saved to .env!")
                else:
                    self.send_response(500)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<h1>Error exchanging code for token.</h1>")
            elif "error" in params:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                error_msg = params.get("error_description", params["error"])
                self.wfile.write(f"<h1>Error: {error_msg}</h1>".encode())
        else:
            self.send_response(404)
            self.end_headers()

    def exchange_code(self, code):
        resp = requests.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if resp.status_code == 200:
            return resp.json().get("access_token")
        else:
            print(f"Token exchange failed: {resp.status_code} {resp.text}")
            return None

    def save_token(self, token):
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        with open(env_path, "r") as f:
            lines = f.readlines()
        with open(env_path, "w") as f:
            for line in lines:
                if line.startswith("LINKEDIN_ACCESS_TOKEN="):
                    f.write(f"LINKEDIN_ACCESS_TOKEN={token}\n")
                else:
                    f.write(line)

    def log_message(self, format, *args):
        pass  # Suppress request logs


if __name__ == "__main__":
    print("=" * 60)
    print("LinkedIn OAuth 2.0 Authorization")
    print("=" * 60)
    print(f"\n1. Open this URL in your browser:\n\n{AUTH_URL}\n")
    print("2. Log in and authorize the app")
    print("3. You'll be redirected back here automatically\n")
    print("Waiting for callback on http://localhost:3000 ...")

    server = http.server.HTTPServer(("localhost", 3000), OAuthHandler)
    server.handle_request()  # Handle one request then stop
    print("Done!")
