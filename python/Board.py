"""
Implements the Board class
"""

#Global
import copy
import sys

#Local
from EnterPiece import EnterPiece
from FinalSpace import FinalSpace
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
        self.finishes = {}
        for i in range(len(colors)):
            self.pawns[colors[i]] = [] #list of pawns
            self.starts[colors[i]] = None #StartSpace
            self.finishes[colors[i]] = None  #end spaces
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
            #build the 6 home spaces with appropriate color
            for j in range(6):
                curr_space = HomeSpace(curr_id, colors[i])
                self.spacemap[curr_id] = curr_space
                curr_id += 1
                if j == 0:
                    last_space.next_home = curr_space
                else:
                    last_space.next_space = curr_space
                last_space = curr_space
            #build the final space
            curr_space = FinalSpace(curr_id, colors[i])
            self.spacemap[curr_id] = curr_space
            self.finishes[colors[i]] = curr_id
            curr_id += 1
            last_space.next_space = curr_space
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
            self.spacemap[new_start_space.id] = new_start_space
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
                while not isinstance(curr_space, FinalSpace):
                    homestr += " "+curr_space.color+" home space (id "+str(curr_space.id)+")----------->"
                    curr_space = curr_space.next_space
                    #if curr_space == None:
                    #    break
                #print(homestr)
                #curr_space = curr_space_save.next_space
                #homestr = ""
            elif isinstance(curr_space, SafeSpace):
                if curr_space.next_home != None:
                    homestr += "safe space points to home (id "+str(curr_space.id)+")------------>"
                    curr_space_save = curr_space
                    curr_space = curr_space.next_home
                else:
                    print("safe space (id "+str(curr_space.id)+")")
                    curr_space = curr_space.next_space
            elif isinstance(curr_space, FinalSpace):
                homestr += "final space (id "+str(curr_space.id)+")"
                print(homestr)
                curr_space = curr_space_save.next_space
                homestr = ""
            if curr_space.id == self.first_space.id:
                break
        for color in self.starts.keys():
            print(color, [p.id for p in self.starts[color].pawns], self.starts[color].id)

    def traverse(self, start, num_hops, color):  #Space
        """Takes a start id, a number of hops, and a color string"""
        home_start = self.home_starts[color]
        curr_space = self.spacemap[start]
        for i in range(start, start+num_hops):
            if curr_space.id == home_start.id:
                curr_space = curr_space.next_home  #on this color's safe space before home
            else:
                curr_space = curr_space.next_space
        return curr_space

    def get_relative_pos(self, stop_id, color):
        distance = 0
        home_start = self.home_starts[color]
        entry_space = self.starts[color]
        curr_space = entry_space
        while curr_space.id != stop_id:
            if curr_space.id == home_start.id:
                curr_space = curr_space.next_home
            else:
                curr_space = curr_space.next_space
            distance += 1
        return distance

    def id_to_space(s_id): #Space
        """Takes a space ID"""
        try:
            return self.spacemap[i]
        except KeyError:
            print("Board::id_to_space: ERROR: Pawn without valid location (not mapped to spacemap)")
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
            self.return_pawn(bopped)
            return 20
        else:
            return 0

    def regular_move(self, move):  #int (bonus)
        moving_pawn = move.pawn
        destination = self.traverse(move.start, move.distance, moving_pawn.color)
        print("Board::regular_move: performing a move from "+str(move.start)+" to "+str(destination.id)+" of distance "+str(move.distance))
        current = self.spacemap[moving_pawn.location]
        current.remove_pawn(moving_pawn)
        moving_pawn.location = destination.id
        bopped = destination.add_pawn(moving_pawn)
        if bopped != None:
            print("Board::regular_move: bopped a "+bopped.color+" pawn")
        if bopped != None:
            self.return_pawn(bopped)
            return 20
        else:
            return 0

    def home_move(self, move):  #int (bonus)
        moving_pawn = move.pawn
        destination = self.traverse(move.start, move.distance, moving_pawn.color)
        current = self.spacemap[moving_pawn.location]
        current.remove_pawn(moving_pawn)
        moving_pawn.location = destination.id
        destination.add_pawn(moving_pawn)
        if destination.next_space == None:
            return 10
        else:
            return 0

    def return_pawn(self, bopped):
        start_space = self.starts[bopped.color]
        bopped.location = start_space.id
        start_space.add_pawn(bopped)
       
    def deepcopy(self):
        """self.first_space = None  #Space
        self.spacemap = {}  #maps integer to space
        self.entry_spaces = {}  #maps str(color) to space
        self.home_starts = {}  #maps str color to space (safe spaces before home rows)
        colors = ["green", "red", "blue", "yellow"]
        self.pawns = {}
        self.starts = {}
        for i in range(len(colors)):
            self.pawns[colors[i]] = [] #list of pawns
            self.starts[colors[i]] = None #StartSpace"""
        new_board = Board(4)

    def order_pawns(self, color):
        """Returns a list of pawn objects in order such that
        the first pawn is farthest on the board"""
        pawns = self.pawns[color]
        sorted_pawns = []
        relative_locs = {}  #dictionary mapping from mapped location to pawn object
        for pawn in pawns:
            rel_pawn_loc = self.get_relative_pos(pawn.location, color)
            relative_locs[rel_pawn_loc] = pawn
        for rel_loc in sorted(relative_locs.keys(), reverse=True):
            sorted_pawns.append(relative_locs[rel_loc])
        return sorted_pawns

    def all_out(self, color):
        """Returns True if all pawns for a color are not in start"""
        color_start_id = self.starts[color]
        for pawn in self.pawns[color]:
            if pawn.location == color_start_id:
                return False
        return True

    def categorize_pawns(self):
        start_pawns = []
        home_row_pawns = []
        home_pawns = []
        main_pawns = []

        all_pawns = []
        for color in ["red", "green", "blue", "yellow"]:
            all_pawns += self.pawns[color]
        for pawn in all_pawns:
            if isinstance(self.spacemap[pawn.location], StartSpace):
                start_pawns.append(pawn)
            elif isinstance(self.spacemap[pawn.location], HomeSpace):
                home_row_pawns.append(pawn)
            elif isinstance(self.spacemap[pawn.location], FinalSpace):
                home_pawns.append(pawn)
            else:
                main_pawns.append(pawn)
        return start_pawns, home_row_pawns, home_pawns, main_pawns

if __name__ == "__main__":
    print("The Board class")
    #b = Board(4)
    #b_new = copy.deepcopy(b)
    #move = EnterPiece(b_new.pawns["green"][0])
    #b_new.make_move(move)
    #print(b.pawns["green"][0].location)
    #print(b_new.pawns["green"][0].location)
    #s = SafeSpace(0)
    #print(isinstance(s, SafeSpace))
    #print(isinstance(s, RegularSpace))
    #print(isinstance(s, HomeSpace))

    b = Board(4)
    #print(b.get_relative_pos(17, "green") == 1)
    #print(b.get_relative_pos(19, "green") == 3)
    b.visualizer()
