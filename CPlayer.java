class CPlayer implements IPlayer {
    //general client
    
    //data
    String color;
    //const
    CPlayer() { super(); }
    //functions
    public void startGame(String color) {
        this.color = color;
        System.out.println("My color is "+this.color);
    }
    
    public Move doMove(Board brd, int[] dice) {
        //implement
        return null;
    }
    
    public void DoublesPenalty() {
        //implement
    }
}
