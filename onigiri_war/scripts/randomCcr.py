#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import rospkg
import random
import time

from abstractCcr import *
from geometry_msgs.msg import Twist

class RandomBot(AbstractCcr):
    '''
    AbstractCcr を継承
    '''
    def strategy(self):
        r = rospy.Rate(100)

        UPDATE_FREQUENCY = 1 # 1sec
        update_time = 0

        while not rospy.is_shutdown():
            if self.left_bumper or self.right_bumper:
                update_time = time.time()
                rospy.loginfo('bumper hit!!')
		x = 0
                th = 1

            elif time.time() - update_time > UPDATE_FREQUENCY:
                update_time = time.time()
                value = random.randint(1,1000)
                if value < 500: x = 0.2
                    th = 0

                elif value < 750:
                    x = 0
                    th = 1

                elif value < 1000:
                    x = 0
                    th = -1
                else:
                    x = 0
                    th = 0

            twist = Twist()
            twist.linear.x = x; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
            self.vel_pub.publish(twist)

            r.sleep()

if __name__ == '__main__':
    rospy.init_node('random_ccr')
    bot = RandomBot(use_bumper=True)
    bot.strategy()
