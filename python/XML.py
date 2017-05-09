"""
Builds XML components from game objects
"""

#Global
import copy
import json
import xmltodict

#Local
from Board import Board
from EnterPiece import EnterPiece
from MoveHome import MoveHome
from MoveMain import MoveMain
from Pawn import Pawn
from SafeSpace import SafeSpace

"""
Board
"""

#pawn_sim(self, board, color, pawnid, newpos)

def encode_board(board):
    map_d = build_map()
    start_pawns, home_row_pawns, home_pawns, main_pawns = board.categorize_pawns()
    return "<board> "+encode_start(start_pawns)+encode_main(main_pawns)+encode_home_rows(home_row_pawns)+encode_home(home_pawns)+"</board> "

def decode_board(board_d):
    map_d = build_map()
    board = Board(4)
    start_pawns = decode_start(board_d['start'])
    main_pawns = decode_main(board_d['main'])
    home_row_pawns = decode_home_rows(board_d['home-rows'])
    home_pawns = decode_home(board_d['home'])
    for pawn in start_pawns:
        pawn.location = board.starts[pawn.color].id
    for pawn in home_pawns:
        pawn.location = board.finishes[pawn.color]
    for pawn in start_pawns+main_pawns+home_row_pawns+home_pawns:
    #for pawn in start_pawns+home_row_pawns+home_pawns:
        pawn_sim(board, pawn.color, pawn.id, pawn.location)
    return board

"""
Start
"""

def encode_start(pawns):
    ret_s = "<start> "
    for pawn in pawns:
        ret_s += encode_pawn(pawn)
    return ret_s + "</start> "

def decode_start(start_d):
    if start_d == None:
        return []
    pawns = []
    try:
        for encoded_pawn in start_d['pawn']:
            pawns.append(decode_pawn(encoded_pawn))
    except TypeError:
        pawns.append(decode_pawn(start_d['pawn']))
    return pawns


"""
Main
"""

def encode_main(pawns):
    ret_s = "<main> "
    for pawn in pawns:
        ret_s += encode_piece_loc(pawn)
    return ret_s + "</main> "

def decode_main(main_d):
    if main_d == None:
        return []
    pawns = []
    try:
        for encoded_piece_loc in main_d['piece-loc']:
            pawn, loc = decode_piece_loc(encoded_piece_loc)
            pawn.location = loc
            pawns.append(pawn)
    except TypeError:
        pawn, loc = decode_piece_loc(main_d['piece-loc'])
        pawn.location = loc
        pawns.append(pawn)
    return pawns


"""
Home Rows
"""

def encode_home_rows(pawns):
    ret_s = "<home-rows> "
    for pawn in pawns:
        ret_s += encode_piece_loc(pawn)
    return ret_s + "</home-rows> "

def decode_home_rows(hr_d):
    if hr_d == None:
        return []
    pawns = []
    try:
        for encoded_piece_loc in hr_d['piece-loc']:
            pawn, loc = decode_piece_loc(encoded_piece_loc, home_row=True)
            pawn.location = loc
            pawns.append(pawn)
    except TypeError:
        pawn, loc = decode_piece_loc(hr_d['piece-loc'], home_row=True)
        pawn.location = loc
        pawns.append(pawn)
    return pawns

"""
Home
"""

def encode_home(pawns):
    ret_s = "<home> "
    for pawn in pawns:
        ret_s += encode_pawn(pawn)
    return ret_s + "</home> "

def decode_home(home_d):
    if home_d == None:
        return []
    pawns = []
    try:
        for encoded_pawn in home_d['pawn']:
            pawns.append(decode_pawn(encoded_pawn))
    except TypeError:
        pawns.append(decode_pawn(home_d['pawn']))
    return pawns

"""
piece-loc
"""

def encode_piece_loc(pawn):
    map_d = build_map()
    return "<piece-loc> "+encode_pawn(pawn)+"<loc> "+str(us2robby(pawn.location, map_d))+" </loc> </piece-loc> "

def decode_piece_loc(pl_d, home_row=False):
    if pl_d == None:
        return []
    pawn = decode_pawn(pl_d['pawn'])
    map_d = build_map()
    if home_row:
        loc = robby2us(int(pl_d['loc']), map_d, color=pawn.color)
    else:
        loc = robby2us(int(pl_d['loc']), map_d)
    return pawn, loc

"""
pawn
"""

def encode_pawn(pawn):
    """<pawn> <color> color  </color> id  </pawn>"""
    return "<pawn> <color> "+pawn.color+" </color> "+encode_id(pawn.id)+"</pawn> "

def decode_pawn(pawn_d):
    return Pawn(int(pawn_d['id']), pawn_d['color'], -1)

"""
id
"""

def encode_id(id):
    return "<id> "+str(id)+" </id> "

"""
Dice
"""

def encode_dice(vals):
    ret_s = "<dice> "
    for val in vals:
        ret_s += encode_die(val)
    ret_s += "</dice> "
    return ret_s

def decode_dice(dice_d):
    decoded_dice = []
    for encoded_die in dice_d['die']:
        decoded_dice.append(int(encoded_die))
    return decoded_dice

"""
Die
"""

def encode_die(val):
    return "<die> "+str(val)+" </die> "

"""
Start Loc
"""

def encode_start_loc(pos):
    map_d = build_map()
    return "<start> "+us2robby(str(pos), map_d)+" </start> "

def decode_start_loc(pos, home_row=False, color=""):
    map_d = build_map()
    if home_row:
        return robby2us(str(pos), map_d, color=color)
    else:
        return robby2us(str(pos), map_d)

"""
Distance
"""

def encode_distance(dist):
    return "<distance> "+str(dist)+" </distance> "

"""
Moves
"""

def encode_enter_piece(move):
    return "<enter-piece> "+encode_pawn(move.pawn)+"</enter-piece> "

def decode_enter_piece(ep_d):
    pawn = decode_pawn(ep_d['pawn'])
    return EnterPiece(pawn)

def encode_move_piece_main(move):
    return "<move-piece-main> "+encode_pawn(move.pawn)+encode_start(move.start)+encode_distance(move.distance)+"</move-piece-main> "

def decode_move_piece_main(mm_d):
    pawn = decode_pawn(mm_d['pawn'])
    start = decode_start(mm_d['start'])
    distance = int(mm_d['distance'])
    return MoveMain(pawn, start, distance)

def encode_move_piece_home(move):
    return "<move-piece-home> "+encode_pawn(move.pawn)+encode_start(move.start)+encode_distance(move.distance)+"</move-piece-home> "

def decode_move_piece_main(mm_d):
    pawn = decode_pawn(mm_d['pawn'])
    start = decode_start(mm_d['start'], home_row=True, color=pawn.color)
    distance = int(mm_d['distance'])
    return MoveMain(pawn, start, distance)

"""
Space ID Mapping
"""

def get_home_start_color(board, space):
    for color in board.home_starts.keys():
        color_space = board.home_starts[color]
        if color_space.id == space.id:
            return color
    return None

def build_map():
    board = Board(4)
    try:
        return json.loads(open('board_mapping.json').read())
    except IOError:
        map_d = {}
        reverse_map_d = {}
        home_d = {}  #{color: {us: robby}}
        reverse_home_d = {}  #{color: {robby: us}}
        curr_space = board.spacemap[5]
        curr_robby_id = 0
        while True:
            if isinstance(curr_space, SafeSpace) and curr_space.next_home != None:
                color = get_home_start_color(board, curr_space)
                home_d[color] = {}
                reverse_home_d[color] = {}
                save_curr_space = curr_space
                curr_space = curr_space.next_home
                home_robby = 0
                while curr_space != None:
                    map_d[curr_space.id] = home_robby
                    home_d[curr_space.color][curr_space.id] = home_robby
                    reverse_home_d[curr_space.color][home_robby] = curr_space.id
                    curr_space = curr_space.next_space
                    home_robby += 1
                curr_space = save_curr_space
            map_d[curr_space.id] = curr_robby_id
            reverse_map_d[curr_robby_id] = curr_space.id
            curr_space = curr_space.next_space
            curr_robby_id += 1
            if curr_space.id == 5:
               break
        combined_d = {'map_d': map_d, 'reverse_map_d': reverse_map_d, 
            'home_d': home_d, 'reverse_home_d': reverse_home_d}
        open('board_mapping.json', 'w').write(json.dumps(combined_d))
        
def robby2us(pos, map_d, color=""):
    try:
        if color != "":
            return map_d['reverse_home_d'][color][str(pos)]
        else:
            return map_d['reverse_map_d'][str(pos)]
    except KeyError:
        print("WARNING: Couldn't map robby 2 us "+str(pos))
        return pos

def us2robby(pos, map_d):
    try:
        return map_d['map_d'][str(pos)]
    except KeyError:
        print("WARNING: Couldn't map us 2 robby "+str(pos))
        return pos

"""
Pawn re-locating
"""

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

"""
Testing
"""

def check(boolean, string):
    if not boolean:
        print("*** TEST FAILED *** ("+string+")")

if __name__ == "__main__":
    print("XML parsing class")
    print("=====encodes and decodes a pawn=====")
    pawn_s = encode_pawn(Pawn(0, "red", -1))
    xml_d = xmltodict.parse(pawn_s)
    pawn = decode_pawn(xml_d['pawn'])
    check(pawn == Pawn(0, "red", -1), "pawn decoded did not equal pawn encoded")

    print("=====encodes dice=====")
    vals = [2, 5]
    encoded_dice = encode_dice(vals)
    check(encoded_dice == "<dice> <die> 2 </die> <die> 5 </die> </dice> ", "dice not encoded correctly "+encoded_dice)

    print("=====decodes dice=====")
    dice_xml = encode_dice([2, 5])
    dice_d = xmltodict.parse(dice_xml)
    decoded_dice = decode_dice(dice_d['dice'])
    check(decoded_dice == [2, 5], "dice not decoded correctly "+str(decoded_dice))

    print("=====encode a piece-loc=====")
    pawn = Pawn(0, "red", -1)
    piece_loc_s = encode_piece_loc(pawn)
    check(piece_loc_s == "<piece-loc> <pawn> <color> red </color> <id> 0 </id> </pawn> <loc> -1 </loc> </piece-loc> ", "piece-loc not correctly encoded "+piece_loc_s)

    print("=====decodes a piece-loc=====")
    pawn = Pawn(0, "red", -1)
    piece_loc_s = encode_piece_loc(pawn)
    pl_d = xmltodict.parse(piece_loc_s)
    decoded_pawn, loc = decode_piece_loc(pl_d['piece-loc'])
    check(decoded_pawn == pawn, "decoded piece-loc pawn was not equal to encoded pawn")
    check(loc == -1, "decoded location from piece-loc wasn't correct "+str(loc))
 
    print("=====encodes home=====")
    home_pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    home_s = encode_home(home_pawns)
    correct = "<home> <pawn> <color> red </color> <id> 0 </id> </pawn> <pawn> <color> red </color> <id> 1 </id> </pawn> </home> "
    check(home_s == correct, "home not encoded correctly "+home_s)

    print("====decodes home=====")
    home_pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    home_s = encode_home(home_pawns)
    home_d = xmltodict.parse(home_s)
    decoded_pawns = decode_home(home_d['home'])
    check(decoded_pawns[0] == home_pawns[0], "decodes home first pawns not equivalent")
    check(decoded_pawns[1] == home_pawns[1], "decodes home second pawns not equivalent")

    print("=====encodes home-rows=====")
    pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    home_rows_s = encode_home_rows(pawns)
    correct = "<home-rows> <piece-loc> <pawn> <color> red </color> <id> 0 </id> </pawn> <loc> -1 </loc> </piece-loc> <piece-loc> <pawn> <color> red </color> <id> 1 </id> </pawn> <loc> -1 </loc> </piece-loc> </home-rows> "
    check(home_rows_s == correct, "encoded home rows incorrectly "+home_rows_s) 

    print("=====decodes home rows=====")
    home_pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    home_row_s = encode_home_rows(home_pawns)
    hr_d = xmltodict.parse(home_row_s)
    decoded_home_pawns = decode_home_rows(hr_d['home-rows'])
    check(decoded_home_pawns[0] == home_pawns[0], "decodes home row first pawns not equivalent")
    check(decoded_home_pawns[1] == home_pawns[1], "decodes home row second pawns not equivalent")

    print("=====encodes main=====")
    pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    main_s = encode_main(pawns)
    correct = "<main> <piece-loc> <pawn> <color> red </color> <id> 0 </id> </pawn> <loc> -1 </loc> </piece-loc> <piece-loc> <pawn> <color> red </color> <id> 1 </id> </pawn> <loc> -1 </loc> </piece-loc> </main> "
    check(main_s == correct, "encoded main incorrectly "+main_s) 

    print("=====decodes main=====")
    pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    main_s = encode_main(pawns)
    main_d = xmltodict.parse(main_s)
    decoded_main_pawns = decode_main(main_d['main'])
    check(decoded_main_pawns[0] == pawns[0], "decodes main first pawns not equivalent")
    check(decoded_main_pawns[1] == pawns[1], "decodes main second pawns not equivalent") 

    print("=====encodes start=====")
    start_pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    start_s = encode_start(start_pawns)
    correct = "<start> <pawn> <color> red </color> <id> 0 </id> </pawn> <pawn> <color> red </color> <id> 1 </id> </pawn> </start> "
    check(start_s == correct, "start not encoded correctly "+start_s)

    print("====decodes start=====")
    start_pawns = [Pawn(0, "red", -1), Pawn(1, "red", -1)]
    start_s = encode_start(start_pawns)
    start_d = xmltodict.parse(start_s)
    decoded_pawns = decode_start(start_d['start'])
    check(decoded_pawns[0] == start_pawns[0], "decodes start first pawns not equivalent")
    check(decoded_pawns[1] == start_pawns[1], "decodes start second pawns not equivalent")
 
    #board = Board(4)
    #encoded_board = encode_board(board)
    #board_d = xmltodict.parse(encoded_board)
    #print(board_d['board'])
    #decoded_board = decode_board(board_d['board'])
    
    #pawn_sim(board, color, pawnid, newpos)
       
    print("=====one pawn in each type (main, home_row, home)=====") 
    board = Board(4)
    pawn_sim(board, "green", 0, 17)
    pawn_sim(board, "red", 1, 30)
    pawn_sim(board, "blue", 0, 60)
    pawn_sim(board, "green", 1, 12)
    pawn_sim(board, "green", 2, 9)
    pawn_sim(board, "red", 2, 16)
    encoded_board = encode_board(board)
    board_d = xmltodict.parse(encoded_board)
    db = decode_board(board_d['board'])
    check(db.pawns["green"][0].location == 17, "green 0 isn't at 17")
    check(db.pawns["red"][1].location == 30, "red 1 isn't at 30 ("+str(db.pawns["red"][1].location)+")")
    check(db.pawns["blue"][0].location == 60, "blue 0 isn't at 60")
    check(db.pawns["green"][1].location == 12, "green 1 isn't at 12")
    check(db.pawns["green"][2].location == 9, "green 2 isn't at 9")

    print("=====encodes an EnterPiece=====")
    move = EnterPiece(Pawn(0, "red", -1))
    move_s = encode_enter_piece(move)
    check(move_s == "<enter-piece> <pawn> <color> red </color> <id> 0 </id> </pawn> </enter-piece> ", "encoded enter-piece was incorrect: "+move_s)

    print("=====decodes an EnterPiece=====")
    move = EnterPiece(Pawn(0, "red", -1))
    move_s = encode_enter_piece(move)
    move_d = xmltodict.parse(move_s)
    md = decode_enter_piece(move_d['enter-piece'])
    check(md.pawn == move.pawn, "decoded enter-piece pawn not equal to original")

    print("=====encodes a MoveMain=====")
    move = MoveMain(Pawn(0, "red", -1), 17, 1)
    move_s = encode_move_main(
