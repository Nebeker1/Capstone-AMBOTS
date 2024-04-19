# Ambots First Layer Check Gcode Converter

# To run program run python3 ir_convert.py <gcode file>
# Line 190 of ir_convert should have the new text

import os
import sys

# Take in Original Gcode File
read = ''
file_original = sys.argv[1]
file_name = file_original.split(".gcode")[0]

readingfile = open(file_original)

# List to hold the entire original Gcode text
text_list = []

# Gcode text to run IR probe
L1_text = []
L2_text = []

# Variable to hold number of layer changes
layer_change_count = 0

# Variable to hold add location for ir probe text
L1_index = 0
L2_index = 0

# Current line while reading text
now = " "

# Line number of current text
line_number = 0

minY = 9999
minX = 9999
maxX = 0
maxY = 0

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


# Read until end of file
while now:

    now = readingfile.readline()

    if "G10" in now:
        now = "G10 S210 R210 P0\n"

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
    
    
    # Check for layer change
    if now == ";LAYER_CHANGE\n":
        layer_change_count += 1
        if layer_change_count == 1:
            L1_index = line_number +2 #add 2 to account for remaining layer change comments
        if layer_change_count == 2:
            L2_index = line_number +2
        print(line_number)

    line_number += 1

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

bed_size = "M557 X" + str(minX) + ":" + str(maxX) + " Y" + str(minY) + ":" + str(maxY) + " P8:6"
L1_text.append('var loopControl = 0\n')
L1_text.append(f'{bed_size}\n')
L1_text.append('M98 P"0:/sys/AMB/Macros/AMB_IRTest.g"\n')
L1_text.append('M118 S"Preliminary Scan Complete"\n')
L1_text.append(f'G1 X{str(minX)} Y{str(minY)} Z15 \n')
L1_text.append('G30\n')

L2_text.append('M98 P"0:/sys/AMB/Macros/AMB_IRTest.g"\n')
L2_text.append('M118 S"First Layer Scan Complete"\n')
L2_text.append('M400\n')
L2_text.append('M291 R"First Layer Scan Complete" P"Press OK to continue" S3 T5')
L2_text.append('if (input == 1)\n')
L2_text.append('\tabort "aborted by user choice"\n')
L2_text.append(f'G1 X{str(minX)} Y{str(minY)} Z15 \n')
L2_text.append('G30\n')

# Define random points to scan
#print(randomPoints)

# New file name is original with additional text
new_file_name = file_name + '_ir_convert.gcode'

# Open new file to write
write = open(new_file_name,"w")

line_number = 0

# Write the text list
for x in text_list:
    write.write(x)
    # If the line number is equal to the add location write the new text list
    if line_number == L1_index:
        write.writelines("\n;___Begin L1 Gcode insertion___\n")
        write.writelines(L1_text)
        write.writelines(";___End L1 Gcode insertion___\n\n")
    if line_number == L2_index:
        write.writelines("\n;___Begin L2 Gcode insertion___\n")
        write.writelines(L2_text)
        write.writelines(";___End L2 Gcode insertion___\n\n")
    line_number += 1

write.close()