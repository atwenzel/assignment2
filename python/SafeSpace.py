"""Implements the SafeSpace class (extends Space)"""

#Global

#Local
from Pawn import Pawn
from Space import Space

class SafeSpace(Space):
    def __init__(self, s_id):
        """Takes a space id"""
        Space.__init__(self, s_id)
        self.pawn1 = None
        self.pawn2 = None
        self.next_home = None #Space
    
    def add_pawn(self, pawn): #Pawn
        if self.pawn1 == None:
            self.pawn1 = pawn
            return None
        elif self.pawn1.color == pawn.color:
            self.pawn2 = pawn
            return None
        else:
            removed_pawn = self.remove_pawn(self.pawn1)
            self.pawn1 = pawn
            return removed_pawn

    def remove_pawn(self, pawn): #Pawn
        if pawn == self.pawn1:
            self.pawn1 = self.pawn2
            self.pawn2 = None
            return pawn
        elif pawn == self.pawn2:
            self.pawn2 = None
            return pawn
        else:
            return None

    def get_pawns(self):  #dict of pawns
        return {"pawn1": self.pawn1, "pawn2": self.pawn2}
    
    def has_blockade(self):  #boolean
        return self.pawn1 != None and self.pawn2 != None
 
if __name__ == "__main__":
    print("Safe Space")
