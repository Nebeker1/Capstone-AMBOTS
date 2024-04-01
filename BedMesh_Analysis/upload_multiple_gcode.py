# Description: A script to read a GCode file and send individual commands within file to Duet.
# Author: Capstone Team 9
# Date: Spring 2024

from duet_http import send_gcode_command, get_duet_status
import sys
import time

DUET_IP = '192.168.0.136'

def check_connection(duet_ip):
    if get_duet_status(duet_ip) is None:
        print("ERROR: Cannot connect to Duet.")
        return False
    return True

def get_gcode_list(filename):
    try:
        file = open(filename, 'r')
    except Exception as e:
        print("ERROR: Could not find file with name <" + filename + ">.")
        sys.exit(0)
    
    g_code = []

    lines = file.readlines()
    for line in lines:
        if (line[0] != ';'): # if line isn't a comment
            if ';' in line: # parse comment out of line if it has one.
                parsed_line = line.split(';', 1)
                parsed_line[0] = parsed_line[0].rstrip(' ')
                g_code.append(parsed_line[0])
            else: # otherwise remove the newline character and add the GCode line to list.
                line = line.rstrip('\n')
                if (line != ''):
                    g_code.append(line)
    return g_code

if __name__ == "__main__":

    filename = ""

    try:
        filename = sys.argv[1]
    except:
        print("ERROR: No filename entered to read GCode.")
        sys.exit(0)

    g_code = get_gcode_list(filename)

    if check_connection(DUET_IP):
        for single_g_code in g_code:
            send_gcode_command(DUET_IP, single_g_code)
            time.sleep(1) # May not be needed.
    else:
        sys.exit(0)
