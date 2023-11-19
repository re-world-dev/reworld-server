"""Server of RE:WORLD"""

#IMPORTS
from socket import *
import time as tm
import os
import server as srv
import ALI
from config import server as srv_config
import sys

#VARS & CONSTS
DEBUG = True
SRV_ADRR = srv_config.SERVER_ADDRESS
SRV_PORT = srv_config.SERVER_PORT
SRV_MAX_PLAYER = srv_config.MAX_PLAYER

if __name__ == "__main__":
    if not("-noali" in sys.argv):
        ALI.start()
    if "-nogui" in sys.argv:
        confirm = input("WARNING : use the -nogui argument can cause some issue, and the ctrl+c can't be used. For stop the server, use alt+F4. PLEASE DON'T POST AN ISSUE ANYWHERE IF SOMETHING DOES NOT WORK FOR THE STOP METHOD. To confirm, tape 'confirm -nogui' : ")
        if confirm == 'confirm -nogui':
            server = srv.Server(address=SRV_ADRR, port=SRV_PORT, max=SRV_MAX_PLAYER, debug=DEBUG, nogui=True)
        else:
            print("App will be stopped.")
            exit(-1)
    else:
        server = srv.Server(address=SRV_ADRR, port=SRV_PORT, max=SRV_MAX_PLAYER, debug=DEBUG, nogui=False)
    server.start()
