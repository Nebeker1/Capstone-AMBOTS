;  -------------------------------------------------
;  File: AMB_ScaraConfig_SZP.g
;   Path: "0:/sys/AMB/Calibration/"
;  
;   Date: 2/8/2024
;  
;   Version: 1.0.0
;  
;   Description: Loads the defined values for the Duet3D Scanning Z Probe Scara configuration. (Called in bed.g)
;   
;   Global Variables Used:
;       XXXXXXXXXXXXXXXXXXXX
;       
;       
;  -------------------------------------------------

M118 P0 S"AMB_ScaraConfig_SZP.g" L1
G90 ; absolute positioning (may not be needed)
; M669 K4 P222.59974 D248.02516 A-49.2972:130 B20:170.0372 X-282.30569 Y64.0079
; M669 K(Kinematics type) P(Proximal arm length) D(Distal arm length) A(Proximal arm joint movement min:max) B(Proximal-to-distal arm join movement min:max) X(offset of bed orgin from prox. joint) Y(offset of bed orgin from prox. joint)
M669 K4 P220.63789 D250.44497 A-49.93961:130 B20:170.09973 X-280.76805 Y65.02017
