# Judge
以下でサーバーの確認
```
python judgeServer.py
python visualizeWindow.py
bash test.sh
```
## API user
|URI|GET|POST|
|---|----|---|
|/warState|ALL|--|
|/warState/targets|-|abmin|
|/warState/players|-|admin|
|/warState/state|-|admin|
|/submits|-|player|
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
