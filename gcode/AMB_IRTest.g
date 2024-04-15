;  -------------------------------------------------
;  File: AMB_IRTest.g
;   Path: "0:/sys/AMB/Calibration/"
;  
;   Date: 4/10/2024
;  
;   Version: 1.0.0
;  
;   Description: used to scan the first layer of a print defined previously using M557. Will return the heightmap as IR_Mesh.csv
;   
;   Global Variables Used:
;       XXXXXXXXXXXXXXXXXXXX
;       
;       
;  -------------------------------------------------

M18 E0		                                                        ; Turn off extruder motor (otherwise BLTouch doesn't respond)
M118 P0  S"bed.g" L3
G90                                                               ; absolute positioning
M561                                                              ; Cancel any existing bed compensation

G29 S2 ; Disable bed mesh compensation

if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g")
	M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g"           ; Call the custom M669 parameters for the Scanning Z Probe.
	echo "SZP"
else 	
	M291 P"Error: No Scara Config file found" R"Error" S3 T5

M98 P"0:/sys/homeall_NoPark.g"  
G1 z20

G29 S1 P"heightmap.csv"
G29 S3 P"temp.csv"
G29 S2
G29 S0 K2
G29 S3 P"IR_Mesh.csv" K2
G29 S1 P"temp.csv" 
G29 S3 P"heightmap.csv"

M472 P"temp.csv" 	; Delete temp.csv

M203 X9000.00 Y9000.00 Z600 E6000.00                                                           

if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_HotEnd.g")
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_HotEnd.g" 

M98 P"0:/sys/homeall_NoPark.g"
M561
G1 Z20
M400
M568 P0 A2