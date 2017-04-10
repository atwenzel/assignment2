// represents a move that starts on one of the home rows
class MoveHome implements Move {
    Pawn pawn;
    int start;
    int distance;
    IMove.MoveType mt = IMove.MoveType.HOME;

    MoveHome(Pawn pawn, int start, int distance) {
        this.pawn=pawn;
        this.start=start;
        this.distance=distance;
    }
}
