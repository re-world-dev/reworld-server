"""Server of RE:WORLD"""

#IMPORTS
from socket import *
import time as tm
import os
import server as srv
import ALI
from config import server

#VARS & CONSTS
DEBUG = True
SRV_ADRR = server.SERVER_ADDRESS
SRV_PORT = server.SERVER_PORT
SRV_MAX_PLAYER = server.MAX_PLAYER

if __name__ == "__main__":
    ALI.start()
    server = srv.Server(address=SRV_ADRR, port=SRV_PORT, max=5, debug=DEBUG)
    server.start()