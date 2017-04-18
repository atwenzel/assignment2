"""
Testing modules
"""

#Global

#Local
from Board import Board
from CPlayer import CPlayer
from EnterPiece import EnterPiece
from RuleChecker import RuleChecker
from SPlayer import SPlayer

class Tester:
    def __init__(self):
        self.enter_tests()

    def check(self, boolean, string):
        if not boolean:
            print("*** TEST FAILED *** ("+string+")")

    def enter_tests(self):
        #enter with 1, 4
        board = Board(4)
        rc = RuleChecker(board, [1, 4])
        pawn_to_move = board.pawns["green"][0]
        #print(pawn_to_move.id)
        move = EnterPiece(pawn_to_move)
        valid, bonus = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        #print(moved_pawn.id)
        self.check(valid, "1, 4 failed as invalid")
        self.check(bonus == 0, "1, 4 bonus wasn't 0")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "1, 4 pawn location didn't change")
        #print(rc.b_final.pawns["green"][0].id)
        #print(moved_pawn.location, rc.b_final.entry_spaces["green"].id)
        self.check(rc.b_final.entry_spaces["green"].pawn1 == moved_pawn, "1, 4 pawn not moved to entry space")
        #print(rc.b_final.entry_spaces["green"].pawn1.id, moved_pawn.id)
        #for pawn in board.pawns["green"]:
        #    print(vars(pawn))
        #print("")
        #for pawn in rc.b_start.pawns["green"]:
        #    print(vars(pawn))

        ##enter with 2, 3
        board = Board(4)
        rc = RuleChecker(board, [2, 3])
        pawn_to_move = board.pawns["green"][0]
        move = EnterPiece(pawn_to_move)
        valid, bonus = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "2, 3 failed as invalid")
        self.check(bonus == 0, "2, 3 bonus wasn't 0")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "2, 3 pawn location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn1 == moved_pawn, "2, 3 pawn not moved to entry space")
    
        ##cannot enter witha non-5 roll
        board = Board(4)
        rc = RuleChecker(board, [1, 2])
        pawn_to_move = board.pawns["green"][0]
        move = EnterPiece(pawn_to_move)
        valid, bonus = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(not valid, "1, 2 was allowed to move")
        self.check(bonus == 0, "1, 2 bonus wasn't 0")
        self.check(moved_pawn.location != rc.b_final.entry_spaces["green"].id, "1, 2 pawn location changed")
        self.check(rc.b_final.entry_spaces["green"].pawn1 != moved_pawn, "1, 2 pawn moved to entry space")
     
        ##enter two pieces with double 5's
        board = Board(4)
        rc = RuleChecker(board, [5, 5])
        pawn_to_move = board.pawns["green"][0]
        move = EnterPiece(pawn_to_move)
        valid, bonus = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "5, 5 move 1 failed as invalid")
        self.check(bonus == 0, "5, 5 move 1 bonus wasn't 0")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "5, 5 pawn 1 location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn1 == moved_pawn, "5, 5 pawn 1 not moved to entry space")
        pawn_to_move = board.pawns["green"][1]
        move = EnterPiece(pawn_to_move)
        valid, bonus = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][1]
        self.check(valid, "5, 5 move 2 failed as invalid")
        self.check(bonus == 0, "5, 5 move 2 bonus wasn't 0")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "5, 5 pawn 2 location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn1 == moved_pawn, "5, 5 pawn 2 not moved to entry space")

    def basic_tests(self):
        ##moving a piece
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[18].add_pawn(pawn_to_move)
        pawn_to_move.location = 18
        rc = RuleChecker(board, [2, 3])
        move = MoveMain(pawn_to_move, 18, 2)
        valid, bonus = rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(bonus == 0, "moving a piece bonus wasn't 0")
        self.check(moved_pawn.location == 20, "moving a piece pawn isn't on 20")
        self.check(rc.b_final.spacemap[20].pawn1 == moved_pawn, "moving a piece pawn not location 20")
 
        ##moving into home row
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[5].add_pawn(pawn_to_move)
        pawn_to_move.location = 5
        rc = RuleChecker(board, [1, 3])
        move = MoveMain(pawn_to_move, 5, 1)
        valid, bonus = rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(bonus == 0, "moving a piece bonus wasn't 0")
        self.check(moved_pawn.location == 6, "moving into home row pawn isn't on 6")
        self.check(rc.b_final.spacemap[6].pawn1 == moved_pawn, "moving into home row  pawn not location 6")
    
        ##moving on home row
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[6].add_pawn(pawn_to_move)
        pawn_to_move.location = 6
        rc = RuleChecker(board, [2, 3])
        move = MoveMain(pawn_to_move, 6, 2)
        valid, bonus = rc.single_move_check(move)
        self.check(valid, "moving on a home row failed as invalid")
        self.check(bonus == 0, "moving a piece bonus wasn't 0")
        self.check(moved_pawn.location == 8, "moving on a home row location not 8")
        self.check(rc.b_final.spacemap[8].pawn1 == moved_pawn, "moving on a home row pawn not location 8")

        ##moving to home
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[11].add_pawn(pawn_to_move)
        pawn_to_move.location = 11
        rc = RuleChecker(board, [2, 3])
        move = MoveHome(pawn_to_move, 11, 2)
        valid, bonus = rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(bonus == 20, "moving to home bonus wasn't 20")
        self.check(moved_pawn.location == 13, "movingt to home location not 13")
        self.check(rc.b_final.spacemap[13].pawn1 == moved_pawn, "moving a piece pawn not location 13")
 
        ##cannot move if no piece present
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        rc = RuleChecker(board, [2, 3])
        move = MoveMain(pawn_to_move, 18, 2)
        valid, bonus = rc.single_move_check(move)
        self.check(not valid, "cannot move if no piece - move was valid")
        self.check(bonus == 0, "moving a piece bonus wasn't 0")

    def bopping(self):
        ## bopping a piece and getting a bonus
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[18].add_pawn(pawn_to_move)
        pawn_to_move.location = 18
        second_pawn = board.pawns["red"][0]
        board.starts["red"].remove_pawn(second_pawn)
        board.spacemap[17].add_pawn(second_pawn)
        second_pawn.location = 17
        move = MoveMain(second_pawn, 17, 1)
        rc = RuleChecker(board, [1, 3])
        valid, bonus = rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(bonus == 10, "bopping - bonus wasn't 10")
        self.check(pawn_to_move.location == rc.b_final.starts["green"].id, "bopped pawn wasn't sent home")
        self.check(rc.b_final.spacemap[18].pawn1 == second_pawn, "bopping pawn didn't move to space 18")
        self.check(second_pawn.location == 18, "seocnd pawn didn't move to 18")

        ##enter a piece and bop on safety
        board = Board(4)
        second_pawn = board.pawns["red"][0]
        board.starts["red"].remove_pawn(second_pawn)
        board.spacemap[17].add_pawn(second_pawn)
        second_pawn.location = 17
        piece_to_enter = board.pawns["green"][0]
        move = EnterPiece(piece_to_enter)
        rc = RuleChecker(board, [1, 5])
        valid, bonus = rc.single_move_check(move)
        self.check(valid, "bop on enter failed as invalid")
        self.check(bonus == 10, "bopping - bonus wasn't 10")
        
        ##bopping on a safety
        board = Board(4)
        pawn_to_bop = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(pawn_to_bop)
        board.spacemap[5].add_pawn(pawn_to_bop)
        pawn_to_bop.location = 5
        second_pawn = board.pawns["red"][0]
        board.starts["red"].remove_pawn(second_pawn)
        board.spacemap[4].add_pawn(second_pawn)
        second_pawn.location = 4
        move = MoveMain(second_pawn, 4, 1)
        rc = RuleChecker(board, [1, 3])
        valid, bonus = rc.single_move_check(move)
        self.check(not valid, "invalid bopping was valid")
        self.check(bonus == 0, "invalid bopping - bonus wasn't 0")

        ##bop two pieces       
        board = Board(4)

        pawn_to_bop1 = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(pawn_to_bop1)
        board.spacemap[4].add_pawn(pawn_to_bop1)
        pawn_to_bop1.location = 4

        pawn_to_bop2 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(pawn_to_bop2)
        board.spacemap[14].add_pawn(pawn_to_bop2)
        pawn_to_bop2.location = 14

        bopping_pawn = board.pawns["blue"][0]
        board.starts["blue"].remove_pawn(bopping_pawn)
        board.spacemap[3].add_pawn(bopping_pawn)
        pawn_to_bop2.location = 3
    
        moves = [
            MoveMain(bopping_pawn, 3, 1),
            MoveMain(bopping_pawn, 4, 3)]
        cplayer = CPlayer("blue", moves)
        splayer = SPlayer(cplayer)
        splayer.doMove(board, [1, 3])
        
        yellow_start = board.starts["yellow"]
        self.check(pawn_to_bop1.location == yellow_start.id, "multiple bop - pawns weren't bopped")

        ##cannot bop twice and move blockade together by 20
        board = Board(4)

        pawn_to_bop1 = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(pawn_to_bop1)
        board.spacemap[4].add_pawn(pawn_to_bop1)
        pawn_to_bop1.location = 4

        pawn_to_bop2 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(pawn_to_bop2)
        board.spacemap[14].add_pawn(pawn_to_bop2)
        pawn_to_bop2.location = 14

        bopping_pawn = board.pawns["blue"][0]
        board.starts["blue"].remove_pawn(bopping_pawn)
        board.spacemap[3].add_pawn(bopping_pawn)
        bopping_pawn.location = 3
        
        block_pawn1 = board.pawns["blue"][1]
        board.starts["blue"].remove_pawn(block_pawn1)
        board.spacemap[18].add_pawn(block_pawn1)
        block_pawn1.location = 18
 
        block_pawn2 = board.pawns["blue"][2]
        board.starts["blue"].remove_pawn(block_pawn2)
        board.spacemap[18].add_pawn(block_pawn2)
        block_pawn2.location = 18
 
    
        moves = [
            MoveMain(bopping_pawn, 3, 1),
            MoveMain(bopping_pawn, 4, 3)]
        cplayer = CPlayer("blue", moves)
        splayer = SPlayer(cplayer)
        splayer.doMove(board, [1, 3])
        
        
        self.check(pawn_to_bop1.location == 18, "multiple bop - blockade was moved together")
 
        ##cannot enter home and then move a blockade together by 10
        board = Board(4)

        pawn_to_bop1 = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_bop1)
        board.spacemap[9].add_pawn(pawn_to_bop1)
        pawn_to_bop1.location = 9

        pawn_to_bop2 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(pawn_to_bop2)
        board.spacemap[10].add_pawn(pawn_to_bop2)
        pawn_to_bop2.location = 10
       
        block_pawn1 = board.pawns["green"][2]
        board.starts["green"].remove_pawn(block_pawn1)
        board.spacemap[18].add_pawn(block_pawn1)
        block_pawn1.location = 18
 
        block_pawn2 = board.pawns["green"][3]
        board.starts["green"].remove_pawn(block_pawn2)
        board.spacemap[18].add_pawn(block_pawn2)
        block_pawn2.location = 18
 
    
        moves = [
            MoveHome(bopping_pawn, 9, 4),
            MoveHome(bopping_pawn, 10, 3)]
        cplayer = CPlayer("green", moves)
        splayer = SPlayer(cplayer)
        splayer.doMove(board, [4, 3])
        
        
        self.check(pawn_to_bop1.location == 18, "multiple bop - blockade was moved together")
  
    def blockade(self):
        ##cannot enter with a blockade on the entry point
        board = Board(4)

        block_pawn1 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[17].add_pawn(block_pawn1)
        block_pawn1.location = 17
 
        block_pawn2 = board.pawns["yellow"][3]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[17].add_pawn(block_pawn2)
        block_pawn2.location = 17
 
        pawn_to_enter = board.pawns["green"][0]
        move = EnterPiece(pawn_to_enter)

        rc = RuleChecker(board, [5, 1])

        valid, bonus = rc.single_move_checker(move)
        
        self.check(not valid, "invalid enter onto a blockade is valid")
        self.check(bonus==0, "bonus for enter onto a blockade isn't 0")

        ##can form a blockade but cannot add a third piece
        board = Board(4)
    
        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        pawn_to_add = board.pawns["yellow"][3]
        board.starts["yellow"].remove_pawn(pawn_to_add)
        board.spacemap[15].add_pawn(pawn_to_add)
        block_pawn2.location = 15

        move = MoveMain(pawn_to_add, 15, 1)
        
        rc = RuleChecker(board, [1, 2])
        valid, bonus = rc.single_move_checker(move)

        self.check(not valid, "invalid move onto blockade is valid")
        self.check(bonus==0, "bonus for move into blockade isn't 0")

        ##cannot move directly onto opponents blockade
        board = Board(4)
    
        block_pawn1 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["green"][2]
        board.starts["green"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        pawn_to_add = board.pawns["yellow"][3]
        board.starts["yellow"].remove_pawn(pawn_to_add)
        board.spacemap[15].add_pawn(pawn_to_add)
        block_pawn2.location = 15

        move = MoveMain(pawn_to_add, 15, 1)
        
        rc = RuleChecker(board, [1, 2])
        valid, bonus = rc.single_move_checker(move)

        self.check(not valid, "invalid move onto opponent blockade is valid")
        self.check(bonus==0, "bonus for move into opponent blockade isn't 0")
  
        ##cannot pass a blockade of an opponent
        board = Board(4)
    
        block_pawn1 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["green"][2]
        board.starts["green"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        pawn_to_add = board.pawns["yellow"][3]
        board.starts["yellow"].remove_pawn(pawn_to_add)
        board.spacemap[15].add_pawn(pawn_to_add)
        block_pawn2.location = 15

        move = MoveMain(pawn_to_add, 15, 2)
        
        rc = RuleChecker(board, [2, 3])
        valid, bonus = rc.single_move_checker(move)

        self.check(not valid, "invalid move past opponent blockade is valid")
        self.check(bonus==0, "bonus for move past opponent blockade isn't 0")
 
        ##cannot pass one's own blockade
        board = Board(4)
    
        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        pawn_to_add = board.pawns["yellow"][3]
        board.starts["yellow"].remove_pawn(pawn_to_add)
        board.spacemap[15].add_pawn(pawn_to_add)
        block_pawn2.location = 15

        move = MoveMain(pawn_to_add, 15, 2)
        
        rc = RuleChecker(board, [1, 2])
        valid, bonus = rc.single_move_checker(move)

        self.check(not valid, "invalid move pass own blockade is valid")
        self.check(bonus==0, "bonus for move pass own blockade isn't 0")

        ##cannot pass blockade in home row
        board = Board(4)
    
        block_pawn1 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(block_pawn1)
        board.spacemap[9].add_pawn(block_pawn1)
        block_pawn1.location = 9
 
        block_pawn2 = board.pawns["green"][2]
        board.starts["green"].remove_pawn(block_pawn2)
        board.spacemap[9].add_pawn(block_pawn2)
        block_pawn2.location = 9
 
        pawn_to_add = board.pawns["green"][3]
        board.starts["green"].remove_pawn(pawn_to_add)
        board.spacemap[8].add_pawn(pawn_to_add)
        block_pawn2.location = 8

        move = MoveHome(pawn_to_add, 8, 2)
        
        rc = RuleChecker(board, [1, 2])
        valid, bonus = rc.single_move_checker(move)

        self.check(not valid, "invalid move past home blockade is valid")
        self.check(bonus==0, "bonus for move past home blockade isn't 0")
 
        ##can break blockade
        board = Board(4)

        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        move = MoveMain(block_pawn1, 16, 1)
        
        rc = RuleChecker(board, [1, 2])
        valid, bonus = rc.single_move_checker(move)
        self.check(valid, "valid move out of blockade is invalid")
        self.check(bonus==0, "bonus for move out of blockade isn't 0")

        ##cannot move a blockade together with two fours
        board = Board(4)

        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        moves = [
            MoveMain(block_pawn1, 16, 4),
            MoveMain(block_pawn2, 16, 4)]
        
        cplayer = CPlayer("yellow", moves)
        splayer = SPlayer(cplayer)
        splayer.doMove(board, [4, 4])
 
        self.check(block_pawn1.location == 16, "blockade should not have moved together (pawn1)")
        self.check(block_pawn2.location == 16, "blockade should not have moved together (pawn2)")

        ##cannot move a blockade with two fours and two threes even if moving 4, 3 out one piece and a 3, 4 with the other
        board = Board(4)

        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        moves = [
            MoveMain(block_pawn1, 16, 4),
            MoveMain(block_pawn2, 16, 3),
            MoveMain(block_pawn1, 20, 3),
            MoveMain(block_pawn2, 19, 4)]
        
        cplayer = CPlayer("yellow", moves)
        splayer = SPlayer(cplayer)
        splayer.doMove(board, [4, 4])
 
        self.check(block_pawn1.location == 16, "blockade should not have moved together (pawn1)")
        self.check(block_pawn2.location == 16, "blockade should not have moved together (pawn2)")

        ##with a blockade and one piece in front of the blockade and a roll of 1, 2 it is possible to form a new blockade
        board = Board(4)

        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
        block_pawn3 = board.pawns["yellow"][3]
        board.starts["yellow"].remove_pawn(block_pawn3)
        board.spacemap[17].add_pawn(block_pawn3)
        block_pawn3.location = 17

        move = MoveMain(block_pawn2, 16, 1)

        rc = RuleChecker(board, [1, 2])
        valid, bonus = rc.single_move_checker(move)
        
        self.check(block_pawn2.location == 17, "couldn't form a new blockade")

    def exit_row(self):
        ##can move from the main ring to the exit row
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[2].add_pawn(pawn_to_move)
        pawn_to_move.location = 2
        rc = RuleChecker(board, [4, 3])
        move = MoveMain(pawn_to_move, 2, 4)
        valid, bonus = rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(bonus == 0, "moving a piece bonus wasn't 0")
        self.check(moved_pawn.location == 6, "moving into home row pawn isn't on 6")
        self.check(rc.b_final.spacemap[6].pawn1 == moved_pawn, "moving into home row  pawn not location 6")
 
        ##can move from the main ring directly home (without landing on home row)
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[4].add_pawn(pawn_to_move)
        pawn_to_move.location = 4
        rc = RuleChecker(board, [4, 5])
        move = MoveMain(pawn_to_move, 4, 9)
        valid, bonus = rc.single_move_check(move)
        
        self.check(pawn_to_move.location == 14, "pawn didn't move to finish space")

    def complete_move(self):
        ##cannot ignore die roll

if __name__ == "__main__":
    print("Testing...")
    t = Tester()
