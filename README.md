# onigiri_war
OneNightROBOCON競技「onigiri war」プロジェクト

ロボットで戦車対戦をするようなゲームです。
大砲で撃つ代わりに、カメラでターゲットのARマーカーを読み取ります。


## 目次
- インストール
- 審判サーバー
- ファイル構成
- その他
- 動作環境

## インストール
onigiri_warには**実機**と**シミュレータ**があります。
シミュレータで動かす場合には `4. PC上でシミュレーションする場合`も実行してください。


### 1. ros (kinetic) のインストール
**2018年からkineticで開発しています**

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
- pip : pythonのパッケージ管理ツール
- requests : HTTP lib
- flask : HTTP server 審判サーバーで使用

```
# pip のインストール 
sudo apt-get install python-pip
#　requests flask のインストール
sudo pip install requests flask
```

- aruco (ARマーカー読み取りライブラリ）

opencv必要なのでrosをinstallしてからインストールしてください。

以下のURLからaruco-2.0.19.zipをダウンロード　※バージョンは都度変更する可能性あり
(2018/5/14現在 aruco-3.0.9のバージョンではmake時にエラーが発生するためaruco-2.0.19を推奨)

https://sourceforge.net/projects/aruco/files/2.0.19/
```
cd Downloads/aruco-2.0.19
mkdir build
cd build
cmake ..
make
sudo make install 
```

### 4. PC上でシミュレーションする場合
- ロボットモデルのインストール
LetsBotコミュニティのOneNightROBOCONグループで共有されている
`rulo_sim_package.tar.gz`
を支持に従い`src`以下に展開

ロボットモデルをコピー
```
cp -a ~/catkin_ws/src/ros_simulator/models ~/.gazebo/
```

このリポジトリのフィールド用のGAZEBOモデルにPATHを通す
```
export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/onigiri_war/onigiri_war/models/
```
シェルごとに毎回実行するのは面倒なので上記は`~/.bashrc`に書いておくと便利です｡

### 5. make
```
cd ~/catkin_ws
catkin_make
```

arucoのmakeがうまく行かない場合、下記を試してみてください
```
catkin_make --pkg ros_aruco -DARUCO_PATH=/usr/local  
```
インストールは以上です。

## サンプルの実行
### シミュレータ
シミュレータ､ロボット(turtle_bot),審判サーバー､観戦画面のすべてを一発で起動する。大会で使用するスクリプト。
```
bash scripts/sim_with_judge.sh
```
フィールドとロボットが立ち上がったら
別のターミナルで下記ロボット動作スクリプトを実行
```
bash scripts/start.sh
```

![screenshot at 2018-01-09 23 52 12](https://user-images.githubusercontent.com/17049327/34726839-7ed4694e-f598-11e7-8e8e-2e0311b099d2.png)

↑このようなフィールドが現れロボットが2台出現します。
審判画面も表示されます。


審判サーバーを立ち上げずにシミュレータとロボットのみ立ち上げる場合
```
roslaunch onigiri_war　onigiri_setup_sim.launch
```
フィールドとロボットが立ち上がったら
別のターミナルで下記ロボット動作スクリプトを実行
```
bash scripts/start.sh
```
審判サーバー以外は上記と同じです。


### 実機
センサなどが立ち上がりロボットを動かす準備
```
roslaunch onigiri_war onigiri_setup.launch
```
別のターミナルで
```
roslaunch onigiri_war action.launch
```

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
│   │   ├── sim_robot_run.launch  シミュレータ上で２台のロボットを動かすlaunchファイル
│   │   └─ onigiri_setup_sim.launch  Gazeboシミュレータ上でフィールドの生成ロボットを起動、初期化するlaunchファイル
│   │
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
│   ├── judgeServer.py  審判サーバー本体
│   ├── log   ログがここにたまる
│   ├── marker_set  マーカーの配置設定ファイル置き場
│   ├── picture  観戦画面用画像素材
│   ├── README.md  
│   ├── test_scripts   初期化などのスクリプト
│   └── visualizeWindow.py  観戦画面表示プログラム
|
├── README.md   これ
├── ros_aruco  ARマーカーの読み取りパッケージ
├── rulebook.md  ルールブック(過去版 2017/03の第３回大会のもの)
└── scripts      一発起動スクリプト
    ├─── sim_with_judge.sh   シミュレーターとロボットと審判サーバーの立ち上げ初期化をすべて行う    
    └──  start.sh             赤サイド、青サイドのロボットを動作させるノードを立ち上げるスクリプト
```
↑ディレクトリと特に重要なファイルのみ説明しています。

## その他
### カメラの露光時間の設定
実機で動作する場合のカメラの露光時間の設定に関する情報です。
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
