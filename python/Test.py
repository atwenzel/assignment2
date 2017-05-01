"""
Testing modules
"""

#Global

#Local
from Board import Board
from CPlayer import CPlayer
from EnterPiece import EnterPiece
from Game import Game
from MoveHome import MoveHome
from MoveMain import MoveMain
from RuleChecker import RuleChecker
from SPlayer import SPlayer

class Tester:
    def __init__(self):
        self.enter_tests()
        self.basic_tests()
        self.bopping()
        self.blockade()
        self.exit_row()
        self.game_loop()
        self.complete_move()

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
            if rc.tvals.bonus == move.distance:
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
        self.check(rc.tvals.bonus == -1, "1, 4 bonus wasn't -1")
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
        self.check(rc.tvals.bonus == -1, "2, 3 bonus wasn't -1")
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
        self.check(rc.tvals.bonus == -1, "1, 2 bonus wasn't -1")
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
        self.check(rc.tvals.bonus == -1, "5, 5 move 1 bonus wasn't 0")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "5, 5 pawn 1 location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn1 == moved_pawn, "5, 5 pawn 1 not moved to entry space")
        pawn_to_move = board.pawns["green"][1]
        move = EnterPiece(pawn_to_move)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][1]
        self.check(valid, "5, 5 move 2 failed as invalid")
        self.check(rc.tvals.bonus == -1, "5, 5 move 2 bonus wasn't 0")
        self.check(moved_pawn.location == rc.b_final.entry_spaces["green"].id, "5, 5 pawn 2 location didn't change")
        self.check(rc.b_final.entry_spaces["green"].pawn2 == moved_pawn, "5, 5 pawn 2 not moved to entry space")

    def basic_tests(self):
        ##moving a piece
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[18].add_pawn(pawn_to_move)
        pawn_to_move.location = 18
        rc = RuleChecker(board, [2, 3], "green")
        self.check(rc.b_final.spacemap[18].pawn1 == rc.b_final.pawns["green"][0], "moving a piece: pawn wasn't moved to space 18")
        move = MoveMain(pawn_to_move, 18, 2)
        valid = rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == -1, "moving a piece bonus wasn't 0")
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(moved_pawn.location == 20, "moving a piece pawn isn't on 20")
        self.check(rc.b_final.spacemap[20].pawn1 == moved_pawn, "moving a piece pawn not location 20")
 
        ##moving into home row
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[5].add_pawn(pawn_to_move)
        pawn_to_move.location = 5
        rc = RuleChecker(board, [1, 3], "green")
        move = MoveMain(pawn_to_move, 5, 1)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == -1, "moving a piece bonus wasn't 0")
        self.check(moved_pawn.location == 6, "moving into home row pawn isn't on 6")
        self.check(rc.b_final.spacemap[6].pawn1 == moved_pawn, "moving into home row  pawn not location 6")
    
        ##moving on home row
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[6].add_pawn(pawn_to_move)
        pawn_to_move.location = 6
        rc = RuleChecker(board, [2, 3], "green")
        move = MoveMain(pawn_to_move, 6, 2)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "moving on a home row failed as invalid")
        self.check(rc.tvals.bonus == -1, "moving a piece bonus wasn't 0")
        self.check(moved_pawn.location == 8, "moving on a home row location not 8")
        self.check(rc.b_final.spacemap[8].pawn1 == moved_pawn, "moving on a home row pawn not location 8")

        ##moving to home
        print("=====moving to home=====")
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[10].add_pawn(pawn_to_move)
        pawn_to_move.location = 10
        rc = RuleChecker(board, [2, 3], "green")
        move = MoveHome(pawn_to_move, 10, 2)
        valid = rc.single_move_check(move)
        moved_pawn = rc.b_final.pawns["green"][0]
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == 10, "moving to home bonus wasn't 10")
        self.check(moved_pawn.location == 12, "moving to home location not 12")
        self.check(rc.b_final.spacemap[12].pawn1 == moved_pawn, "moving a piece pawn not location 12")
 
        ##cannot move if no piece present
        print("=====cannot move if no piece present=====")
        board = Board(4)
        pawn_to_move = board.pawns["green"][0]
        rc = RuleChecker(board, [2, 3], "green")
        move = MoveMain(pawn_to_move, 18, 2)
        valid = rc.single_move_check(move)
        self.check(not valid, "cannot move if no piece - move was valid")
        self.check(rc.tvals.bonus == -1, "moving a piece bonus wasn't 0")

    def bopping(self):
        ## bopping a piece and getting a bonus
        print("")
        print("=====bopping a piece and getting a bonus=====")
        print("")
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
        rc = RuleChecker(board, [1, 3], "green")
        valid = rc.single_move_check(move)
        pawn_to_move_final = rc.b_final.pawns["green"][0]
        second_pawn_final = rc.b_final.pawns["red"][0]
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == 20, "bopping - bonus wasn't 20")
        self.check(pawn_to_move_final.location == rc.b_final.starts["green"].id, "bopped pawn wasn't sent home")
        self.check(rc.b_final.spacemap[18].pawn1 == second_pawn_final, "bopping pawn didn't move to space 18")
        self.check(second_pawn_final.location == 18, "seocnd pawn didn't move to 18")

        ##enter a piece and bop on safety
        print("")
        print("======Enter a piece and bop on safety======")
        print("")
        board = Board(4)
        second_pawn = board.pawns["red"][0]
        board.starts["red"].remove_pawn(second_pawn)
        board.spacemap[17].add_pawn(second_pawn)
        second_pawn.location = 17
        piece_to_enter = board.pawns["green"][0]
        move = EnterPiece(piece_to_enter)
        rc = RuleChecker(board, [1, 5], "green")
        second_pawn_final = rc.b_final.pawns["red"][0]
        enter_piece_final = rc.b_final.pawns["green"][0]
        valid = rc.single_move_check(move)
        self.check(second_pawn_final.location == rc.b_final.starts["red"].id, "bop on enter: red pawn not returned to start space")
        self.check(enter_piece_final.location==17, "bop on enter: enter piece not on enter space, is actually at "+str(enter_piece_final.location))
        self.check(valid, "bop on enter failed as invalid")
        self.check(rc.tvals.bonus == 20, "bopping - bonus wasn't 20")
        
        ##bopping on a safety
        print("")
        print("=====Bopping on a safety=====")
        print("")
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
        rc = RuleChecker(board, [1, 3], "red")
        valid = rc.single_move_check(move)
        self.check(not valid, "invalid bopping was valid")
        self.check(rc.tvals.bonus == -1, "invalid bopping - bonus wasn't 0")

        ##bop two pieces
        print("")
        print("======BOP TWO PIECES=====")
        print("")
        board = Board(4)

        pawn_to_bop1 = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(pawn_to_bop1)
        board.spacemap[15].add_pawn(pawn_to_bop1)
        pawn_to_bop1.location = 15

        pawn_to_bop2 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(pawn_to_bop2)
        board.spacemap[42].add_pawn(pawn_to_bop2)
        pawn_to_bop2.location = 42

        bopping_pawn = board.pawns["green"][0]
        board.starts["green"].remove_pawn(bopping_pawn)
        board.spacemap[14].add_pawn(bopping_pawn)
        bopping_pawn.location = 14
    
        """moves = [
            MoveMain(bopping_pawn, bopping_pawn.location, 1),
            MoveMain(bopping_pawn, 69, 3)
        ]

        bonus_moves = [
            MoveMain(bopping_pawn, 15, 20),
            MoveMain(bopping_pawn, 42, 20)
        ]"""

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
 
    
        """moves = [
            MoveMain(bopping_pawn, 3, 1),
            MoveMain(bopping_pawn, 4, 3)
        ]

        bonus_moves = [
            MoveMain(block_pawn1, 18, 20),
            MoveMain(block_pawn2, 18, 20)
        ]"""

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

        pawn_to_move_home_1 = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move_home_1)
        board.spacemap[11].add_pawn(pawn_to_move_home_1)
        pawn_to_move_home_1.location = 11

        pawn_to_move_home_2 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(pawn_to_move_home_2)
        board.spacemap[10].add_pawn(pawn_to_move_home_2)
        pawn_to_move_home_2.location = 10

        blockade_pawn_1 = board.pawns["green"][2]
        board.starts["green"].remove_pawn(blockade_pawn_1)
        board.spacemap[17].add_pawn(blockade_pawn_1)
        blockade_pawn_1.location = 17

        blockade_pawn_2 = board.pawns["green"][3]
        board.starts["green"].remove_pawn(blockade_pawn_2)
        board.spacemap[17].add_pawn(blockade_pawn_2)
        blockade_pawn_2.location = 17

        """moves = [
            MoveHome(pawn_to_move_home_1, 11, 1),
            MoveHome(pawn_to_move_home_2, 10, 2)
        ]

        bonus_moves = [
            MoveMain(blockade_pawn_1, 17, 10),
            MoveMain(blockade_pawn_2, 17, 10)
        ]"""

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

        rc = RuleChecker(board, [5, 1], "green")

        valid = rc.single_move_check(move)
        
        self.check(not valid, "invalid enter onto a blockade is valid")
        self.check(rc.tvals.bonus==-1, "bonus for enter onto a blockade isn't 0")

        ##can form a blockade but cannot add a third piece
        print("=====can form a blockade but cannot add a third piece=====""")
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

        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16
 
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

        block_pawn1 = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(block_pawn1)
        board.spacemap[16].add_pawn(block_pawn1)
        block_pawn1.location = 16
 
        block_pawn2 = board.pawns["yellow"][2]
        board.starts["yellow"].remove_pawn(block_pawn2)
        board.spacemap[16].add_pawn(block_pawn2)
        block_pawn2.location = 16

        other_pawn1 = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(other_pawn1)
        board.spacemap[25].add_pawn(other_pawn1)
        other_pawn1.location = 25

        other_pawn2 = board.pawns["yellow"][3]
        board.starts["yellow"].remove_pawn(other_pawn2)
        board.spacemap[43].add_pawn(other_pawn2)
        other_pawn2.location = 43
 
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
    
        bonus_moves = []

        rc = RuleChecker(board, [4, 4, 3, 3], "yellow")

        res = self.apply_moves(rc, moves)
        
        #self.check(block_pawn1.location == 16, "blockade should not have moved together (pawn1)")
        #self.check(block_pawn2.location == 16, "blockade should not have moved together (pawn2)")

        self.check(res == False, "player was allowed to move a blockade with two fours and two threes even if moving 4, 3 out one piece and a 3, 4 with the other")

        ##with a blockade and one piece in front of the blockade and a roll of 1, 2 it is possible to form a new blockade
        print("=====with a blockade and one piece in front of the blockade and a roll of 1, 2 it is possible to form a new blockade=====")
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

        random_pawn = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(random_pawn)
        board.spacemap[20].add_pawn(random_pawn)
        random_pawn.location = 20
 
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
        pawn_to_move = board.pawns["green"][0]
        board.starts["green"].remove_pawn(pawn_to_move)
        board.spacemap[2].add_pawn(pawn_to_move)
        pawn_to_move.location = 2
        rc = RuleChecker(board, [4, 3], "green")
        move = MoveMain(pawn_to_move, 2, 4)
        valid= rc.single_move_check(move)
        self.check(valid, "moving a piece failed as invalid")
        self.check(rc.tvals.bonus == -1, "moving a piece bonus wasn't 0")
        self.check(rc.b_final.pawns["green"][0].location == 6, "moving into home row pawn isn't on 6")
        self.check(rc.b_final.spacemap[6].pawn1 == rc.b_final.pawns["green"][0], "moving into home row  pawn not location 6")
 
        ##can move from the main ring directly home (without landing on home row)
        print("=====can move from the main ring directly home (without landing on home row=====")
        board = Board(4)

        first_pawn = board.pawns["green"][0]
        board.starts["green"].remove_pawn(first_pawn)
        board.spacemap[11].add_pawn(first_pawn)
        first_pawn.location = 11

        second_pawn = board.pawns["green"][1]
        board.starts["green"].remove_pawn(second_pawn)
        board.spacemap[0].add_pawn(second_pawn)
        second_pawn.location = 0

        """moves = [
            MoveMain(second_pawn, 0, 2),
            MoveHome(first_pawn, 11, 1)
        ]

        bonus_moves = [
            MoveMain(second_pawn, 2, 10)
        ]"""

        moves = [
            MoveMain(second_pawn, 0, 2),
            MoveHome(first_pawn, 11, 1),
            MoveMain(second_pawn, 2, 10),
        ]

        rc = RuleChecker(board, [1, 2], "green")
        #move = MoveMain(pawn_to_move, 4, 9)
        res = self.apply_moves(rc, moves)
        
        self.check(rc.b_final.pawns["green"][0].location == 12, "first_pawn didn't move to finish space")
        self.check(rc.b_final.pawns["green"][1].location == 12, "second_pawn didn't move to finish space")

    def complete_move(self):
        ##cannot ignore die roll
        print("=====cannot ignore die roll=====")
        board = Board(4)
        first_pawn = board.pawns["green"][0]
        board.starts["green"].remove_pawn(first_pawn)
        board.spacemap[17].add_pawn(first_pawn)
        first_pawn.location = 17

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

        blockade_pawn_1 = board.pawns["green"][0]
        board.starts["green"].remove_pawn(blockade_pawn_1)
        board.spacemap[20].add_pawn(blockade_pawn_1)
        blockade_pawn_1.location = 20

        blockade_pawn_2 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(blockade_pawn_2)
        board.spacemap[20].add_pawn(blockade_pawn_2)
        blockade_pawn_2.location = 20

        first_pawn = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(first_pawn)
        board.spacemap[18].add_pawn(first_pawn)
        first_pawn.location = 18

        second_pawn = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(second_pawn)
        board.spacemap[19].add_pawn(second_pawn)
        first_pawn.location = 19

        moves = [
        ]

        bonus_moves = []

        rc = RuleChecker(board, [4, 3], "yellow")
        
        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not allowed to not take moves because there were none")

        #can only take the first die, due to blockade
        print("=====can only take the first die, due to blockade=====")
        board = Board(4)

        blockade_pawn_1 = board.pawns["green"][0]
        board.starts["green"].remove_pawn(blockade_pawn_1)
        board.spacemap[20].add_pawn(blockade_pawn_1)
        blockade_pawn_1.location = 20

        blockade_pawn_2 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(blockade_pawn_2)
        board.spacemap[20].add_pawn(blockade_pawn_2)
        blockade_pawn_2.location = 20

        first_pawn = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(first_pawn)
        board.spacemap[18].add_pawn(first_pawn)
        first_pawn.location = 18

        second_pawn = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(second_pawn)
        board.spacemap[17].add_pawn(second_pawn)
        first_pawn.location = 17

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

        blockade_pawn_1 = board.pawns["green"][0]
        board.starts["green"].remove_pawn(blockade_pawn_1)
        board.spacemap[20].add_pawn(blockade_pawn_1)
        blockade_pawn_1.location = 20

        blockade_pawn_2 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(blockade_pawn_2)
        board.spacemap[20].add_pawn(blockade_pawn_2)
        blockade_pawn_2.location = 20

        first_pawn = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(first_pawn)
        board.spacemap[18].add_pawn(first_pawn)
        first_pawn.location = 18

        second_pawn = board.pawns["yellow"][1]
        board.starts["yellow"].remove_pawn(second_pawn)
        board.spacemap[17].add_pawn(second_pawn)
        first_pawn.location = 17

        moves = [
            MoveMain(second_pawn, 17, 1)
        ]

        bonus_moves = []

        rc = RuleChecker(board, [1, 4], "yellow")
        
        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not allowed to take only the second die")

        #bop, but don't take the 20
        blockade_pawn_1 = board.pawns["green"][0]
        board.starts["green"].remove_pawn(blockade_pawn_1)
        board.spacemap[20].add_pawn(blockade_pawn_1)
        blockade_pawn_1.location = 20

        blockade_pawn_2 = board.pawns["green"][1]
        board.starts["green"].remove_pawn(blockade_pawn_2)
        board.spacemap[20].add_pawn(blockade_pawn_2)
        blockade_pawn_2.location = 20

        bopping_pawn = board.pawns["yellow"][0]
        board.starts["yellow"].remove_pawn(bopping_pawn)
        board.spacemap[4].add_pawn(bopping_pawn)
        blockade_pawn_1.location = 4

        pawn_to_bop = board.pawns["blue"][0]
        board.starts["blue"].remove_pawn(pawn_to_bop)
        board.spacemap[13].add_pawn(pawn_to_bop)
        blockade_pawn_1.location = 13
         
        moves = [
            MoveMain(bopping_pawn, 4, 2)
        ]

        rc = RuleChecker(board, [2, 1], "yellow")
        
        res = self.apply_moves(rc, moves)

        self.check(res == True, "player was not allowed to skip their bonus because there was no move to take")

    def game_loop(self):
        #player is deactivated after cheating
        print("=====player is deactivated after cheating=====")
        game = Game()
        moves = [
            EnterPiece(game.board.pawns["red"][0])
        ]
        bonus_moves = []
        cplayer = CPlayer("red", moves)
        game.register(cplayer)
        game.start(override_dice=[4, 3])
        
        self.check(game.status["red"]["active"] == False, "red player is still active after cheating")
        

if __name__ == "__main__":
    print("Testing...")
    t = Tester()
