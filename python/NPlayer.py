"""
Network player

Game has list of these

when functions called, send requests to SPlayer
"""

#Global
import xmltodict
import socket

#Local
from Board import Board
import XML

class NPlayer:
    def __init__(self, ip='localhost', port=8000):
        self.ip = ip
        self.port = port
        print("will contact the client on "+ip+":"+str(port))

    def contact_client(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        sock.connect((self.ip, self.port))
        sock.sendall(data)
        resp = sock.recv(8192)
        #print("NPlayer: data receieved: "+resp)
        sock.close()
        return resp

    def startGame(self, color):
        start_game_message = XML.encode_start_game(color)
        name_xml = self.contact_client(start_game_message)
        name_d = xmltodict.parse(name_xml)
        return name_d['name']

    def doMove(self, board, dice):
        do_move_msg = XML.encode_do_move(board, dice)
        moves_xml = self.contact_client(do_move_msg)
        moves = XML.decode_moves(moves_xml)
        return moves

    def doublesPenalty(self):
        dp_msg = XML.encode_doubles_penalty()
        resp = self.contact_client(dp_msg)
        print(resp)

if __name__ == "__main__":
    np = NPlayer()
    #np.contact_client("hello player!")
    print(np.startGame("green"))
    print(np.doMove(Board(4), [5, 2]))
    #np.doublesPenalty()
