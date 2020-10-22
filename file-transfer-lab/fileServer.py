#!/usr/bin/env python3

import os, socket, sys
sys.path.append("../lib")  # for params
import params
from framedSock import framedReceive

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # bind socket to host and port number
        s.bind(bindAddr)

        s.listen(5)
        print("listening on: ", bindAddr)

        conn, addr = s.accept()
        print('Connection from: ', addr)
        os.chdir(FILE_PATH)

        while True:
            conn, addr = s.accept()
            if not conn or not addr:
                sys.exit(1)
            if not os.fork():
                print("Connected by: ", addr)
                try:
                    fileName, fileContent = framedReceive(conn, debug)
                except:
                    print("File transfer failed")
                    # send failed status
                    conn.sendall(str(0).encode())
                    sys.exit(1)

                try:
                    fileWriter = open(fileName.decode(), 'wb')
                    fileWriter.write(fileContent)
                    fileWriter.close()
                    print("File %s received from client %s" %(fileName.decode(), addr))
                except FileNotFoundError:
                    print("File %s not found" % fileName.decode())

                # send success status
                conn.sendall(str(1).encode())
                sys.exit(0)

if __name__ == "__main__":
    server()