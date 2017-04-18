"""
Implements the game class
"""

#Global

#Local
import Player
import SPlayer

class Game:
    def __init__(self):
        self.players = []  #list of SPlayer objects
        self.colors = ["red", "blue", "green", "yellow"]

    def register(self, player):
        """Takes a Player object registers it"""
        self.players.append(SPlayer(player))

    def start(self):
        """Starts a game loop"""
        for player in self.players:
            player.startGame(colors[i])

if __name__ == "__main__":
    print("The game class")
