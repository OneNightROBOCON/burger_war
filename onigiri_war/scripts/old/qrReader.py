#!/usr/bin/env python
# -*- coding: utf-8 -*-
import libqr # local lib
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np


class QrReader(object):

    def __init__(self):
        # for convert image topic to opencv obj
        self.bridge = CvBridge()

        # camera subscriver
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.imageCallback, queue_size=1)

        # qr reader lib
        self.reader = libqr.QrReader()

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

        #im = self.crop(im)

        # read QR code
        qrs = self.reader.readQr(im)
        if qrs:
            print(qrs)
        for qr in qrs:
            # make marked image
            pts = np.array(qr["pos"], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(im,[pts],True,(255,0,0) , 10)

            # pub qr_val
            str = qr["val"]
            self.qr_val_pub.publish(str)

        im_msg = self.bridge.cv2_to_imgmsg(im, "bgr8")
        self.qr_img_pub.publish(im_msg)

        #cv2.imshow("Capture", im)
        #cv2.waitKey(33)
    def crop(self, im):
        sh = im.shape
        w = int(sh[1]/2)
        h = int(sh[0]/2)
        x = int(sh[1]/4)
        y = int(sh[0]/4)
        croped_im =  im[y:y+h, x:x+w]
        return croped_im

if __name__=="__main__":
    rospy.init_node("qr_reader")
    qr = QrReader()
    rospy.spin()
