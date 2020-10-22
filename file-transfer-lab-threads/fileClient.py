#! /usr/bin/env python3
import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from encapFramedSock import encapFramedSock

FILE_PATH = "Send/"

def client():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-d', '--debug'), "debug", False),  # boolean (set if present)
        (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

    if usage:
        params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)


    # create socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverHost, serverPort))
        fSock = encapFramedSock((s,(serverHost, serverPort)))

        while True:
            fileName = input("Enter the file name: ")
            fileName.strip()

            if fileName == "exit":
                sys.exit(0)

            else:
                if not fileName:
                    continue
                elif os.path.exists(FILE_PATH + fileName):
                    file = open(FILE_PATH + fileName, "rb")
                    fileContent = file.read()
                    if len(fileContent) <= 0:
                        print("File is empty")
                        continue
                    fSock.send(fileName, fileContent, debug)

                    if int(fSock.sock.recv(128)): # if the server received the file
                        print("File %s has been received" % fileName)
                        sys.exit(0)
                    else:
                        print("File %s was not received" % fileName)
                        sys.exit(1)

                else:
                    print("File %s not found" % fileName)


if __name__ == "__main__":
    client()