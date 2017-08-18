from flask import Flask, request, jsonify
app = Flask(__name__)

class Target:
    def __init__(self, name, id , point=1):
        self.id = id
        self.name =name
        self.player = "NoPlayer"
        self.point = point
    def makeJson(self):
        json = {
            "name":self.name,
            #"id": self.id,
            "player": self.player,
        }
        return json

class WarState:
    def __init__(self):
        self.state = "end"
        self.players = {"r":"NoPlayer", "b":"NoPlayer"}
        self.scores = {"r":0, "b":0}
        self.ready = {"r":False, "b":False}
        self.targets = []

    def makeJson(self):
        json = {
            "state":self.state,
            "players":self.players,
            "ready":self.ready,
            "scores":self.scores,
            "targets":[t.makeJson() for t in self.targets],
        }
        return json

class Referee:
    def __init__(self):
        self.war_state = WarState()

    def judgeTargetId(self, data):
        player_name = data["name"]
        player_side = data["side"]
        target_id = data["id"]

        # set ready if id = 0000
        if target_id == "0000":
            self.war_state.ready[player_side] = True
            return {"name":player_name}

        for target in self.war_state.targets:
            if target_id == target.id:
                self.updateWarState(target, player_name, player_side)
                return target.makeJson()
        return False

    def checkBothPlayerReady(self):
        if self.war_state.ready["r"] and self.war_state.ready["b"]:
            self.war_state.state = "running"
        return

    def updateWarState(self, target, player_name, player_side):
        if not target.player == "NoPlayer":
            return 1
        else:
            target.player = player_name
            self.war_state.scores[player_side] += target.point
        return 0

    def registPlayer(self, data):
        name = data["name"]
        if self.war_state.players['r'] == "NoPlayer":
            self.war_state.players['r'] = name
            ret = {"side":"r", "name":name}
        elif self.war_state.players['b'] == "NoPlayer":
            self.war_state.players['b'] = name
            ret = {"side":"b", "name":name}
        else:
            ret = "##Errer 2 player already registed"
        return ret

    def registTarget(self, data):
        target = Target(data["name"], data["id"])
        self.war_state.targets.append(target)
        return target.name

    def setState(self, data):
        state = data["state"]
        if state == "end":
            self.war_state.state = state
        elif state == "running":
            if self.checkBothPlayerReady():
                self.war_state.state = state
        elif state == "stop":
            self.war_state.state = state
        else:
            pass
        return state

referee = Referee()

@app.route('/')
def index():
    msg = "Hello, Welcome to ONIGIRI WAR!"
    return msg

@app.route('/submits', methods=['POST'])
def judgeTargetId():
    ret = referee.judgeTargetId(request.json)
    return jsonify(ret)

@app.route('/warState', methods=['GET'])
def getState():
    state_json = referee.war_state.makeJson()
    return jsonify(state_json)

@app.route('/warState/players', methods=['POST'])
def registPlayer():
    ret = referee.registPlayer(request.json)
    return jsonify(ret)

@app.route('/warState/targets', methods=['POST'])
def registTarget():
    name  = referee.registTarget(request.json)
    return jsonify({"name":name})

@app.route('/warState/state', methods=['POST'])
def setState():
    state = referee.setState(request.json)
    return jsonify({"state":state})

@app.route('/reset', methods=['GET'])
def reset():
    global referee
    referee = Referee()
    return jsonify("reset")

@app.route('/test', methods=['GET'])
def getTest():
    return jsonify({
                     "foo":"bar",
                     "hoge":"hogehoge"
                   })

@app.route('/test', methods=['POST'])
def postTest():
    ret = request.json
    print(ret)
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True)

