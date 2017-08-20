# -*- coding: utf-8 -*-

import requests
from time import sleep

def urlreq():
    resp = requests.get("http://localhost:5000/warState")
    return resp.text

def visualizeState(state_json):
    print(state_json)

if __name__ == "__main__":
    while True:
        state = urlreq()
        visualizeState(state)
        sleep(1)

