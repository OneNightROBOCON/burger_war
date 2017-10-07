#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import rospy
from std_msgs.msg import String

if __name__ == "__main__":
    rospy.init_node("qr_reader")
    # publish qr_val
    qr_val_pub = rospy.Publisher('qr_val', String, queue_size=10)
    sample_id_list = ['hoge', 'fooo', 'barr', 'code',
                      'onig', 'robo', 'seve', 'byte']
    while not rospy.is_shutdown():
        for qr_id in sample_id_list:
            qr_val_pub.publish(qr_id)
            sleep(1)
