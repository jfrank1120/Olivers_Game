from google.cloud import datastore
from player import Player
from main import log


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
