import socket
import json
import random
import sys
import time


class AI(object):
    def __init__(self, name, id, host="localhost", port=2016):
        # Attributes
        self.name = name
        self.id = id
        
        # Connect to server and send handshake with name
        self.socket = socket.socket()
        self.socket.connect((host, port))
        self.socket_file = self.socket.makefile()
        self.socket.send(json.dumps({"name": self.name + "_" + str(self.id)}) + "\n")

    def think(self):
        while True:
            # Read line by line and append it to buffer.
            line = self.socket_file.readline().rstrip('\n')
            
            # Server is shutting down
            if not line or line == "":
                break
            else:
                # parse packet
                packet = json.loads(line) # dictinary (key-value-store)
                
                # Defaults
                speed = 1
                turn = 0
                aim = 0
                shot = 2
                  
                # create control packet
                out_packet = {"speed": speed, "turn": turn, "shoot": shot, "aim": aim}
                
                # Send over network
                self.socket.send(json.dumps(out_packet) + "\n")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        ai = AI(sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
        ai.think()
    else:
        print("Usage: python ai.py <name> <id> <host> <port>")
