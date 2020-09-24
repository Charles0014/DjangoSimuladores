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

def convert_status(status):
	return '0' if status == ' A' else '1' if status == ' M' else '2'

def format_telemetry_data():
	telemetry_data = []
	
	lines_telemetry = []
	text_file = open('{}/scripts/cortex/20200519_104658.pickle.all.channel.30seg'.format(PATH), "rU")
	lst_telemetry = text_file.readlines()
	text_file.close()
	for line in lst_telemetry:
		lines_telemetry.append(line)
	for k in lines_telemetry:
		telemetry_data.append(k)
	return lines_telemetry

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
		if (name == 'Telemetry'):
			telemetry_data = format_telemetry_data()
			t_telemetry = threading.Thread(name='radar_telemetry', target=radar_handler, args=(client_sock, addr, telemetry_data))
			t_telemetry.start()


if (__name__ == '__main__'):
	buf_siz = 128
	telemetry_host = '0.0.0.0'
	telemetry_port = 3070
	telemetry_addr = (telemetry_host, telemetry_port)
	telemetry_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	telemetry_server_socket.bind(telemetry_addr)
	telemetry_server_socket.listen(1)
	thread.start_new_thread(radar, (telemetry_server_socket, 'Telemetry'))

	while 1:
		sleep(0.1)
