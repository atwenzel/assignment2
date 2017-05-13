"""
Testing modules
"""

#Global

#Local
from Board import Board
from CPlayer import CPlayer
from EnterPiece import EnterPiece
from Game import Game
from Player import Player
from MoveFirstPawn import MoveFirstPawn
from MoveHome import MoveHome
from MoveMain import MoveMain
from RuleChecker import RuleChecker
from SPlayer import SPlayer

class Tester:
    def __init__(self):
        #self.enter_tests()
        #self.basic_tests()
        #self.bopping()
        #self.blockade()
        #self.exit_row()
        #self.game_loop()
        #self.complete_move()
        print("init tester")

    def check(self, boolean, string):
        if not boolean:
            print("*** TEST FAILED *** ("+string+")")

    """def apply_moves(self, rc, moves, bonus_moves):
        valid = True
        for move in moves:
            print("move", move)
            valid, bonus = rc.single_move_check(move)
            while bonus != 0:
                valid, bonus = rc.single_move_check(bonus_moves[0], is_bonus_move=True)
                bonus_moves = bonus_moves[1:]
            if not valid:
                print("move not valid")
                break
        print(valid)
        if valid:
            print(rc.multi_move_check(moves))
        return valid and rc.multi_move_check(moves)"""
    
    def apply_moves(self, rc, moves):
        valid = True
        for move in moves:
            #if rc.tvals.bonus == [move.distance]:
            if move.distance in rc.tvals.bonus:
                valid = rc.single_move_check(move, is_bonus_move=True)
            else:
                valid = rc.single_move_check(move)
            if not valid:
                print("move not valid")
                break
        print(valid)
        #if valid:
        #    print(rc.multi_move_check(moves))
        return valid and rc.multi_move_check(moves)

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

    def enter_tests(self):
        #enter with 1, 4
        board = Board(4)
        rc = RuleChecker(board, [1, 4], "green")
        pawn_to_move = board.pawns["green"][0]
        #print(pawn_to_move.id)
        move = EnterPiece(pawn_to_move)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        #print(moved_pawn.id)
        self.check(valid, "1, 4 failed as invalid")
        self.check(rc.tvals.bonus == [], "1, 4 bonus wasn't []")
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
        rc = RuleChecker(board, [2, 3], "green")
        pawn_to_move = board.pawns["green"][0]
        move = EnterPiece(pawn_to_move)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "2, 3 failed as invalid")
        self.check(rc.tvals.bonus == [], "2, 3 bonus wasn't []")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "2, 3 pawn location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn1 == moved_pawn, "2, 3 pawn not moved to entry space")
    
        ##cannot enter witha non-5 roll
        board = Board(4)
        rc = RuleChecker(board, [1, 2], "green")
        pawn_to_move = board.pawns["green"][0]
        move = EnterPiece(pawn_to_move)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(not valid, "1, 2 was allowed to move")
        self.check(rc.tvals.bonus == [], "1, 2 bonus wasn't []")
        self.check(moved_pawn.location != rc.b_final.entry_spaces["green"].id, "1, 2 pawn location changed")
        self.check(rc.b_final.entry_spaces["green"].pawn1 != moved_pawn, "1, 2 pawn moved to entry space")

        ##enter two pieces with double 5's
        board = Board(4)
        rc = RuleChecker(board, [5, 5], "green")
        pawn_to_move = board.pawns["green"][0]
        move = EnterPiece(pawn_to_move)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "5, 5 move 1 failed as invalid")
        self.check(rc.tvals.bonus == [], "5, 5 move 1 bonus wasn't []")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "5, 5 pawn 1 location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn1 == moved_pawn, "5, 5 pawn 1 not moved to entry space")
        pawn_to_move = board.pawns["green"][1]
        move = EnterPiece(pawn_to_move)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][1]
        self.check(valid, "5, 5 move 2 failed as invalid")
        self.check(rc.tvals.bonus == [], "5, 5 move 2 bonus wasn't[]")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "5, 5 pawn 2 location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn2 == moved_pawn, "5, 5 pawn 2 not moved to entry space")

    def basic_tests(self):
        ##moving a piece
        board = Board(4)
        pawn_to_move = self.pawn_sim(board, "green", 0, 18)
        rc = RuleChecker(board, [2, 3], "green")
        self.check(rc.b_final.spacemap[18].pawn1 == rc.b_final.pawns["green"][0], "moving a piece: pawn wasn't moved to space 18")
        move = MoveMain(pawn_to_move, 18, 2)
        valid = rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == [], "moving a piece bonus wasn't []")
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(moved_pawn.location == 20, "moving a piece pawn isn't on 20")
        self.check(rc.b_final.spacemap[20].pawn1 == moved_pawn, "moving a piece pawn not location 20")
 
        ##moving into home row
        board = Board(4)
        pawn_to_move = self.pawn_sim(board, "green", 0, 5)
        rc = RuleChecker(board, [1, 3], "green")
        move = MoveMain(pawn_to_move, 5, 1)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == [], "moving a piece bonus wasn't []")
        self.check(moved_pawn.location == 6, "moving into home row pawn isn't on 6")
        self.check(rc.b_final.spacemap[6].pawn1 == moved_pawn, "moving into home row  pawn not location 6")
    
        ##moving on home row
        board = Board(4)
        pawn_to_move = self.pawn_sim(board, "green", 0, 6)
        rc = RuleChecker(board, [2, 3], "green")
        move = MoveMain(pawn_to_move, 6, 2)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "moving on a home row failed as invalid")
        self.check(rc.tvals.bonus == [], "moving a piece bonus wasn't []")
        self.check(moved_pawn.location == 8, "moving on a home row location not 8")
        self.check(rc.b_final.spacemap[8].pawn1 == moved_pawn, "moving on a home row pawn not location 8")

        ##moving to home
        print("=====moving to home=====")
        board = Board(4)
        pawn_to_move = self.pawn_sim(board, "green", 0, 10)
        rc = RuleChecker(board, [2, 3], "green")
        move = MoveHome(pawn_to_move, 10, 2)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == [10], "moving to home bonus wasn't [10]")
        self.check(moved_pawn.location == 12, "moving to home location not 12")
        self.check(rc.b_final.spacemap[12].pawns[0] == moved_pawn, "moving a piece pawn not location 12")
 
        ##cannot move if no piece present
        print("=====cannot move if no piece present=====")
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        rc = RuleChecker(board, [2, 3], "green")
        move = MoveMain(pawn_to_move, 18, 2)
        valid = rc.single_move_check(move)
        self.check(not valid, "cannot move if no piece - move was valid")
        self.check(rc.tvals.bonus == [], "moving a piece bonus wasn't []")

    def bopping(self):
        ## bopping a piece and getting a bonus
        print("")
        print("=====bopping a piece and getting a bonus=====")
        print("")
        board = Board(4)
        pawn_to_move = self.pawn_sim(board, "green", 0, 18)
        second_pawn = self.pawn_sim(board, "red", 0, 17)
        move = MoveMain(second_pawn, 17, 1)
        rc = RuleChecker(board, [1, 3], "green")
        valid = rc.single_move_check(move)
        pawn_to_move_final = rc.b_final.pawns["green"][0]
        second_pawn_final = rc.b_final.pawns["red"][0]
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == [20], "bopping - bonus wasn't [20]")
        self.check(pawn_to_move_final.location == rc.b_final.starts["green"].id, "bopped pawn wasn't sent home")
        self.check(rc.b_final.spacemap[18].pawn1 == second_pawn_final, "bopping pawn didn't move to space 18")
        self.check(second_pawn_final.location == 18, "seocnd pawn didn't move to 18")

        ##enter a piece and bop on safety
        print("")
        print("======Enter a piece and bop on safety======")
        print("")
        board = Board(4)
        second_pawn = self.pawn_sim(board, "red", 0, 17)
        piece_to_enter = board.pawns["green"][0]
        move = EnterPiece(piece_to_enter)
        rc = RuleChecker(board, [1, 5], "green")
        second_pawn_final = rc.b_final.pawns["red"][0]
        enter_piece_final = rc.b_final.pawns["green"][0]
        valid = rc.single_move_check(move)
        self.check(second_pawn_final.location == rc.b_final.starts["red"].id, "bop on enter: red pawn not returned to start space")
        self.check(enter_piece_final.location==17, "bop on enter: enter piece not on enter space, is actually at "+str(enter_piece_final.location))
        self.check(valid, "bop on enter failed as invalid")
        self.check(rc.tvals.bonus == [20], "bopping - bonus wasn't [20]")
        
        ##bopping on a safety
        print("")
        print("=====Bopping on a safety=====")
        print("")
        board = Board(4)
        pawn_to_bop = self.pawn_sim(board, "yellow", 0, 5)
        second_pawn = self.pawn_sim(board, "red", 0, 4)
        move = MoveMain(second_pawn, 4, 1)
        rc = RuleChecker(board, [1, 3], "red")
        valid = rc.single_move_check(move)
        self.check(not valid, "invalid bopping was valid")
        self.check(rc.tvals.bonus == [], "invalid bopping - bonus wasn't []")

        ##bop two pieces
        print("")
        print("======BOP TWO PIECES=====")
        print("")
        board = Board(4)

        pawn_to_bop1 = self.pawn_sim(board, "yellow", 0, 15)

        pawn_to_bop2 = self.pawn_sim(board, "yellow", 1, 42)

        bopping_pawn = self.pawn_sim(board, "green", 0, 14)
    
        moves = [
            MoveMain(bopping_pawn, bopping_pawn.location, 1),
            MoveMain(bopping_pawn, 15, 20),
            MoveMain(bopping_pawn, 42, 20),
            MoveMain(bopping_pawn, 69, 3)
        ]
        
        rc = RuleChecker(board, [1, 3], "green")

        res = self.apply_moves(rc, moves)

        yellow_start = rc.b_final.starts["yellow"]
        pawn_to_bop1_final = rc.b_final.pawns["yellow"][0]
        pawn_to_bop2_final = rc.b_final.pawns["yellow"][1]
        green_pawn_final = rc.b_final.pawns["green"][0]
        self.check(green_pawn_final.location==72, "green pawn not moved correctly: is actually at "+str(green_pawn_final.location))
        self.check(pawn_to_bop1_final.location == yellow_start.id, "multiple bop - first pawn wasn't returned, is at "+str(pawn_to_bop1_final.location))
        self.check(pawn_to_bop2_final.location == yellow_start.id, "multiple bop - second pawn wasn't returned, is at "+str(pawn_to_bop2_final.location))
        
        ##cannot bop twice and move blockade together by 20
        print("")
        print("=====Bopping twice and moving blockade by 20======")
        print("")
        board = Board(4)

        pawn_to_bop1 = self.pawn_sim(board, "yellow", 0, 4)
        pawn_to_bop2 = self.pawn_sim(board, "yellow", 1, 14)
        bopping_pawn = self.pawn_sim(board, "blue", 0, 3)        
        block_pawn1 = self.pawn_sim(board, "blue", 1, 18) 
        block_pawn2 = self.pawn_sim(board, "blue", 2, 18)
 
        moves = [
            MoveMain(bopping_pawn, 3, 1),
            MoveMain(block_pawn1, 18, 20),
            MoveMain(bopping_pawn, 4, 3),
            MoveMain(block_pawn2, 18, 20)
        ]

        rc = RuleChecker(board, [1, 3], "blue")

        res = self.apply_moves(rc, moves)
    
        self.check(res == False, "player was allowed to bop twice and move a blockade by 20")
 
        ##cannot enter home twice and then move a blockade together by 10
        print("=====cannot enter home twice and then move a blockade together by 10=====")
        board = Board(4)

        pawn_to_move_home_1 = self.pawn_sim(board, "green", 0, 11)
        pawn_to_move_home_2 = self.pawn_sim(board, "green", 1, 10)
        blockade_pawn_1 = self.pawn_sim(board, "green", 2, 17)
        blockade_pawn_2 = self.pawn_sim(board, "green", 3, 17)

        moves = [
            MoveHome(pawn_to_move_home_1, 11, 1),
            MoveMain(blockade_pawn_1, 17, 10),
            MoveHome(pawn_to_move_home_2, 10, 2),
            MoveMain(blockade_pawn_2, 17, 10)
        ]
        
        rc = RuleChecker(board, [1, 2], "green")

        res = self.apply_moves(rc, moves)

        self.check(res == False, "player was allowed to enter home twice and move a blockade together by 10")
  
    def blockade(self):
        ##cannot enter with a blockade on the entry point
        print("=====cannot enter with a blockade on the entry point=====")
        board = Board(4)

        block_pawn1 = self.pawn_sim(board, "yellow", 2, 17)
        block_pawn2 = self.pawn_sim(board, "yellow", 3, 17)
        pawn_to_enter = board.pawns["green"][0]
        move = EnterPiece(pawn_to_enter)

        rc = RuleChecker(board, [5, 1], "green")

        valid = rc.single_move_check(move)
        
        self.check(not valid, "invalid enter onto a blockade is valid")
        self.check(rc.tvals.bonus==[], "bonus for enter onto a blockade isn't []")

        ##can form a blockade but cannot add a third piece
        print("=====can form a blockade but cannot add a third piece=====""")
        board = Board(4)
    
        block_pawn1 = self.pawn_sim(board, "yellow", 1, 16) 
        block_pawn2 = self.pawn_sim(board, "yellow", 2, 16)
        pawn_to_add = self.pawn_sim(board, "yellow", 3, 15)

        moves = [
            MoveMain(pawn_to_add, 15, 1),
            MoveMain(pawn_to_add, 16, 2)
        ]
        bonus_moves = []

        rc = RuleChecker(board, [1, 2], "yellow")

        res = self.apply_moves(rc, moves)

        self.check(res == False, "player was allowed to move a third piece onto a blockade")

        ##cannot move directly onto opponents blockade
        print("=====cannot move directly onto opponent's blockade=====")
        board = Board(4)
    
        block_pawn1 = self.pawn_sim(board, "green", 1, 16)
        block_pawn2 = self.pawn_sim(board, "green", 2, 16)
        pawn_to_add = self.pawn_sim(board, "yellow", 3, 15)

        moves = [
            MoveMain(pawn_to_add, 15, 1),
            MoveMain(pawn_to_add, 16, 3)
        ]
        bonus_moves = []

        rc = RuleChecker(board, [1, 3], "yellow")

        res = self.apply_moves(rc, moves)

        self.check(res == False, "player was allowed to move onto opponent's blockade")

        ##cannot pass a blockade of an opponent
        print("=====cannot pass a blockade of an opponent=====")
        board = Board(4)
    
        block_pawn1 = self.pawn_sim(board, "green", 1, 16)
        block_pawn2 = self.pawn_sim(board, "green", 2, 16) 
        pawn_to_add = self.pawn_sim(board, "yellow", 3, 15)

        moves = [
            MoveMain(pawn_to_add, 15, 2),
            MoveMain(pawn_to_add, 17, 3)
        ]
        bonus_moves = []

        rc = RuleChecker(board, [2, 3], "yellow")

        res = self.apply_moves(rc, moves)

        self.check(res == False, "player was allowed to pass the blockade of an opponent")
 
        ##cannot pass one's own blockade
        print("=====cannot pass one's own blockade=====")
        board = Board(4)
    
        block_pawn1 = self.pawn_sim(board, "yellow", 1, 16)
        block_pawn2 = self.pawn_sim(board, "yellow", 2, 16)
        pawn_to_add = self.pawn_sim(board, "yellow", 3, 15)
       
        moves = [
            MoveMain(pawn_to_add, 15, 2),
            MoveMain(pawn_to_add, 17, 1)
        ]
        bonus_moves = []

        rc = RuleChecker(board, [2, 1], "yellow")

        res = self.apply_moves(rc, moves)

        self.check(res == False, "player was allowed to pass own blockade")

        ##cannot pass blockade in home row
        print("=====cannot pass blockade in home row=====")
        board = Board(4)
    
        block_pawn1 = self.pawn_sim(board, "green", 1, 9)
        block_pawn2 = self.pawn_sim(board, "green", 2, 9) 
        pawn_to_add = self.pawn_sim(board, "green", 3, 8)
       
        moves = [
            MoveHome(pawn_to_add, 8, 4)
        ]
        bonus_moves = []
        rc = RuleChecker(board, [4, 2], "green")

        res = self.apply_moves(rc, moves)

        self.check(res == False, "player was able to pass a blockade in the home row")
 
        ##can break blockade
        print("=====can break blockade=====")
        board = Board(4)

        block_pawn1 = self.pawn_sim(board, "yellow", 1, 16)
        block_pawn2 = self.pawn_sim(board, "yellow", 2, 16)
 
        moves = [
            MoveMain(block_pawn1, 16, 1),
            MoveMain(block_pawn1, 17, 2)  #to pass the multi move checker
        ]
        bonus_moves = []

        rc = RuleChecker(board, [1, 2], "yellow")

        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not able to break blockade")

        ##cannot move a blockade together with two fours
        print("=====cannot move a blockade together with two fours=====")
        board = Board(4)

        block_pawn1 = self.pawn_sim(board, "yellow", 1, 16)
        block_pawn2 = self.pawn_sim(board, "yellow", 2, 16)
        other_pawn1 = self.pawn_sim(board, "yellow", 0, 25)
        other_pawn2 = self.pawn_sim(board, "yellow", 3, 43)
 
        moves = [
            MoveMain(block_pawn1, 16, 4),
            MoveMain(block_pawn2, 16, 4),
            MoveMain(other_pawn1, 25, 3),
            MoveMain(other_pawn2, 43, 3)
        ]

        bonus_moves = []
    
        rc = RuleChecker(board, [4, 4, 3, 3], "yellow")

        res = self.apply_moves(rc, moves)    

        self.check(res == False, "player was allowed to move a blockade with two fours")    

        ##cannot move a blockade with two fours and two threes even if moving 4, 3 out one piece and a 3, 4 with the other
        print("=====cannot move a blockade with two fours and two threes even if moving 4, 3 out one piece and a 3, 4 with the other=====")
        board = Board(4)

        block_pawn1 = self.pawn_sim(board, "yellow", 1, 16)
        block_pawn2 = self.pawn_sim(board, "yellow", 2, 16)
 
        moves = [
            MoveMain(block_pawn1, 16, 4),
            MoveMain(block_pawn2, 16, 3),
            MoveMain(block_pawn1, 20, 3),
            MoveMain(block_pawn2, 19, 4)]
    
        bonus_moves = []

        rc = RuleChecker(board, [4, 4, 3, 3], "yellow")

        res = self.apply_moves(rc, moves)
        
        #self.check(block_pawn1.location == 16, "blockade should not have moved together (pawn1)")
        #self.check(block_pawn2.location == 16, "blockade should not have moved together (pawn2)")

        self.check(res == False, "player was allowed to move a blockade with two fours and two threes even if moving 4, 3 out one piece and a 3, 4 with the other")

        ##with a blockade and one piece in front of the blockade and a roll of 1, 2 it is possible to form a new blockade
        print("=====with a blockade and one piece in front of the blockade and a roll of 1, 2 it is possible to form a new blockade=====")
        board = Board(4)

        block_pawn1 = self.pawn_sim(board, "yellow", 1, 16)
        block_pawn2 = self.pawn_sim(board, "yellow", 2, 16)
        block_pawn3 = self.pawn_sim(board, "yellow", 3, 17)
        random_pawn = self.pawn_sim(board, "yellow", 0, 20)
 
        moves = [
            MoveMain(block_pawn2, 16, 1),
            MoveMain(random_pawn, 20, 2)
        ]
        bonus_moves = []

        rc = RuleChecker(board, [1, 2], "yellow")

        res = self.apply_moves(rc, moves)

        self.check(res == True, "couldn't form a new blockade")

    def exit_row(self):
        ##can move from the main ring to the exit row
        print("=====can move from the main ring to the exit row=====")
        board = Board(4)
        pawn_to_move = self.pawn_sim(board, "green", 0, 2)
        rc = RuleChecker(board, [4, 3], "green")
        move = MoveMain(pawn_to_move, 2, 4)
        valid= rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == [], "moving a piece bonus wasn't []")
        self.check(rc.b_final.pawns["green"][0].location == 6, "moving into home row pawn isn't on 6")
        self.check(rc.b_final.spacemap[6].pawn1 == rc.b_final.pawns["green"][0], "moving into home row  pawn not location 6")
 
        ##can move from the main ring directly home (without landing on home row)
        print("=====can move from the main ring directly home (without landing on home row=====")
        board = Board(4)

        first_pawn = self.pawn_sim(board, "green", 0, 11)
        second_pawn = self.pawn_sim(board, "green", 1, 0)

        moves = [
            MoveMain(second_pawn, 0, 2),
            MoveHome(first_pawn, 11, 1),
            MoveMain(second_pawn, 2, 10),
        ]

        rc = RuleChecker(board, [1, 2], "green")
        res = self.apply_moves(rc, moves)
        
        self.check(rc.b_final.pawns["green"][0].location == 12, "first_pawn didn't move to finish space")
        self.check(rc.b_final.pawns["green"][1].location == 12, "second_pawn didn't move to finish space")

    def complete_move(self):
        ##cannot ignore die roll
        print("=====cannot ignore die roll=====")
        board = Board(4)
        first_pawn = self.pawn_sim(board, "green", 0, 17)

        moves = [
            MoveMain(first_pawn, 17, 1)
        ]
        
        bonus_moves = []

        rc = RuleChecker(board, [1, 2], "green")

        res = self.apply_moves(rc, moves)

        self.check(res == False, "player was allowed to skip using a die")

        #cannot move either piece, due to blockade
        print("=====cannot move either piece, due to blockade=====")
        board = Board(4)

        blockade_pawn_1 = self.pawn_sim(board, "green", 0, 20)
        blockade_pawn_2 = self.pawn_sim(board, "green", 1, 20)
        first_pawn = self.pawn_sim(board, "yellow", 0, 18)
        second_pawn = self.pawn_sim(board, "yellow", 1, 19)

        moves = [
        ]

        bonus_moves = []

        rc = RuleChecker(board, [4, 3], "yellow")
        
        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not allowed to not take moves because there were none")

        #can only take the first die, due to blockade
        print("=====can only take the first die, due to blockade=====")
        board = Board(4)

        blockade_pawn_1 = self.pawn_sim(board, "green", 0, 20)
        blockade_pawn_2 = self.pawn_sim(board, "green", 1, 20)
        first_pawn = self.pawn_sim(board, "yellow", 0, 18)
        second_pawn = self.pawn_sim(board, "yellow", 1, 17)

        moves = [
            MoveMain(second_pawn, 17, 1)
        ]

        bonus_moves = []

        rc = RuleChecker(board, [4, 1], "yellow")
        
        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not allowed to take only the first die")

        #can only take the second die, due to blockade
        print("=====can only take the second die, due to blockade=====")
        board = Board(4)

        blockade_pawn_1 = self.pawn_sim(board, "green", 0, 20)
        blockade_pawn_2 = self.pawn_sim(board, "green", 1, 20)
        first_pawn = self.pawn_sim(board, "yellow", 0, 18)
        second_pawn = self.pawn_sim(board, "yellow", 1, 17)

        moves = [
            MoveMain(second_pawn, 17, 1)
        ]

        bonus_moves = []

        rc = RuleChecker(board, [1, 4], "yellow")
        
        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not allowed to take only the second die")

        #bop, but don't take the 20
        blockade_pawn_1 = self.pawn_sim(board, "green", 0, 20)
        blockade_pawn_2 = self.pawn_sim(board, "green", 1, 20)
        bopping_pawn = self.pawn_sim(board, "yellow", 0, 4)
        pawn_to_bop = self.pawn_sim(board, "blue", 0, 13)
         
        moves = [
            MoveMain(bopping_pawn, 4, 2),
            MoveMain(bopping_pawn, 13, 1)
        ]

        rc = RuleChecker(board, [2, 1], "yellow")
        
        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not allowed to skip their bonus because there was no move to take")

        #go home but don't take 10
        print("=====go home but don't take 10=====")
        board = Board(4)
        to_move_home = self.pawn_sim(board, "green", 0, 11)

        moves = [
            MoveHome(to_move_home, 11, 1)
        ]

        rc = RuleChecker(board, [2, 1], "green")

        res = self.apply_moves(rc, moves)
        
        self.check(res == True, "player wasn't allowed to skip 10 bonus with no moves to take")

        #can't take any more moves because they would move a blockade
        print("=====can't take any more moves because they would move a blockade=====")
        blockade1 = self.pawn_sim(board, "yellow", 0, 3)
        blockade2 = self.pawn_sim(board, "yellow", 1, 3)
        blockade3 = self.pawn_sim(board, "green", 0, 18)
        blockade4 = self.pawn_sim(board, "green", 1, 18)

        moves = [
            MoveMain(blockade1, 3, 1),
            MoveMain(blockade2, 3, 1),
            MoveMain(blockade1, 4, 6)
        ]

        rc = RuleChecker(board, [1, 1, 6, 6], "yellow")
        
        res = self.apply_moves(rc, moves)
        
        self.check(res == True, "player wasn't allowed to skip because it would move a blockade")

        #a third piece can go home
        print("=====a third piece can go home=====")
        board = Board(4)
        already_home_1 = self.pawn_sim(board, "green", 0, 12)
        already_home_2 = self.pawn_sim(board, "green", 1, 12)
        to_move_home = self.pawn_sim(board, "green", 2, 11)

        moves = [
            MoveHome(to_move_home, 11, 1)
        ]

        rc = RuleChecker(board, [2, 1], "green")

        print("to_move_home location before moves: ", rc.b_final.pawns["green"][2].location)
        
        res = self.apply_moves(rc, moves)
        
        self.check(res == True, "player wasn't allowed to move a third piece home")

    def game_loop(self):
        #player is deactivated after cheating
        """print("=====player is deactivated after cheating=====")
        game = Game()
        moves = [
            EnterPiece(game.board.pawns["red"][0])
        ]
        bonus_moves = []
        cplayer = CPlayer("red", moves)
        game.register(cplayer)
        game.start(override_dice=[4, 3])
        
        self.check(game.status["red"]["active"] == False, "red player is still active after cheating")"""

        #player gets bonus penalty
        print("=====player gets bonus penalty=====")
        game = Game()
        player = MoveFirstPawn("red")
        game.register(player)
        game.start(override_dice=[5, 5, 2, 2])

        #print(game.board.pawns["red"][0].location)
        self.check(game.board.pawns["red"][0].location == game.board.starts["red"].id, "a pawn wasn't moved back because of doubles (at: "+str(game.board.pawns["red"][0].location))
        #print(game.board.pawns["red"][1].location)
        self.check(game.board.pawns["red"][1].location == game.board.starts["red"].id, "a pawn wasn't moved back because of doubles (at: "+str(game.board.pawns["red"][1].location))
        #print(game.board.pawns["red"][2].location)
        self.check(game.board.pawns["red"][2].location == game.board.starts["red"].id, "a pawn wasn't moved back because of doubles (at: "+str(game.board.pawns["red"][2].location))
        #print(game.board.pawns["red"][3].location)
        self.check(game.board.pawns["red"][3].location == game.board.starts["red"].id, "a pawn wasn't moved back because of doubles (at: "+str(game.board.pawns["red"][3].location))

if __name__ == "__main__":
    print("Testing...")
    t = Tester()
    #t.enter_tests()
    #t.basic_tests()
    t.bopping()
    #t.blockade()
    #t.exit_row()
    #t.game_loop()
    #t.complete_move()
