import Queue
import threading
import time


queue = Queue.Queue()

class QueueTester(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global queue
		while True:
			if not queue.empty():
				print queue.get()
			
for i in range(10):
	queue.put(i)


qt = QueueTester()
qt.daemon = True
qt.start()


time.sleep(5)

for i in range(10):
	queue.put(i)

while True:
	time.sleep(1)


