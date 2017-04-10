// represents a move that starts on the main ring
// (but does not have to end up there)
class MoveMain implements Move {
    Pawn pawn;
    int start;
    int distance;
    IMove.MoveType mt = IMove.MoveType.REGULAR;

    MoveMain(Pawn pawn, int start, int distance) {
        this.pawn=pawn;
        this.start=start;
        this.distance=distance;
    } 
}
