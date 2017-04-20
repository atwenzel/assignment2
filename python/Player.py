"""
Implements the general Player class
"""

#Global

#Local

class Player:
    def __init__(self):
        self.color = ""

    def startGame(self, color):
        self.color = color
        print("Your color is "+self.color)

    def doublesPenalty(self):
        print("You have a doubles penalty")

if __name__ == "__main__":
    print("General Player class")
