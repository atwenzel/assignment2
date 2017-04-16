"""Implements the Space base class"""

#Global

#Local

class Space:
    def __init__(self, s_id):
        """Takes an integer id"""
        self.id = s_id
        self.next_space = None  #Space

if __name__ == "__main__":
    print("The base Space class")
