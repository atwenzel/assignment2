import java.io.*;
import java.util.List;

class RuleChecker {
    //data
    Board b_start;
    Board b_final;
    List<IMove> moves;
    List<int> bonus;
    int[] dice;
    boolean[] used = {false, false};

    //constructor
    RuleChecker(Board b, List<IMove> moves, int[] dice) {
        this.b_start = b;
        this.dice = dice;
        this.b_final = (Board) clone(b);
        this.moves = moves;
        this.bonus = 0;
    }

    //functions
    private boolean single_move_check(Board b, IMove m) {
        if (m.mt == IMove.MoveType.ENTER) {
            if (dice[0] != 5 || dice[1] != 5 || dice[0] + dice[1] != 5) {
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
           if (m.distance == dice[0] && !this.used[0]) {
                this.used[0] = true;
            } else if (m.distance == dice[1] && !this.used[1]) {
                this.used[1] = true;
            } else {
                return false
            }
        }
        if (blockade_in_path(b, m)) {
            return false;
        } else if (m.mt == IMove.MoveType.REGULAR) {
            //if it can't move into a safe space
            if (safe_space_taken(b, m)) {
                return false;
            }
        } else if (m.mt == IMove.MoveType.HOME) {
            if (!can_go_home(b, m)) {
                return false;
            }
        }
        bonus.add(b.make_move(m));
        if (m.distance == dice[0] && !this.used[0]) {
            this.used[0] = true;
        } else if (m.distance == dice[1] && !this.used[1]) {
            this.used[1] = true;
        } else {
            return false;
        }
        return true;
    }

    public boolean can_go_home(Board b, IMove m) {
        try {
            ISpace next_space = b.traverse(m.start, m.distance, m.pawn.color);
            if (next_space.get_next_space != null) {
                return false;
            } else {
                return true;
            }
        } catch (Exception e) {
            return false;
        }
    }

    public boolean blockade_in_path(Board b, IMove m) {
        ISpace curr_space;
        for(i=m.start+1; i<m.start+m.distance+1; i++) {
            curr_space = b.id_to_space(m.start+1);
            if (curr_space.has_blockade()) {
                return true;
            }
        } 
        return false;
    }

    public boolean space_available(Board b, IMove m) {
        //checks if space is either empty or 1 of same color
        ISpace next_space = b.traverse(m.start, m.distance, m.pawn.color);
        Hashtable<String, Pawn> pawns = next_space.get_pawns();
        Pawn pawn1 = pawns.get("pawn1");
        Pawn pawn2 = pawns.get("pawn2");
        if (pawn1 == null) {
            return true;
        } else if (pawn2 == null && pawn1.color.equals(m.pawn.color)) {
            return true;
        } else {
            return false;
        }
    }

    public boolean safe_space_taken(Board b, IMove m) {
        //returns if destination is safe and if it is
        ISpace next_space = b.traverse(m.start, m.distance, m.pawn.color);
        return (next_space.st == ISpace.SpaceType.SAFE && !space_available(b, m));
    }

    public boolean bop_check(Board b, IMove m) {
        //returns true if the proposed move would bop a piece
       
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

}
