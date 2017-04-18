"""
Implements the SPlayer class
"""

#Global

#Local
from Board import Board
from Player import Player
from RuleChecker import RuleChecker

class SPlayer:
    def __init__(self, player): 
        """Takes a Player object"""
        self.player = player
        self.color = ""
    
    def startGame(self, color): #None
        """Takes a color string and starts
        the game"""
        self.color = color
        self.player.startGame(self.color)

    def doMove(self, board, dice):  #list of Move
        """Takes a Board object and an int
        list (dice) and executes a move"""
        moves = self.player.doMove(board, dice)
        rc = RuleChecker(board, dice) 
        for move in moves:
            valid, bonus = rc.single_move_check(move)
            if not valid:
                return None
            while bonus != 0:
                bonus_move = self.player.doMove(rc.b_final, [bonus])
                bonus = rc.single_move_check(bonus_move[0])
        if rc.all_moves_check():
            return moves
        else:
            return None

    def doublesPenalty(self):  #None
        self.player.doublesPenalty()
