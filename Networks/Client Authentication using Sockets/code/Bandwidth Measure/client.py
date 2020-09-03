import socket
import sys

MAXL = 128
NMSG = 500
sv_add = '172.21.5.199'
port_listen = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sv_add, port_listen))
msg = '0' * MAXL
for i in range(NMSG):
    sock.recv(MAXL)
    sock.send(msg.encode())
sock.close()