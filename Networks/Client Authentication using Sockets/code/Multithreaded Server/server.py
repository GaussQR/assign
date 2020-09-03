import socket
import csv
import threading

MAX_REQS = 5
MAX_LEN = 64

def verify_login(username, password):
	return lg_dict.get(username) == password

class AuthThr(threading.Thread):
	def __init__(self, cl_sock, add):
		threading.Thread.__init__(self)
		self.cl_sock = cl_sock
		self.add = add
		cl_sock.send(('/'*24+'Welcome'+'/'*24+'\n').encode())

	def fail(self):
		print('Disconnected from', self.add[0], ':', self.add[1])
		self.cl_sock.close()

	def run(self):
		username = self.cl_sock.recv(MAX_LEN).decode()
		if username is '': 
			self.fail()
			return
		self.cl_sock.send('UID_RECVD'.encode())
		password = self.cl_sock.recv(MAX_LEN).decode()
		if password is '': 
			self.fail()
			return
		result = verify_login(username, password)
		if result == True:
			self.cl_sock.send('Successful Authentication'.encode())
		else:
			self.cl_sock.send('Unsuccessful Authentication'.encode())		
		if self.cl_sock.recv(MAX_LEN).decode() == '':
			self.fail()
			return

if __name__ == '__main__':
	f = csv.reader(open('login_credentials.csv', mode='r'))
	lg_dict = {}
	for row in f: lg_dict[row[0]] = row[1]
	lg_dict.pop('Username')

	sv_add = '127.0.0.1'
	port_listen = int(input('Enter port number: '))
	# port_listen = 9999

	sv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sv_sock.bind((sv_add, port_listen))
	sv_sock.listen(MAX_REQS)
	threads = []

	while True:
		cl_sock, add = sv_sock.accept()
		print('Connection Succesful for', add[0], ':', add[1])
		n_thr = AuthThr(cl_sock, add)
		n_thr.start()
		threads.append(n_thr)
	
	for thr in threads:
		thr.join()