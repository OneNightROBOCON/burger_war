#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This is dummy ar marker reader node.
mainly for judge server test.

by Takuya Yamaguhi.
'''

from time import sleep
import rospy
from std_msgs.msg import String

if __name__ == "__main__":
    rospy.init_node("qr_reader")
    # publish qr_val
    qr_val_pub = rospy.Publisher('target_id', String, queue_size=10)
    sample_id_list = ['0001', '0002', '0003', '0004',
                      '0005', '0006', '0007', '0008']
    while not rospy.is_shutdown():
        for qr_id in sample_id_list:
            qr_val_pub.publish(qr_id)
            sleep(3)
