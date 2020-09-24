import sys
import socket
import errno
from time import sleep
import threading 
import thread
import re
from datetime import *
import time

FREQUENCE=20 #20Hz
timeToSleep=1.0/FREQUENCE #50ms

#~ from threading import Thread, Lock

tempList = []

old_len = 0

thing = []

text_file = open('MARACATI2_454_gdat_TESTE.txt', "rU")

lst = text_file.readlines()
text_file.close()

radardata 		= []

#~ Radar Shit
print len(lst)
for line in lst:
    thing.append(line.replace("\n", "").split(','))

#~ k[7] + ";" + k[5] + ";" + k[6] + ";"
#~ DA            SA            GA

for k in thing:
#	DA = 
#	if k[7] == "D":
#		DA
#~                0                    1                      2                        3                       4                        5                       6                        7                       8                           9                      10                   11                   12                   13                     14                    15                      16                      17     
    msg = k[0] + ";" + "0" + ";" + k[16] + ";" + k[17] + ";" + k[18] + ";" + k[11] + ";" + k[10] + ";" + k[12] + ";" + "0000" + ";" + k[8] + ";" + k[9] + ";" + "1" + ";" + k[7] + ";" + k[5] + ";" + k[6] + ";" + k[13] + ";" + k[14] + ";" + k[15] + ";" + k[3] + ";" + k[0]
    msg = re.sub(r"\s", "", msg)
    msg += "\n"
    radardata.append(msg)
#~ Radar Shit

def mdtbchandler():
	while 1:
		cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		cs.sendto('<MDTE|201|400|UDP|192.168.2.201|5553>', ('255.255.255.255', 7777))
		sleep(1)

#~ <L|28102013|090758370|230000000|050500000|1|030105000|1|1|1>
def mdthandler(clientsock,addr):
    while 1:

		today = datetime.now()
		clientsock.send("<L|" + today.strftime('%d%m%Y') + "|" + today.strftime('%H%M%S%f')[:-3] + "|230000000|050500000|1|030105000|1|1|1>")
		sleep(0.1)

def radarhandler(clientsock,addr):
        print 'Iniciando lancamento ...'
        sleep(10)
        for t in radardata:
          while ((datetime.now().microsecond/1000)%50)!=0:
                 continue
          clientsock.send(t)
          sleep(0.001)


def mdt(serversock):
	thread.start_new_thread(mdtbchandler, ())
	while 1:
		print 'waiting for connection... port 5555'
		clientsock, addr = serversock.accept()
		print '...connected from:', addr
		thread.start_new_thread(mdthandler, (clientsock, addr))

def radar(serversock):
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(radarhandler, (clientsock, addr))


if __name__=='__main__':
    BUFSIZ = 128

    RADHOST = '0.0.0.0'
    RADPORT = 5555
    RADADDR = (RADHOST, RADPORT)
    RADserversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    RADserversock.bind(RADADDR)
    RADserversock.listen(2)
    thread.start_new_thread(radar, (RADserversock,))


    while 1:
        sleep(1)

