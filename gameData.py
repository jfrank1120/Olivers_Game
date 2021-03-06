from google.cloud import datastore
from game import Game

GAME_ENTITY = 'Game'


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


# Add a game to the database
def add_game(game):
    client = get_client()
    entity = datastore.Entity(load_key(client, GAME_ENTITY, game.game_code))
    entity['Game Code'] = game.game_code
    entity['Number of Players'] = game.num_players
    entity['Players'] = game.players
    entity['Host'] = game.hostname
    entity['Current Card'] = game.current_card
    entity['Cards Used'] = game.cards_used
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
        #print(new_game.players)
        return_list.append(new_game.players)
    return return_list


# Adds a player to the number of players as well as to the current play list
def add_player_to_game(player_name, game_code):
    log('Loading games for game_code' + str(game_code))
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    iterable = list(query.fetch())
    for x in iterable:
        log('Found Game with game code')
        # Alter the fields needed to change
        num_players = int(x['Number of Players'])
        players = list(x["Players"])
        num_players = num_players + 1
        players.append(player_name)
        x['Players'] = players
        x['Number of Players'] = num_players
        client.put(x)


# Checks to see if a game is in the Database
def check_for_game(game_code):
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    iterable = list(query.fetch())
    if len(iterable) != 0:
        return True
    return False


def get_current_card(game_code):
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    games = list(query.fetch())
    for x in games:
        return x['Current Card']


def set_current_card(game_code, card_str):
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    games = list(query.fetch())
    for x in games:
        x['Current Card'] = card_str
        client.put(x)


# Add a card index to the cards used list in the game entity
def add_card_to_used(game_code, card_index):
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    iterable = list(query.fetch())
    for x in iterable:
        cards_used = list(x["Cards Used"])
        cards_used.append(card_index)
        x['Cards Used'] = cards_used
        client.put(x)


def get_game_object(game_code):
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    iterable = list(query.fetch())
    log('Num Games: ' + str(len(iterable)))
    for x in iterable:
        new_game = game_from_entity(x)
        return new_game
    log('No game found for ' + game_code)
    return None


def check_card_indexes_used(game_code, index):
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    iterable = list(query.fetch())
    return_list = []
    for x in iterable:
        new_game = game_from_entity(x)
        return_list.append(new_game.cards_used)
        if return_list.contains(index):
            return False
        return True


def check_all_cards_used(game_code, index_size):
    client = get_client()
    query = client.query(kind='Game')
    query.add_filter('Game Code', '=', game_code)
    iterable = list(query.fetch())
    return_list = []
    for x in iterable:
        new_game = game_from_entity(x)
        return_list.append(new_game.cards_used)
        if len(return_list) == index_size:
            return False
        return True
