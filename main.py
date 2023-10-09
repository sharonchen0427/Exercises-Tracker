import os

import requests
from datetime import datetime

# https://developer.nutritionix.com/docs/v2
# https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/edit#heading=h.zhjgcprrgvim

# step1: use nutritionix api to process natural language in query input
NUTRITIONIX_APP_ID = os.environ['NUTRITIONIX_APP_ID']
NUTRITIONIX_API_KEY = os.environ['NUTRITIONIX_API_KEY']
# os.environ either set it in system environment vars   | pycharm Run > Edit Configuration > Environment > add key=value to Environment Variables
NUTRITIONIX_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"
# NUTRITIONIX_ENDPOINT = "/v2/natural/exercise"
HEADERS = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content-Type": "application/json"
}
USER_INPUT = input("Tell me which exercise you did: ")
PARAMS = {
    "query": USER_INPUT,
    "gender": "female",
    "weight_kg": 72.5,
    "height_cm": 167.64,
    "age": 30
}

resp = requests.post(url=NUTRITIONIX_URL, json=PARAMS, headers=HEADERS)
print(resp.text)
result = resp.json()

# step2:
# google account > settings > security > allow sheety to access google account
# use sheety api to generate a new row of data in google sheet
GMAIL_USER = "jennieabout591@gmail.com"
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1cA55gntAdJIqRZz750KN3XQy4mjKfsph4b4vl3YWbjA/edit#gid=0"
SHEETY_URL = "https://api.sheety.co/2e06395c013d40e08e67a5458fcea8ff/workoutTracking/sheet1"
# SHEETY_URL = f"https://api.sheety.co/{SHEETY_API_KEY}/workoutTracking/sheet1"
# SHEETY_API_KEY = "2e06395c013d40e08e67a5458fcea8ff"
shetty_bearer_token = os.environ['shetty_bearer_token']
bear_headers = {
    "Authorization": f'Bearer {shetty_bearer_token}'
}

today_date = datetime.now().strftime("%d%m%Y")
now_time = datetime.now().strftime("%X")
for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {  # google sheet name tab
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"],
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    # sheet_response = requests.post(SHEETY_URL, json=sheet_inputs) # without self-defined bearer token
    sheet_response = requests.post(SHEETY_URL, json=sheet_inputs, headers=bear_headers)
    # print(sheet_response.text)
# {
#   "sheet1": {
#     "date": "09102023",
#     "time": "15:47:09",
#     "exercise": "tennis",
#     "duration": 30,
#     "calories": 264.63,
#     "id": 8
#   }
# }

# result in google sheet:
# 09102023	15:47:09	tennis	30	264.63
