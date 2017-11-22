#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2


class QrReader(object):

    def __init__(self):
        # for convert image topic to opencv obj
        self.bridge = CvBridge()

        # camera subscriver
        self.image_sub = rospy.Subscriber('/image_raw', Image, self.imageCallback, queue_size=1)

        # publish qr_val
        self.qr_val_pub = rospy.Publisher('qr_val', String, queue_size=1)

        # publish marked qr area image
        self.qr_img_pub = rospy.Publisher('qr_image', Image, queue_size=1)

    # comvert image topic to opencv object and show
    def imageCallback(self, data):
        try:
            im = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        # read AR code
        aruco = cv2.aruco
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_7X7_50)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(im, dictionary)
        aruco.drawDetectedMarkers(im, corners, ids)
        if ids is not None:
            for i in ids:
                self.qr_val_pub.publish(str(i[0]))
        
        im_msg = self.bridge.cv2_to_imgmsg(im, "bgr8")
        self.qr_img_pub.publish(im_msg)


if __name__ == "__main__":
    rospy.init_node("ar_reader")
    qr = QrReader()
    rospy.spin()
