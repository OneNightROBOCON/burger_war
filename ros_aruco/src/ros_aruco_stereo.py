
import sys
import rospy
import numpy as np
from sensor_msgs.msg import Image
from stereo_msgs.msg import DisparityImage
from geometry_msgs.msg import Pose
import cv2
from cv_bridge import CvBridge, CvBridgeError
import math
import time

class disp_centre:
	def __init__(self):
		self.bridge = CvBridge()
		self.c_x = 1
		self.c_y = 1
		self.flag = 0

	def centre_callback(self,msg):
		#print "centre_call"
		self.flag = 1
		self.c_x = msg.position.x 
		self.c_y = msg.position.y
		#print (self.c_x,self.c_y)
	
	def stereo_callback(self,data):
		#print "stereo_call"
		self.im_array = self.bridge.imgmsg_to_cv2(data.image)
		focal = data.f
		base = data.T
		#cv2.imshow("test",a)
		if self.flag == 1:
			if self.im_array.item(self.c_y,self.c_x) == 0:
				print ("disparity is 0")
			else:
				print (focal*base)/self.im_array.item(self.c_y,self.c_x)
			#print self.im_array.item(self.c_y,self.c_x)
			
		else:
			self.flag = 0
	
		
def main(args):
  rospy.init_node("listener", anonymous=True)
  ic = disp_centre()
  rospy.init_node('listener',anonymous=True)
  rospy.Subscriber("/camera/disparity",DisparityImage, ic.stereo_callback)
  rospy.Subscriber("/aruco/centre/pose",Pose, ic.centre_callback)
  rospy.spin()  
if __name__ == '__main__':
    main(sys.argv)
