import socket
import sys

MAX_LEN = 64
serv_name = input('Enter Server ip: ')
# serv_name = '127.0.0.1'
port = int(input('Enter port number: '))
# port = 9999

cl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl_sock.connect((serv_name, port))
rmsg = cl_sock.recv(MAX_LEN)
if rmsg is '': sys.exit(1)
print('Successfully Connected to', serv_name, ':', port)
print('Server:', rmsg.decode())

username = input('Enter username: ')
if username == 'EXIT': sys.exit(1)
cl_sock.send(username.encode())
rmsg = cl_sock.recv(MAX_LEN)
print('Server:', rmsg.decode())
if rmsg.decode() != 'UID_RECVD':
    cl_sock.close()
    sys.exit(0)

password = input('Enter password: ')
if password == 'EXIT': sys.exit(1)
cl_sock.send(password.encode())
print('Server:', cl_sock.recv(MAX_LEN).decode())
cl_sock.close()