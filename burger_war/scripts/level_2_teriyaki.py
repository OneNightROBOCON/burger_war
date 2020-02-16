#!/usr/bin/env python
# -*- coding: utf-8 -*-

# level_2_teriyaki.py
# write by yamaguchi takuya @dashimaki360
## GO around field by AMCL localizer


import rospy
import random

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan

import tf

PI = 3.1416
# 8x8  [rad]
TARGET_TH = (
    (-PI/4, -PI/4, -PI/2, -PI/2, -PI*3/4, -PI*3/4, -PI*3/4, -PI*3/4),
    (-PI/4, -PI/4, -PI/4, -PI/4, -PI*3/4, -PI*3/4, -PI*3/4, -PI*3/4),
    (-PI/4, -PI/4, -PI/4,     0,   -PI/2, -PI*3/4, -PI*3/4,      PI),
    (-PI/4, -PI/4,     0,     0,   -PI/2,   -PI/2, -PI*3/4,      PI),
    (    0,  PI/4,  PI/2,  PI/2,      PI,      PI,  PI*3/4,  PI*3/4),
    (    0,  PI/4,  PI/3,  PI/2,      PI,  PI*3/4,  PI*3/4,  PI*3/4),
    ( PI/4,  PI/4,  PI/3,  PI/4,  PI*3/4,  PI*3/4,  PI*3/4,  PI*3/4),
    ( PI/4,  PI/4,  PI/4,  PI/4,    PI/2,    PI/2,  PI*3/4,  PI*3/4),
)
WIDTH = 1.2 * (2 **0.5) # [m]

class TeriyakiBurger():
    def __init__(self, bot_name):
        # bot name 
        self.name = bot_name
        # robot state 'inner' or 'outer'
        self.state = 'inner' 
        # robot wheel rot 
        self.wheel_rot_r = 0
        self.wheel_rot_l = 0
        self.pose_x = 0
        self.pose_y = 0

        self.k = 0.5

        # speed [m/s]
        self.speed = 0.07

        # publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        # subscriber
        self.pose_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.poseCallback)
        self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallback)

        self.twist = Twist()
        self.twist.linear.x = self.speed; self.twist.linear.y = 0.; self.twist.linear.z = 0.
        self.twist.angular.x = 0.; self.twist.angular.y = 0.; self.twist.angular.z = 0.
 


    def poseCallback(self, data):
        '''
        pose topic from amcl localizer
        update robot twist
        '''
        pose_x = data.pose.pose.position.x
        pose_y = data.pose.pose.position.y
        quaternion = data.pose.pose.orientation
        rpy = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))
        th = rpy[2]

        th_xy = self.calcTargetTheta(pose_x,pose_y)
        
        th_diff = th_xy - th
        while not PI >= th_diff >= -PI:
            if th_diff > 0:
                th_diff -= 2*PI
            elif th_diff < 0:
                th_diff += 2*PI
        new_twist_ang_z = th_diff * self.k
        
        self.twist.angular.z = new_twist_ang_z
        print(pose_x, pose_y, th, th_xy, new_twist_ang_z)


    def calcTargetTheta(self, pose_x, pose_y):
        x = self.poseToindex(pose_x)
        y = self.poseToindex(pose_y)
        th = TARGET_TH[x][y]
        print("POSE pose_x: {}, pose_y: {}. INDEX x:{}, y:{}".format(pose_x, pose_y, x, y))
        return th

    def poseToindex(self, pose):
        i = 7 - int((pose + WIDTH) / (2 * WIDTH) * 8)
        i = max(0, min(7, i))
        return i

    def lidarCallback(self, data):
        '''
        lidar scan use for bumper
        controll speed.x
        '''
        is_near_wall = self.isNearWall(data.ranges)
        if is_near_wall:
            self.twist.linear.x = -self.speed
        else:
            self.twist.linear.x = self.speed

    def isNearWall(self, scan):
        if not len(scan) == 360:
            return False
        forword_scan = scan[:10] + scan[-10:]
        # drop too small value ex) 0.0
        forword_scan = [x for x in forword_scan if x > 0.1]
        if min(forword_scan) < 0.2:
            return True
        return False

    def strategy(self):
        '''
        calc Twist and publish cmd_vel topic
        Go and Back loop forever
        '''
        r = rospy.Rate(10) # change speed 10fps

        while not rospy.is_shutdown():
            # publish twist topic
            self.vel_pub.publish(self.twist)

            r.sleep()


if __name__ == '__main__':
    rospy.init_node('enemy')
    bot = TeriyakiBurger('teriyaki_burger')
    bot.strategy()

