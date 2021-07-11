# kitchen.py
import socket
import threading
#####################################


allorder = {}
orderlist = []
currentorder = 0

colorlist = ['#ff0000','#00ff00']

def select_color(check):
	if check == True:
		return colorlist[0]
	else:
		return colorlist[1]

current_index = True



def UpdateDataFromServer(server):
	global current_index
	while True:
		data_server = server.recv(1024).decode('utf-8')
		# ORDER|ONB=103|C=C108,Q=1|C=C107,Q=1|
		data_server = data_server.split('|')
		if data_server[0] == 'ORDER':
			odnumber = data_server[1] #ODID
			allitem = []
			for dt in data_server[2:-1]:
				code = dt.split(',')[0].split('=')[1]
				quan = dt.split(',')[1].split('=')[1]
				title = allmenu[code]['title']

				data = [odnumber,code,title,quan]
				allitem.append(data)
				table.insert('','end',value=data,tag=odnumber) # ****
				c = select_color(current_index)
				table.tag_configure(tagname=odnumber, background=c)
				current_index = not current_index

		
			allorder[odnumber] = allitem
			orderlist.append(odnumber)

			if len(orderlist) == 1:
				# ครั้งแรกเซ็ตรหัสไว้
				v_currentorder.set('#{}'.format(odnumber))






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


	server.send('CONN|KITCHEN|<<<<<TEST FROM KITCHEN>>>>>'.encode('utf-8'))
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

allmenu = {'C101':{'code':'C101','title':'ไก่ไม่มีกระดูก','price':45},
		   'C102':{'code':'C102','title':'ไก่ทอดออริจินอล','price':42},
		   'C103':{'code':'C103','title':'ไก่ย่างสูตรพิเศษ','price':50},
		   'C104':{'code':'C104','title':'ขนมปัง','price':20},
		   'C105':{'code':'C105','title':'เบอร์เกอร์ไก่','price':60},
		   'C106':{'code':'C106','title':'เบอร์เกอร์ปลา','price':70},
		   'C107':{'code':'C107','title':'น้ำอัดลมเล็ก','price':45},
		   'C108':{'code':'C108','title':'น้ำอัดลมใหญ่','price':60}}

GUI = Tk()
GUI.title('Kitchen')
GUI.geometry('1020x700+50+50')



header = ['ORDER-ID','CODE','TITLE','QUAN']
table = ttk.Treeview(GUI,columns=header, show='headings',height=20)
table.place(x=20,y=80)

for hd in header:
	table.heading(hd,text=hd)

hwidth = [70,200,80,80,80]
for w,hd in zip(hwidth, header):
	table.column(hd,width=w)



v_currentorder = StringVar()
result1 = ttk.Label(GUI,textvariable=v_currentorder,font=(None,40))
result1.place(x=550,y=50)

def UpdateTable():
	# clear old data
	table.delete(*table.get_children())
	for od in allorder.values():
		for o in od:
			table.insert('','end',value=o)

def Finish(event=None):
	global orderlist
	order = orderlist[currentorder]
	del orderlist[currentorder]
	del allorder[order]
	# update table
	UpdateTable()
	v_currentorder.set('#{}'.format(orderlist[currentorder]))
	text = 'FINISH|{}'.format(order)
	ThreadSendData(text)



GUI.bind('<F1>',Finish)
GUI.mainloop()