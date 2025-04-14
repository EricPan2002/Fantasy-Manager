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

# Yahoo OAuth 1.0 ���_
CONSUMER_KEY = os.environ.get("YAHOO_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("YAHOO_CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("YAHOO_ACCESS_TOKEN")



# �A�i�H�b�o�̦۰ʼg�J .env ��
#----------------------------�n��ƪ�����----------------------------------------

# �إ� OAuth �{�Ҫ���
# auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN)

# game_id = "454" #2024-25 Basketball��game ID
# league_id = "30747" #����n���ϥΪ̿�J
# league_key = f"{game_id}.l.{league_id}"

# # API endpoint�]�̦h 25 ���A�i�[�����^
# url = f"https://fantasysports.yahooapis.com/fantasy/v2/player/454.p.5013/stats;type=last_14_days"

# # �I�s API�]Bearer Token�^
# headers = {
#     "Authorization": f"Bearer {ACCESS_TOKEN}",
#     "Accept": "application/json"  # Yahoo �䴩 JSON�A���^�ǥi���٬O XML�A�n parse
# }

# response = requests.get(url, headers=headers)
# print(response.text)  # �q�`�O XML

#----------------------------�n��ƪ�����----------------------------------------

#--------------------���j�u-----------------------

