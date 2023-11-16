"""Server system"""
#===================
#     RE:WORLD
#===================
# Server Software

#IMPORTS
import os
import time as tm
from socket import *
from threading import Thread
import signal
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox



class Server(object):
    def __init__(self, address:str, port:int, max:int, debug:bool=False, nogui=False):
        print("Initialising. Please wait...")
        self.nogui = nogui
        self.max_players = max
        self.DEBUG = debug
        self.addr = address
        self.port = port
        self.be_ready_to_log()
        if self.nogui:
            self.log("Argument -nogui used. Ctrl+c is not disponnible for a technical issue. Alt+F4 is to use in this case, but will cause maybe some issue for saving, port using, and client connexion.", 1)
        
        if not(self.nogui):
            th = Thread(target=self.gui)
            th.start()

        tm.sleep(5)

        self.log("Creating the server...", 0)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.addr, self.port))
        self.clients_list = []
        self.clients_thread = []
        self.status = 0
        signal.signal(signal.SIGINT, self.stop)
        self.log("Server created !", 0)

    def gui(self):
            self.tk_root = tk.Tk()
            self.tk_root.title("RE:WORLD Server")

            self.scrolled_txt = ScrolledText(self.tk_root, height=50, width=100)
            self.scrolled_txt.pack()

            self.scrolled_txt.insert(tk.END, "Initialising. Please wait...\n")

            #self.scrolled_txt.attribute(state="disabled")

            self.btn_stop = tk.Button(self.tk_root, text="STOP", bg="red", command=self.stop)
            self.btn_stop.pack()

            self.tk_root.resizable(False, False)
            tk.mainloop()
            self.stop()

    
    def start(self):
        """Start the server"""
        self.log("Launching the server.", 3)
        self.status = 1

        self.socket.listen(self.max_players + 1)
        self.main()


    def main(self):
        while self.status == 1:
            try:
                cl_sock, cl_info = self.socket.accept()
                cl = Client(cl_sock, cl_info, self)
                self.clients_list.append(cl)
                cl_thread = Thread(target=cl.main)
                cl_thread.start()
                self.clients_thread.append(cl_thread)
                tm.sleep(0.1)
            except Exception as e:
                self.log(f"Skipping 1 main loop : {e}", 3)
                continue

    def stop(self, signal=None, crash=False, reason="UNKNOW REASON"):
        if crash:
            self.log(f"A FATAL ERROR OCCURED : {reason}", 100)
            self.log("Creating the crash report...", 0)
            c = 1
            while os.path.exists("crash_reports/crash{0}".format(c)):
                c += 1
            with open("crash_reports/crash{0}".format(c), "w") as crashfile:
                crashfile.write("""RE:WORLD server crash report
________________________________________________________________________________________________________________
A critical error advent, that force the server to stop. This crash report contain informations about the crash.
________________________________________________________________________________________________________________
{0}""".format(reason))
            self.log("Crash report created !", 0)
        self.log("Stopping the server...", 0)
        for cl in self.clients_list:
            cl.disconnect()
        self.status = 2
        self.socket.close()
        if not(self.nogui):
            self.tk_root.destroy()
        if crash:
            exit(-1)
        else:
            exit(0)


    def log(self, msg:str, type:int=-1):
        """Types:
        - 0: info
        - 1: warning
        - 2: error
        - 3: debug
        - 4: chat
        - 100: critical
        - other: unknow"""
        if type == 0:
            t = "INFO"
        elif type == 1:
            t = "WARN"
        elif type == 2:
            t = "ERROR"
        elif type == 3:
            t = "DEBUG"
            if not(self.DEBUG):
                return
        elif type == 4:
            t = "CHAT"
        elif type == 100:
            t = "CRITICAL"
        else:
            t = "UNKNOW"
        time = self.gettime()
        text = f"[{time}] [Server/{t}]: {msg}"
        if not(self.nogui):
            self.scrolled_txt.insert(tk.END, text + "\n")
        print(text)
        with open(self.logfile, "+a") as file:
            file.write(text + "\n")

        return

    def gettime(self):
        return tm.asctime(tm.localtime(tm.time())).split(" ")[-2]

    def be_ready_to_log(self):
        self.logfile = None
        nb = 1
        while os.path.exists(f"logs/log{nb}.log"):
            nb += 1
        self.logfile = f"logs/log{nb}.log"
        print("Log system ready !")

class Client(object):
    def __init__(self, skt, info, srv):
        self.socket = skt
        self.info = info
        self.server_object = srv
        self.connected = True

    def main(self):
        while self.connected:
            try:
                msg = self.socket.recv(1024)
            except Exception as e:
                self.log(f"Skipping one loop in client main : {e}", 3)
                continue
            if msg[0] == "something":       #will not work for an evident reason. it is a template
                #do something
                self.socket.send("other thing", 1024)
            elif msg[0] == "something":
                #do something
                self.socket.send("other thing", 1024)
            else:
                self.log(f"An unknow request was sent by the client {self} : {msg}.", 2)
                self.log("Client will be disconnected.")
                break
        self.socket.close()

    def disconnect(self):
        self.connected = False
        self.socket.close()