from random import randint, choice
import string


class Game(object):
    def __init__(self, hostname):
        self.hostname = hostname
        self.players = []
        self.game_code = ""
        for i in range(7):
            if i % 2 == 0:
                self.game_code = self.game_code + choice(string.ascii_letters)
            else:
                self.game_code = self.game_code + str(randint(1, 9))
        print(self.game_code)

    def toDict(self):
        return {
            'hostname': self.hostname,
            'players': self.players,
            'game_code': self.game_code
        }
