// represents a move that starts on one of the home rows
class MoveHome implements IMove {
    Pawn pawn;
    int start;
    int distance;
    IMove.MoveType mt = IMove.MoveType.HOME;

    MoveHome(Pawn pawn, int start, int distance) {
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
