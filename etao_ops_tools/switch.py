#!/usr/bin/env python
import sys
import socket

clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cmd = 'switch'+sys.argv[1]
print cmd
clientsocket.connect(('localhost',9000))
clientsocket.send(cmd)
print clientsocket.recv(100)
result = clientsocket.recv(100)
if result.find('ok!') == -1:
    clientsocket.close()
    sys.exit(1)

sys.exit(0)
