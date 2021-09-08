#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response, g, send_from_directory
import os
import socket
import random
import json
import requests

option_a = os.getenv('OPTION_A', u"Horse 🐺")
option_b = os.getenv('OPTION_B', u"Dog 🐶")
hostname = socket.gethostname()

app = Flask(__name__)


@app.route("/", methods=['POST','GET'])
def hello():
    rest_endpoint="http://" + os.environ["VOTING_API_SERVICE_HOST"] + ":" + os.environ["VOTING_API_SERVICE_PORT"]
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None
    if request.method == 'POST':
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        requests.post(url=rest_endpoint + "/vote", data=data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

@app.route("/result", methods=['GET'])
def result():
    return make_response(render_template('result/index.html'))


@app.route("/votes", methods=['GET'])
def votes():
    rest_endpoint="http://" + os.environ["VOTING_API_SERVICE_HOST"] + ":" + os.environ["VOTING_API_SERVICE_PORT"]
    response = requests.get(url=rest_endpoint + "/vote")
    print(response.content)
    return response.content

@app.route('/templates/<path:path>')
def send_js(path):
    return send_from_directory('templates', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
