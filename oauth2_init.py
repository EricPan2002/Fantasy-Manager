# -*- coding: utf-8 -*-

import requests
import webbrowser
import base64
import json
import time
from urllib.parse import urlencode

CONSUMER_KEY = "dj0yJmk9YmVCQXIwcXNYQll6JmQ9WVdrOVUxUm9PVGxIYkVrbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTU1"
CONSUMER_SECRET = "bcb49b0781877d2f9e9984dc76bbcbfe81da0c73"
REDIRECT_URI = "oob"  # CLI �Ҧ��� oob

# Step 1: �إ߱��v URL
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

# Step 2: �ϥΪ̿�J verifier code
auth_code = input("Please paste the verifier (code): ")

# Step 3: �� access_token + refresh_token
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
    
    # �x�s�� token.json
    with open("token.json", "w") as f:
        json.dump(token_data, f, indent=4)
    print("already save to token.json")
else:
    print("ERROR", response.status_code, response.text)