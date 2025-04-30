# -*- coding: utf-8 -*-
import os
import requests
import json
import xmltodict
from dotenv import load_dotenv
from pathlib import Path
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth1Session
from Refresh_auth import get_valid_token

dotenv_path = Path(__file__).parent / ".env" #讀檔，找到.env
load_dotenv(dotenv_path)

# OAuth 1.0 金鑰
CONSUMER_KEY = os.environ.get("YAHOO_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("YAHOO_CONSUMER_SECRET")
#ACCESS_TOKEN = os.environ.get("YAHOO_ACCESS_TOKEN") #不確定會不會用到

token = get_valid_token() #取得access token

#取得個別球員數據，type:上週->lastweek,賽季->season
url = f"https://fantasysports.yahooapis.com/fantasy/v2/player/454.p.5013/stats;type=season"

#取得球隊陣容資訊，454.l.(league ID).t.(team number)
#url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/454.l.18599.t.1/roster/players"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/xml"
}

response = requests.get(url, headers=headers)
print(response.text)
#----------------------------要資料的部分----------------------------------------

# 建立 OAuth 認證物件
# auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN)

# game_id = "454" #2024-25 Basketball的game ID
# league_id = "30747" #之後要讓使用者輸入
# league_key = f"{game_id}.l.{league_id}"

# # API endpoint（最多 25 筆，可加分頁）
# url = f"https://fantasysports.yahooapis.com/fantasy/v2/player/454.p.5013/stats;type=last_14_days"

# # 呼叫 API（Bearer Token）
# headers = {
#     "Authorization": f"Bearer {ACCESS_TOKEN}",
#     "Accept": "application/json"  # Yahoo 支援 JSON，但回傳可能還是 XML，要 parse
# }

# response = requests.get(url, headers=headers)
# print(response.text)  # 通常是 XML

#----------------------------要資料的部分----------------------------------------

#--------------------分隔線-----------------------

