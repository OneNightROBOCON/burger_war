#!/usr/bin/env python
# -*- coding: utf-8 -*-

# level_3_clubhouse.py
# write by yamaguchi takuya @dashimaki360
## GO around field by AMCL localizer, and find enemy.

import rospy
import random
import math

from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan

import tf

PI = math.pi
# 8x8  [rad]
TARGET_TH = (
    (-PI/4, -PI/4, -PI/2, -PI/2, -PI*3/4, -PI*3/4, -PI*3/4, -PI*3/4),
    (-PI/4, -PI/4, -PI/3, -PI/2, -PI*3/5, -PI*3/4, -PI*3/4, -PI*3/4),
    (-PI/4, -PI/4, -PI/6,     0,   -PI/2, -PI*3/4,     -PI,  PI*3/4),
    (-PI/4, -PI/5,     0,     0,      PI,  PI*6/10,  PI*3/4,    PI/2),
    (    0,     0,  PI/2,  PI/2,      PI,  PI*3/4,  PI*3/4,    PI/2),
    (    0,  PI/4,  PI/3,  PI/2,  PI*5/6,  PI*3/4,  PI*3/4,  PI*3/4),
    ( PI/4,  PI/4,  PI/3,  PI/4,  PI*5/6,    PI/2,  PI*3/4,  PI*3/4),
    ( PI/4,  PI/4,  PI/4,  PI/4,    PI/2,    PI/2,  PI*3/4,  PI*3/4),
)
WIDTH = 1.2 * (2 **0.5) # [m]


# respect is_point_enemy freom team rabbit
# https://github.com/TeamRabbit/burger_war
class EnemyDetector:
    '''
    Lidarのセンサ値から簡易的に敵を探す。
    obstacle detector などを使ったほうがROSらしいがそれは参加者に任せます。
    いろいろ見た感じ Team Rabit の実装は綺麗でした。
    方針
    実測のLidarセンサ値 と マップと自己位置から期待されるLidarセンサ値 を比較
    ズレている部分が敵と判断する。
    この判断は自己位置が更新された次のライダーのコールバックで行う。（フラグで管理）
    0.7m 以上遠いところは無視する。少々のズレは許容する。
    '''
    def __init__(self):
        self.max_distance = 0.7
        self.thresh_corner = 0.25
        self.thresh_center = 0.35

        self.pose_x = 0
        self.pose_y = 0
        self.th = 0
    

    def findEnemy(self, scan, pose_x, pose_y, th):
        '''
        input scan. list of lider range, robot locate(pose_x, pose_y, th)
        return is_near_enemy(BOOL), enemy_direction[rad](float)
        '''
        if not len(scan) == 360:
            return False
        
        # update pose
        self.pose_x = pose_x
        self.pose_y = pose_y
        self.th = th

        # drop too big and small value ex) 0.0 , 2.0 
        near_scan = [x if self.max_distance > x > 0.1 else 0.0 for x in scan]

        enemy_scan = [1 if self.is_point_emnemy(x,i) else 0 for i,x in  enumerate(near_scan)]

        is_near_enemy = sum(enemy_scan) > 5  # if less than 5 points, maybe noise
        if is_near_enemy:
            idx = enemy_scan.index(1)
            enemy_direction = idx / 360.0 * 2*PI
            enemy_dist = near_scan[idx]
        else:
            enemy_direction = None
            enemy_dist = None

        #print("Enemy: {}, Direction: {}".format(is_near_enemy, enemy_direction))
        #print("enemy points {}".format(sum(enemy_scan)))
        return is_near_enemy, enemy_direction, enemy_dist
        

    def is_point_emnemy(self, dist, ang_deg):
        if dist == 0:
            return False

        ang_rad = ang_deg /360. * 2 * PI
        point_x = self.pose_x + dist * math.cos(self.th + ang_rad)
        point_y = self.pose_y + dist * math.sin(self.th + ang_rad)

        #フィールド内かチェック
        if   point_y > (-point_x + 1.53):
            return False
        elif point_y < (-point_x - 1.53):
            return False
        elif point_y > ( point_x + 1.53):
            return False
        elif point_y < ( point_x - 1.53):
            return False

        #フィールド内の物体でないかチェック
        len_p1 = math.sqrt(pow((point_x - 0.53), 2) + pow((point_y - 0.53), 2))
        len_p2 = math.sqrt(pow((point_x - 0.53), 2) + pow((point_y + 0.53), 2))
        len_p3 = math.sqrt(pow((point_x + 0.53), 2) + pow((point_y - 0.53), 2))
        len_p4 = math.sqrt(pow((point_x + 0.53), 2) + pow((point_y + 0.53), 2))
        len_p5 = math.sqrt(pow(point_x         , 2) + pow(point_y         , 2))

        if len_p1 < self.thresh_corner or len_p2 < self.thresh_corner or len_p3 < self.thresh_corner or len_p4 < self.thresh_corner or len_p5 < self.thresh_center:
            return False
        else:
            #print(point_x, point_y, self.pose_x, self.pose_y, self.th, dist, ang_deg, ang_rad)
            #print(len_p1, len_p2, len_p3, len_p4, len_p5)
            return True

# End Respect

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
        self.th = 0

        self.k = 0.7

        # speed [m/s]
        self.speed = 0.08

        self.is_near_wall = False

        # publisher
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        # subscriber
        self.pose_sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, self.poseCallback)
        self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallback)

        self.pose_twist = Twist()
        self.pose_twist.linear.x = self.speed; self.pose_twist.linear.y = 0.; self.pose_twist.linear.z = 0.
        self.pose_twist.angular.x = 0.; self.pose_twist.angular.y = 0.; self.pose_twist.angular.z = 0.

        self.is_near_enemy = False
        self.enemy_direction = None
        self.enemy_dist = None
        self.near_enemy_twist = Twist()
        self.near_enemy_twist.linear.x = self.speed; self.near_enemy_twist.linear.y = 0.; self.near_enemy_twist.linear.z = 0.
        self.near_enemy_twist.angular.x = 0.; self.near_enemy_twist.angular.y = 0.; self.near_enemy_twist.angular.z = 0.

        self.is_initialized_pose = False
        self.enemy_detector = EnemyDetector()
        


    def poseCallback(self, data):
        '''
        pose topic from amcl localizer
        update robot twist
        '''
        self.pose_x = data.pose.pose.position.x
        self.pose_y = data.pose.pose.position.y
        quaternion = data.pose.pose.orientation
        rpy = tf.transformations.euler_from_quaternion((quaternion.x, quaternion.y, quaternion.z, quaternion.w))

        self.th = rpy[2]
        th_xy = self.calcTargetTheta(self.pose_x,self.pose_y)
        
        self.updatePoseTwist(self.th, th_xy)
        self.is_initialized_pose = True

    def updatePoseTwist(self, th, th_xy):
        # update pose twist
        th_diff = th_xy - th
        while not PI >= th_diff >= -PI:
            if th_diff > 0:
                th_diff -= 2*PI
            elif th_diff < 0:
                th_diff += 2*PI
        new_twist_ang_z = th_diff * self.k
        
        self.pose_twist.angular.z = new_twist_ang_z
        self.pose_twist.linear.x = self.speed
        #print(th, th_xy, new_twist_ang_z)

    def calcTargetTheta(self, pose_x, pose_y):
        x = self.poseToindex(pose_x)
        y = self.poseToindex(pose_y)
        th = TARGET_TH[x][y]
        #print("POSE pose_x: {}, pose_y: {}. INDEX x:{}, y:{}".format(pose_x, pose_y, x, y))
        return th

    def poseToindex(self, pose):
        i = 7 - int((pose + WIDTH) / (2 * WIDTH) * 8)
        i = max(0, min(7, i))
        return i

    def lidarCallback(self, data):
        '''
        lidar scan use for bumper , and find enemy
        controll speed.x
        '''
        self.is_near_wall = self.isNearWall(data.ranges)
        
        # enemy detection
        if self.is_initialized_pose:
            self.is_near_enemy, self.enemy_direction, self.enemy_dist = self.enemy_detector.findEnemy(data.ranges, self.pose_x, self.pose_y, self.th)
        
        if self.is_near_enemy:
            self.updateNearEnemyTwist()

    def updateNearEnemyTwist(self):
        # update pose twist
        th_diff = self.enemy_direction
        while not PI >= th_diff >= -PI:
            if th_diff > 0:
                th_diff -= 2*PI
            elif th_diff < 0:
                th_diff += 2*PI
        new_twist_ang_z = th_diff * 1.2

        if self.enemy_dist > 0.45:
            speed = self.speed
        else:
            speed = -self.speed
        print("enemy_dist {}".format(self.enemy_dist))
        
        self.near_enemy_twist.angular.z = new_twist_ang_z
        self.near_enemy_twist.linear.x = speed
        #print("Update near Enemy Twist")

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
            twist = Twist()
            if self.is_near_enemy:
                twist.linear.x = self.near_enemy_twist.linear.x
                twist.angular.z = self.near_enemy_twist.angular.z
            else:
                twist.linear.x = self.pose_twist.linear.x
                twist.angular.z = self.pose_twist.angular.z

            if self.is_near_wall:
                twist.linear.x = -self.speed
            self.vel_pub.publish(twist)
            # for debug
            # print("POSE TWIST: {}, {}".format(self.pose_twist.linear.x, self.pose_twist.angular.z))
            # print("ENEMY TWIST: {}, {}".format(self.near_enemy_twist.linear.x, self.near_enemy_twist.angular.z))
            # print("wall: {}, Enemy: {}, X: {}, Z: {}".format(self.is_near_wall, self.is_near_enemy, twist.linear.x, twist.angular.z))

            r.sleep()


if __name__ == '__main__':
    rospy.init_node('enemy')
    bot = TeriyakiBurger('teriyaki_burger')
    bot.strategy()

