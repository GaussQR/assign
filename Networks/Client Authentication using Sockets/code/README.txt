README

All the client and server in each part can easily be located on different machines
within a network and would still work if the server is hosted on its private IP in
the network. This can be easily done by changing the variable sv_add in the server.py
file.

1. Part 1
->  Open a shell ./python3 server.py. The server would request a port that it
    will listen to. Then open a ./python3 client.py and enter the server ip and port.
    The ip is set to 127.0.0.1 and the port is same as that entered in the server.py.

->  The client would request login details. They are sent to the authentication server.
    It will verify that using a hash table containing username and password stored in
    login_credentials.csv

->  If client exits before authentication, the server would print that client has been
    disconnected.


2. Part 2
->  Open a shell ./python3 server.py. The server would request a port that it
    will listen to. Then open two shells and write ./python3 client.py and enter the 
    server ip and port in both of them. The ip is set to 127.0.0.1 and the port is 
    same as that entered in the server.py.

->  The clients would request login details. As this is a multithreaded server no
	request is blocked and they can be handled concurrently.

->  If client exits before authentication, the server would print that client has been
    disconnected.


3. Part 3
->  In this part, there are two processes which if run on different platforms, and the ip
	is set to the private IP of the computer on the network. 

->  The server would send data to client a number of times(set to 500) and determine the
	average bandwidth of the medium. It has been determined to be 7.43 MBps on IITRPR
	WiFi.


4. Part 4
*****Run ./python3 splitter.py to split the login_credentials.csv in three equal parts.*****

->  Open 4 shells and run ./python3 record_hostA.py, ./python3 record_hostB.py,
	./python3 record_hostC.py, ./python3 record_host_attendance.py, each one in 1 shell.

->	Open a shell ./python3 server.py. The server would request a port that it
    will listen to. Then open a ./python3 client.py and enter the server ip and port.
    The ip is set to 127.0.0.1 and the port is same as that entered in the server.py.

->  The client would prompt user to enter login details which will be sent to the server.py
	which will then set up connections with the record hosts to validate the details and 
	will then connect with record_host_attendance to check whether the student has 
	atleast 80% attendance. If he/she doesn't satisfy this criteria access is denied.

->  The user can exit the client typing EXIT when prompted for username/password. The record
	hosts can be hosted on different ip and ports just by changing the .rtl file.