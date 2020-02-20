// burger war c++ example
// respect from https://demura.net/lecture/13932.html


#include "ros/ros.h"  // rosで必要はヘッダーファイル
#include <geometry_msgs/Twist.h> // ロボットを動かすために必要
#include <cstdlib>
using namespace std;



int main(int argc, char **argv)
{
    ros::init(argc, argv, "my_teleop_node");
    // initでROSを初期化し、my_teleop_nodeという名前をノードにつける
    // 同じ名前のノードが複数あるとだめなので、ユニークな名前をつける

    ros::NodeHandle nh;
    // ノードハンドラの作成。ハンドラは必要時に起動される。

    ros::Publisher  pub;
    // パブリッシャの作成。トピックに対してデータを送信。

    ros::Rate rate(1);
    // ループの頻度を設定するためのオブジェクトを作成。この場合は1Hz、1秒間に1回

    geometry_msgs::Twist vel;
    // geometry_msgs::Twist　この型は並進速度と回転速度(vector3:3次元ベクトル) を合わせたもので、速度指令によく使われる

    pub= nh.advertise<geometry_msgs::Twist>("cmd_vel", 10);
    // マスターにgeometry_msgs::Twist型のデータを送ることを伝える
    // マスターは/cmd_velトピック(1番目の引数）を購読する
    // 全てのノードにトピックができたことを知らせる(advertise)。
    // 2番目の引数はデータのバッファサイズ


    int rnd = 0;
    float x = 0.0;
    float th = 0.0;

    while (ros::ok()) { // このノードが使える間は無限ループする

        rnd = rand() % 1000;

        if (rnd < 250){
            x  =  0.2;
            th = 0.0; 
        }
        else if (rnd < 500){
            x  =  -0.2;
            th = 0.0; 
        }
        else if (rnd < 750){
            x  =  0.0;
            th =  1.0; 
        }
        else if (rnd < 1000){
            x  =  0.0;
            th = -1.0; 
        }
        else {
            x  =  0.0;
            th = 0.0; 
        }
     
        // linear.xは前後方向の並進速度(m/s)。前方向が正。
        // angular.zは回転速度(rad/s)。反時計回りが正。
        vel.linear.x   =  x;
        vel.linear.y   =  0.0;
        vel.linear.z   =  0.0;
        vel.angular.x  =  0.0;
        vel.angular.y  =  0.0;
        vel.angular.z  =  th;

        pub.publish(vel);    // 速度指令メッセージをパブリッシュ（送信）
        cout << vel << endl;
        ros::spinOnce();     // １回だけコールバック関数を呼び出す
        rate.sleep();        // 指定した周期でループするよう寝て待つ
    }

    return 0;
}

