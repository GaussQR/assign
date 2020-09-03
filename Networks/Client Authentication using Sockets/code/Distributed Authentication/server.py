import socket
import csv
import threading

MAX_REQS = 5
MAX_LEN = 64

def verify_login(username, password):
	res = False
	rtab = open('dist_auth.rtl', mode='r')
	l_addr = rtab.readlines()
	for sv_p in l_addr[:-1]:
		addr = sv_p.split()
		addr = (addr[1], int(addr[2]))
		sv_as_cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sv_as_cl.connect(addr)
		print('Successfully Connected to', addr[0], ':', addr[1])
		sv_as_cl.send(username.encode())
		rmsg = sv_as_cl.recv(MAX_LEN).decode()
		print(f'Message from {addr}:', rmsg)
		if rmsg != 'UID_RECVD':
			print('Disconnected from', addr[0], addr[1])
			sv_as_cl.close()
			continue
		sv_as_cl.send(password.encode())
		rmsg = sv_as_cl.recv(MAX_LEN).decode()
		print(f'Message from {addr}:', rmsg)
		if rmsg == 'SUCCESS':
			res = True
			break
		print('Disconnected from', addr[0], addr[1])
		sv_as_cl.close()
	if res == True:
		addr = l_addr[-1].split()
		addr = (addr[1], int(addr[2]))
		sv_as_cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sv_as_cl.connect(addr)
		print('Successfully Connected to', addr[0], ':', addr[1])
		sv_as_cl.send(username.encode())
		rmsg = sv_as_cl.recv(MAX_LEN).decode()
		print(f'Message from {addr}:', rmsg)
		if rmsg == 'GRANT':
			res = True
		else: res = False
		print('Disconnected from', addr[0], addr[1])
		sv_as_cl.close()
	return res

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
		print(f'Message from {self.addr}:', username)
		if username is '': 
			self.fail()
			return
		self.cl_sock.send('UID_RECVD'.encode())
		password = self.cl_sock.recv(MAX_LEN).decode()
		print(f'Message from {self.addr}:', password)
		if password is '': 
			self.fail()
			return
		result = verify_login(username, password)
		if result == True:
			self.cl_sock.send('Successful Authentication'.encode())
		else:
			self.cl_sock.send('Unsuccessful Authentication'.encode())		
		self.fail()

if __name__ == '__main__':
	sv_add = '127.0.0.1'
	# port_listen = int(input('Enter port number: '))
	port_listen = 9999

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