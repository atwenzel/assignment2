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
        #self.bonus = -1
        self.bonus = []
        if len(dice) == 4:
            self.doubles = True
            self.die3 = dice[2]
            self.die4 = dice[3]

    def get_all_dice(self):
        #return [die for die in self.dice+[self.bonus] if die != -1]  #TODO: change bonus to a list
        return [die for die in [self.die1, self.die2, self.die3, self.die4]+self.bonus if die != -1]
    
    def get_highest_die(self):
        #return max([self.die3, self.die4, self.die1, self.die2, self.bonus])
        #when bonus is a list, return max([self.die3, self.die4, self.die1, self.die2, max(self.bonus)])
        return max([self.die3, self.die4, self.die1, self.die2, max(self.bonus)])

if __name__ == "__main__":
    print("The Turn Values class")
