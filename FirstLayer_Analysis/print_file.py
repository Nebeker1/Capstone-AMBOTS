# Description: The file can take a GCode file as input and print the GCode file on the printer,
#   allowing user to select if they wish to continue after first layer.
# Author: Capstone Team 9
# Date: Spring 2024

from ../BedMesh_Analysis/duet_http import send_gcode_command, get_duet_status, upload_file, get_reply_sequence, recieve_reply
import sys
import time
import os
import ctypes

DUET_IP = '192.168.0.136'

def write_new_file(lines, index, new_filename):
    m291_command = "M291 P\"Do you wish to continue the print?\" R\"Duet3D Print\" S3\n"
    try:
        new_file = open(new_filename, 'w')
        new_file.writelines(lines[:index])
        new_file.writelines(m291_command)
        new_file.writelines(lines[index:])
    except:
        print("ERROR: Could not write new files.")
        sys.exit(0)

def get_file_info(filename):
    try:
        file = open(filename, 'r')
    except:
        print("ERROR: Could not find file with name <" + filename + ">.")
        sys.exit(0)

    lines = file.readlines()
    for index, line in enumerate(lines):
        if "G32 K2" in line:
            break
    
    return lines, index+1

if __name__ == "__main__":
    filename = ""

    try:
        filename = sys.argv[1]
    except:
        print("ERROR: No filename entered.")
        sys.exit(0)

    # Get the new updated file
    lines, index = get_file_info(filename)
    pre, ext = os.path.splitext(filename)
    new_filename = pre + "_updated" + ext
    write_new_file(lines, index, new_filename)
    print("New file generated, sending to Duet...")
    
    #Send the updated file to Duet
    file = os.path.join(os.path.dirname(__file__), new_filename)
    dst_filepath = '/gcodes/' + new_filename
    upload_file(DUET_IP, file, dst_filepath)

    # Run the new file
    print(f"Running file {dst_filepath}...")
    run_gcode = f"M98 P\"{dst_filepath}\""
    send_gcode_command(DUET_IP, run_gcode)
