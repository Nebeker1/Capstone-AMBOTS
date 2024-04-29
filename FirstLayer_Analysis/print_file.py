# Description: The file can take a GCode file as input and print the GCode file on the printer,
#   allowing user to select if they wish to continue after first layer.
# Author: Capstone Team 9
# Date: Spring 2024

import sys
import time
import os

from BedMesh_Analysis.duet_http import send_gcode_command, upload_file, get_reply_sequence, recieve_reply, download_file

DUET_IP = '192.168.0.106'

def generate_first_layer_info(prelim_scan_filepath, first_layer_scan_filepath):
    # Open the preliminary scan file
    try:
        prelim_file = open(prelim_scan_filepath, 'r')
        first_layer_file = open(first_layer_scan_filepath, 'r')
    except:
        print("ERROR: Could not find file")
        sys.exit(0)
    # Read the preliminary scan file
    prelim_info = prelim_file.readline().split(',')
    first_layer_info = first_layer_file.readline().split(',')
    prelim_file.close()
    first_layer_file.close()

    prelim_mean = float((prelim_info[3])[6:]) 
    first_layer_mean = float((first_layer_info[3])[6:])

    #return answer to 3 decimals
    return f'difference between means: {(first_layer_mean - prelim_mean):.3f} mm'

if __name__ == "__main__":
    filename = ""
    prelim_scan_filepath = os.path.join(os.path.dirname(__file__), 'prelim_scan.csv')
    first_layer_scan_filepath = os.path.join(os.path.dirname(__file__), 'first_layer.csv')
    try:
        filename = sys.argv[1]
    except:
        print("Usage: python print_file.py <filename>")
        print("ERROR: No filename entered.")
        sys.exit(0)
    
    # Send the file to Duet
    file = os.path.join(os.path.dirname(__file__), filename)
    dst_filepath = '/gcodes/' + filename
    upload_file(DUET_IP, file, dst_filepath)

    # Run the file
    print(f"Running file {dst_filepath}...")
    run_gcode = f"M98 P\"{dst_filepath}\""
    send_gcode_command(DUET_IP, run_gcode)
    current_seq =  get_reply_sequence(DUET_IP)
    last_seq = current_seq

    while True:
        time.sleep(1)
        current_seq = get_reply_sequence(DUET_IP)
        if current_seq > last_seq:
            last_seq = current_seq
            response = recieve_reply(DUET_IP)
            print(response)
            # Check if there was an error
            if 'Error' in response:
              print('Error in response')
            elif 'Preliminary Scan Complete' in response:
                download_file(DUET_IP, '/sys/IR_Mesh.csv',  os.path.join(os.path.dirname(__file__), 'prelim_scan.csv'))
            elif 'First Layer Scan Complete' in response:
                download_file(DUET_IP, '/sys/IR_Mesh.csv',  os.path.join(os.path.dirname(__file__), 'first_layer.csv'))
                info = generate_first_layer_info(prelim_scan_filepath, first_layer_scan_filepath)
                send_gcode_command(DUET_IP, f'M291 R"Analysis Complete" P"Data: {info}.' +
                     'Would you like to continue with the print?" K{"Yes","No"} S4\n')
                print('program complete')
                break
