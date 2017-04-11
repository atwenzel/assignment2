// represents a move that starts on the main ring
// (but does not have to end up there)
class MoveMain implements IMove {
    Pawn pawn;
    int start;
    int distance;
    IMove.MoveType mt = IMove.MoveType.REGULAR;

    MoveMain(Pawn pawn, int start, int distance) {
        this.pawn=pawn;
        this.start=start;
        this.distance=distance;
    }
    
    public Pawn get_pawn() {
        return this.pawn;
    }

    public int get_start() {
        return this.start;
    }
    
    public int get_distance() {
        return this.distance;
    }

    public IMove.MoveType get_type() {
        return this.mt;
    }  
}
