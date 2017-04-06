class SPlayer {
    //data
    String color = "";
    private IPlayer player;
    //constructor
    SPlayer(IPlayer player) { this.player = player; }
    //functions
    public void startGame(String color) {
        this.color = color;
        player.startGame(color);
    }

    public Move doMove(Board brd, int[] dice) {
        //implement
        return null;
    }

    public void DoublesPenalty() {
        //implement
    }
}
