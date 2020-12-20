# Player class for each time a new player joins the game
class Player(object):
    def __init__(self, username, cards_won=[], active=True):
        self.username = username
        self.cards_won = cards_won
        self.active = active

    def add_card_won(self, card_data):
        self.cards_won.append(card_data)

    def set_inactive(self):
        self.active = False

    def to_dict(self):
        return {
            'username': self.username,
            'cards_won': self.cards_won,
            'active': self.active
        }
