import socket
import threading
import json
from protocols import Protocols

class Client:
    def __init__(self, host="127.0.0.1", port=55555):
        self.nickname = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.lock = threading.RLock()

        self.players = {}

        self.closed = False
        self.started = False

    def start(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def receive(self):
        while not self.closed:
            try:
                data = self.server.recv(1024).decode("ascii")
                print(data)
                if len(data) != 0:
                    message = json.loads(data)
                    self.handle_response(message)
            except Exception as e:
                print("etwas ist schief gelaufen")
                print(e)
                import traceback
                traceback.print_exc()
                #Heul doch mal JUNGE
                #break
        
        self.close()

    def send(self, request, message):
        data = {"type": request, "data": message}
        with self.lock:
            self.server.send(json.dumps(data).encode("ascii"))

    def handle_response(self, response):
        r_type = response.get("type")
        data = response.get("data")

        if r_type == Protocols.Response.START:
            self.started = True
        elif r_type == Protocols.Response.PLAYER_LEFT:
            self.close()
        elif r_type == Protocols.Response.PLAYERS_POS:
            #print("data kommmt an")
            self.players = data

    def close(self):
        self.closed = True
        self.server.close()