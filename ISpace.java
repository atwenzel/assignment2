interface ISpace {
    //data
    enum SpaceType {
        REGULAR, SAFE, HOME;
    }

    //functions
    boolean add_pawn(Pawn p);  //add a pawn to the space

    boolean remove_pawn(Pawn p);  //remove the pawn

    ISpace get_next_space(); //get the next space
    
    void set_next_space(ISpace s); //get the next space

    ISpace get_next_home(); //get the next home

    void set_next_home(ISpace s); //set the next home
}
