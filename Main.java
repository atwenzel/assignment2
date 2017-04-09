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
        b.visualizer();
    }
}
