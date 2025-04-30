# -*- coding: utf-8 -*-

import requests
import webbrowser
import base64
import json
import time
from urllib.parse import urlencode
from pathlib import Path

TOKEN_PATH = Path(__file__).parent / "token.json"

with open(TOKEN_PATH, "r") as f:
    token_data = json.load(f)

CONSUMER_KEY = token_data.get("consumer_key")
CONSUMER_SECRET = token_data.get("consumer_secret")
REDIRECT_URI = "oob"  # CLI 模式用 oob

# Step 1: 建立授權 URL
authorize_url = "https://api.login.yahoo.com/oauth2/request_auth"
query = {
    "client_id": CONSUMER_KEY,
    "redirect_uri": REDIRECT_URI,
    "response_type": "code",
    "language": "en-us"
}
url = f"{authorize_url}?{urlencode(query)}"
print(f"Please open the website to authorize: \n{url}")
webbrowser.open(url)

# Step 2: 使用者輸入 verifier code
auth_code = input("Please paste the verifier (code): ")

# Step 3: 拿 access_token + refresh_token
token_url = "https://api.login.yahoo.com/oauth2/get_token"
headers = {
    "Authorization": "Basic " + base64.b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode(),
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
    "code": auth_code
}
response = requests.post(token_url, headers=headers, data=data)

if response.status_code == 200:
    token_data = response.json()
    token_data["consumer_key"] = CONSUMER_KEY
    token_data["consumer_secret"] = CONSUMER_SECRET
    token_data["token_time"] = time.time()
    print("Complete to Access Token / Refresh Token:")
    print(json.dumps(token_data, indent=4))
    
    # 儲存成 token.json
    with open("token.json", "w") as f:
        json.dump(token_data, f, indent=4)
    print("already save to token.json")
else:
    print("ERROR", response.status_code, response.text)