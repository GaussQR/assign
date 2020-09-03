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

    def fail(self):
        print('Disconnected from', self.add[0], ':', self.add[1])
        self.cl_sock.close()

    def run(self):
        username = self.cl_sock.recv(MAX_LEN).decode()
		print('Message from {self.add}:', username)
        if username is '': 
            self.fail()
            return
        self.cl_sock.send('UID_RECVD'.encode())
        password = self.cl_sock.recv(MAX_LEN).decode()
		print('Message from {self.add}:', password)
        if password is '': 
            self.fail()
            return
        result = verify_login(username, password)
        if result == True:
            self.cl_sock.send('SUCCESS'.encode())
        self.fail()
        return

if __name__ == '__main__':
	f = csv.DictReader(open('login_credentials2.csv', mode='r'))
	lg_dict = {}
	for row in f:
		lg_dict[row['Username']] = row['Password']
	f = open('dist_auth.rtl', mode='r')
	__addr = f.readlines()[1].split()
	
	sv_add = __addr[1]
	# port_listen = int(input('Enter port number: '))
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