# onigiri_war
OneNightROBOCON競技「onigiri war」プロジェクト

ロボットで戦車対戦をするようなゲームです。
大砲で撃つ代わりに、カメラでターゲットのARマーカーを読み取ります。

**画像準備中**
![demo](onigiri_war.gif)


## 目次
- ルール
- インストール
- ファイル構成
- その他
- 動作環境

## ルール
大会のルールは[rulebook.md](rulebook.md)を参照

## インストール

### 1. ros (indigo) のインストール

rosのインストールが終わっている人は`4.このリポジトリをクローン` まで飛ばしてください。

参考  ROS公式サイト<http://wiki.ros.org/ja/indigo/Installation/Ubuntu>
上記サイトと同じ手順です。
ros インストール
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu trusty main" > /etc/apt/sources.list.d/ros-latest.list'
wget http://packages.ros.org/ros.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install ros-indigo-desktop-full
```
環境設定
```
sudo rosdep init
rosdep update
echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
ワークスペース作成

参考<http://wiki.ros.org/ja/catkin/Tutorials/create_a_workspace>
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace
cd ~/catkin_ws/
catkin_make
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 4. このリポジトリをクローン
turtlr_war リポジトリをクローンします。
先程作ったワークスペースの`src/`の下においてください。
```
cd ~/catkin_ws/src
git clone https://github.com/OneNightROBOCON/onigiri_war
```
### 5. 依存ライブラリのインストール
- requests : HTTP lib

requests
```
sudo pip install requests
```

- aruco (ARマーカー読み取りライブラリ）

opencv必要なのでrosをinstallしてからインストールしてください。

以下のURLからaruco-2.0.19.zipをダウンロード　※バージョンは都度変更する可能性あり

https://sourceforge.net/projects/aruco/files/2.0.19/
```
cd Downloads/aruco-2.0.14
mkdir build
cd build
cmake ..
make
sudo make install 
```

####　5.1　PC上でシミュレーションする場合
LetsBotコミュニティのOneNightROBOCONグループで共有されている
`rulo_sim_package.tar.gz`
を支持に従い`src`以下に展開

ロボットモデルをコピー
```
cp -a ~/catkin_ws/src/ros_simulator/models ~/.gazebo/
```

### 6. make

```
cd ~/catkin_ws
catkin_make

```

arucoのmakeがうまく行かない場合、下記を試してみてください
```
catkin_make --pkg ros_aruco -DARUCO_PATH=/usr/local  
```

### 7. サンプルの実行
サンプルの実行します。うまく行けばインストール終了です。

実機の場合
```
roslaunch onigiri_war setup.launch
roslaunch onigiri_war action.launch
```

PCでGazeboでシミュレーションする場合
```
roslaunch onigiri_war setup_sim.launch
roslaunch onigiri_war action.launch
```

PCにUSBカメラをつないでマーカー読み取りのみ実験する場合
```
roslaunch onigiri_war run_with_usbcam.launch
```

PCにRealSenceをつないでマーカー読み取りのみ実験する場合
```
roslaunch onigiri_war run_with_realsense.launch
```

## ファイル構成
各ディレクトリの役割と、特に参加者に重要なファイルについての説明

下記のようなフォルダ構成になっています。  
sample では 
- 実機で動かす場合 `setup.launch` 
- PC上のシミュレータで動かす場合 `setup.launch` 
でセンサなどが立ち上がりロボットを動かす準備ができるようになっています。

`action.launch`でロボットに移動する指令をします。

走行制御はかべぎわ走行する`opt_run.py`が実装されています。

```
onigiri_war/
|-launch/        : launchファイルの置き場
| |-setup.launch  ロボットを起動するlaunchファイル
| |-setup_sim.launch  Gazeboシミュレータ上でロボットを起動するlaunchファイル
| |-action.launch  ロボットを動かすlaunchファイル
| |-run_with_usbcam.launch  ロボットを動かすlaunchファイル
|
|- scripts/      : pythonファイルの置き場
| |-sendIdToJudge.py : Judgeサーバーに読み取ったターゲットIDを提出するノード。
| |-dummyArReader.py : ターゲットID読み取りノードとしてふるまうダミー（テスト用）。
| |-opt_run.py   : かべぎわ走行するサンプルプログラム
|
|- doc/      : ドキュメントファイルの置き場
| |-rulebook.md : 競技のルールブック
|
|- src/          : cppファイルの置き場
|
|-README.md : これ
```
↑ディレクトリと特に重要なファイルのみ説明しています。

## その他
### カメラの露光時間の設定
QRコード認識の時に画像ぶれにより認識精度が落ちないように設定が必要

#### Webカメラの場合
ターミナルを開いて以下を実行
```
v4l2-ctl -c exposure_auto=1
v4l2-ctl -c exposure_absolute=20
```

exposure_auto=1で露光の調整をマニュアルに変更し、exposure_absolute=20で露光時間を設定

#### RealSenseの場合
~/realsense/realsense_camera/launch/includes/nodelet_rgbd_launch.xmlを開き、以下の該当箇所を探す。
```
<node pkg="nodelet" type="nodelet" name="driver"
        args="load realsense_camera/$(arg camera_type)Nodelet $(arg manager)">
```
        
この直下に以下の内容を記載。
```
<param name="color_enable_auto_exposure" value="0"/>
<param name="color_exposure" value="39"/>
```
#### 注意点
環境の明るさにより画像が暗くなりすぎるので、環境により適宜調整が必要


## 動作環境
- Ubuntu 14.04
- Ros indigo
