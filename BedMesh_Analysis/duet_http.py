# Description: A module for interfacing with the Duet Web Control API
# Author: Capstone Team 9
# Date: Spring 2024

import requests
import datetime
import time

DUET_IP = '192.168.0.136'

def connect_to_duet(duet_ip):
	# Get the current time in the format the Duet expects
	current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

	url = f'http://{duet_ip}/rr_connect'
	params = {
		'password': 'reprap',  # Default password, replace if custom
		'time': current_time, 
	}
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		return response.json()
	except requests.RequestException as e:
		print(f"Error connecting to Duet: {e}")
		return None
	
def disconnect_from_duet(duet_ip):
	url = f'http://{duet_ip}/rr_disconnect'
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.json()
	except requests.RequestException as e:
		print(f"Error disconnecting from Duet: {e}")
		return None

def get_duet_status(duet_ip):
	url = f'http://{duet_ip}/rr_status?type=3'
	try:
		response = requests.get(url)
		response.raise_for_status()
		status = response.json()
		return status
	except requests.RequestException as e:
		print(f"Error fetching status from Duet: {e}")
		return None

def get_reply_sequence(duet_ip):
	url = f'http://{duet_ip}/rr_model?key=seqs'
	try:
			response = requests.get(url)
			response.raise_for_status()
			data = response.json()
			return data.get('result', {}).get('reply', None)
	except requests.RequestException as e:
			print(f"Error fetching reply sequence: {e}")
			return None
		
def recieve_reply(duet_ip):
	url = f'http://{duet_ip}/rr_reply'
	try:
		response = requests.get(url)
		response.raise_for_status()
		return response.text
	except requests.RequestException as e:
		print(f"Error fetching reply from Duet: {e}")
		return None

def download_file(duet_ip, filepath, savepath):
	url = f'http://{duet_ip}/rr_download'
	params = {
		'name': filepath
	}
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		with open(savepath, 'wb') as file:
			file.write(response.content)
		return True
	except requests.RequestException as e:
		print(f"Error downloading file from Duet: {e}")
		return False
	

def send_gcode_command(duet_ip, gcode):
	url = f'http://{duet_ip}/rr_gcode'
	params = {
		'gcode': gcode
	}
	try:
		response = requests.get(url, params=params)
		response.raise_for_status()
		print(recieve_reply(duet_ip))
		return response.json()
	except requests.RequestException as e:
		print(f"Error sending G-Code to Duet: {e}")
		return None

if __name__ == "__main__":
	pass	
	# print(send_gcode_command(DUET_IP, 'M115'))
	# print(get_reply_sequence(DUET_IP))
	# print(recieve_reply(DUET_IP))
	# print(connect_to_duet(DUET_IP))
	# print(get_duet_status(DUET_IP))
	# print(download_file(DUET_IP, '/sys/heightmap.csv', 'saved_heightmap.csv'))
	# print(disconnect_from_duet(DUET_IP))