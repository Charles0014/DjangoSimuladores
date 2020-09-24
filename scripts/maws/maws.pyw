import sys
import socket
import errno
from time import sleep
import threading 
import thread
import re
from datetime import *
import os

tempList = []

old_len = 0

PATH = os.path.abspath(os.getcwd())

file = open('{}/scripts/maws/maws.bin'.format(PATH), "bU")
lst = file.read()
file.close()

# Handler que ira lidar com as conexões
def mawsHandler(clientsock,addr):
	print "Iniciando mawsHandler"
	while 1:
		for t in lst:
			clientsock.send(t)
			print t
		sleep(1)


def maws(serversock):
    while 1:
        print 'Esperando conexão...'
        clientsock, addr = serversock.accept()
        print '...conectado! ', addr
        thread.start_new_thread(mawsHandler, (clientsock, addr))
			
if __name__ == '__main__':
	print "Iniciando mock do MAWS"
	print "Porta: 6006"
	HOST_MAWS = '0.0.0.0'
	PORT_MAWS = 6006
	MAWS_ADDR = (HOST_MAWS, PORT_MAWS)
	socketMAWS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketMAWS.bind(MAWS_ADDR)
	socketMAWS.listen(2)
	thread.start_new_thread(maws, (socketMAWS,))
	
	while 1:
		sleep(1)