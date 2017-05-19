"""
Starts the SPlayer, GUIPlayer and GUI appropriately
"""

#Global

#Local
from GUI import GUI
from GUIPlayer import GUIPlayer
from MoveFirstPawn import MoveFirstPawn
from SPlayer import SPlayer

if __name__ == "__main__":
    #guiplayer = GUIPlayer()
    #splayer = SPlayer(guiplayer)
    #guiplayer.start_gui()

    mfp = MoveFirstPawn()
    splayer = SPlayer(mfp, use_gui=False)
