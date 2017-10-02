# -*- coding: utf-8 -*-

import requests
from time import sleep
import json
import numpy as np
import cv2


w_height = 960
w_width = 1280
font_size = 4
text_color = (255,255,0)
p_color = {"b":(255,0,0), "r":(0,0,255)}
print(type(p_color["b"]))
font = cv2.FONT_HERSHEY_PLAIN
"""
cv2.FONT_HERSHEY_COMPLEX
cv2.FONT_HERSHEY_COMPLEX_SMALL
cv2.FONT_HERSHEY_DUPLEX
cv2.FONT_HERSHEY_PLAIN
cv2.FONT_HERSHEY_SCRIPT_COMPLEX
cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
cv2.FONT_HERSHEY_SIMPLEX
cv2.FONT_HERSHEY_TRIPLEX
cv2.FONT_ITALIC
"""
def urlreq():
    resp = requests.get("http://localhost:5000/warState")
    return resp.text

def visualizeState(state_json,w_name):
    
    print(state_json)
    j = json.dumps(state_json)
    state = json.loads(state_json)
    
    display = np.zeros((w_height,w_width,3))

    cv2.putText(display, "Game State: " + state["state"],(w_width*1/4, w_height/20), font, font_size, text_color)
    cv2.putText(display, "Players", (w_width*2/5, w_height*1/7), font, font_size, text_color)
    cv2.putText(display, " Score ", (w_width*2/5, w_height*2/7), font, font_size, text_color)
    for player, position in ("b", 0), ("r", w_width*12/20):
        cv2.putText(display, state["players"][player].center(10, ' '), (position-len(state["players"][player])*0,  w_height*1/7),font, font_size+2, p_color[player])
        cv2.putText(display, str(state["scores"][player]).center(10, ' '), (position,  w_height*2/7), font, font_size+2, p_color[player])
    cv2.imshow(w_name,display)
    cv2.waitKey(3)
    
if __name__ == "__main__":
    WINDOW_NAME = "Onigiri War!!"
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(WINDOW_NAME, 0,0)
    while True:
        state = urlreq()
        visualizeState(state,WINDOW_NAME)
        sleep(1)

