#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is Speed limitter for burger bot

subscribe 'cmd_vel' topic. 
publish 'limited_cmd_vel' topic

by Takuya Yamaguhi.
'''

import rospy
from time import sleep
from geometry_msgs.msg import Twist


class SpeedLimitter(object):

    def __init__(self, max_linear_vel, max_ang_vel):
        # target ID  val subscriver
        self.max_linear_vel = max_linear_vel
        self.max_ang_vel = max_ang_vel
        self.target_id_sub = rospy.Subscriber('cmd_vel', Twist, self.cmdVelCallback)
        # ADD limited cdm vel publisser
        self.vel_pub = rospy.Publisher('limited_cmd_vel', Twist,queue_size=1)

    def cmdVelCallback(self, data):
        # check limit velocity
        if data.linear.x > self.max_linear_vel:
            data.linear.x = self.max_linear_vel
        elif data.linear.x < -self.max_linear_vel:
            data.linear.x  = -self.max_linear_vel

        if data.angular.z > self.max_ang_vel:
            data.angular.z = self.max_ang_vel
        elif data.angular.z < -self.max_ang_vel:
            data.angular.z = -self.max_ang_vel
    
        # Publish limited_cmd_vel
        self.vel_pub.publish(data)


if __name__ == "__main__":
    rospy.init_node("speed_limitter")
    MAX_LINEAR_VEL = float(rospy.get_param('~max_linear_vel', "0.22"))
    MAX_ANG_VEL = float(rospy.get_param('~max_ang_vel', "2.84"))
    speed_limitter = SpeedLimitter(MAX_LINEAR_VEL, MAX_ANG_VEL)
    rospy.spin()    


