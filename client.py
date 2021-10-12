import socket 
import threading
import sys

def receive(socket , signal):
    while signal:
        try:
            data =socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("Failed!!")
            signal = False
            break

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost",12345))
        print("Success connect to server")
    except:
        print("Cannot connect to server")
        sys.exit(0)

    receiveThread = threading.Thread(target= receive,args=(sock, True))
    receiveThread.start()

    while True:
        message = input()
        sock.sendall(str.encode(message))

main()

