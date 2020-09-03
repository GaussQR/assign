import socket
import csv
import threading, sys

MAX_REQS = 5
MAX_LEN = 64
FRAME_LEN = 4 * 1024
SEQNO_LEN = 16
CHECKSUM_LEN = 16

def verify_login(username, password):
	return lg_dict.get(username) == password
	
def extract_data(data_):
	arqno = int(chr(data_[0]))
	fsq = int(data_[1:SEQNO_LEN].decode() , 2)
	data = data_[SEQNO_LEN:]
	chks = 0
	for i in range(len(data)):
		chks = chks + int(data[i])
	chks %= (1 << 8)
	data = data[:-CHECKSUM_LEN]
	return data, int(chks == 0), arqno, fsq

def check_write(fn, end_recv):
	if file_dict.get(fn) == None: return 0
	file_part_all = file_dict[fn]
	print(file_part_all[-1][0], len(file_part_all) - 1)
	if file_part_all[-1][0] != len(file_part_all) - 1 or end_recv == 0:
		return 0
	tfile = b''
	for it in file_part_all:
		tfile += it[1]
	file_write = open('../output/'+fn+'2', mode='wb')
	file_write.write(tfile)
	file_write.close()
	file_dict.pop(fn)
	return 1



class AuthThr(threading.Thread):
	def __init__(self, cl_sock, add):
		threading.Thread.__init__(self)
		self.cl_sock = cl_sock
		self.add = add

	def fail(self):
		print('Disconnected from', self.add[0], ':', self.add[1])
		self.cl_sock.close()

	def transfer_file(self):
		self.cl_sock.send('SUCCESS'.encode())
		fn = self.cl_sock.recv(MAX_LEN).decode()
		print(f'Message from {self.add}:', fn)
		if file_dict.get(fn) == None:
			file_dict[fn] = []
		arqno_req = 0
		isend = 0
		end_recv = 0
		while True:
			integf = 0
			fsq = -1
			extr = b''
			while integf == 0:
				file_part = self.cl_sock.recv(FRAME_LEN)
				print(f'Message from {self.add}:', len(file_part))
				if file_part == b'/END/' or file_part == b'':
					isend = 1
					if file_part == b'/END/': end_recv = 1
					break
				extr, integf, arqno, fsq = extract_data(file_part)
				if integf == 1:
					if arqno == arqno_req:
						arqno_req ^= 1
					else:
						integf = 0
					smsg = str(arqno) + 'ACK'
					self.cl_sock.send(str(smsg).encode())
			if isend:
				break
			if len(extr) > 0:
				file_dict[fn].append((fsq, extr))
		if check_write(fn, end_recv):
			self.cl_sock.send(b'111111111111')

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
	# port_listen = int(input('Enter port number: '))
	port_listen = int(__addr[2])
	sv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# sv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sv_sock.bind((sv_add, port_listen))
	sv_sock.listen(MAX_REQS)
	threads = []
	file_dict = {}
	while True:
		cl_sock, add = sv_sock.accept()
		print('Connection Succesful for', add[0], ':', add[1])
		n_thr = AuthThr(cl_sock, add)
		n_thr.start()
		threads.append(n_thr)

	for thr in threads:
		thr.join()
