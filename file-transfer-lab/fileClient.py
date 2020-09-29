#! /usr/bin/env python3
import os, re, socket, sys

sys.path.append("../lib")  # for params
import params

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

        while True:
            fileName = input("Enter the file name: ")
            fileName.strip()

            if fileName == "exit":
                sys.exit(0)
                
            else:
                if not fileName:
                    continue
                elif os.path.exists(FILE_PATH + fileName):
                    s.sendall(fileName.encode())
                    fileContent = open(FILE_PATH + fileName, "rb")
                    while True:
                        data = fileContent.read(1024)
                        s.sendall(data)
                        if not data:
                            break
                    fileContent.close()
                else:
                    print("File %s not found" % fileName)


if __name__ == "__main__":
    client()