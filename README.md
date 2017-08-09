# Judge

## API user
|URI|GET|POST|
|---|----|---|
|/warState|ALL|--|
|/warState/targets|-|abmin|
|/warState/players|-|player|
|/warState/state|-|admin|
|/submits|-|player|

## json format
now sample only... sorry
### WarState
`/warState` GET
send
No Message

get
```
{
    "state":"running"
    "score":{
        "r":{
            "player":"UMETARO",
            "point":10
        },
        "b":{
            "player":"SHAKEKO",
            "point":15
        }
    },
    "targets":[
        {
            "id":0,
            "name":"r_back",
            "player":"None"
        },
        {
            "id":1,
            "name":"field_center",
            "player":"UMETARO"
        },
    ]
}
```

### Submit Target
`/submits` POST

send
```
{
    "player":"UMETARO",
    "passcode":"0123456789",
    "target_id":"f2a9"
}
```

get
```
{
    "return":"success"
}
```

### Regist Target
`/warState/targets` POST

send
```
{
    "player":"admin",
    "passcode":"0123456789",
    "target":{
        "id":0,
        "name":"r_back",
        "player":"None"
    },
}
```

get
```
{
    "return":"success"
}
```

### Regist Player
`/warState/players` POST

send
```
{
    "plyer":"UMETARO",
    "passcode":"0123456789"
}
```

get
```
{
    "return":"success"
    "player":"UMETARO"
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
