#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import random
import time

from abstractCcr import *
from geometry_msgs.msg import Twist

class WallRunBot(AbstractCcr):
    '''
    self.opt = [LeftLaserScan, RightLaserScan]
    left turn
    stright
    '''

    def strategy(self):
        r = rospy.Rate(10)

        DIST_THRETH_CM = 0.2 # m

        while not rospy.is_shutdown():
            if len(self.opt[0].ranges) == 0:
                r.sleep()
                continue

            if self.opt[0].ranges[0] < DIST_THRETH_CM:
                # turn at corner
                x = -0.1
                th = 0.5 
            elif self.opt[1].ranges[0] < 0.1:
                # too near wall
                x = -0.1
                th = 0.5
            elif self.opt[1].ranges[0] < DIST_THRETH_CM:
                # far from wall
                x = 0.1
                th = 0.2
            else:
                # near to wall
                x = 0.1
                th = -0.2

            twist = Twist()
            twist.linear.x = x; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
            self.vel_pub.publish(twist)


            # for debug
            print(self.opt[0].ranges[0])
            print(self.opt[1].ranges[0])
            print(twist)
            print('')

            r.sleep()

if __name__ == '__main__':
    rospy.init_node('random_ccr')
    bot = WallRunBot(use_opt=True)
    bot.strategy()

