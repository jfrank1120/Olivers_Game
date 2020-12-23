from google.cloud import datastore
from game import Game
from gameData import game_from_entity
from votingRound import VotingRound

VOTING_ENTITY = 'Voting Round'


def log(msg):
    file_parts = __file__.split("\\")
    smaller_file = file_parts[len(file_parts) - 1]
    print(smaller_file + ": " + msg)


def get_client():
    try:
        client = datastore.Client()
        return client
    except:
        return datastore.Client.from_service_account_json("oliversgame-c83cab85b0e1.json")


def load_key(client, entity_type, entity_id=None, parent_key=None):
    key = None
    if entity_id:
        key = client.key(entity_type, entity_id, parent_key=parent_key)
    else:
        key = client.key(entity_type)
    return key


def load_entity(client, entity_type, entity_id, parent_key=None):
    key = load_key(client, entity_type, parent_key)
    entity = client.get(key)
    log('Retrieved entity for ' + str(entity_id))
    return entity


# Load the Voting Round from DataStore into an object
def voting_round_from_entity(voting_round_entity):
    votes = voting_round_entity['Votes']
    card_data = voting_round_entity['Card Info']
    game_code = voting_round_entity['Game Code']
    voting_round_val = VotingRound(game_code, card_data, votes)
    return voting_round_val


# Add a voting round to the database
def add_voting_round(voting_round):
    client = get_client()
    entity = datastore.Entity(load_key(client, VOTING_ENTITY, voting_round.game_code))
    entity['Game Code'] = voting_round.game_code
    entity['Number of Votes Needed'] = voting_round.num_votes_needed
    entity['Card Info'] = voting_round.card_data
    entity['Votes'] = []
    log('Placing Voting Round')
    client.put(entity)
    log('Created Round for: ' + voting_round.card_data)


# Searches for the voting round matching the passed in game code and then returns the object
def get_current_voting_round_obj(game_code):
    client = get_client()
    query = client.query(kind='Voting Round')
    query.add_filter('Game Code', '=', game_code)
    log('Searching for voting rounds with game code: ' + game_code)
    voting_round_entity = query.fetch()
    voting_round = voting_round_from_entity(voting_round_entity)
    return voting_round


# Get the current voting round in entity form
def get_curr_voting_round_entity(game_code):
    client = get_client()
    query = client.query(kind='Voting Round')
    query.add_filter('Game Code', '=', game_code)
    log('Searching for voting rounds with game code: ' + game_code)
    voting_round_entities = list(query.fetch())
    for x in voting_round_entities:
        return x


# Cast a vote to the current voting round
def cast_vote(game_code, vote_str):
    client = get_client()
    voting_entity = get_curr_voting_round_entity(game_code)
    votes = list(voting_entity["Votes"])
    votes.append(vote_str)
    voting_entity['Votes'] = votes
    client.put(voting_entity)


# Get the number of players that are currently in the game
def get_num_players(voting_round):
    log('Loading players for game_code' + str(voting_round.game_code))
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', voting_round.game_code)
    iterable = list(query.fetch())
    for x in iterable:
        new_game = game_from_entity(x)
        return new_game.num_players
# TODO - FIGURE OUT HOW TO MAKE IT SO EACH PLAYER CAN ONLY VOTE ONCE
