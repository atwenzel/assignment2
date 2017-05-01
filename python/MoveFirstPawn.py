"""
Implements a client player that always tries to move
its first pawn
"""

#Global

#Local
from Board import Board
from EnterPiece import EnterPiece
from Player import Player
from Rulechecker import Rulechecker

class MoveFirstPawn(Player):
    def __init__(self, color):
        Player.__init__(self)
        self.color = color

    def doMove(self, board, dice):
        """Uses the given board and dice to decide
        on a set of moves to take"""
        return []
