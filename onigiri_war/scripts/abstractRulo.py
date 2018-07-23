#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from abc import ABCMeta, abstractmethod
from geometry_msgs.msg import Twist
from rulo_msgs.msg import Bumper
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2


class AbstractRulo(object):
    __metaclass__ = ABCMeta

    def __init__(self, bot_name):
        # bot name 
        self.name = bot_name

        # bumper state
        self.bumper = Bumper()
        self.left_bumper = False
        self.right_bumper = False

        # for convert image topic to opencv obj
        self.bridge = CvBridge()

        # velocity publisher
        self.vel_pub = rospy.Publisher('/Rulo/cmd_vel', Twist,queue_size=1)
	self.mode_pub = rospy.Publisher('/mobile_base/command/mode', String,queue_size=1)
        # bumper subscrivre
        self.bumper_sub = rospy.Subscriber('/mobile_base/event/bumper', Bumper, self.bumperCallback)

        # camera subscriver
        # please uncoment out if you use camera
        #self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.imageCallback)

    # bumper topic call back sample
    # update bumper state
    def bumperCallback(self, data):
        if data.left.state:
            self.left_bumper = True
        else:
            self.left_bumper = False

        if data.right.state == 1:
            self.right_bumper = True
        else:
            self.right_bumper = False

    # camera image call back sample
    # comvert image topic to opencv object and show
    def imageCallback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv2.imshow("Image window", cv_image)
        cv2.waitKey(3)

    @abstractmethod
    def strategy(self):
        pass

