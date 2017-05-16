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
        #self.start_gui()
        #self.gui_thread = Thread(target=self.start_gui)
        #self.gui_thread.start()

    def start_gui(self):
        self.gui.start()    

    def startGame(self, color):
        self.color = color
        #self.gui = GUI()
        #b = Board(4)
        #self.start_gui()
        #self.gui.draw_board(b)
        #self.gui.build_player_status(self.color)
        #print("my color is "+color)
        self.queue.put(color)
        return self.color+" player"

    def doMove(self, board, dice):
        #self.gui.update_board(board)
        #self.gui.build_move_interface(dice)
        #while True:
        #    if self.gui.done:
        #        return self.gui.moves
        self.queue.put((board, dice))
        time.sleep(1)
        while self.queue.empty():
            continue
        return self.queue.get()

if __name__ == "__main__":
    print("GUI Player")
    player = GUIPlayer()
    print("back in main execution loop")
    #player.startGame("green")
    player.start_gui()
