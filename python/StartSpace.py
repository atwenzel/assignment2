"""Implements the StartSpace class (extends Space)"""

#Global

#Local
from Pawn import Pawn
from Space import Space

class StartSpace(Space):
    def __init__(self, s_id, pawns, color):
        """Takes a space id"""
        Space.__init__(self, s_id)
        self.pawns = pawns
        self.color = color
    
    def add_pawn(self, pawn): #Pawn
        self.pawns.append(pawn)
        return None

    def remove_pawn(self): #Pawn
        pawn_to_return = self.pawns[0]
        self.pawns = self.pawns[1:]
        return pawn_to_return

    def get_pawns(self):  #list of pawns
        return self.pawns

if __name__ == "__main__":
    print("Start Space")
