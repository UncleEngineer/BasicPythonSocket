# monitor
import socket
import threading

def UpdateDataFromServer(server):
	global current_index
	while True:
		data_server = server.recv(1024).decode('utf-8')
		# COOKING|103|
		data_server = data_server.split('|')
		if data_server[0] == 'COOKING':
			odnumber = data_server[1] #ODID
			current = v_cooking.get()
			v_cooking.set('{}#{} | '.format(current,odnumber))
		elif data_server[0] == 'FINISH':
			odnumber = data_server[1]
			current = v_finish.get()
			v_finish.set('{}#{} | '.format(current,odnumber))
			cooking_current = v_cooking.get()
			replace = '#{} | '.format(odnumber)
			v_cooking.set(cooking_current.replace(replace,''))


def ConnectServer():
	global server
	global serverip
	global port
	serverip = '192.168.0.100'
	port = 9500
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	#print('Server Status: Connected')

	# run message from data
	task = threading.Thread(target=UpdateDataFromServer,args=[server])
	task.start()


	server.send('CONN|MONITOR|<<<<<TEST FROM MONITOR>>>>>'.encode('utf-8'))
	data_server = server.recv(1024).decode('utf-8')
	print('Status: ',data_server)

def ThreadConectServer():
	task = threading.Thread(target=ConnectServer)
	task.start()


try:
	ThreadConectServer()
except Exception as e:
	print('Server Error')
	print('ERROR:',e)

def SendData(data):
	server.send(data.encode('utf-8'))
	

def ThreadSendData(data):
	task = threading.Thread(target=SendData,args=[data])
	task.start()



from tkinter import *
from tkinter import ttk


GUI = Tk()
GUI.title('Monitor')
GUI.geometry('1020x700+50+50')


L = ttk.Label(GUI,text='กำลังทำอาหาร...',font=(None,40),foreground='orange')
L.pack()

v_cooking = StringVar()
result1 = ttk.Label(GUI,textvariable=v_cooking,font=(None,40))
result1.pack()


L = ttk.Label(GUI,text='เสร็จแล้ว...',font=(None,40),foreground='green')
L.pack()

v_finish = StringVar()
result1 = ttk.Label(GUI,textvariable=v_finish,font=(None,40))
result1.pack()

GUI.mainloop()