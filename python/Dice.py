"""
Implements the Dice class
"""

#Global
import random

#Local

class Dice:
    def __init__(self):
        self.result = []
        res1 = random.randint(1, 6)
        res2 = random.randint(1, 6)
        if res1 == res2:
            self.result = [res1, res2, 7-res1, 7-res2]
        else:
            self.result = [res1, res2]

if __name__ == "__main__":
    print("The Dice class")
