"""
Implements the Turn Values class (handles values for mini moves)
"""

#Global

#Local
from Dice import Dice

class TurnValues:
    def __init__(self, dice):
        self.dice = dice
        self.die3 = -1
        self.die4 = -1
        self.bop_bonus = -1
        self.home_bonus = -1
        self.die1 = dice.result[0]
        self.die2 = dice.result[1]
        if len(dice.result) == 4:
            self.die3 = dice.result[2]
            self.die4 = dice.result[3]

if __name__ == "__main__":
    print("The Turn Values class")
