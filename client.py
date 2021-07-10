# client.py

import socket

serverip = '192.168.0.100'
port = 9000

while True:
	data = input('Send message: ')
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

	server.connect((serverip,port))
	server.send(data.encode('utf-8'))

	data_server = server.recv(1024).decode('utf-8')
	print('Data from server: ', data_server)
	server.close()