"""
Player that uses the graphical interface
"""

#Global
from multiprocessing import Queue
import socket
from threading import Thread
import time

#Local
from Board import Board
from GUI import GUI
from Player import Player

class GUIPlayer(Player):
    def __init__(self):
        Player.__init__(self)
        self.queue = Queue()
        self.gui = GUI(self.queue)

    def start_gui(self):
        self.gui.start()    

    def startGame(self, color):
        self.color = color
        self.queue.put(color)
        return self.color+" player"

    def doMove(self, board, dice):
        self.queue.put((board, dice))
        time.sleep(1)
        while self.queue.empty():
            continue
        return self.queue.get()

if __name__ == "__main__":
    print("GUI Player")
    player = GUIPlayer()
    print("back in main execution loop")
    player.start_gui()
