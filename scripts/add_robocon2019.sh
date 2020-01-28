#!/bin/bash

echo "#git install"
sudo apt-get install -y git

echo "#forkしたgitをダウンロード(環境に合わせて修正する事)"
cd ~/catkin_ws/src
git clone https://github.com/gogo5nta/burger_war

echo "model path add .bashrc"
echo "export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/burger_war/burger_war/models/" >> ~/.bashrc
source ~/.bashrc

echo "# pip のインストール" 
sudo apt-get install -y python-pip

echo "#　requests flask のインストール"
sudo pip install requests flask

echo "# turtlebot3 ロボットモデルのインストール"
sudo apt-get install -y ros-kinetic-turtlebot3 ros-kinetic-turtlebot3-msgs ros-kinetic-turtlebot3-simulations

echo "# aruco (ARマーカー読み取りライブラリ）"
sudo apt-get install -y ros-kinetic-aruco-ros

echo "# catkin_make"
cd ~/catkin_ws
catkin_make
