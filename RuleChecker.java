import java.io.*;
import java.util.*;

class RuleChecker {
    //data
    public Board b_start;
    public Board b_final;
    public List<IMove> moves;
    public List<Integer> bonus = new ArrayList<Integer>();
    public int[] dice;
    public boolean[] used = {false, false};

    //constructor
    RuleChecker(Board b, List<IMove> moves, int[] dice) {
        this.b_start = b;
        this.dice = dice;
        this.b_final = (Board) clone(this.b_start);
        if (this.b_start == this.b_final) {
            System.out.println("WARNING: SAME POINTER");
        }
        this.moves = moves;
        for (int i = 0; i < moves.size(); i++) {
            if (!single_move_check(this.b_final, moves.get(i))) {
                this.b_final = null;
                return;
            }
        }
        if (!multi_move_checker(this.b_start, this.b_final, this.moves)) {
            this.b_final = null;
        }
    }

    //functions
    private boolean single_move_check(Board b, IMove m) {
        System.out.println(m.get_type());
        if (m.get_type() == IMove.MoveType.ENTER) {
            //if ((dice[0] != 5 || dice[1] != 5) && !(dice[0] + dice[1] != 5)) {
            if (dice[0] != 5 && dice[1] != 5 && (dice[0] + dice[1] != 5) && b.pawns_at_start(m.get_pawn().color)) {
                System.out.println("Either none of the dice were 5 or they didn't sum to 5!");
                return false;
            } else if (dice[0] == 5 && !this.used[0]) {
                this.used[0] = true;
            } else if (dice[1] == 5 && !this.used[1]) {
                this.used[1] = true;
            } else if (!this.used[0] && !this.used[1]) {
                this.used[0] = true;
                this.used[1] = true;
            }
        } else {
           if (m.get_distance() == dice[0] && !this.used[0]) {
                this.used[0] = true;
            } else if (m.get_distance() == dice[1] && !this.used[1]) {
                this.used[1] = true;
            } else {
                return false;
            }
            if (blockade_in_path(b, m)) {
                return false;
            } else if (m.get_type() == IMove.MoveType.REGULAR) {
                //if it can't move into a safe space
                if (safe_space_taken(b, m)) {
                    return false;
                }
            } else if (m.get_type() == IMove.MoveType.HOME) {
                if (!can_go_home(b, m)) {
                    return false;
                }
            }
            /*if (m.get_distance() == dice[0] && !this.used[0]) {
                this.used[0] = true;
            } else if (m.get_distance() == dice[1] && !this.used[1]) {
                this.used[1] = true;
            } else {
                return false;
            }*/
        }
        if (b == null) {
            System.out.println("board is null!");
        } else if (m == null) {
            System.out.println("move is null!");
        }
        bonus.add(b.make_move(m));
        return true;
    }

    private boolean multi_move_checker(Board orig_b, Board final_b, List<IMove> moves) {
        if (!this.used[0] || !this.used[1]) {
            System.out.println("all the dice were not used!");
            return false;
        } else if (duplicate_blockades(orig_b, final_b)) {
            System.out.println("a blockade was moved together!");
            return false;
        } else {
            return true;
        }
    }

    public boolean duplicate_blockades(Board orig_b, Board final_b) {
        Hashtable<Pawn, ISpace> orig_locs = orig_b.get_pawn_locs();
        Hashtable<Pawn, ISpace> final_locs = final_b.get_pawn_locs();
        List<Pawn> orig_pawns = orig_b.get_all_pawns();
        List<Pawn> final_pawns = final_b.get_all_pawns();
        for (int i=0; i<orig_pawns.size(); i++) {
            Pawn orig_pawn = orig_pawns.get(i);
            Pawn final_pawn = final_pawns.get(i);
            ISpace orig_loc = orig_locs.get(orig_pawn);
            ISpace final_loc = final_locs.get(final_pawn);
            System.out.println("orig space type: "+orig_loc.get_space_type());
            System.out.println("orig space id: "+orig_loc.get_id());
            System.out.println("final space type: "+final_loc.get_space_type());
            if (orig_loc.get_space_type() != ISpace.SpaceType.START && final_loc.get_space_type() != ISpace.SpaceType.START) {
                if (orig_loc.has_blockade()) {
                    if (final_loc.has_blockade()) {
                        Hashtable<String, Pawn> orig_loc_pawns = orig_loc.get_pawns();
                        Hashtable<String, Pawn> final_loc_pawns = final_loc.get_pawns();
                        Pawn orig_pawn_1 = orig_loc_pawns.get("pawn1");
                        Pawn orig_pawn_2 = orig_loc_pawns.get("pawn2");
                        Pawn final_pawn_1 = final_loc_pawns.get("pawn1");
                        Pawn final_pawn_2 = final_loc_pawns.get("pawn2");
                        //if ((orig_pawn_1 == final_pawn_1 || orig_pawn_1 == final_pawn_2)
                        //        && (orig_pawn_2 == final_pawn_1 || orig_pawn_2 == final_pawn_2)){
                        if ((orig_pawn_1.equals(final_pawn_1) || orig_pawn_1.equals(final_pawn_2))
                                && (orig_pawn_2.equals(final_pawn_1) || orig_pawn_2.equals(final_pawn_2))) {
                            System.out.println("found a blockade that moved together!");
                            return true;
                        }
                    }
                }
            }
        }
        return false;
    }

    public boolean can_go_home(Board b, IMove m) {
        try {
            ISpace next_space = b.traverse(m.get_start(), m.get_distance(), m.get_pawn().color);
            /*if (next_space.get_next_space() != null) {
                return false;
            } else {
                return true;
            }*/
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean blockade_in_path(Board b, IMove m) {
        ISpace curr_space;
        for(int i=m.get_start()+1; i<m.get_start()+m.get_distance()+1; i++) {
            curr_space = b.id_to_space(m.get_start()+1);
            if (curr_space.has_blockade()) {
                return true;
            }
        } 
        return false;
    }

    public boolean space_available(Board b, IMove m) {
        //checks if space is either empty or 1 of same color
        ISpace next_space = b.traverse(m.get_start(), m.get_distance(), m.get_pawn().color);
        Hashtable<String, Pawn> pawns = next_space.get_pawns();
        Pawn pawn1 = pawns.get("pawn1");
        Pawn pawn2 = pawns.get("pawn2");
        if (pawn1 == null) {
            return true;
        } else if (pawn2 == null && pawn1.color.equals(m.get_pawn().color)) {
            return true;
        } else {
            return false;
        }
    }

    public boolean safe_space_taken(Board b, IMove m) {
        //returns if destination is safe and if it is
        ISpace next_space = b.traverse(m.get_start(), m.get_distance(), m.get_pawn().color);
        return (next_space.get_space_type() == ISpace.SpaceType.SAFE && !space_available(b, m));
    }

    public static Object clone(Object object) {
        //inspired by http://alvinalexander.com/java/java-deep-clone-example-source-code
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(object);
            ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
            ObjectInputStream ois = new ObjectInputStream(bais);
            return ois.readObject();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args) {
        Board b = new Board();
        IMove m1 = new EnterPiece(b.green_pawns[0]);
        IMove m2 = new MoveMain(b.green_pawns[0], 17, 2);
        List<IMove> moves = new ArrayList<IMove>();
        int[] dice = {5, 2};
        moves.add(m1);
        moves.add(m2);
        RuleChecker r = new RuleChecker(b, moves, dice);
        if (r.b_final != null) {
            System.out.println("all moves accepted!");
        } else {
            System.out.println("a move was invalid!");
        }
    }
}
