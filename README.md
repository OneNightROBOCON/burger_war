# onigiri_war
OneNightROBOCON競技「onigiri war」プロジェクト

ロボットで戦車対戦をするようなゲームです。
大砲で撃つ代わりに、カメラでターゲットのARマーカーを読み取ります。


## 目次
- ルール
- インストール
- 審判サーバー
- ファイル構成
- その他
- 動作環境

## ルール
大会のルールは[rulebook.md](rulebook.md)を参照

## インストール

### 1. ros (kinetic) のインストール
**2018年からkineticで開発しています｡
indigoでもまだ動くと思いますがところどころ不具合がある可能性があります｡**

rosのインストールが終わっている人は`2.このリポジトリをクローン` まで飛ばしてください。

参考  ROS公式サイト<http://wiki.ros.org/ja/kinetic/Installation/Ubuntu>
上記サイトと同じ手順です。
ros インストール
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
sudo apt-get update
sudo apt-get install ros-kinetic-desktop-full
```
環境設定
```
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
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

### 2. このリポジトリをクローン
turtlr_war リポジトリをクローンします。
先程作ったワークスペースの`src/`の下においてください。
```
cd ~/catkin_ws/src
git clone https://github.com/OneNightROBOCON/onigiri_war
```
### 3. 依存ライブラリのインストール
- requests : HTTP lib
- flask : HTTP server 審判サーバーで使用
```
sudo pip install requests flask
```

- aruco (ARマーカー読み取りライブラリ）

opencv必要なのでrosをinstallしてからインストールしてください。

以下のURLからaruco-2.0.19.zipをダウンロード　※バージョンは都度変更する可能性あり

https://sourceforge.net/projects/aruco/files/2.0.19/
```
cd Downloads/aruco-2.0.19
mkdir build
cd build
cmake ..
make
sudo make install 
```

#### 3.1　PC上でシミュレーションする場合
- LetsBotを使う場合
LetsBotコミュニティのOneNightROBOCONグループで共有されている
`rulo_sim_package.tar.gz`
を支持に従い`src`以下に展開

**LetBotシミュレータの注意点**
- 赤外線距離センサトピックと超音波センサトピックは実機と形式が違います。
実機は左右のセンサを別トピックでpublishしていますが、
シミュレーションではleft,rightのタグをつけて１つのトピックでpublishしています。

ロボットモデルをコピー
```
cp -a ~/catkin_ws/src/ros_simulator/models ~/.gazebo/
```
- turtlebot を使う場合
turtlebot 関係のインストール
```
sudo apt-get install ros-indigo-turtlebot ros-indigo-turtlebot-apps ros-indigo-turtlebot-interactions ros-indigo-turtlebot-simulator ros-indigo-kobuki-ftdi ros-indigo-rocon-remocon ros-indigo-rocon-qt-library ros-indigo-ar-track-alvar-msgs
```

このリポジトリのフィールド用のGAZEBOモデルにPATHを通す
```
export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/onigiri_war/onigiri_war/models/
```
シェルごとに毎回実行するのは面倒なので
`~/.bashrc`に書いておくと便利です｡

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

#### とにかく起動してみる
シミュレータ､ロボット(turtle_bot),審判サーバー､観戦画面のすべてを一発で起動するスクリプトを用意してあります
```
bash scripts/sim_with_judge.sh
```
いろいろ画面がたちあがります｡
ロボットを動かしたい場合はシミュレーターの起動完了後にロボットを動かすノードを起動してください｡

#### マニュアルで起動する

sample では
- 実機で動かす場合 `{ROBOTNAME}_setup.launch` 
- PC上のシミュレータで動かす場合 `{ROBOTNAME}_setup_sim.launch` 
でセンサなどが立ち上がりロボットを動かす準備ができるようになっています。

`action.launch`でロボットに移動を指令するノードが立ち上がります。

サンプルでは走行制御はランダム走行する`randomRulo.py`が実装されています。

#### 実機の場合
```
roslaunch onigiri_war onigiri_setup.launch
roslaunch onigiri_war action.launch
```

#### PCでGazeboでシミュレーションする場合
```
roslaunch onigiri_war onigiri_setup_sim.launch
roslaunch onigiri_war action.launch
```
![screenshot at 2018-01-09 23 52 12](https://user-images.githubusercontent.com/17049327/34726839-7ed4694e-f598-11e7-8e8e-2e0311b099d2.png)

このようなフィールドが現れます

#### PCにUSBカメラをつないでマーカー読み取りのみ実験する場合
```
roslaunch onigiri_war run_with_usbcam.launch
```

#### PCにRealSenceをつないでマーカー読み取りのみ実験する場合
```
roslaunch onigiri_war run_with_realsense.launch
```
## 審判サーバー
審判サーバーは`onigiri_war_judge/`以下にあります
そちらのREADMEを参照ください

## ファイル構成
各ディレクトリの役割と、特に参加者に重要なファイルについての説明

下記のようなディレクトリ構成になっています。  

```
onigiti_war
├── onigiri_war
│   ├── CMakeLists.txt
│   ├── launch  launchファイルの置き場
│   │   ├── action.launch  ロボットを動かすlaunchファイル
│   │   ├── onigiri_setup.launch  初期化、センサの起動などするlaunchファイル
│   │   ├── onigiri_setup_sim.launch  Gazeboシミュレータ上でロボットを起動、初期化するlaunchファイル
│   │   ├── run_with_realsense.launch  カメラ単体でテストするlaunchファイル
│   │   ├── run_with_usbcam.launch     カメラ単体でテストするlaunchファイル
│   │   └── turtlebot_setup_sim.launch   Gazeboシミュレータ上でロボットを起動、初期化するlaunchファイル
│   ├── models   GAZEBOシミュレーター用のモデルファイル
│   ├── package.xml
│   ├── scripts    pythonで書かれたROSノード
│   └── world     シミュレータGAZEBO用の環境ファイル
│       ├── field_v0.world  昔のヤツ
│       ├── gen.sh          onigiri_field.world.emから onigiri_field.worldを作成するスクリプト
│       ├── onigiri_field.world  最新のworldファイル
│       └── onigiri_field.world.em  worldファイルのマクロ表記版､こっちを編集する
|
├── onigiri_war_judge   審判サーバー
│   ├── judgeServer.py  審判サーバー
│   ├── log   ログがここにたまる
│   ├── marker_set  マーカーの配置ファイル
│   ├── picture  観戦画面用
│   ├── README.md  
│   ├── test_scripts   初期化などのスクリプト
│   └── visualizeWindow.py  観戦画面
|
├── README.md   これ
├── ros_aruco  ARマーカーの読み取りパッケージ
├── rulebook.md  ルールブック
└── scripts       一発起動スクリプト
    └── sim_with_judge.sh   シミュレーターとturtlebotと審判サーバーの立ち上げ初期化をすべて行う
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


## 推奨動作環境
- Ubuntu 16.04 
- Ros kinetic
2018年からkineticで開発しています｡
indigoでもまだ動くと思いますがところどころ不具合がある可能性があります｡
