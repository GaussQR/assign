import socket
import csv
import threading

MAX_REQS = 5
MAX_LEN = 102400
DAYS = 8
THRSHLD = .8

class AuthThr(threading.Thread):
	def __init__(self, cl_sock, add):
		threading.Thread.__init__(self)
		self.cl_sock = cl_sock
		self.add = add

	def fail(self):
		print('Disconnected from', self.add[0], ':', self.add[1])
		self.cl_sock.close()

	def run(self):
		username = self.cl_sock.recv(MAX_LEN).decode()
		print('Message from {self.add}:', username)
		if username == '': 
			self.fail()
			return
		if lg_dict.get(username) >= THRSHLD:
			self.cl_sock.send('GRANT'.encode())
		else:
			self.cl_sock.send('DENIED'.encode())
		self.fail()
		return

if __name__ == '__main__':
	f = csv.reader(open('attendance.csv', mode='r'))
	lg_dict = {}
	for row in f:
		if row[0] == '': continue
		num_d = 0
		for st in row[2:]:
			if st == 'Done':
				num_d += 1
		lg_dict[row[1]] = num_d / DAYS
	f = open('dist_auth.rtl', mode='r')
	__addr = f.readlines()[3].split()
	
	sv_add = __addr[1]
	# port_listen = int(input('Enter port number: '))
	port_listen = int(__addr[2])
	# port_listen = int(input('Enter port number: '))

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