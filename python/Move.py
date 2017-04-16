"""
Implements the Move base class
"""

#Global

#Local
from Pawn import Pawn

class Move:
    def __init__(self, pawn):
        self.pawn = pawn

if __name__ == "__main__":
    print("Base Move class")
