"""
Builds XML components from game objects
"""

#Global
import json
import xmltodict

#Local
from Board import Board
from Pawn import Pawn

"""
Board
"""

def encode_board(board):
    start_pawns, home_row_pawns, home_pawns, main_pawns = board.categorize_pawns()
    return "<board> "+encode_start(start_pawns)+encode_main(main_pawns)+encode_home_rows(home_row_pawns)+encode_home(home_pawns)+"</board> "

def decode_board(board):
    return None

"""
Start
"""

def encode_start(pawns):
    ret_s = "<start> "
    for pawn in pawns:
        ret_s += encode_pawn(pawn)
    return ret_s + "</start> "

def decode_start(start_d):
    pawns = []
    for encoded_pawn in start_d['pawn']:
        pawns.append(decode_pawn(encoded_pawn))
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
    pawns = []
    for encoded_piece_loc in main_d['piece-loc']:
        pawn, loc = decode_piece_loc(encoded_piece_loc)
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
    pawns = []
    for encoded_piece_loc in hr_d['piece-loc']:
        pawn, loc = decode_piece_loc(encoded_piece_loc)
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
    pawns = []
    for encoded_pawn in home_d['pawn']:
        pawns.append(decode_pawn(encoded_pawn))
    return pawns

"""
piece-loc
"""

def encode_piece_loc(pawn):
    return "<piece-loc> "+encode_pawn(pawn)+"<loc> "+str(pawn.location)+" </loc> </piece-loc> "

def decode_piece_loc(pl_d):
    pawn = decode_pawn(pl_d['pawn'])
    loc = int(pl_d['loc'])
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
Space ID Mapping
"""

def build_map(map_d_path, map_d_reverse_path):
    board = Board(4)
    try:
        map_d = json.loads(open(map_d_path).read())
        reverse_map_d = json.loads(open(map_d_reverse_path).read())
    except IOError:
        map_d = {}
        reverse_map_d = {}
        curr_space = board.spacemap[5]
        curr_robby_id = 0
        while True:
            map_d[curr_space.id] = curr_robby_id
            curr_space = curr_space.next_space
            curr_robby_id += 1
            if curr_space.id == 5:
                break
        print(map_d)
        for key in map_d.keys():
            reverse_map_d[map_d[key]] = key
        print(reverse_map_d)
        #safe space before green entry

def robby2us(pos):
    return 0

def us2robby(pos):
    return 0

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
 
    board = Board(4)
    print(encode_board(board))

    build_map("", "")
