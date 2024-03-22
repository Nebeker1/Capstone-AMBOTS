from duet_http import get_reply_sequence, recieve_reply, get_duet_status, download_file, send_gcode_command
import sys
import datetime
import time
import os

DUET_IP = '192.168.0.136'

SZP_ABL_CMD = 'G32 K1'
BLTOUCH_ABL_CMD = 'G32 K0'
ITERATIONS = 1

def check_connection(duet_ip):
	#check if connection to duet can be established
	if get_duet_status(duet_ip) is None:
		print('Error connecting to Duet')
		return False
	return True

def create_info_file(save_path):
	# create a file to store the information about the heightmaps
	file_path = os.path.join(save_path, 'info.txt')
	with open(file_path, 'w') as file:
		file.write('Heightmap Information' + '\n')
		file.write('Date: ' + datetime.datetime.now().strftime("%Y-%m-%d") + '\n')
		file.write('Time: ' + datetime.datetime.now().strftime("%H:%M:%S") + '\n')
		file.write('Number Of Scans: ' + str(ITERATIONS) + '\n')
		file.write('Probe Type: _____' + '\n')
		file.write('Points Probed: _____' + '\n')
		file.write('Trigger Height: _____' + '\n')
		file.write('Feed Rate: _____' + '\n')
		file.write('Drive Level: _____' + '\n')
		file.write('Offset: _____' + '\n')
		file.write('Bed Material: _____' + '\n')

def create_save_path():
	save_path = os.path.join(os.path.dirname(__file__), f'heightmaps/{datetime.datetime.now().strftime("%Y-%m-%d")}')
	if not os.path.exists(save_path):
		os.makedirs(save_path, exist_ok=False)
		create_info_file(save_path)
		return save_path
	else:
		for i in range(1, 100):
			save_path = os.path.join(os.path.dirname(__file__), f'heightmaps/{datetime.datetime.now().strftime("%Y-%m-%d")}_{i}')
			if not os.path.exists(save_path):
				os.makedirs(save_path, exist_ok=False)
				create_info_file(save_path)
				return save_path

def save_heightmap(duet_ip, save_path, coefficients, itr):
	file_path = os.path.join(save_path, f'heightmap_{itr}.csv')
	download_file(duet_ip, '/sys/heightmap.csv', file_path)
	#append the coefficients section to the file
	with open(file_path, 'a') as file:
		file.write('coefficients,\n')
		file.write(coefficients)

def perform_abl(duet_ip, abl_cmd, save_path, itr):
	last_seq = get_reply_sequence(duet_ip)
	current_seq = last_seq
	response = ''
	coefficients = ''
	print(send_gcode_command(duet_ip, abl_cmd))
	print(get_reply_sequence(duet_ip))
	print(recieve_reply(duet_ip))

	while True:
		time.sleep(1)
		current_seq = get_reply_sequence(duet_ip)
		if current_seq > last_seq:
			last_seq = current_seq
			response = recieve_reply(duet_ip)
			print(response)
			#check if there was an error
			if 'Error' in response:
				print('Error in response')
				sys.exit(1)
			if 'coefficients' in response:
				coefficients = response
		
		# check if the printer is idle. indicates that the scan is complete
		if get_duet_status(duet_ip).get('status', None) == 'I':
			print('Duet is idle, command complete')
			break
	# download the heightmap, and decrement the iterations
	save_heightmap(duet_ip, save_path, coefficients, itr)


if __name__ == "__main__":
	create_save_path()
	if check_connection(DUET_IP):
		save_path = create_save_path()
		if save_path is not None:
			for i in range(ITERATIONS):
				perform_abl(DUET_IP, SZP_ABL_CMD, save_path, i)
				# perform_abl(DUET_IP, BLTOUCH_ABL_CMD, save_path, i)
	else:
		sys.exit(1)
