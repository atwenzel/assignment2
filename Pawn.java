class Pawn {
    int /* 0-3 */ id;
    String color;
    Pawn (int id, String color) {
        this.id=id;
        this.color=color;
    }
    
    public boolean equals(Pawn p) {
        return (this.id == p.id && this.color.equals(p.color));
    }
}
