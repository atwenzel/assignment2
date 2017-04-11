import java.util.*;

class Main {
    public static void main(String argv[]) {
        Game g = Game.game;

        CPlayer c1 = new CPlayer();
        g.register(c1);

        CPlayer c2 = new CPlayer();
        g.register(c2);

        CPlayer c3 = new CPlayer();
        g.register(c3);
        
        CPlayer c4 = new CPlayer();
        g.register(c4);

        g.start();

        Board b = new Board();
        int[] dice = {5, 4};
        List<IMove> moves = new ArrayList<IMove>();
        moves.add(null);
        RuleChecker r = new RuleChecker(b, moves, dice);
    }
}
