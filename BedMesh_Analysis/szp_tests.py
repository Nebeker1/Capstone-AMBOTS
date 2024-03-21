from duet_http import *
import sys
import datetime
import os

DUET_IP = '192.168.0.136'

SZP_ABL_CMD = 'G32 K1'
BLTOUCH_ABL_CMD = 'G32 K0'
ITERATIONS = 1

if __name__ == "__main__":
	absolute_path = os.path.dirname(__file__)
	save_path = os.path.join(absolute_path, f'heightmaps/{datetime.datetime.now().strftime("%Y-%m-%d")}')
	os.makedirs(save_path, exist_ok=True)
	last_seq = get_reply_sequence(DUET_IP)
	current_seq = last_seq
	response = ''
	coefficients = ''
	iterations = ITERATIONS
	while iterations > 0:
		idle = False
		print(send_gcode_command(DUET_IP, SZP_ABL_CMD))
		print(get_reply_sequence(DUET_IP))
		print(recieve_reply(DUET_IP))

		while not idle:
			time.sleep(1)
			current_seq = get_reply_sequence(DUET_IP)

			if current_seq > last_seq:
				last_seq = current_seq
				response = recieve_reply(DUET_IP)
				print(response)
				
				#check if there was an error
				if response.find('Error') != -1:
					print('Error in response')
					sys.exit(1)
				
				# check if the scan was successful
				elif response.find('Height map saved') != -1:
					print('Command successful')

				elif response.find('coefficients') != -1:
					coefficients = response
				# check if the printer is idle
				if get_duet_status(DUET_IP).get('status', None) == 'I':
					print('Duet is idle')
					idle = True
		# download the heightmap, and decrement the iterations
		file_path = os.path.join(save_path, f'heightmap_{iterations}.csv')
		download_file(DUET_IP, '/sys/heightmap.csv', file_path)
		#append the coefficients to the file
		file = open(file_path, 'a')
		file.write(coefficients)
		file.close()
		iterations -= 1
