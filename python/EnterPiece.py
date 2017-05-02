"""
Implements EnterPiece (expands Move)
"""

#Global

#Local
from Move import Move
from Pawn import Pawn

class EnterPiece(Move):
    def __init__(self, pawn):
        Move.__init__(self, pawn)

    def __eq__(self, other):
        if other == None:
            return False
        return self.pawn == other.pawn
