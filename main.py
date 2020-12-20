from flask import Flask, Response, redirect, session
import flask
import json
from game import Game
import gameData

app = flask.Flask(__name__)
app.secret_key = b'@U\xb0\xadf\x92f\xe8\x10\xee\xdf\x81O\x92\xb7\xe5\xca\x10rE&=\xd0\x7f'


def log(msg):
    print(__file__ + ": " + msg)


@app.route('/')
def root():
    return redirect("/static/index.html", code=302)


@app.route('/create_game')
def create_game_route():
    return redirect('/static/create_game.html', code=302)


@app.route('/begin_game', methods=["GET"])
def begin_game():
    return redirect('/static/main_game.html', code=302)


@app.route('/user_join_attempt', methods=["POST"])
def user_join_attempt():
    game_code = flask.request.form['game_code']
    log('Player Attempting to join game: ' + str(game_code))
    # Access the Database to see if a game with that code exists

    # If successful add it to the game_code session value
    session['game_code'] = game_code

@app.route('/start_game', methods=["POST"])
def start_game():
    log('Starting the game')
    host_name = flask.request.form['Hostname']
    game_name = flask.request.form['GameName']
    session['username'] = host_name
    log(host_name + " " + game_name)
    # Create the Game object
    new_game = Game(hostname=host_name)
    session['game_code'] = new_game.game_code
    # Add game to database
    gameData.add_game(new_game)
    # Add player to game
    add_player(host_name, game_name)
    # Send to the game screen
    json_result = {
        "hostName": host_name,
        "gameName": game_name
    }
    return Response(json.dumps(json_result), mimetype='application/json')


@app.route('/get_session_data', methods=["POST"])
def get_session_data():
    json_data = {
        'username': session['username'],
        'game_code': session['game_code']
    }
    return Response(json.dumps(json_data), mimetype='application/json')


def add_player(username, game_name):
    log('Adding ' + username + " to " + game_name)


# Set a new card as the current card for the game
@app.route('/get_new_card', methods=["POST"])
def get_new_card():
    log('GENERATING NEW CARD')


# Get the player names from the database to return to the front-end
@app.route('/populate_players', methods=["POST"])
def populate_players():
    game_code = flask.request.form['game_code']
    log('populating players for game_code: ' + game_code)
    players_list = gameData.load_players(game_code)
    log(players_list)
    json_val = {
        'players': players_list
    }
    return Response(json.dumps(json_val), mimetype='application/json')


# Main Method, Nothing to see here
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)