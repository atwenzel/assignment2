"""
Implements the MoveMain class (expands Move)
"""

#Global

#Local
from Move import Move
from Pawn import Pawn

class MoveMain(Move):
    def __init__(self, pawn, start, distance):
        Move.__init__(self, pawn)
        self.start = start
        self.distance = distance

if __name__ == "__main__":
    print("The MoveMain class")
