import socket
import sys, random

MAX_LEN = 64
FRAME_LEN = 4 * 1024
SEQNO_LEN = 15
CHECKSUM_LEN = 16
p_fail = 0.1

def append_seq_no(data, arqno, fsq):
	if fsq >= (1 << SEQNO_LEN):
		print('Framing Protocol can\'t handle such big files')
		fsq %= (1 << SEQNO_LEN)
	str_f = bin(fsq)[2:]
	# print('str_f', len(str_f))
	str_f = str(arqno) + '0'*(SEQNO_LEN - len(str_f)) + str_f
	return str_f.encode() + data

def corrupt_frame(data):
	if random.random() < p_fail:
		ind = len(data) // 3
		data = data[:ind] + (data[ind]^255).to_bytes(1, 'little') + data[ind+1:]
	return data

def append_checksum(data):
	chks = 0
	for i in range(len(data)):
		chks = chks + int(data[i])
	chks %= (1 << 8)
	if chks: chks = (1 << 8) - chks
	chks = chks.to_bytes(1, 'little') + ('\x00'*(CHECKSUM_LEN-1)).encode()
	return data + chks


rmsg, rmsg2 = b'',b''
flag_1 = 1; flag_2 = 1
serv_name1 = ''
port1 = 9999
serv_name2 = ''
port2 = 8888
if len(sys.argv) >= 3:
	serv_name1 = sys.argv[1]
	port1 = int(sys.argv[2])
	serv_name2 = sys.argv[3]
	port2 = int(sys.argv[4])
	if len(sys.argv) > 5: FRAME_LEN = int(sys.argv[5])
	if len(sys.argv) > 6: p_fail = float(sys.argv[6])
BYTES_FROM_FILE = FRAME_LEN - CHECKSUM_LEN - SEQNO_LEN - 1
cl_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	cl_sock1.connect((serv_name1, port1))
except ConnectionRefusedError:
	flag_1 = 0
cl_sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	cl_sock2.connect((serv_name2, port2))
except ConnectionRefusedError:
	flag_2 = 0
if flag_1:
	rmsg = cl_sock1.recv(MAX_LEN)
	print('Successfully Connected to', serv_name1, ':', port1)
	print(rmsg.decode())
if flag_2:
	rmsg2 = cl_sock2.recv(MAX_LEN)
	print('Successfully Connected to', serv_name2, ':', port2)
	print(rmsg2.decode())
if not(flag_1 or flag_2):
	sys.exit()

username = input('Enter username: ')
# username = '2017csb1061@iitrpr.ac.in'
if flag_1:
	cl_sock1.send(username.encode())
	rmsg = cl_sock1.recv(MAX_LEN)
	print(f'({(serv_name1, port1)}): ',rmsg)
	if rmsg.decode() != 'UID_RECVD':
		flag_1 = 0
		cl_sock1.close()
if flag_2:
	cl_sock2.send(username.encode())
	rmsg2 = cl_sock2.recv(MAX_LEN)
	print(f'({(serv_name2, port2)}): ',rmsg2)
	if rmsg2.decode() != 'UID_RECVD':
		flag_2 = 0
		cl_sock2.close()

password = input('Enter password: ')
# password = 'ABHINAV'
auth_f = 0
if flag_1:
	cl_sock1.send(password.encode())
	rmsg = cl_sock1.recv(MAX_LEN)
	print(f'({(serv_name1, port1)}): ',rmsg)
	if rmsg.decode()[0] == 'S': auth_f = 1
if flag_2:
	cl_sock2.send(password.encode())
	rmsg2 = cl_sock2.recv(MAX_LEN)
	print(f'({(serv_name2, port2)}): ',rmsg2)
	if rmsg2.decode()[0] == 'S': auth_f = 1

if not(flag_1 or flag_2):
	sys.exit()

if auth_f:
	filepath = input("Enter the path of the file you wish to transfer\n")
	# filepath = 'pg12169.txt'
	filename = filepath.split('/')[-1]
	file_t = open(filepath, mode='rb')
	if flag_1:
		cl_sock1.send(filename.encode())
		if cl_sock1.recv(1) != b'1' :
			cl_sock1.close()
	if flag_2:
		cl_sock2.send(filename.encode())
		if cl_sock2.recv(1) != b'1' :
			cl_sock2.close()
	cl_sock1.settimeout(1.0)
	cl_sock2.settimeout(1.0)
	file_seqno = 0
	seqno_arq_1 = 0
	seqno_arq_2 = 0
	st = 0
	if not (flag_1 and flag_2):
		if (flag_1 or flag_2) == 0:
			sys.exit()
		if flag_1:
			st = 0
		else: st = 1
	while True:
		# print(file_seqno)
		data_trans = file_t.read(BYTES_FROM_FILE)
		if len(data_trans) == 0:
			if flag_1: cl_sock1.send('/END/'.encode())
			else: cl_sock2.send('/END/'.encode())
			break
		data_trans = append_checksum(data_trans)
		data_trans = append_seq_no(data_trans, seqno_arq_1 if st == 0 else seqno_arq_2, file_seqno)
		while True:
			data_t = corrupt_frame(data_trans)
			# print(len(data_t))
			if st == 0:
				cl_sock1.send(data_t)
				try:
					rmsg = cl_sock1.recv(MAX_LEN)
				except socket.timeout:
					# print(data_t)
					print('timeout')
					continue
				print(f'({(serv_name1, port1)}): ',rmsg)
				if rmsg.decode()[0] == str(seqno_arq_1):
					seqno_arq_1 ^= 1
					break
				# print(rmsg)
			else:
				cl_sock2.send(data_t)
				try:
					rmsg2 = cl_sock2.recv(MAX_LEN)
				except socket.timeout:
					# print(data_t)
					print('timeout')
					continue
				print(f'({(serv_name2, port2)}): ',rmsg2)
				if rmsg2.decode()[0] == str(seqno_arq_2):
					seqno_arq_2 ^= 1
					break
				# print(rmsg2)
		if flag_1 and flag_2:
			st ^= 1
		file_seqno += 1
	file_fl = 0
	if flag_1:
		try:
			rmsg = cl_sock1.recv(MAX_LEN)
			print(f'({(serv_name1, port1)}): ',rmsg)
			if rmsg == b'111111111111':
				file_fl = 1
		except socket.timeout:
			pass
	if flag_2:
		try:
			rmsg2 = cl_sock2.recv(MAX_LEN)
			print(f'({(serv_name1, port1)}): ',rmsg)
			if rmsg2 == b'111111111111':
				file_fl = 1
		except socket.timeout:
			pass
	if file_fl == 1:
		print('File transmitted successfully')
	else:
		print('File not transmitted')
cl_sock1.close()
cl_sock2.close()
