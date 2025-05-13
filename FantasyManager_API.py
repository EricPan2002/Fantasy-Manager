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

dotenv_path = Path(__file__).parent / ".env" #Ū�ɡA���.env
load_dotenv(dotenv_path)

# OAuth 1.0 ���_
CONSUMER_KEY = os.environ.get("YAHOO_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("YAHOO_CONSUMER_SECRET")
#ACCESS_TOKEN = os.environ.get("YAHOO_ACCESS_TOKEN") #���T�w�|���|�Ψ�

token = get_valid_token() #���oaccess token

#���o�ӧO�y���ƾڡAtype:�W�g->lastweek,�ɩu->season
#url = f"https://fantasysports.yahooapis.com/fantasy/v2/player/454.p.5352/stats;type=season"

#���o�y���}�e��T�A454.l.(league ID).t.(team number)
#url = f"https://fantasysports.yahooapis.com/fantasy/v2/team/454.l.18599.t.1/roster/players"

#���o�o���p�����Ҧ�FA�����
#url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/454.l.18599/players;status=FA;start=0;count=100"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/xml"
}

#response = requests.get(url, headers=headers)
#print(response.text)

start = 0
count = 25  # �C���̦h�i�� 25 ��
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

    # �ন list�]�Y����@�y���ɡA�|�O dict�^
    if isinstance(players, dict):
        players = [players]
    elif not players:
        break  # �S����h�y���F

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

    # �p�G�^�ǲy���ƶq�֩�@���� count�A�N��w�g�짹
    if len(players) < count:
        break
    start += count

# ��X�Ҧ��y��
# for p in valid_players:
#     print(p)

#--------------------------------------------------------------------

# game_id = "454" #2024-25 Basketball��game ID
# league_id = "18599" #����n���ϥΪ̿�J
# league_key = f"{game_id}.l.{league_id}"
