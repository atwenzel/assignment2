import java.io.*;
class Pawn implements Serializable {
    int /* 0-3 */ id;
    String color;
    int location;
    Pawn (int id, String color, int location) {
        this.id=id;
        this.color=color;
        this.location = location;
    }
    
    public boolean equals(Pawn p) {
        return (this.id == p.id && this.color.equals(p.color));
    }
}
