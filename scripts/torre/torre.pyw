import sys
import socket
import errno
from time import sleep
import threading 
import thread
import re
from datetime import *
import os

#~ from threading import Thread, Lock

tempList = []

#~ mutex = Lock()
#~ s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#~ s.connect(('192.168.2.201',8888))
#~ t = Thread(target = parseThomson, args = (tempList,))

old_len = 0

PATH = os.path.abspath(os.getcwd())
file = open('{}/scripts/torre/vento.bin'.format(PATH), "rU")

lst = file.readlines()
file.close()

# Handler que ira lidar com as conexões
def plcHandler(clientsock,addr):
	print "Iniciando plcHandler"
	while 1:
		for t in lst:
			clientsock.send(t)
			sleep(0.001)
		sleep(1)


def plc(serversock):
    while 1:
        print 'Esperando conexão...'
        clientsock, addr = serversock.accept()
        print '...conectado! ', addr
        thread.start_new_thread(plcHandler, (clientsock, addr))
			
if __name__ == '__main__':
	print "Iniciando mock do PLC"
	print "Porta: 7777"
	HOST_PLC = '0.0.0.0'
	PORT_PLC = 7777
	PLC_ADDR = (HOST_PLC, PORT_PLC)
	socketPLC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketPLC.bind(PLC_ADDR)
	socketPLC.listen(2)
	thread.start_new_thread(plc, (socketPLC,))
	
	while 1:
		sleep(1)