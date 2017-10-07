# onigiri_war
OneNightROBOCON競技「onigiri war」プロジェクト

ロボットで戦車対戦をするようなゲームです。
大砲で撃つ代わりに、カメラで的のQRコードを読み取ります。

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

### 5. make

```
cd ~/catkin_ws
catkin_make
```

### 6. サンプルの実行
サンプルの実行します。うまく行けばインストール終了です。

```
roslaunch onigiri_war run_all.launch
```

## ルール
※ルールは基本的な部分は決定しましたが、障害物の配置やポイント配分など当日までに微調整をする場合があります。
変更があった場合はなるべく早くお知らせいたします。

### 基本ルール

ロボットを自律移動させ１対１で打ち合うゲームです。

主砲の代わりに正面のカメラで的のQRコードを読み取ります。

QRコードを読み取ったIDを審判サーバーに提出すると、その的を撃ち落としたということになります。

### ターゲット

ターゲットは直径１０ｃｍの円形です。

中心にQRコードが印刷されています。

機体に取り付けるターゲットと、フィールどに設置されたターゲットがあり、機体のターゲットは赤、フィールドのターゲットは青色をしています。

**機体のターゲット**は下の画像のように左右１枚ずつ、背後１枚の計**３枚**。**フィールドのターゲット**は点対称に**６枚**設置します。

**ターゲット画像準備中**
![demo](onigiri_war_target.gif)

### 勝敗の決定方法
ターゲットを撃ちぬくとポイントを獲得できます。
また、相手背後のターゲットは撃ちぬいた瞬間に勝利が確定します。（１本勝ち）

配点
- 背後    ： 勝利確定
- 左右    ： ３ポイント
- フィールド ：１ポイント

＊＊制限時間３分間＊＊以内に１本勝ちまたは終了時にポイントが多い方の勝利となります。両者同点の場合は、最終ポイントを獲得した時刻の早い方の勝利となります。両者ポイント無しの場合はじゃんけんで勝敗を決めます。

通常のキャンディは赤色で、とると1ポイント加算されます。スペシャルキャンディは黄色で、とると5ポイント加算されます。

### フィールド
フィールドは**3.5m**四方の壁で囲われた空間です。お弁当箱をモチーフにしています。

フィールドにはおかず型の障害物が設置されています。設置初期位置は常に同じです。障害物は簡単には動きにくいよう設置していますが、動いた場合も試合は続行します。壁はロボットで押しても動きません。

### ロボット
ロボットはONIGIRI_BOT使用します。

使用可能なセンサは
- カメラ：realsense r200 
- Lidar ：日立LG　Lidar
- 左右斜め前方赤外線測距センサ 2個
- 前方バンパースイッチ　2個

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
| |-qrReader.py : QRコード読み取りノード。
| |-sendQrToJudge.py : Judgeサーバーに読み取ったQRコードを提出するノード。
| |-libqr.py : qrコード読み取りライブラリ。
| |-dummyQrReader.py : qrReader.pyとしてふるまうダミー（テスト用）。
| |-randomBot.py   : ランダム走行するサンプルプログラム
|
|- doc/      : ドキュメントファイルの置き場
| |-qrReader.md : QRコード読み取り機能のドキュメント。
|
|- scripts/      : pythonファイルの置き場
|- src/          : cppファイルの置き場
|
|-README.md : これ
```
↑ディレクトリと特に重要なファイルのみ説明しています。

## 動作環境
- OS  : Ubuntu 14.04
- ROS : indigo
- Python : 2.7