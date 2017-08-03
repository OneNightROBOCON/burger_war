from flask import Flask, request, jsonify
app = Flask(__name__)


class Player:
    def __init__(self, name, id=0):
        self.name = name
        self.id = id
    pass

class Score:
    def __init__(self, player_r, player_b):
        self.player_r = player_r
        self.player_b = player_b
        self.point = {"r":0, "b":0}
    pass

class WarState:
    def __init__(self, score, targets):
        self.score = score
        self.targets = targets

class Target:
    def __init__(self, pos, id):
        self.pos = pos
        self.id = id
        self.player = "None"
        self.json = {
                        "pos":self.pos,
                        "id": self.id,
                        "player": self.player,
                    }

class Submit:
    def __init__(self, player, id):
        self.player = player
        self.id = id

class Referee:
    def __init__(self, state):
        self.war_state = state

    def judgeTargetId(self, submit):
        for target in self.war_state.targets:
            if submit.id == target.id:
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

# init
p1 = Player("taro")
p2 = Player("satoru")
score = Score(p1, p2)
t1 = Target('head',0)
t2 = Target('wall_1',1)
t3 = Target('wall_2',2)
targets = [t1,t2,t3]
state = WarState(score, targets)
referee = Referee(state)

@app.route('/')
def index():
    return "Hello, Welcome to ONIGIRI WAR!"

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
