README:

FRAME SIZE = 4 KB
Part 1: File transmission.
1. Run python3 record_host_attendance.py, python3 record_host_A.py, python3 record_host_B.py, python3 record_host_C.py in seperate terminals. You can use a cmdline argument to change FRAME SIZE.
2. Run python3 server.py and python3 client.py on seperate terminals. You can use cmdline arguments to change server ip, port and FRAME SIZE. On the client side enter username and password for authentication. Afterwards you will be prompted for file path of file you want to transmit. Enter it and after a short while the file will be transmitted to output folder.

Part 3: Stop and Wait ARQ
1. Run python3 record_host_attendance.py, python3 record_host_A.py, python3 record_host_B.py, python3 record_host_C.py in seperate terminals. You can use a cmdline argument to change FRAME SIZE.
2. Run python3 server.py and python3 client.py on seperate terminals. You can use cmdline arguments to change server ip, port and FRAME SIZE and failure probability of frames. On the client side enter username and password for authentication. Afterwards you will be prompted for file path of file you want to transmit. Enter it and after a short while the file will be transmitted to output folder. Depending on the value of p_fail(def value = 0.1) and FRAME_LEN various timeouts will be observed. If file is received correctly, success message will be printed.

Part 2: Multiple Servers with Random Delays (Stop and Wait ARQ)
1. Run python3 record_host_attendance.py, python3 record_host_A.py, python3 record_host_B.py, python3 record_host_C.py in seperate terminals. You can use a cmdline argument to change FRAME SIZE.
2. Run python3 server.py and python3 client.py on seperate terminals. You can use cmdline arguments to change server ip, port and FRAME SIZE and failure probability of frames. On the client side enter username and password for authentication. Afterwards you will be prompted for file path of file you want to transmit. Enter it and after a short while the file will be transmitted to output folder. Depending on the value of p_fail(def value = 0.1) and FRAME_LEN various timeouts will be observed. If file is received correctly, success message will be printed.
