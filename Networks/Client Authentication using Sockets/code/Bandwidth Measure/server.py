import socket
MAXL = 128
NMSG = 500
sv_add = '172.21.5.199'
port_listen = 9999

sv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sv_sock.bind((sv_add, port_listen))
sv_sock.listen(5)

import time

c, addr = sv_sock.accept()
msg = ('0' * MAXL).encode()
st = time.time()
for i in range(NMSG):
    c.send(msg)
    c.recv(MAXL)
en = time.time()
print('Bytes transferred', 2*MAXL*NMSG)
print('Time taken', en - st)
print('Bandwidth (Bps):', 2*MAXL*NMSG / (en - st))
c.close()
sv_sock.close()