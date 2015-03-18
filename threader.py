#! /usr/bin/python

##	This script spawns a user-defined number of threads to sequentially execute a list of shell calls.
##	The shell calls are located in file threadme.txt and each shell call is on a separate line.
##	It also tells you which thread completed which call and when each thread terminated.
##	This is useful for things like multiple STRUCTURE runs.
##	Don't forget to specify the number of threads on the next line!

threads = 4		# User-defined number of threads

import threading
import os
import subprocess

# Only one thread at a time can open the lock
lock = threading.Lock()

# What to do within each spawned thread
def threader():
	# Start next call if threadme.txt still contains calls
	while os.stat('threadme.txt').st_size >0:
		# Only one thread at a time may read/write threadme.txt
		with lock:
			# Read the first call from threadme.txt
			with open('threadme.txt','rb') as f:
				call = f.readline()
			# Delete the first call from threadme.txt
			subprocess.call("tail -n +2 threadme.txt > smaller.tmp",shell=True)
			os.rename("smaller.tmp","threadme.txt")
		# Send the call to the shell
		subprocess.call(call,shell=True)
		if call != "":
			print(threading.current_thread().name + " did call: " + call)
	print(threading.current_thread().name + " terminated")

# Spawn the threads		
for t in range(threads):
	threading.Thread(target = threader).start()
	print("Thread-" + str(t+1) + " spawned")