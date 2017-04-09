class SafeSpace implements ISpace {
    //data
    public SpaceType st = ISpace.SpaceType.SAFE;
    public int id;
    public ISpace next_space = null;
    public ISpace next_home = null;
    private Pawn pawn1 = null;
    private Pawn pawn2 = null;

    //constructor
    SafeSpace(int id) {
        this.id = id;
    }

    //functions
    public boolean add_pawn(Pawn p) {
       //adds pawn to Space, checks legality
        if (this.pawn1 == null) {
            this.pawn1 = p;
            return true;
        } else if (this.pawn2 == null) {
            if (this.pawn1.color.equals(p.color)) {
                this.pawn2 = p;
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    public boolean remove_pawn(Pawn p) {
        if (p.equals(this.pawn1)) {
            this.pawn1 = this.pawn2;
            this.pawn2 = null;
            return true;
        } else if (p.equals(this.pawn2)) {
            this.pawn2 = null;
            return true;
        } else {
            return false;
        }
    }

    public ISpace get_next_space() {
        return this.next_space;
    }

    public void set_next_space(ISpace s) {
        this.next_space = s;
    }

    public ISpace get_next_home() {
        return this.next_home;
    }

    public void set_next_home(ISpace s) {
        this.next_home = s;
    }

    public ISpace.SpaceType get_space_type() {
        return this.st;
    }

    public String get_color() {
        return "";
    }
    
    public int get_id() {
        return this.id;
    }
}
