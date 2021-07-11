# counter.py

import socket
import threading
#####################################



def ConnectServer():
	global server
	global serverip
	global port
	serverip = '192.168.0.100'
	port = 9500
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	server.send('CONN|COUNTER|<<<<<TEST FROM COUNTER>>>>>'.encode('utf-8'))
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
	# data_server = server.recv(1024).decode('utf-8')
	# print('Data from server: ', data_server)

def ThreadSendData(data):
	task = threading.Thread(target=SendData,args=[data])
	task.start()

#####################################
from tkinter import *
from tkinter import ttk

allmenu = {'C101':{'code':'C101','title':'ไก่ไม่มีกระดูก','price':45},
		   'C102':{'code':'C102','title':'ไก่ทอดออริจินอล','price':42},
		   'C103':{'code':'C103','title':'ไก่ย่างสูตรพิเศษ','price':50},
		   'C104':{'code':'C104','title':'ขนมปัง','price':20},
		   'C105':{'code':'C105','title':'เบอร์เกอร์ไก่','price':60},
		   'C106':{'code':'C106','title':'เบอร์เกอร์ปลา','price':70},
		   'C107':{'code':'C107','title':'น้ำอัดลมเล็ก','price':45},
		   'C108':{'code':'C108','title':'น้ำอัดลมใหญ่','price':60}}

GUI = Tk()
GUI.title('Counter')
GUI.geometry('1020x700+50+50')
#GUI.state('zoomed')

FT = Frame(GUI)
Tab = ttk.Notebook(FT,width=400,height=400)

T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(expand=1)
FT.place(x=50,y=50)

Tab.add(T1,text='Menu')
Tab.add(T2,text='All Menu')

# Tab 1

# B1 = ttk.Button(T1,text='ไก่ไม่มีกระดูก')
# B1.grid(row=0,column=0,ipady=20,ipadx=20)

# B2 = ttk.Button(T1,text='ไก่ทอดออริจินอล')
# B2.grid(row=0,column=1,ipady=20,ipadx=20)

# B3 = ttk.Button(T1,text='ไก่ย่างสูตรพิเศษ')
# B3.grid(row=0,column=2,ipady=20,ipadx=20)

current_table = {}


def UpdateTable():
	# clear old data
	table.delete(*table.get_children())
	for mn in current_table.values():
		table.insert('','end',value=mn)


def AddItem(CODE):
	#print(allmenu[CODE])
	item = allmenu[CODE]
	if CODE not in current_table:
		data = [item['code'],item['title'],item['price'],1,item['price']]
		current_table[CODE] = data
	else:
		data = current_table[CODE]
		cal = data[2] * (data[3] + 1)
		data[3] = data[3] + 1 # update quantity
		data[4] = cal # update total
		current_table[CODE] = data
	print(current_table)
	UpdateTable()
	#table.insert('','end',value=data)

rownumber = 0
columnnumber = 0
for i,mn in enumerate(allmenu.values(),start=1):
	B = ttk.Button(T1,text=mn['title'],width=20,command= lambda x=mn['code']: AddItem(x))
	B.grid(row=rownumber,column=columnnumber,ipady=20)
	columnnumber +=1
	if i % 3 == 0:
		rownumber += 1
		columnnumber = 0


# Table
header = ['CODE','TITLE','PRICE','QUAN','TOTAL']
table = ttk.Treeview(GUI,columns=header, show='headings',height=20)
table.place(x=480,y=80)

for hd in header:
	table.heading(hd,text=hd)

hwidth = [70,200,80,80,80]
for w,hd in zip(hwidth, header):
	table.column(hd,width=w)

# BUTTON for Order

ordernumber = 101

v_ordernumber = StringVar()
v_ordernumber.set('#{}'.format(ordernumber))
Lordernumber = ttk.Label(GUI,textvariable=v_ordernumber,font=('Impact',30),foreground='green')
Lordernumber.place(x=800,y=20)


def ClearTable():
	global current_table # reset outside function
	table.delete(*table.get_children())
	current_table = {}


def Order():
	global ordernumber
	# convert dict to str
	text = 'ORDER|{}|'.format(ordernumber)
	for mn in current_table.values():
		txt = 'C={},Q={}|'.format(mn[0],mn[3])
		text += txt
	print('TEXT:',text)
	ThreadSendData(text)
	ClearTable()
	
	ordernumber += 1
	v_ordernumber.set('#{}'.format(ordernumber))

BFRAME = Frame(GUI)
BFRAME.place(x=750,y=550)
BOrder = ttk.Button(BFRAME,text='ORDER',width=30,command=Order)
BOrder.pack(ipady=30)



GUI.mainloop()