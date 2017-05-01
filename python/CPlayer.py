"""
Implements an automatic client player
"""

#Global

#Local
from Board import Board
from EnterPiece import EnterPiece
from MoveMain import MoveMain
from Player import Player
from RuleChecker import RuleChecker

class CPlayer(Player):
    def __init__(self, color, moves):
        Player.__init__(self)
        self.moves = moves
        self.color = color
        
    def doMove(self, board, dice):
        """if len(dice) == 1:
            #pawn_to_move = board.pawns[self.color][0]
            #return [MoveMain(pawn_to_move, pawn_to_move.location, dice[0])]
            curr_bonus_moves = self.bonus_moves[:]
            self.bonus_moves = self.bonus_moves[1:]
            return curr_bonus_moves[0]
        else:
            return self.moves"""
        return self.moves
