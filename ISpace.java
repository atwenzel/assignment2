import java.util.Hashtable;

interface ISpace {
    //data
    enum SpaceType {
        REGULAR, SAFE, HOME, START;
    }

    //functions
    Pawn add_pawn(Pawn p);  //add a pawn to the space

    Pawn remove_pawn(Pawn p);  //remove the pawn

    ISpace get_next_space(); //get the next space
    
    void set_next_space(ISpace s); //get the next space

    ISpace get_next_home(); //get the next home

    void set_next_home(ISpace s); //set the next home

    SpaceType get_space_type(); //get the space type

    String get_color();  //get the space color

    int get_id();   //return the space id

    Hashtable<String, Pawn> get_pawns();  //returns the Pawns

    boolean has_blockade();
}
