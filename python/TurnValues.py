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
        self.die1 = dice[0]
        self.die2 = dice[1]
        self.doubles = False
        self.bonus = -1
        if len(dice) == 4:
            self.doubles = True
            self.die3 = dice[2]
            self.die4 = dice[3]

    

if __name__ == "__main__":
    print("The Turn Values class")
