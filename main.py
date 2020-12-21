from flask import Flask, Response, redirect, session
import flask
import json
from game import Game
from player import Player
import playerData
import gameData

app = flask.Flask(__name__)
app.secret_key = b'@U\xb0\xadf\x92f\xe8\x10\xee\xdf\x81O\x92\xb7\xe5\xca\x10rE&=\xd0\x7f'


def log(msg):
    file_parts = __file__.split("\\")
    smaller_file = file_parts[len(file_parts) - 1]
    print(smaller_file + ": " + msg)


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
    # TODO - Database query to confirm game exists -> create player object -> add player to game

    # If successful add it to the game_code session value
    session['game_code'] = game_code

    # Create json to return to JS
    json_val = {
        "Success": "True",
        "Error": ""
    }
    return Response(json.dumps(json_val), mimetype='application/json')


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
    add_player(host_name, new_game)
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


def add_player(username, game):
    log('Adding ' + username + " to " + game.hostname)
    new_player = Player(username)
    playerData.add_player(new_player)
    gameData.add_player_to_game(username, game.game_code)


# Set a new card as the current card for the game
@app.route('/get_new_card', methods=["POST"])
def get_new_card():
    log('GENERATING NEW CARD')
    # TODO - PULL A STRING FROM THE TEXT FILE -> UPDATE THE DATABASE WITH IT -> CALL GET CURRENT  CARD


@app.route('/get_current_card', methods=["POST"])
def get_current_card():
    log('GETTING THE CURRENT CARD ')


# Get the player names from the database to return to the front-end
@app.route('/populate_players', methods=["POST"])
def populate_players():
    game_code = flask.request.form['game_code']
    log('populating players for game_code: ' + game_code)
    players_list = gameData.load_players(game_code)
    log(str(players_list))
    json_val = {
        'players': players_list
    }
    return Response(json.dumps(json_val), mimetype='application/json')

# TODO - CHECK THAT A PLAYERS NAME DOES NOT ALREADY EXIST IN THE DATABASE
# TODO - CHECK IF PLAYERS ARE ACTIVE IF NOT REMOVE THEM FROM THE GAME (TIMESTAMP THEIR LAST VOTE?)

# Main Method, Nothing to see here
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)