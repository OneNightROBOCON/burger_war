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
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"BL_B", "id":"0011", "point":3}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"BL_L", "id":"0012", "point":3}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"BL_R", "id":"0013", "point":3}' localhost:5000/warState/targets

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"RE_B", "id":"0021", "point":3}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"RE_L", "id":"0022", "point":3}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"RE_R", "id":"0023", "point":3}' localhost:5000/warState/targets

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"Tomato_N", "id":"1001", "point":1}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"Tomato_S", "id":"1002", "point":1}' localhost:5000/warState/targets

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"Omelette_N", "id":"2001", "point":1}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"Omelette_S", "id":"2002", "point":1}' localhost:5000/warState/targets

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"Pudding_N", "id":"3001", "point":1}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"Pudding_S", "id":"3002", "point":1}' localhost:5000/warState/targets

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"OctopusWiener_N", "id":"4001", "point":1}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"OctopusWiener_S", "id":"4002", "point":1}' localhost:5000/warState/targets

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"FriedShrimp_N", "id":"5001", "point":1}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"FriedShrimp_E", "id":"5002", "point":1}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"FriedShrimp_W", "id":"5003", "point":1}' localhost:5000/warState/targets
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"FriedShrimp_S", "id":"5004", "point":1}' localhost:5000/warState/targets

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
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"4001"}' localhost:5000/submits

sleep 1

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"3002"}' localhost:5000/submits

sleep 1

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"5003"}' localhost:5000/submits

sleep 1

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"1001"}' localhost:5000/submits

sleep 1

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"1002"}' localhost:5000/submits

sleep 1


curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"0011"}' localhost:5000/submits

sleep 1


curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"0023"}' localhost:5000/submits

sleep 1

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"0022"}' localhost:5000/submits

sleep 1


curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"ishiro", "side":"r", "id":"0012"}' localhost:5000/submits

sleep 1

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"name":"jiro", "side":"b", "id":"0021"}' localhost:5000/submits

sleep 1

# set state to "end"
echo "=================set state "end"======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"state":"stop"}' localhost:5000/warState/state

sleep 1


echo "=================STATE end======================"
curl localhost:5000/warState

