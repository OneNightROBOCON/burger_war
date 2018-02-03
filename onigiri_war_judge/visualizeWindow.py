# -*- coding: utf-8 -*-

import requests
from time import sleep
import json
import numpy as np
import cv2
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

#ウィンドウの設定
w_height = 960
w_width = 1280
font_size = 4
text_color = (0,0,0)
p_color = {"b": (255, 50, 50), "r": (100, 100, 255)}
print(type(p_color["b"]))
font = cv2.FONT_HERSHEY_PLAIN
thin = 7
#フォントの種類
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

#フィールドの座標設定
robots = {}
robots["BL"] = {"L":(375,420), "R":(375,310), "B":(300,365)}
robots["RE"] = {"L":(860,890), "R":(860,1000), "B":(930,943)}

objects = {}
objects_name = ["hoge1", "hoge2", "hoge3", "hoge4", "hoge5"]
#h x w
objects[objects_name[0]] = {"N":(470,525), "S":(560,525)}
objects[objects_name[1]] = {"N":(470,790), "S":(560,790)}
objects[objects_name[2]] = {"N":(680,525), "S":(775,525)}
objects[objects_name[3]] = {"N":(680,790), "S":(775,790)}
objects[objects_name[4]] = {"N":(575,660), "E":(630,715), "W":(630,595), "S":(680,660)}

def urlreq():
    resp = requests.get("http://localhost:5000/warState")
    return resp.text

def getMask_checker(img,size):
    
    img = cv2.resize(img,(size, size))

    i_mask = img[:,:,3]  # アルファチャンネルだけ抜き出す。
    i_mask = cv2.cvtColor(i_mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
    i_mask = i_mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
    img = img[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

    return img, i_mask

def getMask_marker(img,size_w,size_h):
    
    img = cv2.resize(img,(size_w, size_h))

    i_mask = img[:,:,3]  # アルファチャンネルだけ抜き出す。
    i_mask = cv2.cvtColor(i_mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
    i_mask = i_mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
    img = img[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

    return img, i_mask

def setMarker(display,name,p):
    object_name,object_pos = name.split("_")
      
    marker_pos_h, marker_pos_w = objects[object_name][object_pos]

    if("E" in object_pos or "W" in object_pos):
        
        m_img = marker[p].transpose(1,0,2) 
        m_mask = mask[p].transpose(1,0,2)

        np.multiply(display[marker_pos_h-marker_size_w/2:marker_pos_h+marker_size_w/2, marker_pos_w-marker_size_h/2:marker_pos_w+marker_size_h/2], 1 - m_mask, out=display[marker_pos_h-marker_size_w/2:marker_pos_h+marker_size_w/2, marker_pos_w-marker_size_h/2:marker_pos_w+marker_size_h/2], casting="unsafe") 
        np.add(display[marker_pos_h-marker_size_w/2:marker_pos_h+marker_size_w/2, marker_pos_w-marker_size_h/2:marker_pos_w+marker_size_h/2], m_img * m_mask, out=display[marker_pos_h-marker_size_w/2:marker_pos_h+marker_size_w/2, marker_pos_w-marker_size_h/2:marker_pos_w+marker_size_h/2], casting="unsafe")

    else:
        m_img = marker[p]
        m_mask = mask[p]
        
        np.multiply(display[marker_pos_h-marker_size_h/2:marker_pos_h+marker_size_h/2, marker_pos_w-marker_size_w/2:marker_pos_w+marker_size_w/2], 1 - m_mask, out=display[marker_pos_h-marker_size_h/2:marker_pos_h+marker_size_h/2, marker_pos_w-marker_size_w/2:marker_pos_w+marker_size_w/2], casting="unsafe") 
        np.add(display[marker_pos_h-marker_size_h/2:marker_pos_h+marker_size_h/2, marker_pos_w-marker_size_w/2:marker_pos_w+marker_size_w/2], m_img * m_mask, out=display[marker_pos_h-marker_size_h/2:marker_pos_h+marker_size_h/2, marker_pos_w-marker_size_w/2:marker_pos_w+marker_size_w/2], casting="unsafe")

def setChecker(display,name,p):
    robot_name, robot_pos = name.split("_")
    
    checker_pos_h, checker_pos_w = robots[robot_name][robot_pos]

    c_img = checker[p]
    c_mask = checker_mask[p]
    np.multiply(display[checker_pos_h-checker_size/2:checker_pos_h+checker_size/2, checker_pos_w-checker_size/2:checker_pos_w+checker_size/2], 1 - c_mask, out=display[checker_pos_h-checker_size/2:checker_pos_h+checker_size/2, checker_pos_w-checker_size/2:checker_pos_w+checker_size/2], casting="unsafe") 
    np.add(display[checker_pos_h-checker_size/2:checker_pos_h+checker_size/2, checker_pos_w-checker_size/2:checker_pos_w+checker_size/2], c_img * c_mask, out=display[checker_pos_h-checker_size/2:checker_pos_h+checker_size/2, checker_pos_w-checker_size/2:checker_pos_w+checker_size/2], casting="unsafe")

#jsonの内容
"""
    players
        b: "jiro" (string) - プレイヤー名 (blue side)
        r: "ishiro"(string) - プレイヤー名 (red side)
    ready
        b: True (boolean) - ジャッジサーバー接続確認、走行準備完了フラグ
        r: True (boolean) - ジャッジサーバー接続確認、走行準備完了フラグ
    scores
        b: 0 (int) - スコア
        r: 2 (int) - スコア
    state: "end" (string) - 試合ステート running, ready, end, etc...
    targets
        name: "one" (string) - ターゲット名 同じ名前はつけない。
        player: "r" (string) - 所有プレイヤーサイド r(BlueSide), b(BlueSide), n(NoPlayer)
        point: 1 (int) - ターゲットを取得したときのポイント
"""

#マーカーの設定
"""
marker_size = 32
neutral_marker = cv2.imread("picture/neutral_marker.png",-1)
neutral_marker, neutral_mask = getMask(neutral_marker, marker_size)
blue_marker = cv2.imread("picture/blue_marker.png",-1)
blue_marker, blue_mask = getMask(blue_marker, marker_size)
red_marker = cv2.imread("picture/red_marker.png",-1)
red_marker, red_mask = getMask(red_marker, marker_size)
"""

marker_size_w = 80
marker_size_h = 8
neutral_marker = cv2.imread(script_dir + "/picture/neutral_marker_bar.png",-1)
neutral_marker, neutral_mask = getMask_marker(neutral_marker, marker_size_w, marker_size_h)
blue_marker = cv2.imread(script_dir + "/picture/blue_marker_bar.png",-1)
blue_marker, blue_mask = getMask_marker(blue_marker, marker_size_w, marker_size_h)
red_marker = cv2.imread(script_dir + "/picture/red_marker_bar.png",-1)
red_marker, red_mask = getMask_marker(red_marker, marker_size_w, marker_size_h)

marker={}
marker["n"]=neutral_marker
marker["b"]=blue_marker
marker["r"]=red_marker

mask={}
mask["n"]=neutral_mask
mask["b"]=blue_mask
mask["r"]=red_mask

#チェッカーの設定
checker_size = 50
blue_checker = cv2.imread(script_dir + "/picture/blue_checker.png",-1)
blue_checker, blue_checker_mask = getMask_checker(blue_checker, checker_size)
red_checker = cv2.imread(script_dir + "/picture/red_checker.png",-1)
red_checker, red_checker_mask = getMask_checker(red_checker, checker_size)

checker={}
checker["b"]=blue_checker 
checker["r"]=red_checker

checker_mask={}
checker_mask["b"]=blue_checker_mask
checker_mask["r"]=red_checker_mask

#ウィンドウへの表示
def visualizeState(state_json, w_name):

    #サーバーから現状を取得
    print(state_json)
    j = json.dumps(state_json)
    state = json.loads(state_json)

    #ウィンドウサイズの決定
    display = cv2.imread(script_dir + "/picture/field_v6_3.png")
    
    #####
    #文字の表示（力技）
    cv2.putText(display, "Game State: " + state["state"], (w_width*1/4, w_height/20), font, font_size, text_color, thin)
    cv2.putText(display, "Players", (w_width*2/5, w_height*1/7), font, font_size, text_color, thin)
    cv2.putText(display, " Score ", (w_width*2/5, w_height*2/7-50), font, font_size, text_color, thin)
    #スコア表示
    for player, position in ("b", 0), ("r", w_width*12/20):
        if(state["ready"][player]):
            ready_color = p_color[player]
        else:
            ready_color = (200,200,200)
        cv2.putText(display, state["players"][player].center(10, ' '), (position,  w_height*1/7),font, font_size+2, ready_color, thin)
        cv2.putText(display, str(state["scores"][player]).center(10, ' '), (position,  w_height*2/7-50), font, font_size+2, ready_color, thin)
    
    if len(state["targets"])>0:
        i = 0
        for target in state["targets"]:
            if("BL" in target["name"] or "RE" in target["name"]):
                if(target["player"]!="n"):
                    setChecker(display,target["name"],target["player"])
                    #ロボットの背面ターゲットを取った場合に勝敗を表示
                    if(target["name"]=="BL_B"):
                        cv2.putText(display, " RED", (150,  675), font, 10, (0,0,255), 10)
                        cv2.putText(display, "WIN!", (750,  675), font, 10, (0,0,255), 10)
                        cv2.putText(display, "One-shot KO!", (480, 300), font, font_size+3, (0,0,255), 5)
                    if(target["name"]=="RE_B"):
                        cv2.putText(display, "BLUE", (150,  675), font, 10, (255,0,0), 10)
                        cv2.putText(display, "WIN!", (750,  675), font, 10, (255,0,0), 10)
                        cv2.putText(display, "One-shot KO!", (0,  300), font, font_size+3, (255,0,0), 5)
            else:
                setMarker(display,target["name"],target["player"])    
     
    #####
    
    cv2.imshow(w_name, display)
    cv2.waitKey(3)


if __name__ == "__main__":
    WINDOW_NAME = "Onigiri War!!"
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.moveWindow(WINDOW_NAME, 0, 0)
    
    while True:
        state = urlreq()
        visualizeState(state, WINDOW_NAME)
        sleep(1)

