from flask import Flask, Response, redirect
import flask
import json
import requests as request_lib

app = flask.Flask(__name__)


def log(msg):
    print(__file__ + ": " + msg)


@app.route('/')
def root():
    return redirect("/static/index.html", code=302)


@app.route('/user_attempt_login', methods=["POST"])
def user_attempt_login():
    print('lol')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)