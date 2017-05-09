"""
Implements the general Player class
"""

#Global
import copy

#Local

from Board import Board
from EnterPiece import EnterPiece
from HomeSpace import HomeSpace
from MoveMain import MoveMain
from MoveHome import MoveHome
from RegularSpace import RegularSpace
from StartSpace import StartSpace
from RuleChecker import RuleChecker

class Player:
    def __init__(self):
        self.color = ""

    def startGame(self, color):
        self.color = color
        print("Your color is "+self.color)
        return self.color+" player"

    def doublesPenalty(self):
        print("You have a doubles penalty")

    """Move decision logic"""
    def check_next_move(self, rc, move):
        """Returns if move is valid"""       
        local_rc = copy.deepcopy(rc)
        valid = local_rc.single_move_check(move)
        if valid and not local_rc.duplicate_blockades(local_rc.b_start, local_rc.b_final):
            return True, local_rc
        else:
            return False, rc
    
    def stop_move_generation(self, rc):
        return (not rc.more_valid_moves()) and (not rc.more_valid_bonus_moves())

if __name__ == "__main__":
    print("General Player class")
