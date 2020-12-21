from google.cloud import datastore
from player import Player

PLAYER_ENTITY = "Player"


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


def player_from_entity(player_entity):
    username = player_entity['Username']
    cards_won = player_entity['Cards Won']
    active = player_entity['Active']
    new_player = Player(username, cards_won, active)
    return new_player


# Get the cards won for the player that is passed in
def get_players_cards(player):
    username = player.username
    client = get_client()
    query = client.query(kind='Player')
    query.add_filter('Username', '=', username)
    iterable = list(query.fetch())
    for x in iterable():
        new_player = player_from_entity(x)
        return new_player.cards_won


# Add a player to the database
def add_player(player):
    client = get_client()
    entity = datastore.Entity(load_key(client, PLAYER_ENTITY, player.username))
    entity['Username'] = player.username
    entity['Cards Won'] = player.cards_won
    entity['Active'] = player.active
    client.put(entity)
    log('Just added player ' + player.username)


# Check to see if a player is in the Database
def check_for_player(player_name):
    client = get_client()
    query = client.query(kind='Player')
    query.add_filter('Username', '=', player_name)
    iterable = list(query.fetch())
    if len(iterable) != 0:
        return False
    return True
