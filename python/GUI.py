"""
???
"""

#Global
from multiprocessing import Queue
import time
#import Tkinter as tk
#import mtTkinter as tk
import Tkinter as tk

#Local
from Board import Board
from EnterPiece import EnterPiece
from FinalSpace import FinalSpace
from HomeSpace import HomeSpace
from MoveHome import MoveHome
from MoveMain import MoveMain
from Pawn import Pawn
from RegularSpace import RegularSpace
from SafeSpace import SafeSpace
from StartSpace import StartSpace

COLORS_D = {
    "red": "#f90c1c",
    "green": "#10c900",
    "blue": "#0c3bf9",
    "yellow": "#f9e10c",
    "safe": "#980fd8",
    "neutral": "#6394ff"
}

FOUR_PAWN_ALIGNMENT_D = {
    0: 'nw',
    1: 'ne',
    2: 'sw',
    3: 'se'
}

class GUISpace(tk.Label):
    def __init__(self, parent, row, col, space_id, bg="", height=0, width=0, text="",
            rowspan=1, columnspan=1):
        tk.Label.__init__(self, parent, bg=bg, height=height, width=width, 
            borderwidth=2, relief='raised', text=str(row)+","+str(col))
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.space_id = space_id
        self.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan)

class GUIPawn(tk.Label):
    def __init__(self, parent, pawn, row, col):
        tk.Label.__init__(self, parent, bg=COLORS_D[pawn.color], height=1, width=1,
            text=str(pawn.id), borderwidth=2, relief='raised')
        self.pawn = pawn
        self.row = row
        self.col = col
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.grid(row=row, column=col)
    
    def get_alignment(self, spacemap):
        on_space = spacemap[self.pawn.location]
        if isinstance(on_space, FinalSpace) or isinstance(on_space, StartSpace):
            self.grid(row=self.row, column=self.col, sticky=FOUR_PAWN_ALIGNMENT_D[self.pawn.id])
        else:
            if self.height==2 and self.width==8:
                if on_space.pawn2 == None:
                    self.grid(row=self.row, column=self.col, sticky='w')
                else:
                    self.grid(row=self.row, column=self.col, sticky='e')
            else:
                if on_space.pawn2 == None:
                    self.grid(row=self.row, column=self.col, sticky='n')
                else:
                    self.grid(row=self.row, column=self.col, sticky='s')

class GUIDie(tk.Label):
    def __init__(self, parent, val, row, col):
        tk.Label.__init__(self, parent, bg='white', height=2, width=2,
            text=str(val), borderwidth=2, relief='raised')
        self.val = val
        self.row = row
        self.col = col
        self.height = self.winfo_height()
        self.width = self.winfo_width()
        self.grid(row=row, column=col)

class GUIMove:
    def __init__(self):
        self.pawn = None
        self.distance = -1
    
    def convert_to_move(self):
        """Returns an internal move object based on input"""
        return None

class GUI:
    def __init__(self, queue):
        self.queue = queue
        self.root = tk.Tk()
        self.spacemap= {}  #board.space.id --> GUISpace
        self.pawns = {
            "green": {},  #pawn.id --> pawn
            "red": {},
            "blue": {},
            "yellow": {}
        }
        self.dice = []  #list of gui dice
        self.board = Board(4)

        self.gui_moves = []
        self.temp_move = GUIMove()
        self.move_state = 'pawn'  #pawn, distance
        self.done = False
        
        self.build_player_status("")
        self.draw_board(Board(4))

    def queue_has_moves(self):
        for elem in list(self.queue):
            if not list(elem):
                return False
        return True

    def start(self):
        self.root.update()
        while True:
            while self.queue.empty():
                continue
            obj = self.queue.get()
            if isinstance(obj, tuple):  #do Move
                board, dice = obj
                self.board = board
                self.update_pawns(board)
                self.update_dice(dice)
                while not self.done:
                    self.root.update()
                    continue
                self.queue.put(self.gui_moves)
                self.gui_moves = []
                self.done = False
            else: #startGame
                self.color = obj
                self.player_color_label.configure(text="Your color: "+self.color)
            self.root.update()    

    def pawn_select(self, event, pawn):
        print("you clicked on pawn "+str(pawn.id))
        if self.move_state == 'pawn':
            self.temp_move.pawn = pawn
            self.move_state = 'die'

    def die_select(self, event, val):
        if self.move_state == 'die':
            self.temp_move.distance = val
            self.append_move()

    def append_move(self):
        board_space = self.board.spacemap[self.temp_move.pawn.location]
        if isinstance(board_space, RegularSpace):
            self.gui_moves.append(MoveMain(self.temp_move.pawn, self.temp_move.pawn.location, self.temp_move.distance))
        elif isinstance(board_space, HomeSpace):
            self.gui_moves.append(MoveHome(self.temp_move.pawn, self.temp_move.pawn.location, self.temp_move.distance))
        else:
            self.gui_moves.append(EnterPiece(self.temp_move.pawn))

    def build_player_status(self, color, row=2, col=20):
        self.player_color_label = tk.Label(self.root, text='Your color: '+color)
        self.player_color_label.grid(row=row, column=col)
        self.player_status_label = tk.Label(self.root, text='Welcome to Parcheesi')
        self.player_status_label.grid(row=row+2, column=col)
        self.submit_button = tk.Button(self.root, text="SUBMIT", command= lambda: self.set_done())
        self.submit_button.grid(row=10, column=20)

    def set_done(self):
        print("setting done to True")
        self.done = True

    def draw_board(self, board, orig_row=0, orig_col=0):
        curr_space = board.spacemap[0]
        col = orig_col+8
        row = orig_row+14
        #space 0 safe space
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id, 
            bg=COLORS_D['safe'], height=2, width=8)
        curr_space = curr_space.next_space
        #four spaces under
        for i in range(4):
            row += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg=COLORS_D['neutral'], height=2, width=8)
            curr_space = curr_space.next_space
        #safe space before green home
        col += 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=2, width=8)
        #green home row
        save_curr_space = curr_space
        curr_space = curr_space.next_home
        for i in range(7):
            row -= 1
            if i == 6:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#10c900", height=2, width=8, text="HOME")
            else:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#10c900", height=2, width=8)
            curr_space = curr_space.next_space
        #four after green home row
        row += 8
        col += 1
        curr_space = save_curr_space.next_space
        for i in range(4):
            row -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=2, width=8)
            curr_space = curr_space.next_space
        #green entry safe space
        row -= 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=2, width=8)
        curr_space = curr_space.next_space
        #3 space after entry
        for i in range(3):
            row -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=2, width=8)
            curr_space = curr_space.next_space
        #3 before safe space next to red home
        row -= 1
        for i in range(3):
            col += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #safe space next to red
        col += 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=5, width=4)
        curr_space = curr_space.next_space
        #4 before red home safe
        for i in range(4):
            col += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #safe space before red home
        row -= 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=5, width=4)
        #red home row
        save_curr_space = curr_space
        curr_space = curr_space.next_home
        for i in range(7):
            col -= 1
            if i == 6:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#f90c1c", height=5, width=4, text="HOME")
            else:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#f90c1c", height=5, width=4)
            curr_space = curr_space.next_space
        #four after red home row
        col += 8
        row -= 1
        curr_space = save_curr_space.next_space
        for i in range(4):
            col -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #red entry safe space
        col -= 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=5, width=4)
        curr_space = curr_space.next_space
        #3 spaces after red entry
        for i in range(3):
            col -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #3 before safe space next to blue home
        col -= 1
        for i in range(3):
            row -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=2, width=8)
            curr_space = curr_space.next_space
        #safe space next to blue home
        row -= 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=2, width=8)
        curr_space = curr_space.next_space
        #4 before blue home safe space
        for i in range(4):
            row -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=2, width=8)
            curr_space = curr_space.next_space
        #safe space before blue home
        col -= 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=2, width=8)
        #blue home row
        save_curr_space = curr_space
        curr_space = curr_space.next_home
        for i in range(7):
            row += 1
            if i == 6:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#0c3bf9", height=2, width=8, text="HOME")
            else:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#0c3bf9", height=2, width=8)
        #four after blue home row
        row -= 8
        col -= 1
        curr_space = save_curr_space.next_space
        for i in range(4):
            row += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=2, width=8)
            curr_space = curr_space.next_space
        #blue entry safe space
        row += 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=2, width=8)
        curr_space = curr_space.next_space
        #3 spaces after blue entry
        for i in range(3):
            row += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=2, width=8)
            curr_space = curr_space.next_space
        #3 before safe space next to yellow home
        row += 1
        for i in range(3):
            col -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #safe space next to yellow home
        col -= 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=5, width=4)
        curr_space = curr_space.next_space
        #4 before yellow home safe space
        for i in range(4):
            col -= 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #safe space before yellow home
        row += 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=5, width=4)
        #yellow home row
        save_curr_space = curr_space
        curr_space = curr_space.next_home
        for i in range(7):
            col += 1
            if i == 6:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#f9e10c", height=5, width=4, text="HOME")
            else:
                self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                    bg="#f9e10c", height=5, width=4)
        #4 after yellow home row
        col -= 8
        row += 1
        curr_space = save_curr_space.next_space
        for i in range(4):
            col += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #yellow entry safe space
        col += 1
        self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
            bg="#980fd8", height=5, width=4)
        curr_space = curr_space.next_space
        #3 after yellow entry
        for i in range(3):
            col += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=5, width=4)
            curr_space = curr_space.next_space
        #3 before safe space before green home
        col += 1
        for i in range(3):
            row += 1
            self.spacemap[curr_space.id] = GUISpace(self.root, row, col, curr_space.id,
                bg="#6394ff", height=2, width=8)
            curr_space = curr_space.next_space
        ###Draw Start Spaces###
        #red start
        red_start_id = board.starts["red"].id
        self.spacemap[red_start_id] = GUISpace(self.root, 2, 12, red_start_id, 
                bg="#f90c1c", height=10, width=10, columnspan=5, rowspan=5)
        #blue start
        blue_start_id = board.starts["blue"].id
        self.spacemap[blue_start_id] = GUISpace(self.root, 2, 2, blue_start_id,
                bg="#0c3bf9", height=5, width=20, columnspan=5, rowspan=5)
        #yellow start
        yellow_start_id = board.starts["yellow"].id
        self.spacemap[yellow_start_id] = GUISpace(self.root, 12, 2, yellow_start_id,
                bg="#f9e10c", height=10, width=10, columnspan=5, rowspan=5)
        #green start
        green_start_id = board.starts["green"].id
        self.spacemap[green_start_id] = GUISpace(self.root, 12, 12, green_start_id,
                bg="#10c900", height=5, width=20, columnspan=5, rowspan=5)

        self.build_pawns(board)
    
    def build_pawns(self, board):
       for color in ["green", "red", "blue", "yellow"]:
            for p_id in range(4):
                pawn = board.pawns[color][p_id]
                pawn_loc_space = self.spacemap[pawn.location]
                gui_pawn = GUIPawn(self.root, pawn, pawn_loc_space.row, pawn_loc_space.col)
                gui_pawn.get_alignment(board.spacemap)
                gui_pawn.bind("<Button-1>", lambda e, pawn=gui_pawn.pawn: self.pawn_select(e, pawn))
                self.pawns[color][p_id] = gui_pawn

    def update_pawns(self, board):  #this pawn is a board.pawn
        for color in ["green", "red", "blue", "yellow"]:
            for pawn in board.pawns[color]:
                gui_pawn = self.pawns[color][pawn.id]
                pawn_loc_space = self.spacemap[pawn.location]
                gui_pawn.pawn = pawn
                gui_pawn.row = pawn_loc_space.row
                gui_pawn.col = pawn_loc_space.col
                gui_pawn.get_alignment(board.spacemap)

    def update_dice(self, dice_vals):
        start_row = 11
        start_col = 20
        print("in update_dice")
        print(len(self.dice))
        print(len(dice_vals))
        if len(self.dice) < len(dice_vals):
            print("building more dice")
            for i in range(len(dice_vals) - len(self.dice)):
                print("adding a GUIDie")
                guidie = GUIDie(self.root, 0, start_row+len(self.dice), start_col)
                guidie.bind("<Button-1>", lambda e, val=guidie.val: self.die_select(e, val))
                self.dice.append(guidie)
        for i in range(len(self.dice)):
            try:
                self.dice[i].val = dice_vals[i]
                self.dice[i].configure(text=str(dice_vals[i]))
                self.dice[i].grid(row=start_row+i, column=start_col)
            except IndexError:
                self.dice[i].grid_forget()

def pawn_sim(board, color, pawnid, newpos):
    """Does the equivalent of 
    pawn_to_bop1 = board.pawns[color][pawnid]
    board.starts[color].remove_pawn(pawn_to_bop1)
    board.spacemap[newpos].add_pawn(pawn_to_bop1)
    pawn_to_bop1.location = newpos"""
    pawn = board.pawns[color][pawnid]
    board.starts[color].remove_pawn(pawn)
    board.spacemap[newpos].add_pawn(pawn)
    pawn.location = newpos
    return pawn
 
if __name__ == "__main__":
    print("GUI?")
    gui = GUI(Queue())
    #gui.draw_board(Board(4))
    gui.start()
    #board = Board(4)
    #pawn_sim(board, "green", 0, 17)
    #gui.build_pawns(board)
