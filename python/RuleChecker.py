"""
Implements the RuleChecker class
"""

#Global
import copy

#Local
from Board import Board
from EnterPiece import EnterPiece
from MoveHome import MoveHome
from MoveMain import MoveMain
from TurnValues import TurnValues

class RuleChecker:
    def __init__(self, board, moves, dice):
        """Board, Moves, dice (int list)"""
        self.b_start = board
        self.b_final = copy.deepcopy(board)
        self.moves = moves
        self.dice = dice
        self.tvals = TurnValues(dice)
        
        all_moves_good = True
        for move in moves:
            if not self.single_move_check(self.b_final, move):
                this.b_final = None
                all_moves_good = False
                break
        if all_moves_good and (not self.multi_move_checker(self.b_start, self.b_final, self.moves)):
            self.b_final = None

    def single_move_check(self, board, move): #boolean
        if isinstance(move, EnterPiece) and self.valid_enter_dice():
            return True
        else
    
    def valid_enter_dice(self):  #boolean
        if self.tvals.die1 == 5:
            self.tvals.die1 = -1
            return True
        elif self.tvals.die2 == 5:
            self.tvals.die2 = -1
            return True
        elif self.tvals.die3 == 5:
            self.tvals.die3 = -1
            return True
        elif self.tvals.die4 == 5:
            self.tvals.die4 = -1
            return True
        elif self.tvals.die1 + self.tvals.die2:
            self.tvals.die1 = -1
            self.tvals.die2 = -1
            return True
        return False

if __name__ == "__main__":
    print("The Rule Checker")
