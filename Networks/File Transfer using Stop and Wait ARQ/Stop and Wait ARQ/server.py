import socket
import csv
import threading, sys

MAX_REQS = 5
MAX_LEN = 64
FRAME_LEN = 4 * 1024

def verify_login(username, password):
	res = False
	rtab = open('dist_auth.rtl', mode='r')
	l_addr = rtab.readlines()
	socket_no = None
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
			socket_no = sv_as_cl
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
	if res == False and socket_no is not None:
		socket_no.close()
	return res, socket_no

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
		print(f'Message from {self.add}:', username)
		if username == '':
			self.fail()
			return
		self.cl_sock.send('UID_RECVD'.encode())
		password = self.cl_sock.recv(MAX_LEN).decode()
		print(f'Message from {self.add}:', password)
		if password == '':
			self.fail()
			return
		result, new_sock = verify_login(username, password)
		if result == True:
			self.cl_sock.send('Successful Authentication'.encode())

			fn = self.cl_sock.recv(MAX_LEN)
			print(f'Message from {self.add}:', fn)
			self.cl_sock.send(b'1')
			new_sock.send(fn)
			# self.cl_sock.settimeout(1.0)
			new_sock.settimeout(1.0)
			while True:
				frm = self.cl_sock.recv(FRAME_LEN)
				if frm == b'': break
				print(len(frm))
				new_sock.send(frm)
				try:
					integf = new_sock.recv(MAX_LEN)
					print(f'Message from {new_sock.getpeername()}:', integf.decode())
					self.cl_sock.send(integf)
				except socket.timeout:
					pass
			new_sock.close()
		else:
			self.cl_sock.send('Unsuccessful Authentication'.encode())
		self.fail()

if __name__ == '__main__':
	sv_add = ''
	port_listen = 9999
	if len(sys.argv) >= 3:
		serv_name = sys.argv[1]
		port = int(sys.argv[2])
		if len(sys.argv) >= 4: FRAME_LEN = int(sys.argv[3])
	sv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# sv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sv_sock.bind((sv_add, port_listen))
	sv_sock.listen(MAX_REQS)

	while True:
		cl_sock, add = sv_sock.accept()
		print('Connection Succesful for', add[0], ':', add[1])
		n_thr = AuthThr(cl_sock, add)
		n_thr.start()
