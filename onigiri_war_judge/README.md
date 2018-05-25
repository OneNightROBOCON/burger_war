# Judge

![onigiri_judge](picture/view.png)
## Quick Start
とりあえず動きを確認する方法(すべて別のシェルで実行）
```
python judgeServer.py
python visualizeWindow.py
bash test_scripts/view_test.sh
```
画面が出てうごけばOK

### 試合の初期化スクリプト
#### 引数
- マーカーセットのcsvファイル
- サーバーIP
- RED側 player name
- BLUE側 player name

#### 試合用
`init.sh`
2台を起動して、set_running.shを実行しないと動きません
```
bash test_scripts/init.sh {makerset file} {server IP(default localhost:5000)} {red side player name} {blue side player name}
```

#### 練習用
`init_single_play.sh`
すぐにマーカーの提出を受け付けるモードになります。
```
bash test_scripts/init_single_play.sh {makerset file} {server IP(default localhost:5000)} {red side player name} {blue side player name}
```

#### マーカーセットcsv
初期化スクリプトで読み込むマーカーセットのcsvファイル形式
```
マーカー名, ポイント, ID
```
マーカー名の命名規則
- BL_{B or L or R} blue側機体のマーカー
- RE_{B or L or R} red側機体マーカー
- hoge{N}_{S or N or E or W} フィールドの障害物（hogeN）のマーカー
- B 背後 
- L,R 左右
- S,N,E,W 東西南北


サンプル
```
BL_B,5,0011
BL_L,5,0012
BL_R,5,0013
RE_B,5,0021
RE_L,5,0022
RE_R,5,0023
hoge1_N,1,0064
hoge1_S,1,0130
hoge2_N,1,2001
hoge2_S,1,2002
hoge3_N,1,3001
hoge3_S,1,3002
hoge4_N,1,4001
hoge4_S,1,4002
hoge5_N,1,5001
hoge5_E,1,5002
hoge5_W,1,5003
hoge5_S,1,5004
```

## install
### 依存関係のインストール
```
pip install flask
```
権限がないというエラーが出る場合はsudoつけてください


### このリポジトリのクローン
```
git clone https://github.com/OneNightROBOCON/onigiri_war_judge
```


# ONIGIRI-WAR Judge WebAPIドキュメント

## 戦況を表示する [/warState]

### warState [GET]
現在の戦況を返します。

#### Response

+ players
    + b: "jiro" (string) - プレイヤー名 (blue side)
    + r: "ishiro"(string) - プレイヤー名 (red side)
+ ready
    + b: True (boolean) - ジャッジサーバー接続確認、走行準備完了フラグ
    + r: True (boolean) - ジャッジサーバー接続確認、走行準備完了フラグ
+ scores
    + b: 0 (int) - スコア
    + r: 2 (int) - スコア
+ state: "end" (string) - 試合ステート running, ready, end, etc...
+ targets
    + name: "one" (string) - ターゲット名 同じ名前はつけない。
    + player: "r" (string) - 所有プレイヤーサイド  r(BlueSide), b(BlueSide), n(NoPlayer)
    + point: 1 (int) - ターゲットを取得したときのポイント

json sample
```
get
{
  "players": {
    "b": "jiro", 
    "r": "ishiro"
  }, 
  "ready": {
    "b": true, 
    "r": true
  }, 
  "scores": {
    "b": 6, 
    "r": 0 
  }, 
  "state": "end", 
  "targets": [
    {
      "name": "hoge_N", 
      "player": "b"
      "point": 1 
    }, 
    {
      "name": "RE_R", 
      "player": "b"
      "point": 5
    }, 
    {
      "name": "RE_L", 
      "player": "n"
      "point": 5
    }
  ]
}
```

## ターゲット情報を提出する [/submits]

### submits [POST]
読み取ったターゲットを提出します。

#### Request

+ player: "ishiro" (string) - プレイヤー名
+ side: "r" (string) - プレイヤーサイド
+ id: "ffff" (string) - ターゲットID

json sample
```
{
    "player":"ishiro",
    "side":"r",
    "id":"0123"
}
```
     
#### Response

+ mutch: True (boolean) - IDの正誤
+ new: True (boolean) - 新規ターゲットかどうか 
+ error: "side val is invalid" (string) - エラーメッセージ
+ targets    mutch Falseの場合はなし
    + name: "one" (string) - ターゲット名 同じ名前はつけない。
    + player: "r" (string) - 所有プレイヤーサイド  r(BlueSide), b(BlueSide), n(NoPlayer)
    + point: 1 (int) - ターゲットを取得したときのポイント

json sample
```
{
  "mutch": True,
  "new": True,
  "error": "no error",
  "targets": {
      "name": "RE_R", 
      "player": "r"
      "point": 5
  }
}
```

# オブジェクトの配置設定
setting.jsonから設定可能
+ nameとmarker_set.csv内で設定する名前をそろえること
+ nameと同じ名前の画像ファイルを/picture内のpng形式で用意すること

## 設定例
```
{
    "objects":{
        "top_left":{ # 場所がわかりやすいような名前
            "name":"Tomato", # オブジェクトの名前
            "position":{ # 画面内での表示位置（画像の中心位置）
                "x":550, 
                "y":540
            },
            "size":{ #画像のサイズ
                "height":100,
                "width":150
            },
            "north":1, #マーカーの場所（1:ON　0:OFF）
            "south":1,
            "west":0,
            "east":0
        },
        "top_right":{ # 場所がわかりやすいような名前
            "name":"Omelette", # オブジェクトの名前
            "position":{ # 画面内での表示位置（画像の中心位置）
                "x":550, 
                "y":830
            },
            "size":{ #画像のサイズ
                "height":100,
                "width":150
            },
            "north":1, #マーカーの場所（1:ON　0:OFF）
            "south":1,
            "west":0,
            "east":0
        },
        "bottom_left":{ # 場所がわかりやすいような名前
            "name":"Pudding", # オブジェクトの名前
            "position":{ # 画面内での表示位置（画像の中心位置）
            "position":{ 
                "x":770,
                "y":550
            },
            "size":{ #画像のサイズ
                "height":100,
                "width":150
            },
            "north":1, #マーカーの場所（1:ON　0:OFF）
            "south":1,
            "west":0,
            "east":0
        },
        "bottom_right":{ # 場所がわかりやすいような名前
            "name":"OctopusWiener", # オブジェクトの名前
            "position":{ # 画面内での表示位置（画像の中心位置）
                "x":770,
                "y":800
            },
            "size":{ #画像のサイズ
                "height":100,
                "width":150
            },
            "north":1, #マーカーの場所（1:ON　0:OFF）
            "south":1,
            "west":0,
            "east":0
        },
        "center":{ # 場所がわかりやすいような名前
            "name":"FriedShrimp", # オブジェクトの名前
            "position":{ # 画面内での表示位置（画像の中心位置）
                "x":660,
                "y":680
            },
            "size":{ #画像のサイズ
                "height":120,
                "width":120
            },
            "north":1, #マーカーの場所（1:ON　0:OFF）
            "south":1,
            "west":1,
            "east":1
        }
    }
}
```
