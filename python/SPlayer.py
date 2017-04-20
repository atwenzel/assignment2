"""
Implements the SPlayer class
"""

#Global
import sys

#Local
from Board import Board
from Player import Player
from RuleChecker import RuleChecker

class SPlayer:
    def __init__(self, player): 
        """Takes a Player object"""
        self.player = player
        self.color = ""
        self.rc = None
    
    def startGame(self, color): #None
        """Takes a color string and starts
        the game"""
        self.color = color
        self.player.startGame(self.color)

    def doMove(self, board, dice):  #list of Move
        """Takes a Board object and an int
        list (dice) and executes a move"""
        moves = self.player.doMove(board, dice)
        self.rc = RuleChecker(board, dice) 
        for move in moves:
            print(str(move.pawn.location) + " before move")
            valid, bonus = self.rc.single_move_check(move)
            print(str(move.pawn.location) + " after move")
            if not valid:
                return None
            while bonus != 0:
                bonus_move = self.player.doMove(self.rc.b_final, [bonus])
                print(vars(bonus_move))
                valid, bonus = self.rc.single_move_check(bonus_move, is_bonus_move=True)
                print(str(move.pawn.location)+" after bonus")
        if self.rc.multi_move_check(moves):
            return moves
        else:
            return None

    def doublesPenalty(self):  #None
        self.player.doublesPenalty()
