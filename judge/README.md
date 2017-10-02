# Judge
以下でサーバーの確認
```
python judgeServer.py
python visualizeWindow.py
bash test.sh
```


# ONIGIRI-WAR Judge WebAPIドキュメント

## 戦況を表示する [/warState]

### warState [GET]
現在の戦況を返します。


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
    "b": 0, 
    "r": 2
  }, 
  "state": "end", 
  "targets": [
    {
      "name": "one", 
      "player": "b"
      "point": 1
    }, 
    {
      "name": "two", 
      "player": "b"
      "point": 1
    }, 
    {
      "name": "three", 
      "player": "n"
      "point": 3
    }
  ]
}
```

## ターゲット情報を提出する [/submits]

### submits [POST]
読み取ったターゲットを提出します。

+ player: "ishiro" (string) - プレイヤー名
+ side: "r" (string) - プレイヤーサイド
+ id: "ffff" (string) - ターゲットID

json sample
```
{
    "player":"ishiro",
    "side":"r",
    "id":"ffff"
}
```
     

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
      "name": "three", 
      "player": "n"
      "point": 3
  }
}
```





# 以下は旧バージョン



## API user
|URI|GET|POST|
|---|----|---|
|/submits|-|player|
|/warState|ALL|--|
|/warState/targets|-|admin|
|/warState/players|-|admin|
|/warState/state|-|admin|
|/reset|-|admin|

## json format
now sample only... sorry
### WarState
`/warState` GET
send
No Message

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
    "b": 0, 
    "r": 2
  }, 
  "state": "end", 
  "targets": [
    {
      "name": "one", 
      "player": "ishiro"
    }, 
    {
      "name": "two", 
      "player": "ishiro"
    }, 
    {
      "name": "three", 
      "player": "NoPlayer"
    }
  ]
}
```

### Submit Target
`/submits` POST

send
```
{
    "player":"ishiro",
    "side":"r",
    "id":"ffff"
}
```

get
```
{
  "name": "three", 
  "player": "ishiro"
}
```

### Regist Target
`/warState/targets` POST

send
```
{
    "name":"three",
    "id":"ffff",
}
```

get
```
{
    "name":"three"
}
```

### Regist Player
`/warState/players` POST

send
```
{
    "name":"ishiro",
}
```

get
```
{
    "name":"ishiro"
    "side":"r"
}
```

### Game State
`/warState/state` POST

- running
- stop
- end

send
```
{
    "state":"running"
}
```

get
```
{
    "state":"runnig"
}
```
