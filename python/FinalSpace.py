"""Implements a final space that can hold 4 pawns"""

#Global

#Local

from Pawn import Pawn
from Space import Space

class FinalSpace(Space):
    def __init__(self, s_id, color):
        Space.__init__(self, s_id)
        self.pawns = []
        self.color = color

    def add_pawn(self, pawn):
        if len(self.pawns) < 4:
            self.pawns.append(pawn)
            return pawn
        else:
            return None
    
    def remove_pawn(self, pawn):
        try:
            self.pawns.remove(pawn)
        except ValueError:  #pawn isn't in the list
            return None
        
    def get_pawns(self):
        return self.pawns

    def has_blockade(self):
        return False

if __name__ == "__main__":
    print("Final Space")
