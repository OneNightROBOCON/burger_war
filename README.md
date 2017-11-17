# onigiri_war
OneNightROBOCON競技「onigiri war」プロジェクト

ロボットで戦車対戦をするようなゲームです。
大砲で撃つ代わりに、カメラでターゲットのARマーカーを読み取ります。

**画像準備中**
![demo](onigiri_war.gif)


## 目次
- インストール
- ルール
- ファイル構成
- その他
- 動作環境


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

### 6. make

```
cd ~/catkin_ws
catkin_make

```


### 7. サンプルの実行
サンプルの実行します。うまく行けばインストール終了です。

```
roslaunch onigiri_war run_all.launch
```

## ルール
大会のルールは`rulebook.md`を参照

## ファイル構成
各ディレクトリの役割と、特に参加者に重要なファイルについての説明

下記のようなフォルダ構成になっています。  
sample では `run_all.launch` ですべてのノードが立ち上がるようになっています。
走行制御はランダム走行する`randomBot.py`が実装されています。

```
onigiri_war/
|-launch/        : launchファイルの置き場
| |-run_all.launch  ロボットを起動するlaunchファイル
|
|- scripts/      : pythonファイルの置き場
| |-sendQrToJudge.py : Judgeサーバーに読み取ったターゲットIDを提出するノード。
| |-dummyQrReader.py : ターゲットID読み取りノードとしてふるまうダミー（テスト用）。
| |-randomBot.py   : ランダム走行するサンプルプログラム
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