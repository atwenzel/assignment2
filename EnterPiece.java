// represents a move where a player enters a piece
class EnterPiece implements Move {
  Pawn pawn;  
  EnterPiece(Pawn pawn) {
    this.pawn=pawn;
  }
}
