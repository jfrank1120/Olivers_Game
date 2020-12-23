
class VotingRound(object):
    def __init__(self, game_code, card_data='', votes=[]):
        self.card_data = card_data
        self.num_votes_needed = 0
        self.game_code = game_code
        self.votes = votes

    def to_dict(self):
        return {
            'card_data': self.card_data,
            'num_votes_needed': self.num_votes_needed,
            'game_code': self.game_code,
            'votes': self.votes
        }
