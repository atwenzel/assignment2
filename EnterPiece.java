// represents a move where a player enters a piece
class EnterPiece implements IMove {
    Pawn pawn;
    IMove.MoveType mt = IMove.MoveType.ENTER;
    EnterPiece(Pawn pawn) {
        this.pawn=pawn;
    }

    public Pawn get_pawn() {
        return this.pawn;
    }

    public int get_start() {
        return -1;
    }
    
    public int get_distance() {
        return -1;
    }

    public IMove.MoveType get_type() {
        return this.mt;
    } 
}
