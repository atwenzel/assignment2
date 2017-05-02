"""
Implements the MoveHome class (expands Move)
"""

#Global

#Local
from Move import Move
from Pawn import Pawn

class MoveHome(Move):
    def __init__(self, pawn, start, distance):
        Move.__init__(self, pawn)
        self.start = start
        self.distance = distance

    def __eq__(self, other):
        if other == None:
            return False
        return self.pawn == other.pawn and self.start == other.start and self.distance == other.distance

if __name__ == "__main__":
    print("The MoveHome class")
