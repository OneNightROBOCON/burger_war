#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from actionlib_msgs.msg import actionlib
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import numpy as np


class OnigiriRun(object):

    def __init__(self):

	#ROS subscriver
	f=open('point_list.txt')
	point_data = f.read()
	f.close()
	point_list_str = point_data.split('n')
	point_list = []
	for point in point_list_str:
		point_list.append(float(point))
	
        self.opt_left_sub = rospy.Subscriber('/move_base/status', LaserScan, self.LaserScanCallback, queue_size=1)
	
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
