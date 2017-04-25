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
        self.started = False
    
    def startGame(self, color): #None
        """Takes a color string and starts
        the game"""
        #player-side color contract
        if color not in ["green", "red", "blue", "yellow"]:
            print("player was not told a valid color")
            sys.exit(1)  #game crashes
        self.color = color
        self.player.startGame(self.color)
        self.started = True

    def doMove(self, board, dice):  #list of Move
        """Takes a Board object and an int
        list (dice) and executes a move"""
        #started contract
        if not self.started:
            print("ERROR: doMove() called before the game started, crashing")
            sys.exit(4)
        #player-side dice contract
        if len(dice) != 2 and len(dice) != 4:
            print("player was given "+str(len(dice))+" dice, expected 2 or 4")
            sys.exit(2)  #game crashes
        moves = self.player.doMove(board, dice)
        """self.rc = RuleChecker(board, dice) 
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
            print("multi move check failed")
            return None"""
        return moves

    def bonus_move(self, board, bonus_val):
        move = self.player.doMove(board, [bonus_val])
        return move

    def doublesPenalty(self):  #None
        if not self.started:  #started contract
            print("ERROR: doublesPenalty() called before the game started, crashing")
            sys.exit(3)
        self.player.doublesPenalty()
