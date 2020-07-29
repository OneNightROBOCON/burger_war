# burger_war
ロボットで戦車対戦をするゲームです。
大砲で撃つ代わりに、カメラでターゲットのARマーカーを読み取ります。<BR>

## 目次
- インストール
- 審判サーバー
- ファイル構成
- その他
- 動作環境

## インストール
burger_warには**実機**と**シミュレータ**があります。

### 1. ros (kinetic) のインストール
rosのインストールが終わっている人は`2.このリポジトリをクローン` まで飛ばしてください。

参考  ROS公式サイト<http://wiki.ros.org/ja/kinetic/Installation/Ubuntu>
上記サイトと同じ手順です。
ros インストール
```
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://ha.pool.sks-keyservers.net:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
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
gitをインストールします。
```
sudo apt-get install git
```

turtlr_war リポジトリをクローンします。
先程作ったワークスペースの`src/`の下においてください。
```
cd ~/catkin_ws/src
git clone https://github.com/OneNightROBOCON/burger_war
```

このリポジトリのフィールド用のGAZEBOモデルにPATHを通す。

Turtlebot3のモデル名の指定を環境変数に追加。
```
echo "export GAZEBO_MODEL_PATH=$HOME/catkin_ws/src/burger_war/burger_war/models/" >> ~/.bashrc
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
source ~/.bashrc
```


### 3. 依存ライブラリのインストール
- pip : pythonのパッケージ管理ツール
- requests : HTTP lib
- flask : HTTP server 審判サーバーで使用
- turtlebot3
- aruco

```
# pip のインストール 
sudo apt-get install python-pip
#　requests flask のインストール
sudo pip install requests flask
# turtlebot3 ロボットモデルのインストール
sudo apt-get install ros-kinetic-turtlebot3 ros-kinetic-turtlebot3-msgs ros-kinetic-turtlebot3-simulations
# aruco (ARマーカー読み取りライブラリ）
sudo apt-get install ros-kinetic-aruco-ros
```


### 5. make
```
cd ~/catkin_ws
catkin_make
```

インストールは以上です。

## サンプルの実行
### シミュレータ
シミュレータ､ロボット(turtle_bot),審判サーバー､観戦画面のすべてを一発で起動する。大会で使用するスクリプト。
最初にburger_warのフォルダまで移動します。
```
cd ~/catkin_ws/src/burger_war
```
初回のみ、以下のコマンドでGazeboを起動し、モデルデータ等を読み込んでおくとよいです。<BR>
(初回はGazeboの起動がおそいので)
```
gazebo
```
gazeboの初回立ち上げには数分かかることもあります。gazeboが空のフィールドで立ち上がったら一度gazeboを終了し、
次にシミュレーションを起動
```
bash scripts/sim_with_judge.sh
```

![screenshot](https://user-images.githubusercontent.com/17049327/61606479-7ed49680-ac85-11e9-8c77-5cad3a5db4ed.png)

↑このようなフィールドが現れロボットが2台出現します。
審判画面も表示されます。

フィールドとロボットが立ち上がったら
別のターミナルで下記ロボット動作スクリプトを実行
```
bash scripts/start.sh
```
敵プログラムはレベル１−３まで３種類用意しています.（デフォルトではレベル１）
下記のように `-l` 引数によって変更できます。

level 2
```
bash scripts/start.sh -l 2
```

level 3
```
bash scripts/start.sh -l 3
```


**審判サーバーを立ち上げずにシミュレータとロボットのみ立ち上げる場合**
```
roslaunch burger_war setup_sim.launch
```
フィールドとロボットが立ち上がったら
別のターミナルで下記ロボット動作スクリプトを実行
```
bash scripts/start.sh
```

審判サーバーが必要ない場合は直接launch ファイルを実行しても走行可能です。
上記と同様にレベル設定も可能です。(defaunt 1)
```
roslaunch burger_war sim_robot_run.launch enemy_level:=1
```

### 実機
センサなどが立ち上がりロボットを動かす準備 `burger_war setup.launch`
引数
- `side`: (default: 'b') ロボットが赤サイドか青サイドか表す引数。審判サーバーに提出する際にどちらサイドか表すために使用する。赤サイドなら `r` 青サイドなら `b`
- `ip`: (default:'http://localhost:5000') 審判サーバーのアドレス。

```
roslaunch burger_war setup.launch ip:=http://127.0.0.1:5000 side:=r
```

審判サーバーを使わない走行テストのみの場合は引数は省略可
```
roslaunch burger_war setup.launch
```

別のターミナルでロボットを動かすノードを起動 `burger_war your_burger.launch`

引数
- `side`: (default: 'b') ロボットが赤サイドか青サイドか表す引数。赤サイドと青サイドによって戦略やパラメータを切り替えるためなどに使用する。赤サイドなら `r` 青サイドなら `b`

赤サイドの場合
```
roslaunch burger_war your_burger.launch side:=r
```
青サイドの場合
```
roslaunch burger_war your_burger.launch side:=b
```

## 審判サーバー
審判サーバーは`judge/`以下にあります
そちらのREADMEを参照ください

## ファイル構成

ソフト全体の構成は下記のようになっています．
白の部分はすでにこのリポジトリに含まれており，参加者はオレンジの部分を開発します．
![soft_map](https://user-images.githubusercontent.com/17049327/73993084-9448ae00-4994-11ea-9d86-ac3c94936845.png)

リポジトリ全体は下記のようなディレクトリ構成になっています。  

```
burger_war
├── burger_war
│   ├── CMakeLists.txt
│   ├── launch  launchファイルの置き場
│   │   ├── your_burger.launch  ロボットの走行ノードを起動するlaunchファイル
│   │   ├── setup.launch  実機でロボットを起動、初期化するlaunchファイル
│   │   ├── sim_robot_run.launch  シミュレータ上で２台のロボットを動かすlaunchファイル
│   │   └─ setup_sim.launch  Gazeboシミュレータ上でフィールドの生成ロボットを起動、初期化するlaunchファイル
│   │
│   ├── models   GAZEBOシミュレーター用のモデルファイル
│   ├── package.xml
│   ├── scripts    pythonで書かれたROSノード
│   └── world     GAZEBO用の環境ファイル
│       ├── gen.sh          burger_field.world.emから burger_field.worldを作成するスクリプト
│       ├── burger_field.world  最新のworldファイル
│       └── burger_field.world.em  worldファイルのマクロ表記版､こっちを編集する
|
├── judge   審判サーバー
│   ├── judgeServer.py  審判サーバー本体
│   ├── log   ログがここにたまる
│   ├── marker_set  マーカーの配置設定ファイル置き場
│   ├── picture  観戦画面用画像素材
│   ├── README.md  
│   ├── test_scripts   初期化などのスクリプト
│   └── visualizeWindow.py  観戦画面表示プログラム
|
├── README.md   これ
├── rulebook.md  ルールブック
└── scripts      一発起動スクリプト
    ├─── sim_with_judge.sh   シミュレーターとロボットと審判サーバーの立ち上げ初期化をすべて行う
    └──  start.sh             赤サイド、青サイドのロボットを動作させるノードを立ち上げるスクリプト
```
↑ディレクトリと特に重要なファイルのみ説明しています。

## 推奨動作環境
- Ubuntu 16.04 
- Ros kinetic
2018年からkineticで開発しています｡

## Turtlebot3のスペック
- http://emanual.robotis.com/docs/en/platform/turtlebot3/specifications/

## その他
https://github.com/gogo5nta さんに一括でインストールするスクリプトを作成いただいたので本リポジトリにも置いています。
ご活用ください。
```
// ROS(kinetic)を一括インストール
$ chdmod 777 ./scripts/install_ros_kinetic.sh
$ ./scripts/install_ros_kinetic.sh

// Robocon2019に必要な物を一括インストール
$ chdmod 777 ./scripts/add_robocon2019.sh
$ ./scripts/add_robocon2019.sh
```
