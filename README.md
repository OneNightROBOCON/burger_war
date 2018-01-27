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
cd Downloads/aruco-2.0.19
mkdir build
cd build
cmake ..
make
sudo make install 
```

#### 5.1　PC上でシミュレーションする場合
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
毎回実行するのは面倒なので
`~/.bashrc`に書いておくと便利です｡

**シミュレータの注意点**
- 赤外線距離センサトピックと超音波センサトピックは実機と形式が違います。
実機は左右のセンサを別トピックでpublishしていますが、
シミュレーションではleft,rightのタグをつけて１つのトピックでpublishしています。

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

sample では
- 実機で動かす場合 `setup.launch` 
- PC上のシミュレータで動かす場合 `setup.launch` 
でセンサなどが立ち上がりロボットを動かす準備ができるようになっています。

`action.launch`でロボットに移動を指令するノードが立ち上がります。

走行制御はランダム走行する`randomRulo.py`が実装されています。

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
審判サーバーは下記のリポジトリで公開しています。
https://github.com/OneNightROBOCON/onigiri_war_judge

## ファイル構成
各ディレクトリの役割と、特に参加者に重要なファイルについての説明

下記のようなフォルダ構成になっています。  


```
onigiri_war/
|-ros_aruco/ : ARマーカーの読み取りパッケージ
|
|-onigiri_war/
  |-launch/        : launchファイルの置き場
  | |-setup.launch  初期化、センサの起動などするlaunchファイル
  | |-setup_sim.launch  Gazeboシミュレータ上でロボットを起動、初期化するlaunchファイル
  | |-action.launch  ロボットを動かすlaunchファイル cmd_vel
  | |-run_with_usbcam.launch  ロボットを動かすlaunchファイル
  |
  |- scripts/      : pythonファイルの置き場
  | |-sendIdToJudge.py : Judgeサーバーに読み取ったターゲットIDを提出するノード。
  | |-dummyArReader.py : ターゲットID読み取りノードとしてふるまうダミー（テスト用）。
  | |-randomRulo.py : ランダム走行するサンプルプログラム
  | |-abstractRulo.py : ロボットの抽象クラス
  | |-opt_run.py   : かべぎわ走行するサンプルプログラム
  |
  |- doc/      : ドキュメントファイルの置き場
  | |-rulebook.md : 競技のルールブック
  |
  |- world/ : シミュレータ環境置き場
  |-rulebook.md : ルールブック
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
