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
+ targets    mutch Falseの場合はなし
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
