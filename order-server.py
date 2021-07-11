# order-server.py
# server.py

import socket
import threading

serverip = '192.168.0.100' #your ip
port = 9500

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

server.bind((serverip,port))
server.listen(1)

def NewConnection(client,conn='KITCHEN'):
	while True:

		try:
			data = client.recv(1024).decode('utf-8')
			print('CLIENT: ',data)
			# ORDER|103|C=C108,Q=1|C=C107,Q=1|
			textsplit = data.split('|')
			if textsplit[0] == 'ORDER':
				if 'KITCHEN' in CONNECTION:
					CONNECTION['KITCHEN'].send(data.encode('utf-8'))
				else:
					print('KITCHEN not found')

				if 'MONITOR' in CONNECTION:
					text = 'COOKING|{}'.format(textsplit[1])
					CONNECTION['MONITOR'].send(text.encode('utf-8'))
				else:
					print('MONITOR not found')
			elif textsplit[0] == 'FINISH':
				if 'MONITOR' in CONNECTION:
					text = 'FINISH|{}'.format(textsplit[1])
					CONNECTION['MONITOR'].send(text.encode('utf-8'))
				else:
					print('MONITOR not found')


		except:
			print('ERROR')
			del CONNECTION[conn]
			print('{} disconnected'.format(conn))


CONNECTION = {}


while True:

	print('Wating for client....')
	client, addr = server.accept() #accept connection from client
	print('Connected from: ',addr)

	data = client.recv(1024).decode('utf-8')
	

	conntext = data.split('|')
	if conntext[0] == 'CONN':
		# CONNECTION['KITCHEN']
		CONNECTION[conntext[1]] = client
	print('CURRENT CONNECTION:',CONNECTION)
	print('First message from client: ',data)
	text = 'Server Connected'
	client.send(text.encode('utf-8'))

	task = threading.Thread(target=NewConnection,args=[client,conntext[1]])
	task.start()
	#client.close()