; bed.g (UPDATED FOR SZP)
; called to perform automatic bed compensation via G32
M18 E0		                                                        ; Turn off extruder motor (otherwise BLTouch doesn't respond)
M118 P0  S"bed.g" L3
G90                                                               ; absolute positioning
M561                                                              ; Cancel any existing bed compensation

G29 S2                                                            ; Disable bed mesh compensation

if exists(param.K) & param.K=1
  if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g")
    echo "SZP"
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g"           ; Call the custom M669 parameters for the Scanning Z Probe.
    M98 P"0:/sys/homeall_NoPark.g"
  else
    echo "SZP Scara Config not found"
  M557 X40:510 Y40:210 P24:8                                      ; Set the grid size and number of points    
  G1 z10                                                          ; Move to start position          
  G1 X40 Y40
  G30
  G1 Z10                                                          ; to avoid backlash
  M558.1 K1 S4                                                    ; This handles the reading v. height calibration.
  M203 X5000.00 Y5000.00 Z200 E6000.00                            ; Scan Speed
  M201 X2000.00 Y2000.00 Z30.00 E50                               ; Scan Acceleration 
  G29 S0 K1                                                       ; Call bed leveling using SZP
elif exists(param.K) & param.K=2
  if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_IR.g")
    echo "IR"
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_IR.g"            ; Call the custom M669 parameters for the IR Probe.
    M98 P"0:/sys/homeall_NoPark.g"
  else
    echo "IR Scara Config not found"
  M557 X40:510 Y40:210 P7:5                                      ; Set the grid size and number of points
  M203 X5000.00 Y5000.00 Z200 E6000.00                            ; Move Speed
  M201 X2000.00 Y2000.00 Z30.00 E50                               ; Move Acceleration 
  G1 z15 
  G1 X40 Y40
  G30 K2
  G29 S0 K2
else 
  if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_BLTouch.g")
    echo "BLTouch"
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_BLTouch.g"       ; Call the custom M669 parameters for the BLTouch.
    M98 P"0:/sys/homeall_NoPark.g"
  else
    echo "BLTouch Scara Config not found"
  M557 X40:510 Y40:210 P7:5                                       ; Set the grid size and number of points
  M203 X5000.00 Y5000.00 Z200 E6000.00                            ; Move Speed
  M201 X2000.00 Y2000.00 Z30.00 E50                               ; Move Acceleration 
  G1 z10 
  G29 S0 K0                                                       ; Call bed leveling using BLTouch
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
