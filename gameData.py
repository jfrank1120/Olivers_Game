from google.cloud import datastore
from game import Game
from main import log

GAME_ENTITY = 'Game'

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

# Add a game to the database
def add_game(game):
    client = get_client()
    entity = datastore.Entity(load_key(client, GAME_ENTITY, game.game_code))
    entity['Game Code'] = game.game_code
    entity['Number of Players'] = game.num_players
    entity['Players'] = game.players
    entity['Host'] = game.hostname
    log('Placing Game')
    client.put(entity)
    log('Saved Game, name' + game.hostname)

# Load the Game from DataStore into an object
def game_from_entity(game_entity):
    hostname = game_entity['Host']
    num_players = game_entity['Number of Players']
    players = game_entity['Players']
    current_card = game_entity['Current Card']
    game_code = game_entity['Game Code']
    game_val = Game(hostname, players, game_code, current_card, num_players)
    return game_val


# Load players in the game based on the Queried Game Code
def load_players(game_code):
    log('Loading players for game_code' + str(game_code))
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    return_list = []
    iterable = list(query.fetch())
    log('Num Games: ' + str(len(iterable)))
    for x in iterable:
        new_game = game_from_entity(x)
        print(new_game.players)
        return_list.append(new_game.players)

    return return_list
