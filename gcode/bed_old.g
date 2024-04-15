; bed.g (UPDATED FOR SZP)
; called to perform automatic bed compensation via G32
M18 E0		                                                        ; Turn off extruder motor (otherwise BLTouch doesn't respond)
M118 P0  S"bed.g" L3
G90                                                               ; absolute positioning
M561                                                              ; Cancel any existing bed compensation

G29 S2 ; Disable bed mesh compensation

if exists(param.K) & param.K=1
  if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g")
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g"           ; Call the custom M669 parameters for the Scanning Z Probe.
    echo "SZP"
else 
  if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_BLTouch.g")
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_BLTouch.g"       ; Call the custom M669 parameters for the Scanning Z Probe.
    echo "BLTouch"
M98 P"0:/sys/homeall_NoPark.g"                                    ; Home all - Does G28 but doesn't park the arm

;M557 is done in config.g for standard printer,
;if nonstandard printer then M557 should be sent to define grid for bed leveling (this printer uses leveling experimental macro)

;Scan Area dependent on sensor
if exists(param.K) & param.K=0
  M557 X40:510 Y40:210 P7:5
if exists(param.K) & param.K=1
  M557 X40:510 Y40:210 P24:8
if exists(param.K) & param.K=2 
  M557 X84:137 Y89:133 P8:6




G1 F200 
G1 z20  
G1 F3000 
G1 X40 Y40 F8000
G30
M203 X5000.00 Y5000.00 Z200 E6000.00                                ; Scan Speeds (Slow)     
M201 X2000.00 Y2000.00 Z30.00 E50                                   ; Scan Accelleration 
 


;---------------------------------------------------------------------------
; Scanning Z Probe Bed Leveling config      
if exists(param.K) & param.K=1            
  G1 Z6                                                           ; to avoid backlash
  M558.1 K1 S4                                                    ; This handles the reading v. height calibration. May need to change S value depending on trigger height from config file (G31 Z##).
; IR Scan Test
if exists(param.K) & param.K=2
  G29 S1 P"heightmap.csv"
  G29 S3 P"temp.csv"
  G29 S2
  G29 S0 K{exists(param.K) ? param.K : 0}
  G29 S3 P"IR_Mesh.csv" K{exists(param.K) ? param.K : 0}
  G29 S1 P"temp.csv" 
  G29 S3 P"heightmap.csv"
else
  G29 S0 K{exists(param.K) ? param.K : 0}                           ; Call bed leveling using SZP
G1 Z10 F18000

; END of Bed Leveling
;---------------------------------------------------------------------------
M203 X9000.00 Y9000.00 Z600 E6000.00                                                           

if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_HotEnd.g")
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_HotEnd.g" 			  ; Call the custom M669 parameters


M561                                                              ; Cancel any existing bed compensation

G28                                                               ; home all

M375   
G29 S1                                                            ; activate heightmap and bed leveling
 
G1 Z40 F200                                                       ; move up 
M400
M568 P0 A2