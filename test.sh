# reset
curl localhost:5000/reset

# GET war state initial
curl localhost:5000/warState

# regist targets 
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"one", "id":"1111"}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"two", "id":"2222"}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"three", "id":"3333"}' localhost:5000/warState/targets

# regist players
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro"}' localhost:5000/warState/players
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro"}' localhost:5000/warState/players

# GET war state end
curl localhost:5000/warState

# ready
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"0000"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"0000"}' localhost:5000/submits

curl localhost:5000/warState

# submit
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"1111"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"2222"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"2222"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"2222"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"2223"}' localhost:5000/submits

# GET war state end
curl localhost:5000/warState

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"state":"end"}' localhost:5000/warState/state

curl localhost:5000/warState
