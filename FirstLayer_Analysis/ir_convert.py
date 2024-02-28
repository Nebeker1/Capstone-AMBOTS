# Ambots First Layer Check Gcode Converter

# To run program run python3 ir_convert.py <gcode file>
# Line 190 of ir_convert should have the new text

import os
import sys

# Take in Original Gcode File
read = ''
file_original = sys.argv[1]

# original file string name
file_string = (str(file_original))

# List to hold original file name with no extention
original_list = []

# Read the original file name string
for x in range (0,len(file_string)):
    if file_string[x] == '.':
        break
    original_list.append(file_string[x])

# Bring original list together as a string.
original_string = ''.join(original_list)

# Add the txt extention to original file
txt_file_name = original_string + '.txt'

# Convert file based on new .txt extention
os.rename(file_original, txt_file_name)

#file_new_name = "active.txt"
readingfile = open(txt_file_name)

# List to hold the entire original Gcode text
text_list = []

# Gcode text to run IR probe
ir_probe_text = ["\n","Place new Gcode Here for First Layer","\n","\n"]

# Variable to hold number of layer changes
layer_change_count = 0

# Variable to hold add location for ir probe text
add_location = 0

# Current line while reading text
now = " "

# Line number of current text
line_number = 0

# Run tell final message line
while now != "; prusaslicer_config = end\n":

    now = str(readingfile.readline())
    text_list.append(now)
    
    # Count Layer Change
    if now == ";LAYER_CHANGE\n":
        layer_change_count += 1

    line_number += 1
    
    if layer_change_count == 1:
        add_location = line_number
        # Ensures add location isn't changed
        layer_change_count == 3

# Return the original file back to gcode
os.rename(txt_file_name, file_original)
readingfile.close()

# New file name is original with additional text
new_file_name = original_string + '_ir_convert.gcode'

# Open new file to write
write = open(new_file_name,"w")

line_number = 0

# Write the text list
for x in text_list:
    write.write(text_list[line_number])

    # If the line number is equal to the add location write the new text list
    if line_number == add_location+2:
        write.writelines(ir_probe_text)

    line_number += 1

write.close()




