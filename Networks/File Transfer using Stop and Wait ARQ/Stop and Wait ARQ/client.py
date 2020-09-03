import socket
import sys, random

MAX_LEN = 64
FRAME_LEN = 4 * 1024
SEQNO_LEN = 15
CHECKSUM_LEN = 16
# PF = FRAME_LEN // MAX_LEN
p_fail = 0.1

def append_seq_no(data, arqno, fsq):
	if fsq >= (1 << SEQNO_LEN):
		print('Framing Protocol can\'t handle such big files')
		fsq %= (1 << SEQNO_LEN)
	str_f = bin(fsq)[2:]
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

serv_name1 = ''
port1 = 9999
if len(sys.argv) >= 3:
	serv_name1 = sys.argv[1]
	port1 = int(sys.argv[2])
	if len(sys.argv) > 3: FRAME_LEN = int(sys.argv[3])
	if len(sys.argv) > 4: p_fail = float(sys.argv[4])
BYTES_FROM_FILE = FRAME_LEN - CHECKSUM_LEN - SEQNO_LEN - 1
cl_sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl_sock1.connect((serv_name1, port1))
rmsg = cl_sock1.recv(MAX_LEN)
if rmsg == b'' :
	sys.exit(1)
else:
	print('Successfully Connected to', serv_name1, ':', port1)
	print(rmsg.decode())

username = input('Enter username: ')
# username = '2017csb1061@iitrpr.ac.in'
cl_sock1.send(username.encode())
rmsg = cl_sock1.recv(MAX_LEN)
print(rmsg)
if rmsg.decode() != 'UID_RECVD':
	cl_sock1.close()
if rmsg == b'' :
	sys.exit(1)

password = input('Enter password: ')
# password = 'ABHINAV'
cl_sock1.send(password.encode())
rmsg = cl_sock1.recv(MAX_LEN).decode()
print(rmsg)

if rmsg[0] == 'S':
	filepath = input("Enter the path of the file you wish to transfer\n")
	# filepath = 'pg12169.txt'
	filename = filepath.split('/')[-1]
	file_t = open(filepath, mode='rb')
	cl_sock1.send(filename.encode())
	if cl_sock1.recv(1) != b'1' :
		cl_sock1.close()
		sys.exit()
	cl_sock1.settimeout(1.0)
	file_seqno = 0
	seqno_arq_1 = 0
	while True:
		# print(file_seqno)
		data_trans = file_t.read(BYTES_FROM_FILE)
		if len(data_trans) == 0:
			cl_sock1.send('/END/'.encode())
			break
		data_trans = append_checksum(data_trans)
		data_trans = append_seq_no(data_trans, seqno_arq_1, file_seqno)
		while True:
			data_t = corrupt_frame(data_trans)
			# print(len(data_t))
			cl_sock1.send(data_t)
			try:
				rmsg = cl_sock1.recv(MAX_LEN).decode()
			except socket.timeout:
				print('timeout')
				continue
			print(rmsg)
			if rmsg[0] == str(seqno_arq_1):
				break
			print(rmsg)
		file_seqno += 1
		seqno_arq_1 ^= 1
	try:
		rmsg = cl_sock1.recv(MAX_LEN)
		print(rmsg.decode())
		if rmsg == b'111111111111':
			print('File transmitted successfully')
	except socket.timeout:
		print('File not transmitted')
cl_sock1.close()
