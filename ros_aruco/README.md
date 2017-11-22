# aruco_ros
arReader for ROS
# 導入手順
## arucoライブラリをインストール
以下のURLからaruco-2.0.19.zipをダウンロード　※バージョンは都度変更する可能性あり

https://sourceforge.net/projects/aruco/files/2.0.19/

任意のダウンロード先で以下のコマンドを実行してインストール
```
cd Downloads/aruco-2.0.14
mkdir build
cd build
cmake ..
make
sudo make install 
```

## aruco_rosをgitから取得し、makeする
```
cd ~/catkin_ws/src  
git clone https://github.com/OneNightROBOCON/aruco_ros
cd ..  
catkin_make --pkg ros_aruco -DARUCO_PATH=/usr/local  
```

# 実行手順
## カメラを起動
```
rosrun uvc_camera uvc_camera_node
```
キャリブレーションパラメータが必要なので、済ませておく
## aruco_rosを実行
```
rosrun ros_aruco ros_aruco
```
コード内にyaml形式のキャリブレーションパラメータのパスを入力するところがあるので、使用するカメラにより変更が必要
（できらたtopicでcamera_infoとして受け取りたい）
# 残務
-- キャリブレーション方法の提示

-- camera_infoをsubscribeするように変換

現状はキャリブレーションファイルのパスをコードに直打ちしている
