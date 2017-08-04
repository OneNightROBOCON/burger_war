from flask import Flask, request, jsonify
app = Flask(__name__)


class Player:
    def __init__(self, name, id=0):
        self.name = name
        self.id = id
    pass

class Score:
    def __init__(self, player_r='NoPlayer', player_b='NoPlayer'):
        self.player = {"r":player_r, "b":player_b}
        self.point = {"r":0, "b":0}
    pass

class WarState:
    def __init__(self):
        self.score = Score()
        self.targets = []
    def __init__(self, score, targets):
        self.score = score
        self.targets = targets

class Target:
    def __init__(self, name, id, passcode):
        self.name =name
        self.id = id
        self.passcode = passcode
        self.player = "None"
        self.json = {
                        "name":self.name,
                        "id": self.id,
                        "player": self.player,
                    }

class Submit:
    def __init__(self, player, passcode):
        self.player = player
        self.passcode =passcode

class Referee:
    def __init__(self):
        self.war_state = State()
    def __init__(self, state=0):
        self.war_state = state

    def judgeTargetId(self, submit):
        for target in self.war_state.targets:
            if submit.passcode == target.passcode:
                updateWarState(target, submit.player)
                return target
        return False

    def updateWarState(self, target, player):
        target.player = player
        return 0

    def makeJson(self):
        json = {
            "score":self.war_state.score.point,
            "targets":[t.json for t in self.war_state.targets],
        }
        self.war_state.json = json
        return json

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

    def registTarget(self, target):
        self.war_state.targets.append(target)
        return target.name

# init
#p1 = Player("taro")
#p2 = Player("satoru")
#score = Score()
#t1 = Target('head',0)
#t2 = Target('wall_1',1)
#t3 = Target('wall_2',2)
#targets = []
#state = WarState(score, targets)
referee = Referee()

@app.route('/')
def index():
    return "Hello, Welcome to ONIGIRI WAR!"

@app.route('/warState/players', methods=['POST'])
def addPlayer():
    submit = Submit(request.data.player, request.data.id)
    referee.judgeTargetId(submit)
    return jsonify({"resule":True})

@app.route('/warState', methods=['POST'])
def aimTarget():
    submit = Submit(request.data.player, request.data.id)
    referee.judgeTargetId(submit)
    return jsonify({"resule":True})

@app.route('/warState', methods=['GET'])
def getState():
    state_json = referee.makeJson()
    return jsonify(state_json)

if __name__ == '__main__':
    app.run(debug=True)
