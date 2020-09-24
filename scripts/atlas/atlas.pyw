import sys
import socket
import errno
import threading
import thread
import re
import os 

from datetime import datetime
from time import sleep

PATH = os.path.abspath(os.getcwd())

tempList = []
old_len = 0
currentIndex=0
FREQUENCE=50
timeToSleep=FREQUENCE/1000.0
flag = 1

def convert_status(status):
	return '0' if status == ' A' else '1' if status == ' M' else '2'

def format_atlas_data():
	atlasData = []
	linesAtlas = []
	text_file_atlas = open('{}/scripts/atlas/atlas.txt'.format(PATH), "rU")
	lst_atlas = text_file_atlas.readlines()
	text_file_atlas.close()
	print('Numero de pontos do radar Atlas:', len(lst_atlas))
	for line in lst_atlas:
		linesAtlas.append(line.replace("\n", "").split(','))
	for k in linesAtlas:
		msg_atlas = "{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(
			k[0].strip(),                 # 0   - V_BaseT_SE_Atlas_Teste
			"0",                          # 1   -
			k[16].strip(),                # 2   - V_ELE_SE_Atlas_Teste
			k[17].strip(),                # 3   - V_AZI_SE_Atlas_Teste
			k[18].strip(),                # 4   - V_DST_SE_Atlas_Teste
			k[11].strip(),                # 5   - V_AZI_BAND_SE_Atlas_Teste
			k[10].strip(),                # 6   - V_ELE_BAND_SE_Atlas_Teste
			k[12].strip(),                # 7   - V_DST_BAND_SE_Atlas_Teste
			"0000",                       # 8   - V_ZERO_SE_Atlas_Teste
			k[8].strip(),                 # 9   - V_TV_SE_Atlas_Teste
			k[9].strip(),                 # 10  - V_TRP_SE_Atlas_Teste
			"1",                          # 11  -
			convert_status(k[7]).strip(), # 12  - V_DST_EST_SE_Atlas_Teste
			convert_status(k[5]).strip(), # 13  - V_ELE_EST_SE_Atlas_Teste
			convert_status(k[6]).strip(), # 14  - V_AZI_EST_SE_Atlas_Teste
			k[13].strip(),                # 15  - V_SR_SE_Atlas_Teste
			k[14].strip(),                # 16  - V_ELE_ERRO_SE_Atlas_Teste
			k[15].strip(),                # 17  - V_AZI_ERRO_SE_Atlas_Teste
			k[3].strip(),                 # 18  - V_TREL_SE_Atlas_Teste
			k[0].strip()                  # 19  - V_TU_SE_Atlas_Teste
    )
		atlasData.append(msg_atlas)
	return atlasData

def radar_handler(clientSock, addr, radarData):
	flag = 1
	currentIndex = 1
	lenData = len(radarData)
	while flag:
		clientSock.send(radarData[currentIndex])
		sleep(timeToSleep)
		currentIndex += 1
		if currentIndex >= lenData:
			currentIndex = 0
			flag = 0

def radar(serversock, name):
	while 1:
		print '%s: Waiting for connection...' % name
		clientsock, addr = serversock.accept()
		print ' ... connected'
		atlasData = format_atlas_data()
		t_atlas = threading.Thread(name='radar_atlas', target=radar_handler, args=(clientsock, addr, atlasData))
		t_atlas.start()

if (__name__ == '__main__'):
	BUFSIZ = 128
	ATLASHOST = '0.0.0.0'
	ATLASPORT = 6666
	ATLASADDR = (ATLASHOST, ATLASPORT)
	ATLASserversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ATLASserversock.bind(ATLASADDR)
	ATLASserversock.listen(1)
	thread.start_new_thread(radar, (ATLASserversock, 'Atlas'))

	while 1:
		sleep(0.1)