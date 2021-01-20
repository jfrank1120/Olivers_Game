# Basic import statements
from flask import Flask, Response, redirect, session
import flask
import json
from random import randint

# Other files/functions to import
from game import Game
from player import Player
from votingRound import VotingRound
import playerData
import gameData
import votingRoundData

# Needed for flask actions
app = flask.Flask(__name__)
app.secret_key = b'@U\xb0\xadf\x92f\xe8\x10\xee\xdf\x81O\x92\xb7\xe5\xca\x10rE&=\xd0\x7f'

global winner_crowned
global latest_winner
global number_of_sips
global number_of_votes


# Simple logging function for server output
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
    username = flask.request.form['username']
    log('Player Attempting to join game: ' + str(game_code))
    # Access the Database to see if a game with that code exists
    error_msg = ""
    if gameData.check_for_game(game_code) is not True:
        success_val = "False"
        error_msg = "Game Does Not Exist"
    elif playerData.check_for_player(username) is not True:
        log('Found player with same name')
        success_val = "False"
        error_msg = "Username Already Taken"
    else:
        # If successful add it to the game_code session value
        log('Passed Checks')
        session['game_code'] = game_code
        session['username'] = username
        success_val = "True"
        new_player = Player(username, [], True)
        playerData.add_player(new_player)
        gameData.add_player_to_game(new_player.username, game_code)

    # Create json to return to JS
    json_val = {
        "Success": success_val,
        "Error": error_msg
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
    game = gameData.get_game_object(session['game_code'])
    json_data = {
        'username': session['username'],
        'game_code': session['game_code'],
        'host_name': game.hostname
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
    with open('Card_Data.txt', 'r') as card_data:
        card_strings = card_data.read().splitlines()
    # Case where all cards have been used
    if gameData.check_all_cards_used(session['game_code'], len(card_strings) - 1):
        json_resp = {
            'current_card': 'All Cards Have Been Used, Please create a new game to restart'
        }
        return Response(json.dumps(json_resp), mimetype='application/json')

    while True:
        index = randint(0, len(card_strings) - 1)
        if gameData.check_card_indexes_used(session['game_code'], index):
            break

    selected_card = card_strings[index]
    log('selected card: ' + selected_card)
    # All the database actions
    gameData.add_card_to_used(session['game_code'], index)
    gameData.set_current_card(session['game_code'], selected_card)
    new_voting_round = VotingRound(session['game_code'], selected_card)
    new_voting_round.num_votes_needed = votingRoundData.get_num_players(new_voting_round)
    votingRoundData.add_voting_round(new_voting_round)
    # Reset the global variables
    reset_globals()

    json_resp = {
        'current_card': selected_card
    }
    return Response(json.dumps(json_resp), mimetype='application/json')


# End point for when the user clicks submit vote
@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    vote_choice = flask.request.form['choice']
    log(session['username'] + ' is casting a vote for ' + vote_choice)
    # Add data to voting round
    votingRoundData.cast_vote(session['game_code'], vote_choice)
    # Update their last time voting on their player entity
    playerData.update_last_vote(session['username'])
    json_resp = {
        'Vote Response': 'Success'
    }
    return Response(json.dumps(json_resp), mimetype='application/json')


@app.route('/get_current_card', methods=["POST"])
def get_current_card():
    log('GETTING THE CURRENT CARD ')
    game_code = flask.request.form['game_code']
    curr_card = gameData.get_current_card(game_code)
    json_data = {
        "current_card": curr_card
    }
    return Response(json.dumps(json_data), mimetype='application/json')


@app.route('/get_UI_info', methods=['POST'])
def get_ui_info():
    players_list = gameData.load_players(session['game_code'])
    current_card = gameData.get_current_card(session['game_code'])
    global winner_crowned
    if winner_crowned is True:
        ui_info = {
            'username': session['username'],
            'game_code': session['game_code'],
            'players': players_list,
            'current_card': current_card,
            'round_winner': latest_winner,
            'num_votes': number_of_votes,
            'num_sips': number_of_sips
        }
    else:
        ui_info = {
            'username': session['username'],
            'game_code': session['game_code'],
            'players': players_list,
            'current_card': current_card,
        }
    return Response(json.dumps(ui_info), mimetype='application/json')


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


@app.route('/get_players_cards', methods=['POST'])
def get_players_cards():
    player_name = flask.request.form['player_name']
    cards_list = playerData.get_players_cards(player_name)
    json_ret = {
        'cards_won': cards_list,
        'selected_player': player_name
    }
    return Response(json.dumps(json_ret), mimetype='application/json')


@app.route('/count_votes', methods=['POST'])
def count_votes():
    # TODO - THINK OF A WAY TO GET ALL PLAYERS TO VIEW THE WINNER MODAL WHEN VOTES ARE TALLIED
    voting_round_obj = votingRoundData.get_current_voting_round_obj(session['game_code'])
    highest_votes = 0
    current_leader = None
    for x in voting_round_obj.votes:
        if voting_round_obj.votes.count(x) > highest_votes:
            highest_votes = voting_round_obj.count(x)
            current_leader = str(x)
    num_sips = randint(0, 5)
    set_globals(current_leader, num_sips, highest_votes)
    json_ret = {
        "winner": current_leader,
        "num_votes": highest_votes,
        "num_sips": num_sips
    }
    votingRoundData.remove_voting_round('game_code')
    # Get player object
    player_obj = playerData.get_player_obj(current_leader)
    # Add won card to player object
    player_obj.cards_won.append(voting_round_obj.card_data)
    # Add won card back to the
    playerData.update_cards_won(player_obj)

    return Response(json.dumps(json_ret), mimetype='application/json')


# Set the globals so that the front-end can show the user a modal
def set_globals(current_leader, num_sips, highest_votes):
    global latest_winner
    latest_winner = current_leader
    global number_of_sips
    number_of_sips = num_sips
    global number_of_votes
    number_of_votes = highest_votes
    global winner_crowned
    winner_crowned = True


# Reset all of the global variables for showing a modal to the player
def reset_globals():
    global latest_winner
    latest_winner = ''
    global number_of_sips
    number_of_sips = 0
    global number_of_votes
    number_of_votes = 0
    global winner_crowned
    winner_crowned = False


# TODO - CHECK THAT TIMESTAMP FUNCTION WORKS WHEN A USER CASTS A VOTE
# TODO - CHECK IF PLAYERS ARE ACTIVE IF NOT REMOVE THEM FROM THE GAME (TIMESTAMP THEIR LAST VOTE?)
# TODO - FIGURE OUT WAY TO ALERT USER WHO HAS WON THE CARD THAT THEY DID WIN (MODAL?)
# TODO - BEGIN DOING UNIT TESTING / UI TESTING


# Main Method, Nothing to see here
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
