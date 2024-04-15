;  -------------------------------------------------
;  File: AMB_ScaraConfig_IR.g
;   Path: "0:/sys/AMB/Calibration/"
;  
;   Date: 4/10/2024
;  
;   Version: 1.0.0
;  
;   Description: Loads the defined values for the Duet3D IR Probe Scara configuration. (Called in bed.g)
;   
;   Global Variables Used:
;       XXXXXXXXXXXXXXXXXXXX
;       
;       
;  -------------------------------------------------

M118 P0 S"AMB_ScaraConfig_IR.g" L1
G90 ; absolute positioning (may not be needed)
; M669