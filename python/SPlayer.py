"""
Implements the SPlayer class
"""

#Global
import socket
import sys
from threading import Thread
import xmltodict

#Local
from Board import Board
from GUIPlayer import GUIPlayer
from MoveFirstPawn import MoveFirstPawn
from Player import Player
from RuleChecker import RuleChecker
import XML

class SPlayer:
    def __init__(self, player, use_gui=True): 
        """Takes a Player object"""
        self.player = player
        self.color = ""
        self.rc = None
        self.started = False
        """Listening loop starts here, decode, perform requests to local player, encode results, send back"""
        if use_gui:
            self.listener_thread = Thread(target=self.dumb_loop)
            self.listener_thread.daemon = True
            self.listener_thread.start()
        else:
            self.dumb_loop()

    def dumb_loop(self, ip='localhost', port=49494, dest_ip='localhost', dest_port=8000):
        print("in dumb loop")
        #ping the game server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((ip, port))
        sock.connect((dest_ip, dest_port))
        #sock.listen(1)
        while True:
            #connection, client_addr = sock.accept()
            data = XML.add_spaces(sock.recv(8192))
            print(data)
            msg_type = data.split()[0][1:-1]
            if msg_type == 'start-game':
                print("SPlayer::dumb_loop: got a start-game")
                sg_d = xmltodict.parse(data)
                name = self.startGame(sg_d['start-game'])
                sock.sendall(XML.encode_name(name))
            elif msg_type == 'do-move':
                print("SPlayer::dumb_loop: got a do-move")
                board, dice = XML.decode_do_move(xmltodict.parse(data)['do-move'])
                moves = self.doMove(board, dice)
                encoded_moves = XML.encode_moves(moves)
                print("sending these moves back: "+encoded_moves)
                print("")
                sock.sendall(encoded_moves)
            elif msg_type == 'doubles-penalty':
                print("SPlayer::dumb_loop: got a doubles-penalty")
                self.doublesPenalty()
                sock.sendall(XML.encode_void())
            #connection.close()
             
    def startGame(self, color): #None
        """Takes a color string and starts
        the game"""
        #player-side color contract
        if color not in ["green", "red", "blue", "yellow"]:
            print("Splayer::startGame: player was not told a valid color")
            sys.exit(1)  #game crashes
        self.color = color
        name = self.player.startGame(self.color)
        self.started = True
        return name

    def doMove(self, board, dice):  #list of Move
        """Takes a Board object and an int
        list (dice) and executes a move"""
        #started contract
        if not self.started:
            print("SPlayer::doMove: ERROR: doMove() called before the game started, crashing")
            sys.exit(4)
        #player-side dice contract
        if len(dice) != 2 and len(dice) != 4:
            print("SPlayer::doMove: player was given "+str(len(dice))+" dice, expected 2 or 4")
            sys.exit(2)  #game crashes
        moves = self.player.doMove(board, dice)
        return moves

    def do_bonus_move(self, board, bonus_val):
        move = self.player.doMove(board, [bonus_val])
        return move

    def doublesPenalty(self):  #None
        if not self.started:  #started contract
            print("SPlayer::doublesPenalty: ERROR: doublesPenalty() called before the game started, crashing")
            sys.exit(3)
        self.player.doublesPenalty()

if __name__ == "__main__":
    splayer = SPlayer(MoveFirstPawn("green"))
    print("in main thread")
#print("SPlayer: entering dumb_loop")
#splayer.dumb_loop
