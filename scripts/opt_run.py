#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import numpy as np


class OnigiriRun(object):

    def __init__(self):
        # for convert image topic to opencv obj
        #self.bridge = CvBridge()

	#ROS subscriver
        # camera
        #self.image_sub = rospy.Subscriber('/image_raw', Image, self.imageCallback, queue_size=1)
	# opt_left
        self.opt_left_sub = rospy.Subscriber('/mobile_base/event/opt_left', LaserScan, self.LaserScanCallback, queue_size=1)
	
	#ROS publisher
	self.cmd_vel_pub = rospy.Publisher('/Rulo/cmd_vel', Twist, queue_size=1)


    # 
    def LaserScanCallback(self, data):
	vel = Twist()
	vel.linear.x = 0.2
        self.range = data.ranges[0]
	if self.range > 0.11:
		vel.angular.z = 0.5+(self.range-0.1)*2
	elif self.range < 0.09:
		vel.angular.z = -0.5+(self.range-0.1)*2
	else:
		vel.angular.z = 0
	self.cmd_vel_pub.publish(vel) 

if __name__=="__main__":
    rospy.init_node("onigiri_run")
    OnigiriRun()
    rospy.spin()
