#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is ar marger Id send node.
subscribe 'target_id' topic. 
if subscribe 'target_id' then post ID to judge server.

by Takuya Yamaguhi.
'''

import rospy
from std_msgs.msg import String
from aruco_msgs.msg import MarkerArray
import requests
import json
from time import sleep


class TargetId(object):

    def __init__(self, judge_url, side, player_name, init_code='0000'):
        # target ID  val subscriver
        self.target_id_sub = rospy.Subscriber('target_id', MarkerArray, self.targetIdCallback)
        self.judge_url = judge_url
        self.historys = []
        self.side = side
        self.player_name = player_name
        self.init_code = init_code

    def sendToJudge(self, target_id):
        data = {"name": self.player_name, "side": self.side, "id": target_id}
        res = requests.post(self.judge_url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res

    def sendInitCode(self):
        try:
            res = self.sendToJudge(self.init_code)
        except:
            print("Requests Error Please Check URL " + self.judge_url)
            return False
        else:
            print("Send " + self.init_code + " as init code To " + self.judge_url)
            print(res)
            return res

    def lengthTo4(self, string):
        '''
        cut or padding string length to 4
        if length is more than 4
          use last 4 char
        if length is less than 4
          padding "0"
        ex) "0123456789" -> "6789"
            "0123" -> "0123" (no change)
            "12" -> "0012"
        '''
        length = len(string)
        if length == 4:
            return string
        elif length > 4:
            return string[-4:]
        elif length < 4:
            return ("0000"+string)[-4:]
        else:
            print("what happen??")
            print(string)
            return False

    def targetIdCallback(self, data):
        markers = data.markers
        for marker in markers:
            target_id = str(marker.id)
            target_id = self.lengthTo4(target_id)
            # if target_id in self.historys:
            #     return
            try:
                resp_raw = self.sendToJudge(target_id)
            except:
                print("Try Send " + target_id + " but, Requests Error Please Check URL " + self.judge_url)
            else:
                resp = json.loads(resp_raw.text)
                print("Send " + target_id + " To " + self.judge_url)
                print(resp)
                # if resp["error"] == "no error" or resp["error"] == "ERR not mutch id":
                #     self.historys.append(target_id)


class WarStatePublisher(object):
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

    def __init__(self, judge_url):
        # target ID  val subscriver
        self.judge_url = judge_url
        self.vel_pub = rospy.Publisher('war_state', String, queue_size=1)

    def publishWarState(self):
        resp = requests.get(self.judge_url)
        msg = resp.text
        self.vel_pub.publish(msg)
        return msg


if __name__ == "__main__":
    rospy.init_node("send_id_to_judge")

    # set param from launch param
    JUDGE_URL = rospy.get_param('~judge_url', 'http://127.0.0.1:5000')
    PLAYER_NAME = rospy.get_param('~player_name', 'NoName')
    SIDE = rospy.get_param('~side', 'r')

    INIT_CODE = '0000'

    target_id = TargetId(JUDGE_URL + "/submits", SIDE, PLAYER_NAME, INIT_CODE)
    state_publisher = WarStatePublisher(JUDGE_URL + "/warState")
    while not rospy.is_shutdown() and target_id.sendInitCode() == False:
        sleep(3)

    while not rospy.is_shutdown():
        state_publisher.publishWarState()
        sleep(3)


