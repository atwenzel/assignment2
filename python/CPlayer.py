"""
Implements an automatic client player
"""

#Global

#Local
from Board import Board
from Player import Player
from RuleChecker import RuleChecker

class CPlayer(Player):
    def __init__(color, moves):
        Player.__init__(color)
        self.moves = moves
        
    def doMove(self, board, dice):
        return self.moves
