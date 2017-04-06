import java.util.*;

class Game implements IGame {
    //const
    public static Game game = new Game();
    private Game() {}

    //data
    private Vector players = new Vector(); //vector of SPlayer
    String[] colors = {"red", "blue", "green", "yellow"};

    //functions
    public void register(IPlayer p) {
        players.add(new SPlayer(p));
    }

    public void start() {
        //initial loop to assign colors
        for (int i=0; i<4; i++) {
            SPlayer p = (SPlayer)players.elementAt(i);
            p.startGame(colors[i]);
        }
        //game loop starts here
    }
}
