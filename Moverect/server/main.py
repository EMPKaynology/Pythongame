import socket
import threading
import json
from protocols import Protocols
import time

class Server:
    def __init__(self, host="127.0.0.1", port=55555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.client_names_and_pos = {}

    def send_pos(self):
        while True:
            time.sleep(0.01)
            temp_dict = {}
            for client in self.client_names_and_pos.keys():
                temp_dict[self.client_names_and_pos[client][0]] = { "x" : self.client_names_and_pos[client][1],"y" : self.client_names_and_pos[client][2]}  
            for client in self.client_names_and_pos.keys():
                print(temp_dict)
                self.send(r_type = Protocols.Response.PLAYERS_POS,data = temp_dict, client = client)

    def send_pos_once(self):
        temp_dict = {}
        for client in self.client_names_and_pos.keys():
            temp_dict[self.client_names_and_pos[client][0]] = { "x" : self.client_names_and_pos[client][1],"y" : self.client_names_and_pos[client][2]}  
        for client in self.client_names_and_pos.keys():
            print(temp_dict)
            self.send(r_type = Protocols.Response.PLAYERS_POS,data = temp_dict, client = client)
    
    def receive(self):
        #thread = threading.Thread(target=self.send_pos,)
        #thread.start()
        while True:
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()

    def handle(self, client):

        self.handle_connect(client)

        while True:
            try:
                data = client.recv(1024).decode("ascii")
                if not data:
                    break
                message = json.loads(data)
                self.handle_receive(message, client)
            except:
                break
        
        self.disconnect(client)

    def handle_connect(self, client):
        while True:
            #self.send(Protocols.Response.NICKNAME, None, client)
            message = json.loads(client.recv(1024).decode("ascii"))
            r_type = message.get("type")
            nickname = message.get("data")

            if r_type == Protocols.Request.NICKNAME:
                self.client_names_and_pos[client] = [nickname,20,20]
                self.send(Protocols.Response.START, None, client)
                print(self.client_names_and_pos)
            
            break

    def handle_receive(self, message, client):
        print(message)
        r_type = message.get("type")
        data = message.get("data")

        if r_type != Protocols.Request.PLAYER_MOVEMENT:
            return
        
        #print(self.client_names_and_pos[client][1])
        self.client_names_and_pos[client][1] += data[0]
        #print(self.client_names_and_pos[client][1])
        #print("pos2")
        #print(self.client_names_and_pos[client][2])
        self.client_names_and_pos[client][2] += data[1]
        #print(self.client_names_and_pos[client][2])
        #print(self.client_names_and_pos)
        #time.sleep(1)
        self.send_pos_once()

    def send(self, r_type, data, client):
        message = {"type": r_type, "data": data}
        message = json.dumps(message).encode("ascii")
        client.send(message)

    def disconnect(self, client):

        del self.client_names_and_pos[client]
        
        client.close()

if __name__ == "__main__":
    server = Server()
    server.receive()