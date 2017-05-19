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
                    doubles = True
                    doubles_count = 0
                    while doubles:
                        if override_dice != []:
                            new_dice = override_dice
                        else:
                            new_dice = Dice().result
                        if len(new_dice) == 4:
                            print("Game::start: player has a double")
                            print("Game::start: current double count: "+str(doubles_count))
                            doubles_count += 1
                            if doubles_count == 3:
                                player.doublesPenalty()
                                self.move_back_furthest_pawn(player.color)
                                return ##debugging
                                break
                            if not self.board.all_out(player.color):
                                new_dice = new_dice[:2]
                        elif len(new_dice) == 2:
                            doubles = False
                        moves = player.doMove(self.board, new_dice)
                        rc = RuleChecker(self.board, new_dice, player.color)
                        for move in moves:
                            try:
                                is_bonus = move.distance in rc.tvals.bonus
                            except AttributeError:  #is an EnterPiece
                                is_bonus = False
                            valid = rc.single_move_check(move, is_bonus_move=is_bonus)
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

    def move_back_furthest_pawn(self, color):
        """Takes color's furthest ahead pawn that is not at home and
        returns it to start space"""
        sorted_pawns = self.board.order_pawns(color)
        for pawn in sorted_pawns:
            if pawn.location == self.board.finishes[color]:
                continue
            else:
                pawn_space = self.board.spacemap[pawn.location]
                pawn_space.remove_pawn(pawn)
                self.board.spacemap[self.board.starts[color].id].add_pawn(pawn)
                pawn.location = self.board.starts[color].id

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
    print("The game class")
