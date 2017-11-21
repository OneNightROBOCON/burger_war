#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import tf
from std_msgs.msg import String
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalStatusArray
from actionlib_msgs.msg import GoalStatus
import numpy as np


class OnigiriRun(object):

    def __init__(self):
	self.goal_count = 0
	self.movebase_status = 0
	#ROS publisher
	self.goal_point_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)
	#ROS subscriber
	self.move_base_status_sub = rospy.Subscriber('/move_base/status', GoalStatusArray, self.GoalStatusArrayCallback, queue_size=1)

	f=open('/home/ubuntu/catkin_ws/src/onigiri_war/scripts/point_list.txt')
	point_str = f.read()
	f.close()
	self.point = []
	point_data_str = point_str.split('\n') 
	for point_data in point_data_str:
		if point_data == '':
			continue
		point_list = []
		point_num_list = point_data.split(' ')
		for point_num in point_num_list:
			point_list.append(float(point_num))
		self.point.append(point_list)
	print self.point

    def GoalStatusArrayCallback(self, data):
	print self.movebase_status
	status_id = 0;
	#uint8 PENDING         = 0  
	#uint8 ACTIVE          = 1 
	#uint8 PREEMPTED       = 2
	#uint8 SUCCEEDED       = 3
	#uint8 ABORTED         = 4
	#uint8 REJECTED        = 5
	#uint8 PREEMPTING      = 6
	#uint8 RECALLING       = 7
	#uint8 RECALLED        = 8
	#uint8 LOST            = 9

	if len(data.status_list) != 0:
		goalStatus = data.status_list[0]
    		status_id = goalStatus.status
		print status_id
	#moving
	if self.movebase_status == 1:
		if status_id == 3 or status_id == 0:
			self.movebase_status = 2
		elif status_id == 4:
			self.movebase_status = 4
		return
	#stop or goal
	elif self.movebase_status == 0 or self.movebase_status == 2:
		self.pose = PoseStamped()
       		self.pose.pose.position.x = self.point[self.goal_count][0]
        	self.pose.pose.position.y = self.point[self.goal_count][1]
        	self.pose.pose.position.z = 0.0
        	#quat = tf.transformations.quaternion_from_euler(0.0, 0.0, 0.0)
        	self.pose.pose.orientation.x = 0
        	self.pose.pose.orientation.y = 0
        	self.pose.pose.orientation.z = self.point[self.goal_count][2]
        	self.pose.pose.orientation.w = self.point[self.goal_count][3]
        	self.pose.header.frame_id = "/map"
        	self.pose.header.stamp = rospy.Time.now()
		self.goal_point_pub.publish(self.pose)
		if (self.goal_count + 1) >= len(self.point):
			self.goal_count = 0
		else:
			self.goal_count += 1
		self.movebase_status = 3
		return
	elif self.movebase_status == 3:
		if status_id == 0:
			self.movebase_status = 0
		elif status_id == 3:
			return
		else:
			self.movebase_status = 1
			return
	elif self.movebase_status == 4:
		self.movebase_status = 0
		return
		

if __name__=="__main__":
    rospy.init_node("onigiri_run")
    OnigiriRun()
    rospy.spin()
