; bed.g (UPDATED FOR SZP)
; called to perform automatic bed compensation via G32
M18 E0		                                                        ; Turn off extruder motor (otherwise BLTouch doesn't respond)
M118 P0  S"bed.g" L3
G90                                                               ; absolute positioning
M561                                                              ; Cancel any existing bed compensation

M557 X20:530 Y20:230 P8:6

if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g")
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_SZP.g"           ; Call the custom M669 parameters for the Scanning Z Probe.
 
M98 P"0:/sys/homeall_NoPark.g"                                    ; Home all - Does G28 but doesn't park the arm

;M557 is done in config.g for standard printer,
; if nonstandard printer then M557 should be sent to define grid for bed leveling (this printer uses leveling experimental macro)
G1 F200 
G1 z20  
G1 F3000 
 
G29 S2                                                            ;Disable mesh bed compensation and clear the height map (also clears the map of invalid probe points in builds that support it) compensation


;---------------------------------------------------------------------------
; Scanning Z Probe Bed Leveling

G1 X0 Y0 F30000
G30
if exists(param.K) & param.K=1
  G1 Z6                                                           ; to avoid backlash
  M558.1 K1 S1.7                                                  ; This handles the reading v. height calibration. May need to change S value depending on trigger height from config file (G31 Z##).
G29 S0 K1                                                         ; Call bed leveling using SZP
G1 X0 Y-150 F18000

; END of Scanning Z Probe Bed Leveling
;---------------------------------------------------------------------------

if fileexists("0:/sys/AMB/Calibration/AMB_ScaraConfig_HotEnd.g")
    M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_HotEnd.g" 			  ; Call the custom M669 parameters


M561                                                              ; Cancel any existing bed compensation

G28                                                               ; home all

M375                                                              ; activate heightmap and bed leveling
G29 S1
 
G1 Z40 F200                                                       ; move up 
M400
