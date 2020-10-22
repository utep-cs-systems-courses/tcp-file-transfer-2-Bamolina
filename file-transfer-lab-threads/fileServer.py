#!/usr/bin/env python3

import os, socket, sys, threading, time
from threading import Thread
sys.path.append("../lib")  # for params
import params
from encapFramedSock import encapFramedSock

HOST = "127.0.0.1"
FILE_PATH = "./FilesReceived"


def server():
    switchesVarDefaults = (
        (('-l', '--listenPort'), 'listenPort', 50001),
        (('-d', '--debug'), "debug", False),  # boolean (set if present)
        (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

    paramMap = params.parseParams(switchesVarDefaults)
    debug, listenPort = paramMap['debug'], paramMap['listenPort']

    if paramMap['usage']:
        params.usage()
    bindAddr = (HOST, listenPort)


    # creating listening socket
    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind socket to host and port number
    s.bind(bindAddr)

    s.listen(5)
    print("listening on: ", bindAddr)

    conn, addr = s.accept()
    print('Connection from: ', addr)
    lock = threading.Lock()


    class Server(Thread):
        def __init__(self, sockAddr):
            Thread.__init__(self)
            self.sock, self.addr = sockAddr
            self.fsock = encapFramedSock(sockAddr)

            def run(self):
                while True:
                    try:
                        fileName, fileContent = self.fsock.receive(debug)
                    except:
                        print("File transfer failed")
                        # send failed status
                        self.fsock.send_status(0, debug)
                        self.fsock.close()
                        sys.exit(1)
                    if debug:
                        print("Received", fileContent)

                    if fileName is None or fileContent is None:
                        print("Client %s has disconnected" % self.addr)
                        sys.exit(0)

                    lock.acquire()
                    if debug:
                        time.sleep(5)
                    try:
                        fileWriter = open(FILE_PATH + fileName.decode(), 'wb')
                        fileWriter.write(fileContent)
                        fileWriter.close()
                        print("File %s received from client %s" %(fileName.decode(), addr))
                    except FileNotFoundError:
                        print("File %s not found" % fileName.decode())
                        sys.exit(1)
                    lock.release()

if __name__ == "__main__":
    server()