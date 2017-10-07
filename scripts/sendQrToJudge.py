#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
import requests
import json


class QrVal(object):

    def __init__(self, judge_url, side, player_name):
        # qr val subscriver
        self.qr_val_sub = rospy.Subscriber('/qr_val', String, self.qrValCallback)
        self.judge_url = judge_url
        self.historys = []
        self.side = side
        self.player_name = player_name

    def sendToJudge(self, qr_val):
        data = {"name": self.player_name, "side": self.side, "id": qr_val}
        res = requests.post(self.judge_url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res

    def qrValCallback(self, data):
        qr_val = data.data
        if qr_val in self.historys:
            return

        res = self.sendToJudge(qr_val)
        self.historys.append(qr_val)


if __name__ == "__main__":
    rospy.init_node("send_qr_to_judge")

    # TODO setting from launch file
    judge_url = 'http://127.0.0.1:5000/submits'
    player_name = 'jiro'
    side = 'r'

    qr = QrVal(judge_url, side, player_name)
    rospy.spin()
