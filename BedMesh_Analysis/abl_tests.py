from duet_http import get_reply_sequence, recieve_reply, get_duet_status, download_file, send_gcode_command
import numpy as np
import sys
import datetime
import time
import os

DUET_IP = '192.168.0.106'

SZP_ABL_CMD = 'G32 K1'
BLTOUCH_ABL_CMD = 'G32 K0'
IR_ABL_CMD = 'G32 K2'
ITERATIONS = 10

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
		file.write('M558.1: _____' + '\n')
		file.write('Probe Speed: _____' + '\n')
		file.write('Probe Acceleration: _____' + '\n')
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
		if get_duet_status(duet_ip).get('status', {}) == 'I':
			print('Duet is idle, command complete')
			break
	# download the heightmap, and decrement the iterations
	save_heightmap(duet_ip, save_path, coefficients, itr)

def create_file(save_path, file_name, arr, header):
	file_path = os.path.join(save_path, file_name)
	with open(file_path, 'w') as file:
		file.write(header + '\n')
		for row in arr:
			for val in row:
				file.write(str(format(val, '.3f')) + ', ')
			file.write('\n')

def data_analysis(save_path):
	#open heightmap files
	heightmaps = []
	for i in range(ITERATIONS):
		file_path = os.path.join(save_path, f'heightmap_{i}.csv')
		heightmaps.append(file_path)
	#determine the dimensions of the heightmap by reading the last two entries in line 3
	with open(heightmaps[0], 'r') as file:
		lines = file.readlines()
		dimensions = lines[2].split(',')
		y_dim = int(dimensions[-1])
	#array of heightmaps is formatted as [heightmap][y][x]
	#ex: array[0][1][2] would be the z value of the first heightmap at row 2, column 3
	heightmap_values = []
	for heightmap in heightmaps:
		with open(heightmap, 'r') as file:
			tmp_arr = []
			lines = file.readlines()
			lines = lines[3:3+y_dim]
			for i in range(len(lines)):
				z_values = lines[i].split(', ')
				#remove spaces and the newline character
				for j in range(len(z_values)):
					z_values[j] = z_values[j].strip()
				z_values = [float(x) for x in z_values]
				tmp_arr.append(z_values)
			heightmap_values.append(tmp_arr)
	#calculate the standard deviation of each point
	np_array = np.array(heightmap_values)
	std_dev = np.round(np.std(np_array, axis=0),3)
	std_dev = std_dev.tolist()
	create_file(save_path, 'std_dev.csv', std_dev, 'Standard Deviation')
	#calculate the range of each point
	range_arr = np.round(np.ptp(np_array, axis=0),3)
	range_arr = range_arr.tolist()
	create_file(save_path, 'range.csv', range_arr, 'Range')

if __name__ == "__main__":
	if check_connection(DUET_IP):
		save_path = create_save_path()
		if save_path is not None:
			for i in range(ITERATIONS):
				perform_abl(DUET_IP, SZP_ABL_CMD, save_path, i)
				# perform_abl(DUET_IP, BLTOUCH_ABL_CMD, save_path, i)
				# perform_abl(DUET_IP, IR_ABL_CMD, save_path, i)
				pass
			data_analysis(save_path)
	else:
		sys.exit(1)
