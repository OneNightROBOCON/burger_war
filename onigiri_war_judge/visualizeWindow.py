# -*- coding: utf-8 -*-

import requests
from time import sleep
import json
import numpy as np
import cv2
import os
import copy

class StatusWindow:
    def __init__(self, w_name=None, window_size=(960,1280), object_info_path=None, picture_path=None ):
        self.w_name = w_name
        cv2.namedWindow(self.w_name, cv2.WINDOW_NORMAL)
        cv2.moveWindow(self.w_name, 0, 0)
        if(picture_path is None):
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.script_dir = os.path.dirname(os.path.abspath(picture_path))


        image_file_path = self.script_dir + "/picture/field_plane.png"
        self.background_image = cv2.imread(image_file_path)

        #Window size
        self.w_height = window_size[0]
        self.w_width = window_size[1]
        self.font_size = 4
        self.text_thickness = 7
        self.text_color = (0,0,0)
        self.p_color = {"b": (255, 50, 50), "r": (100, 100, 255)}
        #Text font
        self.font = cv2.FONT_HERSHEY_PLAIN
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

        #Marker setting
        self.marker_size_h = 8
        self.marker_size_w = 80
        neutral_marker = cv2.imread(self.script_dir + "/picture/neutral_marker_bar.png",-1)
        neutral_marker, neutral_mask = self.getMask(neutral_marker, width=self.marker_size_w, height=self.marker_size_h)
        blue_marker = cv2.imread(self.script_dir + "/picture/blue_marker_bar.png",-1)
        blue_marker, blue_mask = self.getMask(blue_marker, width=self.marker_size_w, height=self.marker_size_h)
        red_marker = cv2.imread(self.script_dir + "/picture/red_marker_bar.png",-1)
        red_marker, red_mask = self.getMask(red_marker, width=self.marker_size_w, height=self.marker_size_h)

        self.marker={}
        self.marker["n"]=neutral_marker
        self.marker["b"]=blue_marker
        self.marker["r"]=red_marker

        self.mask={}
        self.mask["n"]=neutral_mask
        self.mask["b"]=blue_mask
        self.mask["r"]=red_mask

        #Checker setting
        self.checker_size = 50
        blue_checker = cv2.imread(self.script_dir + "/picture/blue_checker.png",-1)
        blue_checker, blue_checker_mask = self.getMask(blue_checker, size=self.checker_size)
        red_checker = cv2.imread(self.script_dir + "/picture/red_checker.png",-1)
        red_checker, red_checker_mask = self.getMask(red_checker, size=self.checker_size)

        self.checker={}
        self.checker["b"]=blue_checker 
        self.checker["r"]=red_checker

        self.checker_mask={}
        self.checker_mask["b"]=blue_checker_mask
        self.checker_mask["r"]=red_checker_mask

        #Robot marker position
        self.robots = {}
        self.robots["BL"] = {"L":(375,440), "R":(375,330), "B":(300,385)}
        self.robots["RE"] = {"L":(900,930), "R":(900,1040), "B":(970,980)}

        self.object_size = (100, 150)
        self.objects_info_path = self.script_dir + "/setting.json"
        object_info_file = open(self.objects_info_path, "r")
        self.objects_info = json.load(object_info_file)["objects"]

        # self.objects_name = []
        # for ob in self.objects_info.keys():
        #     print(ob)
        #     self.objects_name.append(self.objects_info[ob]["name"])
           

        # #self.objects_name = [self.objects_info["top_left"]["name"], self.objects_info["bottom_left"]["name"], self.objects_info["top_right"]["name"], self.objects_info["bottom_right"]["name"], self.objects_info["center"]["name"]]

        self.objects = {}
        # #Object marker position
        # #Tomato
        # self.objects[self.objects_name[0]] = {"N":(470,525), "S":(560,525)}
        # #Pudding
        # self.objects[self.objects_name[1]] = {"N":(470,790), "S":(560,790)}
        # #Fried egg
        # self.objects[self.objects_name[2]] = {"N":(680,525), "S":(775,525)}
        # #Octopus wiener
        # self.objects[self.objects_name[3]] = {"N":(680,790), "S":(775,790)}
        # #Fried shrimp
        # self.objects[self.objects_name[4]] = {"N":(575,660), "E":(630,715), "W":(630,595), "S":(680,660)}

        offset = 5
        for ob in self.objects_info.keys():
            #print(self.objects_info[ob]["name"])
            self.objects[self.objects_info[ob]["name"]] = {}
            
            if(self.objects_info[ob]["north"] == 1):
                self.objects[self.objects_info[ob]["name"]].update({"N":(self.objects_info[ob]["position"]["x"] - self.objects_info[ob]["size"]["height"]/2 - offset, self.objects_info[ob]["position"]["y"])})
            if(self.objects_info[ob]["south"] == 1):
                self.objects[self.objects_info[ob]["name"]].update({"S":(self.objects_info[ob]["position"]["x"] + self.objects_info[ob]["size"]["height"]/2 + offset, self.objects_info[ob]["position"]["y"])})
            if(self.objects_info[ob]["west"] == 1):
                self.objects[self.objects_info[ob]["name"]].update({"W":(self.objects_info[ob]["position"]["x"], self.objects_info[ob]["position"]["y"] - self.objects_info[ob]["size"]["width"]/2 - offset)})
            if(self.objects_info[ob]["north"] == 1):
                self.objects[self.objects_info[ob]["name"]].update({"E":(self.objects_info[ob]["position"]["x"], self.objects_info[ob]["position"]["y"] + self.objects_info[ob]["size"]["width"]/2 + offset)})
            

    def urlreq(self):
        resp = requests.get("http://localhost:5000/warState")
        return resp.text


    def getMask(self, _img, size=None, width=None, height=None):
        
        if(size is not None):
            img = cv2.resize(_img,(size, size))
        elif(width is not None and height is not None):
            img = cv2.resize(_img,(width, height))
        else:
            img = _img

        i_mask = img[:,:,3]  # アルファチャンネルだけ抜き出す。
        i_mask = cv2.cvtColor(i_mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
        i_mask = i_mask / 255.0  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。
        img = img[:,:,:3]  # アルファチャンネルは取り出しちゃったのでもういらない。

        return img, i_mask

    def setMarker(self, display, name, p):
        object_name,object_pos = name.split("_")
        
        marker_pos_h, marker_pos_w = self.objects[object_name][object_pos]

        if("E" in object_pos or "W" in object_pos):
            
            m_img = self.marker[p].transpose(1,0,2) 
            m_mask = self.mask[p].transpose(1,0,2)

            np.multiply(display[marker_pos_h-self.marker_size_w/2:marker_pos_h+self.marker_size_w/2, marker_pos_w-self.marker_size_h/2:marker_pos_w+self.marker_size_h/2], 1 - m_mask, out=display[marker_pos_h-self.marker_size_w/2:marker_pos_h+self.marker_size_w/2, marker_pos_w-self.marker_size_h/2:marker_pos_w+self.marker_size_h/2], casting="unsafe") 
            np.add(display[marker_pos_h-self.marker_size_w/2:marker_pos_h+self.marker_size_w/2, marker_pos_w-self.marker_size_h/2:marker_pos_w+self.marker_size_h/2], m_img * m_mask, out=display[marker_pos_h-self.marker_size_w/2:marker_pos_h+self.marker_size_w/2, marker_pos_w-self.marker_size_h/2:marker_pos_w+self.marker_size_h/2], casting="unsafe")

        else:
            m_img = self.marker[p]
            m_mask = self.mask[p]
            
            np.multiply(display[marker_pos_h-self.marker_size_h/2:marker_pos_h+self.marker_size_h/2, marker_pos_w-self.marker_size_w/2:marker_pos_w+self.marker_size_w/2], 1 - m_mask, out=display[marker_pos_h-self.marker_size_h/2:marker_pos_h+self.marker_size_h/2, marker_pos_w-self.marker_size_w/2:marker_pos_w+self.marker_size_w/2], casting="unsafe") 
            np.add(display[marker_pos_h-self.marker_size_h/2:marker_pos_h+self.marker_size_h/2, marker_pos_w-self.marker_size_w/2:marker_pos_w+self.marker_size_w/2], m_img * m_mask, out=display[marker_pos_h-self.marker_size_h/2:marker_pos_h+self.marker_size_h/2, marker_pos_w-self.marker_size_w/2:marker_pos_w+self.marker_size_w/2], casting="unsafe")

    def setChecker(self, display,name,p):
        robot_name, robot_pos = name.split("_")
        
        checker_pos_h, checker_pos_w = self.robots[robot_name][robot_pos]

        c_img = self.checker[p]
        c_mask = self.checker_mask[p]
        np.multiply(display[checker_pos_h-self.checker_size/2:checker_pos_h+self.checker_size/2, checker_pos_w-self.checker_size/2:checker_pos_w+self.checker_size/2], 1 - c_mask, out=display[checker_pos_h-self.checker_size/2:checker_pos_h+self.checker_size/2, checker_pos_w-self.checker_size/2:checker_pos_w+self.checker_size/2], casting="unsafe") 
        np.add(display[checker_pos_h-self.checker_size/2:checker_pos_h+self.checker_size/2, checker_pos_w-self.checker_size/2:checker_pos_w+self.checker_size/2], c_img * c_mask, out=display[checker_pos_h-self.checker_size/2:checker_pos_h+self.checker_size/2, checker_pos_w-self.checker_size/2:checker_pos_w+self.checker_size/2], casting="unsafe")

    def setImage(self, display, ob):
        
        pos_h = self.objects_info[ob]["position"]["x"]
        pos_w = self.objects_info[ob]["position"]["y"]
        print(pos_h, pos_w)
        
        img = cv2.imread(self.script_dir + "/picture/" + self.objects_info[ob]["name"] + ".png",-1)
        img, mask = self.getMask(img, height=self.objects_info[ob]["size"]["height"], width=self.objects_info[ob]["size"]["width"])
        height, width = img.shape[:2]
        print(height, width)
        np.multiply(display[pos_h-height/2:pos_h+height/2, pos_w-width/2:pos_w+width/2], 1 - mask, out=display[pos_h-height/2:pos_h+height/2, pos_w-width/2:pos_w+width/2], casting="unsafe") 
        np.add(display[pos_h-height/2:pos_h+height/2, pos_w-width/2:pos_w+width/2], img * mask, out=display[pos_h-height/2:pos_h+height/2, pos_w-width/2:pos_w+width/2], casting="unsafe")

        return display

    def setObject(self, display):
        display = copy.deepcopy(self.background_image)
        for ob in self.objects_info.keys():
            display = self.setImage(display, ob)            
        return display

    def initWindow(self):
        display = copy.deepcopy(self.background_image)
        display = self.setObject(display)
        # cv2.imshow(self.w_name, display)
        # cv2.waitKey(3)
        return display

    #jsonの内容
        # players
        #     b: "jiro" (string) - プレイヤー名 (blue side)
        #     r: "ishiro"(string) - プレイヤー名 (red side)
        # ready
        #     b: True (boolean) - ジャッジサーバー接続確認、走行準備完了フラグ
        #     r: True (boolean) - ジャッジサーバー接続確認、走行準備完了フラグ
        # scores
        #     b: 0 (int) - スコア
        #     r: 2 (int) - スコア
        # state: "end" (string) - 試合ステート running, ready, end, etc...
        # targets
        #     name: "one" (string) - ターゲット名 同じ名前はつけない。
        #     player: "r" (string) - 所有プレイヤーサイド r(BlueSide), b(BlueSide), n(NoPlayer)
        #     point: 1 (int) - ターゲットを取得したときのポイント  

    #Show window
    def update(self, _display):

        state_json = self.urlreq()
        #Get current state
        print(state_json)
        j = json.dumps(state_json)
        state = json.loads(state_json)
        
        #Get background image
        display = copy.deepcopy(_display)
        
        #####
        #文字の表示（力技）
        cv2.putText(display, "Game State: " + state["state"], (self.w_width*1/4, self.w_height/20), self.font, self.font_size, self.text_color, self.text_thickness)
        s = cv2.getTextSize("Game State: " + state["state"], self.font, self.font_size, self.text_thickness)
        cv2.putText(display, "Players", (self.w_width*2/5, self.w_height*1/7), self.font, self.font_size, self.text_color, self.text_thickness)
        cv2.putText(display, " Score ", (self.w_width*2/5, self.w_height*2/7-50), self.font, self.font_size, self.text_color, self.text_thickness)
        #スコア表示
        for player, position in ("b", 0), ("r", self.w_width*12/20):
            if(state["ready"][player]):
                ready_color = self.p_color[player]
            else:
                ready_color = (200,200,200)
            cv2.putText(display, state["players"][player].center(10, ' '), (position,  self.w_height*1/7),self.font, self.font_size+2, ready_color, self.text_thickness)
            cv2.putText(display, str(state["scores"][player]).center(10, ' '), (position,  self.w_height*2/7-50), self.font, self.font_size+2, ready_color, self.text_thickness)
        
        if len(state["targets"])>0:
            
            for target in state["targets"]:
                if("BL" in target["name"] or "RE" in target["name"]):
                    if(target["player"]!="n"):
                        self.setChecker(display,target["name"],target["player"])
                        #ロボットの背面ターゲットを取った場合に勝敗を表示
                        if(target["name"]=="BL_B"):
                            cv2.putText(display, " RED", (150,  720), self.font, 10, (0,0,255), 10)
                            cv2.putText(display, "WIN!", (750,  720), self.font, 10, (0,0,255), 10)
                            cv2.putText(display, "One-shot KO!", (480, 300), self.font, self.font_size+3, (0,0,255), 5)
                        if(target["name"]=="RE_B"):
                            cv2.putText(display, "BLUE", (150,  720), self.font, 10, (255,0,0), 10)
                            cv2.putText(display, "WIN!", (750,  720), self.font, 10, (255,0,0), 10)
                            cv2.putText(display, "One-shot KO!", (0,  300), self.font, self.font_size+3, (255,0,0), 5)
                else:
                    self.setMarker(display,target["name"],target["player"])    
        
        #####
        
        cv2.imshow(self.w_name, display)
        cv2.waitKey(3)


if __name__ == "__main__":
    sw = StatusWindow(w_name="Onigiri War")

    display = sw.initWindow()
    
    while(True):
        sw.update(display)
        sleep(0.1)