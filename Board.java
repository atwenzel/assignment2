class Board {
    //data
    private ISpace first_space;
    public ISpace green_entry;
    public ISpace red_entry;
    public ISpace blue_entry;
    public ISpace yellow_entry;
    //constructor
    Board() {
        int curr_id = 0;
        ISpace last_space = null;
        ISpace curr_space = null;
        String[] colors = {"green", "red", "blue", "yellow"};

        for (int i = 0; i < 4; i++) {
            //first safe spcae
            curr_space = new SafeSpace(curr_id);
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
                curr_id++;
                last_space.set_next_space(curr_space);
                last_space = curr_space;
            }
            //safe space that connects to home
            curr_space = new SafeSpace(curr_id);
            curr_id++;
            last_space.set_next_space(curr_space);
            last_space = curr_space;
            //save the safe space that connects to home
            ISpace safe_space_save = curr_space;
            //build 7 home spaces with appropriate color
            for (int j = 0; j < 7; j++) {
                curr_space = new HomeSpace(curr_id, colors[i]);
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
                curr_id++;
                last_space.set_next_space(curr_space);
                last_space = curr_space;
            }
            //build the entry point safe space 
            curr_space = new SafeSpace(curr_id);
            curr_id++;
            set_entry(i, curr_space);
            last_space.set_next_space(curr_space);
            last_space = curr_space;
            //make 6 regular spaces
            for (int j = 0; j < 6; j++) {
                curr_space = new RegularSpace(curr_id);
                curr_id++;
                last_space.set_next_space(curr_space);
                last_space = curr_space;
            } 
        } 
        last_space.set_next_space(this.first_space);
    }  
    //functions
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
}
