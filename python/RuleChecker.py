"""
Implements the RuleChecker class
"""

#Global
import copy

#Local
from Board import Board
from EnterPiece import EnterPiece
from HomeSpace import HomeSpace
from MoveHome import MoveHome
from MoveMain import MoveMain
from RegularSpace import RegularSpace
from SafeSpace import SafeSpace
from StartSpace import StartSpace
from TurnValues import TurnValues

class RuleChecker:
    def __init__(self, board, dice):
        """Board, Moves, dice (int list)"""
        self.b_start = board
        self.b_final = copy.deepcopy(board)
        self.dice = dice
        self.tvals = TurnValues(dice)
        self.pawnmap = self.build_pawnmap()
                
    def build_pawnmap(self):
        pawnmap = {}
        for color in ["green", "red", "blue", "yellow"]:
            pawnmap[color] = {}
            for pawn, i in zip(self.b_start.pawns[color], range(4)):
                pawnmap[color]["pawn"+str(i)] = self.b_final.pawns[color][i]
        return pawnmap
    
    def map_pawn(self, pawn):
        """Assumes pawn is from original board, returns b_final's equivalent pawn"""
        return self.pawnmap[pawn.color]["pawn"+str(pawn.id)]
        
    def single_move_check(self, move, is_bonus_move=False): #boolean
        move.pawn = self.map_pawn(move.pawn)
        if isinstance(move, EnterPiece): 
            if self.valid_enter_dice(move):
                bonus = self.b_final.make_move(move)
                return True, bonus
            else:
                return False, 0
        else:
            if (not self.valid_pawn_to_move(move)) or (not is_bonus_move and not self.valid_distance(move)):
                print("no valid pawn to move or not valid distance")
                return False, 0
            elif self.blockade_in_path(move):
                print("blockade")
                return False, 0
            elif isinstance(move, MoveMain) and self.safe_space_taken(move):
                print("pawn in safe space")
                return False, 0
            elif isinstance(move, MoveHome) and not self.can_go_home(move):
                print("can't go home")
                return False, 0
        bonus = self.b_final.make_move(move)
        return True, bonus

    def valid_pawn_to_move(self, move):
        #check if move.pawn is on move.start
        return move.pawn == self.b_final.spacemap[move.start].pawn1 or move.pawn == self.b_final.spacemap[move.start].pawn2
    
    def valid_enter_dice(self, move):  #boolean
        entry_space = self.b_final.entry_spaces[move.pawn.color]
        found_pawn = False
        for pawn in self.b_final.starts[move.pawn.color].pawns:
            if pawn == move.pawn:
                found_pawn = True
                break
        if not found_pawn:
            print("no pawns to move")
            return False
        if entry_space.has_blockade():
            return False
        elif self.tvals.die1 == 5:
            self.tvals.die1 = -1
            return True
        elif self.tvals.die2 == 5:
            self.tvals.die2 = -1
            return True
        elif self.tvals.die3 == 5:
            self.tvals.die3 = -1
            return True
        elif self.tvals.die4 == 5:
            self.tvals.die4 = -1
            return True
        elif self.tvals.die1 + self.tvals.die2 == 5:
            self.tvals.die1 = -1
            self.tvals.die2 = -1
            return True
        print("not valid entry dice")
        return False

    def valid_distance(self, move): #boolean
        if move.distance == self.tvals.die1:
            self.tvals.die1 = -1
            return True
        elif move.distance == self.tvals.die2:
            self.tvals.die2 = -1
            return True
        elif self.tvals.doubles:
            if move.distance == self.tvals.die3:
                self.tvals.die3 = -1
                return True
            elif move.distance == self.tvals.die4:
                self.tvals.die4 = -1
                return True
        else:
            print("not valid distance")
            return False

    def blockade_in_path(self, move):
        for i in range(move.start+1, move.start+move.distance+1):
            curr_space = self.b_final.spacemap[i+1]
            if curr_space.has_blockade():
                return True
        return False

    def safe_space_taken(self, move):
        next_space = self.b_final.traverse(move.start, move.distance, move.pawn.color)
        return isinstance(next_space, SafeSpace) and not self.space_available(move)

    def space_available(self, move):
        next_space = self.b_final.traverse(move.start, move.distance, move.pawn.color)
        pawns = next_space.get_pawns()
        pawn1 = pawns["pawn1"]
        pawn2 = pawns["pawn2"]
        if pawn1 == None:
            return True
        elif pawn2 == None and pawn1.color == move.pawn.color:
            return True
        else:
            return False

    def can_go_home(self, move):
        try:
            next_space = self.b_final.traverse(move.start, move.distance, move.pawn.color)
            return True
        except AttributeError:
            return False

    def multi_move_check(self, moves):
        if not self.all_dice_used():
            if self.more_valid_moves(moves):
                return False
        elif self.duplicate_blockades():
            return False
        else:
            return True

    def all_dice_used(self):
        return self.tvals.die1 == -1 and self.tvals.die2 == -1 and self.tvals.die3 == -1 and self.tvals.die4 == -1

    def more_valid_moves(self, moves):
        color = moves[0].pawn.color
        for pawn in self.b_final.starts[color].pawns:
            if self.valid_enter_dice(EnterPiece(pawn)):
                return True
            else:
                for dice in [self.tvals.die1, self.tvals.die2, self.tvals.die3, self.tvals.die4]:
                    if dice != -1:
                        for pawn in self.b_final.pawns[color]:
                            if isinstance(self.b_final.spacemap[pawn.location], HomeSpace):
                                if can_go_home(MoveHome(pawn, pawn.location, dice)):
                                    return True
                                if isinstance(self.b_final.spacemap[pawn.location], RegularSpace):
                                    if valid_distance(MoveMain(pawn, pawn.location, dice)):
                                        return True
        return False

    def duplicate_blockades(self):
        """orig_locs = [self.b_start.spacemap[pawn.location] for pawn in self.b_start.pawns["green"]+self.b_start.pawns["red"]+self.b_start.pawns["yellow"]+self.b_start.pawns["blue"]]
        final_locs =[self.b_final.spacemap[pawn.location] for pawn in self.b_final.pawns["green"]+self.b_final.pawns["red"]+self.b_final.pawns["yellow"]+self.b_final.pawns["blue"]]
        orig_pawns = self.b_start.pawns["green"]+self.b_start.pawns["red"]+self.b_start.pawns["yellow"]+self.b_start.pawns["blue"]
        final_pawns = self.b_final.pawns["green"]+self.b_final.pawns["red"]+self.b_final.pawns["yellow"]+self.b_final.pawns["blue"]
        for orig_pawn in orig_pawns:
            for final_pawn in final_pawns:
                orig_loc = self.b_final.spacemap[orig_pawn.location]
                final_loc = self.b_final.spacemap[final_pawn.location]
                if not isinstance(orig_loc, StartSpace) and not isinstance(final_loc, StartSpace):
                    if orig_loc.has_blockade():
                        if final_loc.has_blockade():
                            orig_loc_pawns = orig_loc.get_pawns()
                            final_loc_pawns = final_loc.get_pawns()
                            orig_pawn_1 = orig_loc_pawns["pawn1"]
                            orig_pawn_2 = orig_loc_pawns["pawn2"]
                            final_pawn_1 = final_loc_pawns["pawn1"]
                            final_pawn_2 = final_loc_pawns["pawn2"]
                            if (orig_pawn_1 == final_pawn_1 or orig_pawn_1 == final_pawn_2) and (orig_pawn_2 == final_pawn_1 or orig_pawn_2 == final_pawn_2):
                                return True
        return False"""
        final_pawns = self.b_final.pawns["green"]+self.b_final.pawns["red"]+self.b_final.pawns["yellow"]+self.b_final.pawns["blue"]
        pawn_to_follow = self.b_final.pawns["blue"][1]
        for pawn in final_pawns:
            if pawn == pawn_to_follow:
                print("pawn location: "+str(pawn.location))
            pawn_space = self.b_final.spacemap[pawn.location]
            if isinstance(pawn_space, StartSpace):
                continue
            if pawn_space.has_blockade():
                if pawn == pawn_to_follow:
                    print(str(pawn.location)+" final blockade")
                original_pawn = self.b_start.pawns[pawn.color][pawn.id]
                original_space = self.b_start.spacemap[original_pawn.location]
                print("original pawn location: "+str(original_pawn.location))
                if isinstance(original_space, StartSpace):
                    continue
                if original_space.has_blockade():
                    partner = self.get_other_pawn(pawn, pawn_space)
                    print("partner color "+partner.color+", parnter id: "+str(partner.id))
                    original_partner = self.get_other_pawn(original_pawn, original_space)
                    print("original partner color "+original_partner.color+", original parnter id: "+str(original_partner.id)) 
                    if partner == original_partner:
                        print("FOUND A DUPLICATE BLOCKADE")
                        return True
        print("no duplicate blockades")
        return False
    
    def get_other_pawn(self, pawn, space):
        pawns = space.get_pawns()
        if pawn == pawns["pawn1"]:
            return pawns["pawn2"]
        elif pawn == pawns["pawn2"]:
            return pawns["pawn1"]    

if __name__ == "__main__":
    print("The Rule Checker")
    """board = Board(4)
    dice = [4, 5]
    rc = RuleChecker(board, dice)
    print(vars(rc.tvals))
    move1 = EnterPiece(board.pawns['green'][0])
    move2 = EnterPiece(board.pawns['green'][1])
    print(rc.single_move_check(move1))
    print(vars(rc.tvals))
    print(rc.single_move_check(move2))
    print(vars(rc.tvals))"""
    
    b = Board(4)
    move = EnterPiece(b.pawns["green"][0])
    rc = RuleChecker(b, [5, 5])
    #move = EnterPiece(rc.b_final.pawns["green"][0])
    rc.single_move_check(move)
    print("spaces")
    print(b.spacemap[17].pawn1)
    print(rc.b_final.spacemap[17].pawn1)
    print("pawn locations")
    print(b.pawns["green"][0].location)
    print(rc.b_final.pawns["green"][0].location)
    print("pawns in entry spaces")
    print(len(b.starts["green"].pawns))
    print(len(rc.b_final.starts["green"].pawns))
