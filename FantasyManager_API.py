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
#url = f"https://fantasysports.yahooapis.com/fantasy/v2/player/454.p.5352/stats;type=season"

#取得球隊陣容資訊，454.l.(league ID).t.(team number)
#url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/454.l.18599.t.1/roster/players"

#取得這個聯盟內所有FA的資料
#url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/454.l.18599/players;status=FA;start=0;count=100"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/xml"
}

#response = requests.get(url, headers=headers)
#print(response.text)

start = 0
count = 25  # 每頁最多可取 25 筆
valid_players = []

while True:
    url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/454.l.18599/players;status=FA;start={start};count={count};out=stats"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/xml"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Request failed:", response.status_code, response.text)
        break

    data_dict = xmltodict.parse(response.text)
    players = data_dict["fantasy_content"]["league"]["players"].get("player", [])

    # 轉成 list（若為單一球員時，會是 dict）
    if isinstance(players, dict):
        players = [players]
    elif not players:
        break  # 沒有更多球員了

    for player in players:
        status = player.get("status", "")
        if status == "NA":
            continue

        eligible = player.get("eligible_positions", {}).get("position", [])
        if isinstance(eligible, str):
            eligible = [eligible]

        player_info = {
            "player_key": player.get("player_key", ""),
            "player_id": player.get("player_id", ""),
            "name": player.get("name", {}).get("full", ""),
            "status": player.get("status", "HEALTHY"),
            "status_full": player.get("status_full", ""),
            "eligible_positions": eligible
        }
        valid_players.append(player_info)

    # 如果回傳球員數量少於一頁的 count，代表已經抓完
    if len(players) < count:
        break
    start += count

# 輸出所有球員
# for p in valid_players:
#     print(p)

#--------------------------------------------------------------------

# game_id = "454" #2024-25 Basketball的game ID
# league_id = "18599" #之後要讓使用者輸入
# league_key = f"{game_id}.l.{league_id}"
