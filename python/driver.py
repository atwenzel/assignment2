"""
Starts the SPlayer, GUIPlayer and GUI appropriately
"""

#Global
import sys

#Local
from BestPlayer import BestPlayer
from GUI import GUI
from GUIPlayer import GUIPlayer
from MoveFirstPawn import MoveFirstPawn
from SPlayer import SPlayer

if __name__ == "__main__":
    #guiplayer = GUIPlayer()
    #splayer = SPlayer(guiplayer)
    #guiplayer.start_gui()

    #mfp = MoveFirstPawn()
    #splayer = SPlayer(mfp, use_gui=False)

    bp = BestPlayer()
    try:
        splayer = SPlayer(bp, use_gui=False, ip=sys.argv[1], port=int(sys.argv[2]))
    except IndexError:
        print("Usage: python driver.py <ip> <port>")
        sys.exit(1)
