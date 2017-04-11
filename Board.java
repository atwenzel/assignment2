import java.util.*;
import java.io.*;

class Board implements Serializable {
    //data
    private ISpace first_space;
    private Hashtable<Integer, ISpace> spacemap;

    public ISpace green_entry;
    public ISpace red_entry;
    public ISpace blue_entry;
    public ISpace yellow_entry;

    public ISpace green_home_start;  //these are all the safe spaces before the home
    public ISpace red_home_start;
    public ISpace blue_home_start;
    public ISpace yellow_home_start;

    public Pawn[] green_pawns;
    public Pawn[] red_pawns;
    public Pawn[] blue_pawns;
    public Pawn[] yellow_pawns;

    public int green_pawns_at_start = 4;
    public int red_pawns_at_start = 4;
    public int blue_pawns_at_start = 4;
    public int yellow_pawns_at_start = 4;
    //constructor
    Board() {
        int curr_id = 0;
        ISpace last_space = null;
        ISpace curr_space = null;
        String[] colors = {"green", "red", "blue", "yellow"};
        spacemap = new Hashtable<Integer, ISpace>();
        
        green_pawns = new Pawn[4];
        red_pawns = new Pawn[4];
        blue_pawns = new Pawn[4];
        yellow_pawns = new Pawn[4];
         
        int pawn_id = 0;

        for (int i = 0; i < 4; i++) {
            pawn_id = 0;
            for (int j = 0; j < 4; j++) {
                Pawn p = new Pawn(j, colors[i], -1);
                pawn_id++;
                if (i == 0) {
                    green_pawns[j] = p;
                } else if (i == 1) {
                    red_pawns[j] = p;
                } else if (i == 2) {
                    blue_pawns[j] = p;
                } else if (i == 3) {
                    yellow_pawns[j] = p;
                }
            }
        }

        System.out.println("green pawns 2: "+green_pawns[2].id);

        for (int i = 0; i < 4; i++) {
            //first safe spcae
            curr_space = new SafeSpace(curr_id);
            spacemap.put(curr_id, curr_space);
            curr_id++;
            if (i == 0) {
                this.first_space = curr_space;
            } else {
                last_space.set_next_space(curr_space);
            }
            last_space = curr_space;
            //four regular spaces after safe space
            for (int j = 0; j < 4; j++) {
                curr_space = new RegularSpace(curr_id);
                spacemap.put(curr_id, curr_space);
                curr_id++;
                last_space.set_next_space(curr_space);
                last_space = curr_space;
            }
            //safe space that connects to home
            curr_space = new SafeSpace(curr_id);
            spacemap.put(curr_id, curr_space);
            curr_id++;
            set_home_start(i, curr_space);
            last_space.set_next_space(curr_space);
            last_space = curr_space;
            //save the safe space that connects to home
            ISpace safe_space_save = curr_space;
            //build 7 home spaces with appropriate color
            for (int j = 0; j < 7; j++) {
                curr_space = new HomeSpace(curr_id, colors[i]);
                spacemap.put(curr_id, curr_space);
                curr_id++;
                if (j == 0) {
                    last_space.set_next_home(curr_space);
                } else {
                    last_space.set_next_space(curr_space);
                }
                last_space = curr_space;
            }
            //retreive the saved safe space
            last_space = safe_space_save;
            //build four regular spaces up to entry point
            for (int j = 0; j < 4; j++) {
                curr_space = new RegularSpace(curr_id);
                spacemap.put(curr_id, curr_space);
                curr_id++;
                last_space.set_next_space(curr_space);
                last_space = curr_space;
            }
            //build the entry point safe space 
            curr_space = new SafeSpace(curr_id);
            spacemap.put(curr_id, curr_space);
            curr_id++;
            set_entry(i, curr_space);
            last_space.set_next_space(curr_space);
            last_space = curr_space;
            //make 6 regular spaces
            for (int j = 0; j < 6; j++) {
                curr_space = new RegularSpace(curr_id);
                spacemap.put(curr_id, curr_space);
                curr_id++;
                last_space.set_next_space(curr_space);
                last_space = curr_space;
            } 
        } 
        last_space.set_next_space(this.first_space);
    }  
    //functions
    public int make_move(IMove m) {
        System.out.println("in make_move()");
        int bonus = 0;
        if (m.get_type() == IMove.MoveType.ENTER) {
            bonus += enter_piece(m);
        } else if (m.get_type() == IMove.MoveType.REGULAR) {
            bonus += regular_move(m);
        } else if (m.get_type() == IMove.MoveType.HOME) {
            bonus += home_move(m);
        }
        return bonus;
    }

    public int home_move(IMove m) {
        Pawn p = m.get_pawn();
        ISpace destination = traverse(m.get_start(), m.get_distance(), p.color);
        ISpace current = spacemap.get(p.location);
        current.remove_pawn(p);
        destination.add_pawn(p);
        p.location = destination.get_id();
        if (destination.get_next_space() == null) {
            return 20;
        } else {
            return 0;
        }
    }

    public int regular_move(IMove m) {
        System.out.println("in regular_move()");
        Pawn p = m.get_pawn();
        ISpace destination = traverse(m.get_start(), m.get_distance(), p.color);
        ISpace current = spacemap.get(p.location);
        current.remove_pawn(p);
        Pawn bopped = destination.add_pawn(p);
        p.location = destination.get_id();
        if (bopped != null) {   
            return_pawn(bopped);
            return 10;
        } else {
            return 0;
        }
    }

    public int enter_piece(IMove m) {
        System.out.println("in enter_piece()");
        Pawn p = m.get_pawn();
        Pawn bopped = null;
        if (p.color.equals("green")) {
            bopped = green_entry.add_pawn(p);
            p.location = green_entry.get_id();
            System.out.println("green location: "+p.location);
        } else if (p.color.equals("red")) {
            bopped = red_entry.add_pawn(p);
            p.location = red_entry.get_id();
        } else if (p.color.equals("blue")) {
            bopped = blue_entry.add_pawn(p);
            p.location = blue_entry.get_id();
        } else if (p.color.equals("yellow")) {
            bopped = yellow_entry.add_pawn(p);
            p.location = yellow_entry.get_id();
        }
        if (bopped != null) {
            return_pawn(bopped);
            return 10;
        } else {
            return 0;
        }
    }

    public void return_pawn(Pawn bopped) {
        if (bopped.color.equals("green")) {
            green_pawns_at_start += 1;
        } else if (bopped.color.equals("red")) {
            red_pawns_at_start += 1;
        } else if (bopped.color.equals("blue")) {
            blue_pawns_at_start += 1;
        } else if (bopped.color.equals("yellow")) {
            yellow_pawns_at_start += 1;
        }
        bopped.location = -1;
    }

    public boolean pawns_at_start(String color) {
        if (color.equals("green")) {
            return (green_pawns_at_start > 0);
        } else if (color.equals("red")) {
            return (red_pawns_at_start > 0);
        } else if (color.equals("blue")) {
            return (blue_pawns_at_start > 0);
        } else if (color.equals("yellow")) {
            return (yellow_pawns_at_start > 0);
        }
        return false;
    }

    private void set_entry(int i, ISpace entry_point) {
        if (i == 0) {
            green_entry = entry_point;
        } else if (i == 1) {
            red_entry = entry_point;
        } else if (i == 2) {
            blue_entry = entry_point;
        } else if (i == 3) {
            yellow_entry = entry_point;
        }
    }

    private void set_home_start(int i, ISpace home_start) {
       if (i == 0) {
            green_home_start = home_start;
        } else if (i == 1) {
            red_home_start = home_start;
        } else if (i == 2) {
            blue_home_start = home_start;
        } else if (i == 3) {
            yellow_home_start = home_start;
        } 
    }

    public void visualizer() {
        ISpace curr_space = this.first_space;
        ISpace curr_space_save = null;
        String homestr = "";
        do {
            if (curr_space.get_space_type() == ISpace.SpaceType.REGULAR) {
                System.out.println("regular space (id "+curr_space.get_id()+")");
                curr_space = curr_space.get_next_space();
            } else if (curr_space.get_space_type() == ISpace.SpaceType.HOME) {
                do {
                    homestr += " "+curr_space.get_color()+" home space (id "+curr_space.get_id()+")"+"----->";
                    curr_space = curr_space.get_next_space();
                } while (curr_space != null);
                System.out.println(homestr);
                curr_space = curr_space_save;
                curr_space = curr_space.get_next_space();
                homestr = "";
            } else if (curr_space.get_space_type() == ISpace.SpaceType.SAFE) {
                if (curr_space.get_next_home() != null) {
                    homestr += "safe space points to home (id "+curr_space.get_id()+")"+"--> ";
                    curr_space_save = curr_space;
                    curr_space = curr_space.get_next_home();
                } else {
                    System.out.println("safe space (id "+curr_space.get_id()+")");
                    curr_space = curr_space.get_next_space();
                }
            }
        } while (curr_space.get_id() != this.first_space.get_id());
    }

    public ISpace id_to_space(int id) {
        if (id == -1) {
            ISpace garbage = new StartSpace();
            return garbage;
        } else {
            return this.spacemap.get(id);
        }
    }
    
    public ISpace traverse(int start, int num_hops, String color) {
        //returns the space num_hops ahead of the space at start
        ISpace home_start = null;
        if (color.equals("green")) {
            home_start = green_home_start;
        } else if (color.equals("red")) {
            home_start = red_home_start;
        } else if (color.equals("blue")) {
            home_start = blue_home_start;
        } else if (color.equals("yellow")) {
            home_start = yellow_home_start;
        }
        System.out.println("start location for traverse: "+start);
        ISpace curr_space = this.spacemap.get(start);
        for (int i=start; i<start+num_hops+1; i++) {
            System.out.println("traverse: "+curr_space.get_id());
            if (curr_space.get_id() == home_start.get_id()) {  //on this color's safe space before home
                curr_space = curr_space.get_next_home();
            } else {
                curr_space = curr_space.get_next_space();  //on a regular or safe space that doesn't branch to color's home
            }
        }
        return curr_space;
    }

    public Hashtable<Pawn, ISpace> get_pawn_locs() {
        Hashtable<Pawn, ISpace> pawn_locs = new Hashtable<Pawn, ISpace>();
        for (int i=0; i<4; i++) {
            System.out.println("get_pawn_locs: "+green_pawns[i].id);
            pawn_locs.put(green_pawns[i], id_to_space(green_pawns[i].location));
        }
        for (int i=0; i<4; i++) {
            pawn_locs.put(red_pawns[i], id_to_space(red_pawns[i].location));
        }
        for (int i=0; i<4; i++) {
            pawn_locs.put(blue_pawns[i], id_to_space(blue_pawns[i].location));
        } 
        for (int i=0; i<4; i++) {
            pawn_locs.put(yellow_pawns[i], id_to_space(yellow_pawns[i].location));
        } 
        return pawn_locs;
    }

    public List<Pawn> get_all_pawns() {
        List<Pawn> all_pawns = new ArrayList<Pawn>();
        all_pawns.addAll(Arrays.asList(green_pawns));
        all_pawns.addAll(Arrays.asList(red_pawns));
        all_pawns.addAll(Arrays.asList(blue_pawns));
        all_pawns.addAll(Arrays.asList(yellow_pawns));
        return all_pawns;
    }
}
