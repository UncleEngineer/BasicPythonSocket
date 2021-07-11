import time
import threading

def brushteeth(toothpaste):
	for i in range(10):
		print('กำลังแปรงฟัน...ด้วย{}'.format(toothpaste))
		time.sleep(0.5)

def shower():
	for i in range(10):
		print('กำลังอาบน้ำ...')
		time.sleep(1)

t1 = time.time()
# แบบปกติ
# brushteeth()
# shower()

# แบบทำงานพร้อมกัน
task1 = threading.Thread(target=brushteeth,args=['ดอกบัวคู่'])
task2 = threading.Thread(target=shower)

task1.start()
task2.start()
task1.join()
task2.join()

t2 = time.time()

print('All time:',t2-t1)