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
ir_probe_text = ["\n"]

# Variable to hold number of layer changes
layer_change_count = 0

# Variable to hold add location for ir probe text
add_location = 0

# Current line while reading text
now = " "

# Line number of current text
line_number = 0

minY = 9999
minX = 9999
maxX = 0
maxY = 0
countG = 0

xValue = 0
yValue = 0

xValuesList = []
yValuesList = []

readingX = False
readingY = False
endReadingXY = False
startReadingXY = False
mainShape = False

# Select random points for the IR to probe
randomPoints = []


# Read until final message line
while now != "; prusaslicer_config = end\n":

    now = str(readingfile.readline())
    text_list.append(now)
    
    if now == ";END gcode for filament\n":
        endReadingXY = True
        
    if now == ";TYPE:Perimeter\n":
        mainShape = True
        
    
    if endReadingXY == False and mainShape == True:
        for x in range (0, len(now)):
        
            if readingX == True and now[x] == ' ':
            
                readingX = False
        
            if readingX == True:
                xValuesList.append(now[x])
        
            if now[x] == 'X':
                readingX = True
                
                
            if readingY == True and now[x] == ' ' or now [x] == '\n':
                readingY = False
        
            if readingY == True:
                yValuesList.append(now[x])
        
            if now[x] == 'Y' and now[x+1].isnumeric() == True:
                readingY = True
    
    
    if len(xValuesList) > 0:
        startReadingXY = True
        xValue = ''.join(xValuesList)
        xValue = float(xValue)
        xValuesList.clear()
        
    
    if len(yValuesList) > 0:
        startReadingXY = True
        yValue = ''.join(yValuesList)
        yValue = float(yValue)
        yValuesList.clear()
        
    
    if endReadingXY == False and startReadingXY == True and line_number % 40 == 0:
        
        if (xValue,yValue) not in randomPoints:
            randomPoints.append((xValue,yValue))
    

    if xValue > maxX and endReadingXY == False and startReadingXY == True:
        maxX = xValue
        
    if xValue < minX and endReadingXY == False and startReadingXY == True:
        minX = xValue
        
    if yValue > maxY and endReadingXY == False and startReadingXY == True:
        maxY = yValue
        
    if yValue < minY and endReadingXY == False and startReadingXY == True:
        minY = yValue
    
    
    # Count Layer Change
    if now == ";LAYER_CHANGE\n":
        layer_change_count += 1

    line_number += 1
    
    if layer_change_count == 1:
        add_location = line_number
        # Ensures add location isn't changed
        layer_change_count == 3

readingfile.close()

maxX = round(maxX,0)
maxX = int(maxX)

minX = round(minX,0)
minX = int(minX)

maxY = round(maxY,0)
maxY = int(maxY)

minY = round(minY,0)
minY = int(minY)


print("Max X value: " + str(maxX))
print("Min X value: " + str(minX))

print("Max Y value: " + str(maxY))
print("Min Y value: " + str(minY))

bed_size = "M557 X" + str(minX) + ":" + str(maxX) + " Y" + str(minY) + ":" + str(maxY) + " P24:8"
ir_probe_text.append(bed_size)
ir_probe_text.append("\n")
ir_probe_text.append("G32 K2")
ir_probe_text.append("\n")

# Define random points to scan
#print(randomPoints)

# Return the original file back to gcode
os.rename(txt_file_name, file_original)


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




