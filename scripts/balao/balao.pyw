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

old_len = 0
balaoData = []
thingBalao = []

PATH = os.path.abspath(os.getcwd())
PATH_ = '{}/scripts'.format(PATH) 

text_fileBalao = open('{}/balao/Sonda.dat'.format(PATH_), "rU")

lstBalao = text_fileBalao.readlines()
text_fileBalao.close()

print len(lstBalao)
for kBalao in lstBalao:
#	DA = 
#	if k[7] == "D":
#		DA
#~                0                    1                      2                      
    kBalao += "\n"
    balaoData.append(kBalao)


def balaohandler(clientsock,addr):
        sleep(2)
        for t in balaoData:
            clientsock.send(t)
            sleep(1)
            #sleep(0.01)

def balao(serversock):
    while 1:
        print "Porta: ",BALAOPORT
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(balaohandler, (clientsock, addr))
		
if __name__=='__main__':
    BUFSIZ = 128

BALAOHOST = '0.0.0.0'
BALAOPORT = 6000
BALAODR = (BALAOHOST, BALAOPORT)
BALAOserversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BALAOserversock.bind(BALAODR)
BALAOserversock.listen(2)
thread.start_new_thread(balao, (BALAOserversock,))

while 1:
    sleep(1)
