
class VotingRound(object):
    def __init__(self, card_data, num_votes_needed):
        self.card_data = card_data
        self.num_votes_needed = num_votes_needed

    def to_dict(self):
        return {
            'card_data': self.card_data,
            'num_votes_needed': self.num_votes_needed
        }