// standard libs
#include <iostream>
#include <fstream>
#include <sstream>
#include <math.h>
#include <unistd.h>
#include <mutex>

#include <string>  //20171116 added by T.Okada

// aruco libs
#include "aruco.h"

// cv libs
#include "cvdrawingutils.h"
#include "opencv2/opencv.hpp"

// ROS libs
#include "ros/ros.h"
#include <tf/transform_broadcaster.h>
//#include <geometry_msgs/Pose.h>
//#include <geometry_msgs/PointStamped.h>
#include <visualization_msgs/MarkerArray.h>
#include <visualization_msgs/Marker.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>

#include <std_msgs/String.h>  //20171116 added by T.Okada

//#define DEBUG_BUILD

using namespace aruco;
using namespace cv;

cv::Mat current_image;

CameraParameters TheCameraParameters;
MarkerDetector MDetector;
vector<Marker> TheMarkers;

Dictionary di; //20171116 added by T.Okada


class ImageConverter
{
  Mat src_img;
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;

  public:
  ImageConverter() : it_(nh_)
  {
    image_sub_ = it_.subscribe("/image_raw", 1, &ImageConverter::imageCb, this); 
  }

  void getCurrentImage(cv::Mat *input_image)
  {
    *input_image = src_img;
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, "bgr8");
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }
    src_img = cv_ptr->image;   
  }
};


int main(int argc,char **argv) {
  // ROS messaging init
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  std::string camera_param_path;
  int scan_rate = 3;
  float TheMarkerSize = 0.02; //select the marker size (in m) by measuring it
  bool debug_view;
  if(!ros::param::get("~camera_param_path", camera_param_path))
  {
    ROS_INFO("No camera_param_path setting");
    camera_param_path = "/home/onigiribot/catkin_ws/src/onigiri_war/ros_aruco/data/ost.yaml";
  }
  if(!ros::param::get("~debug_view", debug_view))
  {
    ROS_INFO("No debug_view setting");
    debug_view = false;
  }

  ros::Rate rate(scan_rate);

  ImageConverter ic = ImageConverter();
  std_msgs::String msg_id;  //20171116 added by T.Okada

  while (current_image.empty()) 
  {
    rate.sleep();
    ros::spinOnce();
    ic.getCurrentImage(&current_image);
  }

  TheCameraParameters.readFromXMLFile(camera_param_path);  //20171116 added by T.Okada //20171121 yamaguchi
  TheCameraParameters.resize(current_image.size());

  MDetector.setThresholdParams(7, 7);
  MDetector.setThresholdParamRange(2, 0);
  std::map<uint32_t,MarkerPoseTracker> MTracker;

  MDetector.setDictionary("ARUCO_MIP_36h12",0.f);  //20171116 added by T.Okada
  ros::Publisher ar_pub = n.advertise<std_msgs::String>("target_id", 1); //20171116 added by T.Okada

  while (ros::ok()){
    rate.sleep();
    ros::spinOnce();

    ic.getCurrentImage(&current_image);

    // Detection of markers
    MDetector.detect(current_image, TheMarkers, TheCameraParameters, TheMarkerSize);


    for (unsigned int i = 0; i < TheMarkers.size(); i++) 
    {
      msg_id.data = std::to_string(TheMarkers[i].id); //20171116 added by T.Okada
      ar_pub.publish(msg_id); //20171116 added by T.Okada
      TheMarkers[i].draw(current_image, Scalar(0, 0, 255), 5);
    }

    // Show input with augmented information and the thresholded image
    if (debug_view)
    {
      cv::imshow("ROS_ARUCO", current_image);
      cv::waitKey(1);
    }
  }
}

