"""
Implements the Pawn class
"""

#Global

#Local

class Pawn:
    def __init__(self, p_id, color, loc):
        """Takes integer id, string color, location id"""
        self.id = p_id
        self.color = color
        self.location = loc

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.color == other.color and self.location == other.location
        return False

if __name__ == "__main__":
    print("the Pawn class")
