"""
Implements the SPlayer class
"""

#Global

#Local
from Board import Board
from Player import Player

class SPlayer:
    def __init__(player): 
        """Takes a Player object"""
        self.player = player
        self.color = ""
    
    def startGame(color): #None
        """Takes a color string and starts
        the game"""
        self.color = color
        self.player.startGame(self.color)

    def doMove(board, dice):  #Move
        """Takes a Board object and an int
        list (dice) and executes a move"""
        return None

    def doublesPenalty():  #None
        this.player.doublesPenalty()
