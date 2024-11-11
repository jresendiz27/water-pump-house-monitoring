import requests
import random
import time

url = "http://localhost:5000/water-pump/action"

for i in range(0, 20):
    payload = {
        "water_microphone_value": str(random.randint(110, 130)),
        "tank_microphone_value": str(random.randint(200, 220))
    }

    time.sleep(10)

    response = requests.request("POST", url, data=payload)

    resp = response.text.rstrip()
    if resp != "1":
        print('Failed!!! check the json file!!')
        print(response.text)