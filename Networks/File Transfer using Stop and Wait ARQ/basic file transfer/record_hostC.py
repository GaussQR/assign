import socket
import csv
import threading, sys

MAX_REQS = 5
MAX_LEN = 64
FRAME_LEN = 4 * 1024

def verify_login(username, password):
	return lg_dict.get(username) == password

class AuthThr(threading.Thread):
	def __init__(self, cl_sock, add):
		threading.Thread.__init__(self)
		self.cl_sock = cl_sock
		self.add = add

	def fail(self):
		print('Disconnected from', self.add[0], ':', self.add[1])
		self.cl_sock.close()

	def transfer_file(self):
		tfile = b''
		self.cl_sock.send('SUCCESS'.encode())
		fn = self.cl_sock.recv(MAX_LEN).decode()
		print(f'Message from {self.add}:', fn)
		while True:
			file_part = self.cl_sock.recv(FRAME_LEN)
			print(len(file_part))
			smsg = '1'
			if len(file_part) < FRAME_LEN:
				smsg = '1111'
			self.cl_sock.send(str(smsg).encode())
			tfile += file_part
			if len(file_part) < FRAME_LEN:
				break
		file_write = open('../output/'+fn+'1', mode='wb')
		file_write.write(tfile)
		file_write.close()

	def run(self):
		username = self.cl_sock.recv(MAX_LEN).decode()
		print('Message from {self.add}:', username)
		if username == '':
			self.fail()
			return
		self.cl_sock.send('UID_RECVD'.encode())
		password = self.cl_sock.recv(MAX_LEN).decode()
		print('Message from {self.add}:', password)
		if password == '':
			self.fail()
			return
		result = verify_login(username, password)
		if result == True:
			self.transfer_file()
		self.fail()
		return

if __name__ == '__main__':
	if len(sys.argv) > 1: FRAME_LEN = int(sys.argv[1])
	f = csv.DictReader(open('login_credentials3.csv', mode='r'))
	lg_dict = {}
	for row in f:
		lg_dict[row['Username']] = row['Password']
	f = open('dist_auth.rtl', mode='r')
	__addr = f.readlines()[2].split()

	sv_add = __addr[1]
	port_listen = int(__addr[2])

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
