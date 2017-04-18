"""
Implements the Board class
"""

#Global
import copy
import sys

#Local
from EnterPiece import EnterPiece
from HomeSpace import HomeSpace
from MoveHome import MoveHome
from MoveMain import MoveMain
from Pawn import Pawn
from RegularSpace import RegularSpace
from SafeSpace import SafeSpace
from StartSpace import StartSpace

class Board:
    def __init__(self, num_players):
        num_pawns = 4 #num of pawns per player
        self.first_space = None  #Space
        self.spacemap = {}  #maps integer to space
        self.entry_spaces = {}  #maps str(color) to space
        self.home_starts = {}  #maps str color to space (safe spaces before home rows)
        colors = ["green", "red", "blue", "yellow"]
        self.pawns = {}
        self.starts = {}
        for i in range(len(colors)):
            self.pawns[colors[i]] = [] #list of pawns
            self.starts[colors[i]] = None #StartSpace
        curr_id = 0
        last_space = None
        curr_space = None

        #build the board
        for i in range(4):
            #first safe space
            curr_space = SafeSpace(curr_id)
            self.spacemap[curr_id] = curr_space
            curr_id += 1
            if i == 0:
                self.first_space = curr_space
            else:
                last_space.next_space = curr_space
            last_space = curr_space
            #four regular spaces after safe space
            for j in range(4):
                curr_space = RegularSpace(curr_id)
                self.spacemap[curr_id] = curr_space
                curr_id += 1
                last_space.next_space = curr_space
                last_space = curr_space
            #safe space that connects to home
            curr_space = SafeSpace(curr_id)
            self.spacemap[curr_id] = curr_space
            curr_id += 1
            self.home_starts[colors[i]] = curr_space
            last_space.next_space = curr_space
            last_space = curr_space
            #save the safe space that connects to home
            safe_space_save = curr_space
            #build the 7 home spaces with appropriate color
            for j in range(7):
                curr_space = HomeSpace(curr_id, colors[i])
                self.spacemap[curr_id] = curr_space
                curr_id += 1
                if j == 0:
                    last_space.next_home = curr_space
                else:
                    last_space.next_space = curr_space
                last_space = curr_space
            #retrieve saved space
            last_space = safe_space_save  
            #build four regular spaces up to entry point
            for j in range(4):
                curr_space = RegularSpace(curr_id)
                self.spacemap[curr_id] = curr_space
                curr_id += 1
                last_space.next_space = curr_space
                last_space = curr_space
            #build the entry point safe space
            curr_space = SafeSpace(curr_id)
            self.spacemap[curr_id] = curr_space
            curr_id += 1
            self.entry_spaces[colors[i]] = curr_space
            last_space.next_space = curr_space
            last_space = curr_space
            #make 6 regular spaces
            for j in range(6):
                curr_space = RegularSpace(curr_id)
                self.spacemap[curr_id] = curr_space
                curr_id += 1
                last_space.next_space = curr_space
                last_space = curr_space
        last_space.next_space = self.first_space

        #build the list of pawns, build start space, set its next space to entry point
        for i in range(num_players):
            for j in range(num_pawns):
                np = Pawn(j, colors[i], -1)
                self.pawns[colors[i]].append(np)
            curr_color = colors[i]
            new_start_space = StartSpace(curr_id, self.pawns[curr_color], curr_color)
            for j in range(num_pawns):
                self.pawns[curr_color][j].location = curr_id
            curr_id += 1
            new_start_space.next_space = self.entry_spaces[curr_color]
            self.starts[curr_color] = new_start_space
    
    def visualizer(self):
        curr_space = self.first_space
        curr_space_save = None
        homestr = ""
        while True:
            if isinstance(curr_space, RegularSpace):
                print("regular space (id "+str(curr_space.id)+")")
                curr_space = curr_space.next_space
            elif isinstance(curr_space, HomeSpace):
                while True:
                    homestr += " "+curr_space.color+" home space (id "+str(curr_space.id)+")----------->"
                    curr_space = curr_space.next_space
                    if curr_space == None:
                        break
                print(homestr)
                curr_space = curr_space_save.next_space
                homestr = ""
            elif isinstance(curr_space, SafeSpace):
                if curr_space.next_home != None:
                    homestr += "safe space points to home (id "+str(curr_space.id)+")------------>"
                    curr_space_save = curr_space
                    curr_space = curr_space.next_home
                else:
                    print("safe space (id "+str(curr_space.id)+")")
                    curr_space = curr_space.next_space
            if curr_space.id == self.first_space.id:
                break
        for color in self.starts.keys():
            print(color, [p.id for p in self.starts[color].pawns], self.starts[color].id)

    def traverse(start, num_hops, color):  #Space
        """Takes a start id, a number of hops, and a color string"""
        home_start = self.home_starts[color]
        curr_space = self.spacemap[start]
        for i in range(start, start+num_hops+1):
            if curr_space.id == home_start.id:
                curr_space = curr_space.next_home  #on this color's safe space before home
            else:
                curr_space = curr_space.next_space
        return curr_space

    def id_to_space(s_id): #Space
        """Takes a space ID"""
        try:
            return self.spacemap[i]
        except KeyError:
            print("ERROR: Pawn without valid location (not mapped to spacemap)")
            sys.exit(1)

    def make_move(self, move): #int (bonus)
        bonus = 0
        if isinstance(move, EnterPiece):
            bonus = self.enter_piece(move)
        elif isinstance(move, MoveMain):
            bonus = self.regular_move(move)
        elif isinstance(move, MoveHome):
            bonus = self.home_move(move)
        return bonus

    def enter_piece(self, move):  #int (bonus)
        entering_pawn = move.pawn
        entering_color = entering_pawn.color
        entry_space = self.entry_spaces[entering_color]
        entering_start_space = self.starts[entering_color]
        entering_start_space.remove_pawn(entering_pawn)
        bopped = entry_space.add_pawn(entering_pawn)
        entering_pawn.location = entry_space.id
        if bopped != None:
            return_pawn(bopped)
            return 10
        else:
            return 0

    def regular_move(self, move):  #int (bonus)
        moving_pawn = move.pawn
        destination = self.traverse(m.start, m.distance, moving_pawn.color)
        current = self.spacemap[moving_pawn.location]
        current.remove_pawn(moving_pawn)
        moving_pawn.location = destination.id
        bopped = destination.add_pawn(moving_pawn)
        if bopped != None:
            return_pawn(bopped)
            return 10
        else:
            return 0

    def home_move(self, move):  #int (bonus)
        moving_pawn = move.pawn
        destination = self.traverse(m.start, m.distance, moving_pawn.color)
        current = self.spacemap[moving_pawn.location]
        current.remove_pawn(moving_pawn)
        moving_pawn.location = destination.id
        destination.add_pawn(moving_pawn)
        if destination.next_space == None:
            return 20
        else:
            return 0

    def return_pawn(bopped):
        start_space = self.starts[bopped.color]
        bopped.location = start_space.id
        start_space.add_pawn(bopped)

if __name__ == "__main__":
    print("The Board class")
    b = Board(4)
    b.visualizer()
    
    #s = SafeSpace(0)
    #print(isinstance(s, SafeSpace))
    #print(isinstance(s, RegularSpace))
    #print(isinstance(s, HomeSpace))
