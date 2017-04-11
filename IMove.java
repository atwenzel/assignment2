interface IMove {
    enum MoveType {
        ENTER, REGULAR, HOME
    };

    Pawn get_pawn();  //return the pawn
    
    int get_start();  //return the start int

    int get_distance();  //return the distance int

    MoveType get_type();  //return the move type
}
