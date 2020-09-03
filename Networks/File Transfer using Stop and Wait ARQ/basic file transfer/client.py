import socket
import sys

MAX_LEN = 64
FRAME_LEN = 4 * 1024

serv_name1 = ''
port1 = 9999
if len(sys.argv) >= 3:
	serv_name1 = sys.argv[1]
	port1 = int(sys.argv[2])
	if len(sys.argv) > 3: FRAME_LEN = int(sys.argv[3])
cl_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl_sock1.connect((serv_name1, port1))
rmsg = cl_sock1.recv(MAX_LEN)
if rmsg !=b'':
	print('Successfully Connected to', serv_name1, ':', port1)
	print(rmsg.decode())
else:
	sys.exit()
username = input('Enter username: ')
cl_sock1.send(username.encode())
rmsg = cl_sock1.recv(MAX_LEN)
if rmsg.decode() != 'UID_RECVD':
	cl_sock1.close()
if rmsg == '':
	sys.exit(1)

password = input('Enter password: ')
cl_sock1.send(password.encode())
rmsg = cl_sock1.recv(MAX_LEN)
print(rmsg.decode())

if rmsg.decode()[0] == 'S':
	filepath = input("Enter the path of the file you wish to transfer\n")
	# filepath = 'pg12169.txt'
	filename = filepath.split('/')[-1]
	file_t = open(filepath, mode='rb')
	cl_sock1.send(filename.encode())
	if cl_sock1.recv(1) != b'1' :
		cl_sock1.close()
		sys.exit()
	while True:
		data_trans = file_t.read(FRAME_LEN)
		while True:
			cl_sock1.send(data_trans)
			rmsg = cl_sock1.recv(MAX_LEN).decode()
			if rmsg[0] == '1':
				break
			print(rmsg)
		if len(data_trans) < FRAME_LEN:
			break
	if rmsg == '1111':
		print('File transmitted successfully')
	else:
		print('File not transmitted')
cl_sock1.close()
