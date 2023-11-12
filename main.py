"""Server of RE:WORLD"""

#IMPORTS
from socket import *
import time as tm
import os
import server as srv
import ALI

#VARS & CONSTS
DEBUG = True
addr = ""
port = 25595

if __name__ == "__main__":
    ALI.start()
    server = srv.Server(address=addr, port=port, max=5, debug=DEBUG)
    server.start()