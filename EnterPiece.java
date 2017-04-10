// represents a move where a player enters a piece
class EnterPiece implements Move {
    Pawn pawn;
    IMove.MoveType mt = IMove.MoveType.ENTER;
    EnterPiece(Pawn pawn) {
        this.pawn=pawn;
    }
}
