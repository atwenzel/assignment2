"""
Implements the game class
"""

#Global

#Local
from Board import Board
from Dice import Dice
from Player import Player
from RuleChecker import RuleChecker
from SPlayer import SPlayer

class Game:
    def __init__(self):
        self.players = []  #list of SPlayer objects
        self.colors = ["red", "blue", "green", "yellow"]
        self.board = Board(4)
        self.status = {}
        self.started = False
        #for color in self.colors:
        #    self.status[color] = {}
        #    self.status[color]['active'] = True
        #    self.status[color]['has_won'] = False

    def register(self, player):
        """Takes a Player object registers it"""
        #started contract for register
        if self.started:
            print("The game has started, you cannot register!")
        else:
            self.players.append(SPlayer(player))

    def start(self, override_dice=[]):
        """Starts a game loop (override_dice is an optional field that
        allows us to bypass random dice generation for testing purposes
        and does not affect gameplay when left as the default value)"""
        self.started = True
        player_counter = 0
        for player in self.players:
            assigned_color = self.colors[player_counter]
            self.status[assigned_color] = {}
            self.status[assigned_color]['active'] = True
            self.status[assigned_color]['has_won'] = False
            player.startGame(assigned_color)
            player_counter += 1
        while self.have_winner() == None and not self.all_eliminated():
            for player in self.players:
                if self.is_active(player.color):
                    if override_dice != []:
                        new_dice = override_dice
                    else:
                        new_dice = Dice().result
                    moves = player.doMove(self.board, new_dice)
                    rc = RuleChecker(self.board, new_dice, player.color)
                    for move in moves:
                        if not self.is_active(player.color):
                            break
                        valid, bonus = rc.single_move_check(move)
                        #player legal move contract
                        if not valid:
                            self.eliminate_player(player)
                            break
                        while bonus != 0:
                            #contract - forces players to keep making bonus moves
                            #until they have 0 bonus value
                            bonus_move = self.player.doMove(rc.b_final, [bonus])
                            valid, bonus = rc.single_move_check(bonus_move, is_bonus_move=True)
                            if not valid:
                                self.eliminate_player(player)
                                break
                    if not self.is_active(player.color):
                        continue
                    else:
                        if not rc.multi_move_check(moves):
                            self.eliminate_player(player)
                            continue
                    self.board = rc.b_final

    def eliminate_player(self, player):
        self.status[player.color]['active'] = False
        print(player.color+" player has been eliminated for breaking the rules!!!")
        return True

    def have_winner(self):
        for player in self.players:
            if self.status[player.color]['has_won']:
                return player.color
        return None

    def all_eliminated(self):
        for player in self.players:
            if self.is_active(player.color):
                return False
        return True

    def is_active(self, color):
        return self.status[color]['active']

if __name__ == "__main__":
    ("The game class")
