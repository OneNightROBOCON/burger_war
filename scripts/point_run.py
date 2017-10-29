#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import numpy as np


class OnigiriRun(object):

    def __init__(self):

	#ROS publisher
	self.goal_point_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)

	f=open('point_list.txt')
	point_str = f.read()
	f.close()
	point = []
	point_data_str = point_str.split('\n') 
	for point_data in point_data_str:
		if point_data == '':
			continue
		point_list = []
		point_num_list = point_data.split(' ')
		for point_num in point_num_list:
			point_list.append(float(point_num))
		point.append(point_list)
	print point
	self.pose = PoseStamped()
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z
        quat = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
        pose.pose.orientation.x = quat[0]
        pose.pose.orientation.y = quat[1]
        pose.pose.orientation.z = quat[2]
        pose.pose.orientation.w = quat[3]
        pose.header.frame_id = "/map"
        pose.header.stamp = rospy.Time.now()

if __name__=="__main__":
    rospy.init_node("onigiri_run")
    OnigiriRun()
    rospy.spin()
