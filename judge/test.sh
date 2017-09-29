# reset
echo "=================RESET======================"
curl localhost:5000/reset

sleep 1

# GET war state initial
echo "=================STATE initial======================"
curl localhost:5000/warState

sleep 1

# regist targets 
echo "=================REGIST targets======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"one", "id":"1111", "point":3}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"two", "id":"2222", "point":3}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"three", "id":"3333", "point":3}' localhost:5000/warState/targets

sleep 1

# regist players
echo "=================REGIST players======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro"}' localhost:5000/warState/players
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro"}' localhost:5000/warState/players

sleep 1

# ready
echo "=================set ready players======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"0000"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"0000"}' localhost:5000/submits

sleep 1

# set state to "running"
echo "=================set state "running"======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"state":"running"}' localhost:5000/warState/state

sleep 1

echo "=================STATE running======================"
curl localhost:5000/warState

sleep 1


# submit
echo "=================submit target id======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"1111"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"2222"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"2222"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"2222"}' localhost:5000/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"2223"}' localhost:5000/submits

sleep 1


# set state to "end"
echo "=================set state "end"======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"state":"stop"}' localhost:5000/warState/state

sleep 1


echo "=================STATE end======================"
curl localhost:5000/warState

