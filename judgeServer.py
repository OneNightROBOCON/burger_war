from flask import Flask, request, jsonify
app = Flask(__name__)


class Player:
    def __init__(self, name, id=0):
        self.name = name
        self.id = id
    pass

class Score:
    def __init__(self, player='NoPlayer'):
        self.player = player
        self.point = 0
    pass


    def makeJson(self):
        json = {
            "player":self.player,
            "point":self.point
        }
        return json

class Target:
    def __init__(self, name, id):
        self.id = id
        self.name =name
        self.player = "None"
    def makeJson(self):
        json = {
            "name":self.name,
            "id": self.id,
            "player": self.player,
        }
        return json

class WarState:
    def __init__(self):
        self.state = "end"
        self.score = {"r":Score(),"b":Score()}
        self.targets = [Target("foo","ffff"), Target("bar", "0123")]

    def makeJson(self):
        json = {
            "state":self.state,
            "score":{
                "r":self.score["r"].makeJson(),
                "b":self.score["b"].makeJson(),
            },
            "targets":[t.makeJson() for t in self.targets],
        }
        return json


class Submit:
    def __init__(self, player, passcode,target_id):
        self.player = player
        self.passcode =passcode
        self.target_id = target_id

class Referee:
    def __init__(self):
        self.war_state = WarState()

    def judgeTargetId(self, submit):
        for target in self.war_state.targets:
            if submit.passcode == target.passcode:
                updateWarState(target, submit.player)
                return target
        return False

    def updateWarState(self, target, player):
        target.player = player
        return 0

    def registPlayer(self, name):
        if self.state.score.player['r'] == "NoPlayer":
            self.state.score.player['r'] = name
            ret = "r : " + name
        elif self.state.score.player['b'] == "NoPlayer":
            self.state.score.player['b'] = name
            ret = "b : " + name
        else:
            ret = "##Errer 2 player already registed"
        return ret

    def registTarget(self, data):
        self.war_state.targets.append(target)
        return target.name

referee = Referee()

@app.route('/')
def index():
    return "Hello, Welcome to ONIGIRI WAR!"

@app.route('/warState/players', methods=['POST'])
def addPlayer():
    submit = Submit(request.data.player, request.data.id)
    referee.judgeTargetId(submit)
    return jsonify({"resule":True})

@app.route('/warState/targets', methods=['POST'])
def registTarget():
    #submit = Submit(request.data.player,request.data.passcode request.data.id)
    referee.registTarget(request.data)
    return jsonify({"testversion":"sorry yet"})

@app.route('/warState', methods=['GET'])
def getState():
    state_json = referee.war_state.makeJson()
    return jsonify(state_json)

@app.route('/test', methods=['GET'])
def getTest():
    return jsonify({
                     "foo":"bar",
                     "hoge":"hogehoge"
                   })

@app.route('/test', methods=['POST'])
def postTest():
    ret = request.data
    return jsonify(ret)
if __name__ == '__main__':
    app.run(debug=True)
