import java.io.*;
import java.util.Hashtable;

class StartSpace implements ISpace, Serializable {
    //data
    public SpaceType st = ISpace.SpaceType.START;
    //constructor
    StartSpace() {

    }
    
    public Pawn add_pawn(Pawn p) {
        return null;
    }

    public Pawn remove_pawn(Pawn p) {
        return null;
    }

    public ISpace get_next_space() {
        return null;
    }

    public void set_next_space(ISpace s) {

    }

    public ISpace get_next_home() {
        return null;
    }

    public void set_next_home(ISpace s) {

    }

    public SpaceType get_space_type() {
        return this.st;
    }

    public String get_color() {
        return "";
    }

    public int get_id() {
        return -1;
    }

    public Hashtable<String, Pawn> get_pawns() {
        return null;
    }

    public boolean has_blockade() {
        return false;
    }
}
