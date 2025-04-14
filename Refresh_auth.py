# -*- coding: utf-8 -*-

import requests
import json
import time
import base64
from pathlib import Path

TOKEN_PATH = Path(__file__).parent / "token.json"
TOKEN_EXPIRY_SECONDS = 3600  # Yahoo access_token 有效期為 1 小時

def load_token():
    with open(TOKEN_PATH, "r") as f:
        return json.load(f)

def save_token(token_data):
    with open(TOKEN_PATH, "w") as f:
        json.dump(token_data, f, indent=4)

def is_token_expired(token_data):
    return time.time() - token_data["token_time"] >= TOKEN_EXPIRY_SECONDS

def refresh_access_token(token_data):
    print("Access Token has expired,refreshing...")
    client_id = token_data["consumer_key"]
    client_secret = token_data["consumer_secret"]
    refresh_token = token_data["refresh_token"]

    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": "oob"
    }

    response = requests.post("https://api.login.yahoo.com/oauth2/get_token", headers=headers, data=data)

    if response.status_code == 200:
        new_data = response.json()
        print("get Access Token successfully!")
        token_data["access_token"] = new_data["access_token"]
        token_data["token_time"] = time.time()
        save_token(token_data)
        return token_data
    else:
        raise Exception(f"can't refresh Token: {response.status_code} - {response.text}")

def get_valid_token():
    token_data = load_token()
    if is_token_expired(token_data):
        token_data = refresh_access_token(token_data)
    else:
        print("Access Token hasn't expired")
    return token_data["access_token"]
