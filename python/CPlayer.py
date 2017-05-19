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
        return self.moves
