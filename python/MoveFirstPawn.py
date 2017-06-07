"""
Implements a client player that always tries to move
its first pawn
"""

#Global

#Local
from Board import Board
from EnterPiece import EnterPiece
from FinalSpace import FinalSpace
from HomeSpace import HomeSpace
from MoveMain import MoveMain
from MoveHome import MoveHome
from Player import Player
from RegularSpace import RegularSpace
from StartSpace import StartSpace
from RuleChecker import RuleChecker

class MoveFirstPawn(Player):
    def __init__(self):
        Player.__init__(self)
        #self.color = color
    
    def order_pawns(self, board):
        """Returns a list of pawn objects in order such that
        the first pawn is farthest on the board"""
        pawns = board.pawns[self.color]
        sorted_pawns = []
        relative_locs = {}  #dictionary mapping from mapped location to pawn object
        for pawn in pawns:
            rel_pawn_loc = board.get_relative_pos(pawn.location, self.color)
            relative_locs[rel_pawn_loc] = pawn
        for rel_loc in sorted(relative_locs.keys(), reverse=True):
            sorted_pawns.append(relative_locs[rel_loc])
        return sorted_pawns

    def doMove(self, board, dice):
        """Uses the given board and dice to decide
        on a set of moves to take"""
        rc = RuleChecker(board, dice, self.color)
        moves = []
        sorted_pawns = self.order_pawns(rc.b_final)
        while not Player.stop_move_generation(self, rc):
            sorted_pawns = self.order_pawns(rc.b_final)
            new_move = None
            for pawn in sorted_pawns:
                #print("MoveFirstPawn::doMove:  pawn loop - pawn id: "+str(pawn.id))
                pawn_space = rc.b_final.spacemap[pawn.location]
                if isinstance(pawn_space, FinalSpace):
                    continue
                elif isinstance(pawn_space, HomeSpace):
                    #print("MoveFirstPawn::doMove: mkaing a HomeMove in doMove")
                    for die in rc.tvals.get_all_dice():
                        new_move = MoveHome(pawn, pawn.location, die)
                        valid, rc = Player.check_next_move(self, rc, new_move)
                        if valid:
                            moves.append(new_move)
                            break
                        else:
                            new_move = None
                elif isinstance(pawn_space, StartSpace):
                    #print("MoveFirstPawn::doMove: making an EnterPiece in doMove")
                    new_move = EnterPiece(pawn)
                    valid, rc = Player.check_next_move(self, rc, new_move)
                    if valid:
                        #print("MoveFirstPawn::doMove: EnterPiece was valid using pawn "+str(pawn.id))
                        moves.append(new_move)
                        #print("MoveFirstPawn::doMove: length of moves: "+str(len(moves)))
                    else:
                        new_move = None
                else:  #Regular Space
                    #print("MoveFirstPawn::doMove: making a MoveMain in doMove")
                    for die in rc.tvals.get_all_dice():
                        new_move = MoveMain(pawn, pawn.location, die)
                        valid, rc = Player.check_next_move(self, rc, new_move)
                        #print("MoveFirstPawn::doMove: "+str(rc.tvals.bonus))
                        if valid:
                            moves.append(new_move)
                            break
                        else:
                            new_move = None
                if new_move != None:
                    print("MoveFirstPawn::doMove: breaking from pawn loop")
                    break
        return moves

def check(boolean, string):
    if not boolean:
        print("*** TEST FAILED *** ("+string+")")

def pawn_sim(self, board, color, pawnid, newpos):
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
    #Player chooses to enter with first move given a 5
    print("=====Player chooses to enter with first move given a 5=====")
    board = Board(4)
    dice = [5, 1]
    player = MoveFirstPawn("green")
    moves = player.doMove(board, dice)
    check(isinstance(moves[0], EnterPiece), "player's first move wasn't an EnterPiece")
    check(moves[1].start == 17 and moves[1].distance == 1, "player's second move wasn't correct: "+str(vars(moves[1])))

    #Player chooses to move the furthest ahead of two pawns twice
    """print("=====Player chooses to move the furthest ahead fo two pawns twice=====")
    board = Board(4)
    ahead_pawn = pawn_sim(board, "green", 0, 21)
    behind_pawn = pawn_sim(board, "green", 1, 18)
    dice = [2, 3]
    player = MoveFirstPawn("green")
    moves = player.doMove(board, dice)
    check(moves[0].start == 21, "player didn't choose the furthest ahead pawn")
    check(moves[1].start == 23, "player didn't choose the furthest ahead pawn OR pawn didn't move correctly")

    #player bops a pawn and takes a bonus
    print("=====Player bops a pawn and takes a bonus=====")
    board = Board(4)
    pawn_to_bop = pawn_sim(board, "yellow", 0, 21)
    bopping_pawn = pawn_sim(board, "green", 0, 20)
    dice = [1, 2]
    player = MoveFirstPawn("green")
    moves = player.doMove(board, dice)
    check(len(moves) == 3, "player didn't return 3 moves, gave "+str(len(moves)))
    check(sum([move.distance for move in moves]) == 23, "player didn't move 1 + 20 + 2")

    #player moves all four with doubles
    print("=====Player moves all four with doubles=====")
    board = Board(4)
    pawn_to_move = pawn_sim(board, "green", 0, 17)
    dice = [2, 2, 5, 5]
    player = MoveFirstPawn("green")
    moves = player.doMove(board, dice)
    check(sum([move.distance for move in moves]) == 14, "player didn't move 2 + 2 + 5 + 5")

    #player moves behind pawn because first is blocked
    print("=====player moves behind pawn because first is blocked=====")
    board = Board(4)
    blockade1 = pawn_sim(board, "yellow", 0, 23)
    blockade2 = pawn_sim(board, "yellow", 1, 23)
    ahead_pawn = pawn_sim(board, "green", 0, 21)
    behind_pawn = pawn_sim(board, "green", 1, 18)
    dice = [1, 2]
    player = MoveFirstPawn("green")
    moves = player.doMove(board, dice)
    check(moves[0].pawn.id == 0, "player didn't move the ahead pawn when it could before it was blocked")
    check(moves[1].pawn.id == 1, "player didn't move the behind pawn when the ahead pawn was blocked")"""
