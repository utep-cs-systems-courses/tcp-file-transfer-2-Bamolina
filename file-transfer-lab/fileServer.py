#!/usr/bin/env python3

import os, socket, sys

sys.path.append("../lib")  # for params
import params

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

        # associating socket with host and port number
        s.bind(bindAddr)

        # "makes" s listening socket
        s.listen()
        print("listening on: ", bindAddr)

        # connection and tuple for client address (host, port)
        conn, addr = s.accept()
        print('Connected by', addr)
        os.chdir(FILE_PATH)

        with conn:
            while True:
                data = conn.recv(1024)
                decodedData = data.decode()
                if decodedData: # if file name exists
                    fileWriter = open(decodedData, 'wb') # write + binary
                    fileWriter.write(conn.recv(1024))
                    fileWriter.close()
                    print("File: %s received" % decodedData)
                if not data:
                    break


if __name__ == "__main__":
    server()