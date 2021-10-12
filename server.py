import socket
import threading
from googletrans import Translator

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self,socket,address, id,name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address 
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client" + str(self.address) + "has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    translator = Translator()
                    client.socket.sendall( (translator.translate(data.decode("utf-8"), src='en', dest='ja').text).encode())

def newConnections(socket):
    while True:
        sock , address =socket.accept()
        global total_connections
        connections.append(Client(sock,address,total_connections,"Name", True))
        connections[len(connections)-1].start()
        print("NewID " + str(connections[len(connections)-1]))
        total_connections +=1

def main():
    sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock.bind(("localhost",12345))
    sock.listen(5)

    newConnectionsThread = threading.Thread(target= newConnections , args = (sock,))
    newConnectionsThread.start()

main()
                