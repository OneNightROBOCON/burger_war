# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime
import time

app = Flask(__name__)


class Target:

    def __init__(self, name, id, point):
        self.id = id
        self.name = name
        self.player = "n"
        self.point = point

    def makeJson(self):
        json = {
            "name": self.name,
            "player": self.player,
            "point": self.point,
            # "id": self.id,
        }
        return json


class WarState:
    def __init__(self):
        self.state = "end"
        self.players = {"r": "NoPlayer", "b": "NoPlayer"}
        self.ready = {"r": False, "b": False}
        self.scores = {"r": 0, "b": 0}
        self.targets = []

    def makeJson(self):
        json = {
            "players": self.players,
            "ready": self.ready,
            "scores": self.scores,
            "state": self.state,
            "targets": [t.makeJson() for t in self.targets],
        }
        return json

class Response:
    def __init__(self):
        self.mutch = False
        self.new = False
        self.error = "yet init"
        self.target = None

    def makeJson(self):
        if self.target is None:
            target = None
        else:
            target = self.target.makeJson()
        json = {
            "mutch": self.mutch,
            "new": self.new,
            "error": self.error,
            "target": target
        }
        return json



class Referee:
    def __init__(self):
        self.war_state = WarState()

    def judgeTargetId(self, player_name, player_side, target_id):
        '''
        target_id must be string and length is "4"
        return "False" or "target json"
        '''
        # make Response object
        response = Response()
        # check id length
        if not len(target_id) == 4:
            app.logger.info("ERROR target length is not 4")
            app.logger.info("player_name: " + player_name)
            app.logger.info("player_side: " + player_side)
            app.logger.info("target_id: " + target_id)
            response.error = "ERR id length is not 4"
            return response.makeJson()

        # set ready if id = 0000
        if target_id == "0000":
            self.war_state.ready[player_side] = True
            response.mutch = True
            response.error = "success set ready"
            return response.makeJson()

        # check state is running
        if self.war_state.state != "running":
            response.error = "ERR state is not running"
            return response.makeJson()

        for target in self.war_state.targets:
            if target_id == target.id:
                is_new = self.updateWarState(target, player_name, player_side)
                response.mutch = True
                response.new = is_new
                response.error = "no error"
                response.target = target
                return response.makeJson()
        response.error = "ERR not mutch id"
        return response.makeJson()

    def checkBothPlayerReady(self):
        if self.war_state.ready["r"] and self.war_state.ready["b"]:
            self.war_state.state = "running"
        return

    def updateWarState(self, target, player_name, player_side):
        if not target.player == "n":
            return False
        else:
            target.player = player_side
            self.war_state.scores[player_side] += int(target.point)
        return True

    def registPlayer(self, name):
        if self.war_state.players['r'] == "NoPlayer":
            self.war_state.players['r'] = name
            ret = {"side": "r", "name": name}
        elif self.war_state.players['b'] == "NoPlayer":
            self.war_state.players['b'] = name
            ret = {"side": "b", "name": name}
        else:
            ret = "##Errer 2 player already registed"
        return ret

    def registTarget(self, name, target_id, point):
        target = Target(name, target_id, point)
        self.war_state.targets.append(target)
        return target.name

    def setState(self, state):
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


# global object referee
referee = Referee()


@app.route('/')
def index():
    ip = request.remote_addr
    msg = "Hello, Welcome to ONIGIRI WAR!"
    app.logger.info("GET /(root) "+ str(ip))
    app.logger.info("RESPONSE /(root) "+ str(ip) + msg)
    return msg


@app.route('/submits', methods=['POST'])
def judgeTargetId():
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /submits " + str(ip) + str(body))
    player_name = body["name"]
    player_side = body["side"]
    target_id = body["id"]
    response = referee.judgeTargetId(player_name, player_side, target_id)
    res = response
    app.logger.info("RESPONSE /submits " + str(ip) + str(res))
    return jsonify(res)


@app.route('/warState', methods=['GET'])
def getState():
    ip = request.remote_addr
    app.logger.info("GET /warState " + str(ip))
    state_json = referee.war_state.makeJson()
    res = state_json
    app.logger.info("RESPONSE /warState "+ str(ip) + str(res))
    return jsonify(res)


@app.route('/warState/players', methods=['POST'])
def registPlayer():
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /warState/players " + str(ip) + str(body))
    name = body["name"]
    ret = referee.registPlayer(name)
    res = ret
    app.logger.info("RESPONSE /warState/players " + str(ip)+ str(res))
    return jsonify(res)


@app.route('/warState/targets', methods=['POST'])
def registTarget():
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /warState/targets " + str(ip)+ str(body))
    name = body["name"]
    target_id = body["id"]
    point = body["point"]
    ret = referee.registTarget(name, target_id, point)
    res = {"name": ret}
    app.logger.info("RESPONSE /warState/targets " + str(ip)+ str(res))
    return jsonify(res)


@app.route('/warState/state', methods=['POST'])
def setState():
    body = request.json
    ip = request.remote_addr
    app.logger.info("POST /warState/state " + str(ip)+ str(body))
    state = body["state"]
    ret = referee.setState(state)
    res =  {"state": ret}
    app.logger.info("RESPONSE /warState/state " + str(ip)+ str(res))
    return jsonify(res)


@app.route('/reset', methods=['GET'])
def reset():
    ip = request.remote_addr
    app.logger.info("GET /reset "+ str(ip))
    global referee
    referee = Referee()
    res =  "reset"
    app.logger.info("RESPONSE /reset "+ str(ip) + str(res))
    return jsonify(res)


@app.route('/test', methods=['GET'])
def getTest():
    ip = request.remote_addr
    app.logger.info("GET /test "+ str(ip))
    res = { "foo": "bar", "hoge": "hogehoge" }
    app.logger.info("RESPONSE /test "+ str(ip) + str(res))
    return jsonify(res)


@app.route('/test', methods=['POST'])
def postTest():
    body = request.json
    ip = request.remote_addr
    app.logger.info(str(ip) + body )
    state = body["state"]
    ret = referee.setState(state)
    res = ret
    app.logger.info("RESPONSE /test "+ str(ip) + str(res))
    return jsonify(res)


if __name__ == '__main__':
    now = datetime.datetime.now()
    now_str = now.strftime("%y%m%d_%H%M%S")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_path = script_dir + "/log/" + now_str + ".log"
    handler = RotatingFileHandler(log_file_path, maxBytes = 1000000, backupCount=100)
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0', port=5000)

