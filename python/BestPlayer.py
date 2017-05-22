"""
Our best player for competition
"""

#Global

#Local
from Board import Board
from EnterPiece import EnterPiece
from FinalSpace import FinalSpace
from HomeSpace import HomeSpace
from MoveHome import MoveHome
from MoveMain import MoveMain
from Player import Player
from RuleChecker import RuleChecker

class BestPlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def doMove(self, board, dice):
        rc = RuleChecker(board, dice, self.color)
        moves = []
        #sorted_pawns = self.order_pawns(rc.b_final, reverse=False)
        while not Player.stop_move_generation(self, rc):
            sorted_pawns = self.order_pawns(rc.b_final, reverse=False)
            ##check move home
            move, rc = self.can_move_home(sorted_pawns, rc)
            if move != None:
                print("BestPlayer::doMove: adding a move to home ("+str(vars(move))+")")
                print("BestPlayer::doMove: current dice: "+str(rc.tvals.get_all_dice()))
                moves.append(move)
                continue
            ##check bop
            move, rc = self.can_bop(sorted_pawns, rc)
            if move != None:
                print("BestPlayer::doMove: adding a bopping move ("+str(vars(move))+")")
                print("BestPlayer::doMove: current dice: "+str(rc.tvals.get_all_dice()))
                moves.append(move)
                continue
            ##check enter
            move, rc = self.can_enter(sorted_pawns, rc)
            if move != None:
                print("BestPlayer::doMove: adding an enter move ("+str(vars(move))+")")
                print("BestPlayer::doMove: current dice: "+str(rc.tvals.get_all_dice()))
                moves.append(move)
                continue
            ##check regular move
            move, rc = self.regular_move(sorted_pawns, rc)
            if move != None:
                print("BestPlayer::doMove: adding a regular move ("+str(vars(move))+")")
                print("BestPlayer::doMove: current dice: "+str(rc.tvals.get_all_dice()))
                moves.append(move)
                continue
            #sorted_pawns = self.order_pawns(rc.b_final)
        return moves

    def can_move_home(self, pawns, rc):
        for pawn in pawns:
            for die in rc.tvals.get_all_dice():
                home_move = MoveHome(pawn, pawn.location, die)
                try:
                    if isinstance(rc.b_final.traverse(pawn.location, die, self.color), FinalSpace):
                        valid, rc = Player.check_next_move(self, rc, home_move)
                        if valid:
                            print("BestPlayer::can_move_home: dice have valid move home: "+str(rc.tvals.get_all_dice()))
                            return home_move, rc
                except AttributeError:
                    continue
        return None, rc

    def can_bop(self, pawns, rc):
        print("BestPlayer::can_bop: going to check these dice: "+str(rc.tvals.get_all_dice()))
        for pawn in pawns:
            for die in rc.tvals.get_all_dice():
                bop_move = MoveMain(pawn, pawn.location, die)
                print("BestPlayer::can_bop: Checking this move: "+str(vars(bop_move)))
                try:
                    dest = rc.b_final.traverse(pawn.location, die, self.color)
                except AttributeError:
                    continue
                if dest == None:
                    continue
                if dest.pawn2 == None and (dest.pawn1 != None and dest.pawn1.color != self.color):
                    valid, rc = Player.check_next_move(self, rc, bop_move)
                    if valid:
                        return bop_move, rc
        return None, rc

    def can_enter(self, pawns, rc):
        for pawn in pawns:
            if pawn.location == rc.b_final.starts[self.color].id:
                enter_move = EnterPiece(pawn)
                valid, rc = Player.check_next_move(self, rc, enter_move)
                if valid:
                    return enter_move, rc
        return None, rc

    def regular_move(self, pawns, rc):
        sorted_dice = sorted(rc.tvals.get_all_dice(), reverse=True)
        for pawn in pawns:
            for die in sorted_dice:
                if isinstance(rc.b_final.spacemap[pawn.location], HomeSpace):
                    move = MoveHome(pawn, pawn.location, die)
                else:
                    move = MoveMain(pawn, pawn.location, die)
                valid, rc = Player.check_next_move(self, rc, move)
                if valid:
                    return move, rc
        return None, rc

if __name__ == "__main__":
    print("the best player")
