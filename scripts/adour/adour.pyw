import sys
import socket
import errno
import threading
import thread
import re
import datetime
import os

from time import sleep

tempList = []
old_len = 0
currentIndex=0
FREQUENCE=50
time_to_sleep=FREQUENCE/1000.0
flag = 1

PATH = os.path.abspath(os.getcwd())


#~ Radar Atlas
linesAtlas = []
text_file = open('{}/scripts/atlas/atlas.txt'.format(PATH), "rU")
lst = text_file.readlines()
text_file.close()

def convert_status(status):
	return '0' if status == ' A' else '1' if status == ' M' else '2'

def format_adour_data():
	adour_data = []
	lines_adour = []
	text_file = open('{}/scripts/adour/adour.txt'.format(PATH), "rU")
	
	lst_adour = text_file.readlines()
	text_file.close()
	print('Numero de pontos do radar Adour:', len(lst_adour))
	for line in lst_adour:
		lines_adour.append(line.replace("\n", "").split(','))
	for k in lines_adour:
		msg_adour = "{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}\n".format(
			k[0].strip(),                 # 0   - V_BaseT_SE_Adour_Teste
			"0",                          # 1   -
			k[16].strip(),                # 2   - V_ELE_SE_Adour_Teste
			k[17].strip(),                # 3   - V_AZI_SE_Adour_Teste
			k[18].strip(),                # 4   - V_DST_SE_Adour_Teste
			k[11].strip(),                # 5   - V_AZI_BAND_SE_Adour_Teste
			k[10].strip(),                # 6   - V_ELE_BAND_SE_Adour_Teste
			k[12].strip(),                # 7   - V_DST_BAND_SE_Adour_Teste
			"0000",                       # 8   - V_ZERO_SE_Adour_Teste
			k[8].strip(),                 # 9   - V_TV_SE_Adour_Teste
			k[9].strip(),                 # 10  - V_TRP_SE_Adour_Teste
			"1",                          # 11  -
			convert_status(k[7]).strip(), # 12  - V_DST_EST_SE_Adour_Teste
			convert_status(k[5]).strip(), # 13  - V_ELE_EST_SE_Adour_Teste
			convert_status(k[6]).strip(), # 14  - V_AZI_EST_SE_Adour_Teste
			k[13].strip(),                # 15  - V_SR_SE_Adour_Teste
			k[14].strip(),                # 16  - V_ELE_ERRO_SE_Adour_Teste
			k[15].strip(),                # 17  - V_AZI_ERRO_SE_Adour_Teste
			k[3].strip(),                 # 18  - V_TREL_SE_Adour_Teste
			k[0].strip()                  # 19  - V_TU_SE_Adour_Teste
		)
		adour_data.append(msg_adour)
	return adour_data

def radar_handler(client_sock, addr, radar_data):
	flag = 1
	current_index = 1
	len_data = len(radar_data)
	while flag:
		client_sock.send(radar_data[current_index])
		sleep(time_to_sleep)
		current_index += 1
		if current_index >= len_data:
			current_index = 0
			flag = 0

def radar(server_sock, name):
	while 1:
		print '%s: Waiting for connection...' % name
		client_sock, addr = server_sock.accept()
		print ' ... connected'
		time_to_start = datetime.datetime(
			year = datetime.datetime.now().year,
			month = datetime.datetime.now().month,
			day = datetime.datetime.now().day)
		adour_data = format_adour_data()
		t_adour = threading.Thread(name='radar_adour', target=radar_handler, args=(client_sock, addr, adour_data))
		time_to_start_adour = time_to_start
		print ' ... time to lauch adour is: %s' % time_to_start_adour.strftime("%d/%m/%Y %H:%M:%S.%f")
		while (datetime.datetime.now() < time_to_start):
			sleep(0.1)
		t_adour.start()

if (__name__ == '__main__'):
	buf_siz = 128
	adour_host = '0.0.0.0'
	adour_port = 5555
	adour_addr = (adour_host, adour_port)
	adour_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	adour_server_socket.bind(adour_addr)
	adour_server_socket.listen(1)
	thread.start_new_thread(radar, (adour_server_socket, 'Adour'))

	while 1:
		sleep(0.1)










	