from random import randint, choice
import string


class Game(object):
    def __init__(self, hostname, players=[], game_code=None, current_card='PRESS GET NEW CARD TO BEGIN', num_players=0, cards_used=[]):
        self.game_code = game_code
        self.players = players
        self.hostname = hostname
        self.num_players = num_players
        self.current_card = current_card
        # Number in the index of card strings that have been used
        self.cards_used = cards_used
        if self.game_code is None:
            self.game_code = ""
            for i in range(7):
                if i % 2 == 0:
                    self.game_code = self.game_code + choice(string.ascii_letters)
                else:
                    self.game_code = self.game_code + str(randint(1, 9))

    def to_dict(self):
        return {
            'hostname': self.hostname,
            'players': self.players,
            'game_code': self.game_code,
            'num_players': self.num_players,
            'cards_used': self.cards_used,
            'current_card': self.current_card
        }
