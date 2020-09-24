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
file = open('{}/scripts/thomson/thomsonLog01Radar.bin'.format(PATH), "rU")

lst = file.read()
file.close()

# Handler que ira lidar com as conexões
def thomsonHandler(clientsock,addr):
	print "Iniciando thomsonHandler"
	while 1:
		clientsock.send(lst)
		sleep(0.5)

def radar(serversock):
    while 1:
        print 'Esperando conexão...'
        clientsock, addr = serversock.accept()
        print '...conectado! ', addr
        thread.start_new_thread(thomsonHandler, (clientsock, addr))
			
if __name__ == '__main__':
	print "Iniciando mock do Thomson"
	print "Porta: 8888"
	HOST_RADAR = '0.0.0.0'
	PORT_RADAR = 8888
	RADAR_ADDR = (HOST_RADAR, PORT_RADAR)
	socketRadar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketRadar.bind(RADAR_ADDR)
	socketRadar.listen(2)
	thread.start_new_thread(radar, (socketRadar,))
	
	while 1:
		sleep(1)