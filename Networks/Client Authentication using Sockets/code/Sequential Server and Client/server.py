import socket
import csv

MAX_REQS = 5
MAX_LEN = 64

def fail(cl_sock, add):
	print('Disconnected from', add[0], ':', add[1])
	cl_sock.close()

def verify_login(username, password):
	return lg_dict.get(username) == password

if __name__ == '__main__':
	f = csv.reader(open('login_credentials.csv', mode='r'))
	lg_dict = {}
	for row in f: lg_dict[row[0]] = row[1]
	lg_dict.pop('Username')

	sv_add = 'localhost'
	port_listen = int(input('Enter port number: '))
	# port_listen = 9999

	sv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sv_sock.bind((sv_add, port_listen))
	sv_sock.listen(MAX_REQS)

	while True:
		cl_sock, add = sv_sock.accept()
		print('Connection Succesful for', add[0], ':', add[1])
		msg = '/'*24+'Welcome'+'/'*24+'\n'
		cl_sock.send(msg.encode())

		username = cl_sock.recv(MAX_LEN).decode()
		if username is '': 
			fail(cl_sock, add)
			continue
		cl_sock.send('UID_RECVD'.encode())
		
		password = cl_sock.recv(MAX_LEN).decode()
		if password is '': 
			fail(cl_sock, add)
			continue
		
		result = verify_login(username, password)
		if result == True:
			cl_sock.send('Successful Authentication'.encode())
		else:
			cl_sock.send('Unsuccessful Authentication'.encode())
		
		if cl_sock.recv(MAX_LEN).decode() == '':
			fail(cl_sock, add)