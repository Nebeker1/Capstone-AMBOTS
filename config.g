; Configuration file for Duet 3 Mini 5+ (firmware version 3.4.0)
; executed by the firmware on start-up
 
;________________________________________________________________________
; General preferences
G90							                    ; Send absolute coordinates...
M83							                    ; ...but relative extruder moves
M550 P"amb-6"				                	; Set machine name
 
;________________________________________________________________________
; Network Setup
M552 S1						                    ; Enable network
M586 P0 S1					                    ; Enable HTTP
M586 P1 S0					                    ; Disable FTP
M586 P2 S0					                    ; Disable Telnet

G4 S2                                           ; wait for expansion boards to start (SZP)

;________________________________________________________________________
; Drives
M569 P2 S1 D3					                ; Z driver settings
M569 P1 S1 D3					                ; E driver settings
;M569 P3 S1 D3					                ; U driver settings
M569 P6 S1 T2.5:2.5:5:0							; y driver settings
M569 P5 S1 T2.5:2.5:5:0							; x driver settings
M584 x5 Y6			                   			; X + Y driver settings
M584 Z2 E1 ;U3									; Use onboard drivers
M350 X256 Y256 Z16 E16 I1						; Configure microstepping with interpolation
M92 X694.444 Y694.444 Z2552.48 E568.62 ;U150			; Set steps per degree and per mm (Duet)
M566 X300.00 Y300.00 Z60.00 E600 ;U600				; Set maximum instantaneous speed changes (mm/min)
;M203 X15000.00 Y15000.00 Z600 E6000.00			; Set maximum speeds (mm/min)
M203 X9000.00 Y9000.00 Z600 E6000.00 ;U9000			; Set maximum speeds (mm/min)
M201 X10000.00 Y10000.00 Z30.00 E50 ;U5000				; Set accelerations (mm/s^2)
M906 X1000 Y1000 Z500 E600 I50				    ; Set motor currents (mA) and motor idle factor in per cent
M84 S300											; Set idle timeout
M84 S5 E0
 
;________________________________________________________________________
; Axis Limits
M208 X-50 Y-50 Z-10 S1       	 ; Set axis minima
M208 X620 Y300 Z300 S0           ; Set axis maxima

;________________________________________________________________________
; Endstops
M574 X1 S1 P"!io5.in"							; Set X endstop to low end, active low
M574 Y2 S1 P"io2.in"				            ; Set Y endstop to high end, active low
M574 Z1 S2 ;P"io3.in"						    ; Set Z endstop to high end and as Z-probe

;________________________________________________________________________
; Heaters
;M307 H1 A-1 C-1 D-1						        ; Disable heated bed
M308 S0 P"temp1" Y"thermistor" A"Hotend Temp" T100000 B4138   ; Set thermistor + ADC parameters for heater 1
M950 H0 C"out1" T0
M307 H0 B0 R1.637 C105.9 D4.99 S1.00 V23.4
M143 H0 S280					                ; Set temperature limit for heater 1 to 280C

;________________________________________________________________________
; Bed Heater
M308 S1 P"temp0" Y"thermistor" A"Bed Temp" T93500 B5861 C2.552372e-7	; Set thermistor + ADC parameters for heated bed
M950 H1 C"out0" T1
M307 H1 B0 R0.434 C184.1 D1.08 S1.00
M140 H1
M143 H1 S120

;________________________________________________________________________
; Z-Probe
M950 S0 C"io3.out" 								; servo/gpio 0 is io3.out pin
M558 P9 C"^io3.in" H10 F1000 T17000 R0	    	; Enable Z probe on io3.in pin, set dive height, probe speed and travel speed
G31 P500 Z2.123			            			; Z probe trigger value, offset in relation to nozzle. And trigger height adjustment
M280 P0 S160						            ; Reset BLTouch

;________________________________________________________________________ (NEW)
; Duet3D Scanning Z Probe
M558 K1 P11 C"120.i2c.ldc1612" F8000 T8000    ; configure SZP as probe 1, type 11, on CAN address 120
M308 A"SZP coil" S10 Y"thermistor" P"120.temp0" ; thermistor on SZP coil
G31 K1 Z12                                      ; define probe 1 offsets and trigger height
M558.2 K1 S20 R164359                           ; set drive current and reading offset
M557 X30:520 Y40:250 P7:8                       ; define printing grid

;________________________________________________________________________
;This is a standard single printer setup, send M557 with values if not a standard setup.(or macro call)
;M557 X30:520 Y40:250 P7:8   					; Define the area for mesh grid compensation

;________________________________________________________________________
; Fans
M950 F0 C"out5" Q500                            ; create fan 0 on pin out5 and set its frequency (part cooling fan)
M950 F1 C"out3" Q500							; create fan 1 on pin put6 and set its frequency (hotend fan)
M106 P1 H0 T45		                		    ; Set fan 1 value, PWM signal inversion and frequency. Thermostatic control is turned on

;________________________________________________________________________
; Tools
M563 P0 S"Hotend" D0 H0 F0					    ; Define tool 0
G10 P0 X0 Y0 Z0					                ; Set tool 0 axis offsets
G10 P0 R0 S0					                ; Set initial tool 0 active and standby temperatures to 0C
M572 D0 S0					                    ; Set tool 0 pressure advance
T0                                              ; select first tool

;M563 P1 S"tool1"                                ; Define tool 1
;G10 P1 X36 Y1 Z0                                ; Set offsets for tool 1
;T1                                              ; select second tool (tool1)


;________________________________________________________________________
;Accelerometer for Input Shaping
;M955 P0 C"spi.cs2+spi.cs1" I64
;________________________________________________________________________
; Filament Sensing
;M591 D0 P2 C"io4.in" S2

;----------------------------------------------------------------------- 
; SCARA settings
M98 P"0:/sys/AMB/Calibration/AMB_ScaraConfig_HotEnd.g"            ; Call the custom M669 parameters


;________________________________________________________________________
; Serial settings for External Controller
M575 P1 B57600 S0                               ; Set serial number, Baud rate and as PanelDue mode without checksums

;________________________________________________________________________
; Power Loss
; CFJ Setup Resume.g to work with this !!!
M911 S10 R11 P"M913 X0 Y0 G91 M83 G1 Z3 E-5 F1000" ; set voltage thresholds and actions to run on power loss
 
;----------------------------------------------------------------------- 
; Power Loss
M911 S21.0 R28 P"M913 X0 Y0 M5005" ; set voltage thresholds and actions to run on power loss

M950 P5 C"io0.out" 
M950 P6 C"io1.out" 
M42 P5 S0
M42 P6 S0
M950 J7 C"^io0.in" 
M950 J8 C"^io1.in" 
 

;----------------------------------------------------------------------- 
;-   Alarm Triggers
 
;Motor 1 Driver Failure 
 
M581 P7 S0 T5 R0 ; invoke trigger 5 when an active-to-inactive edge is detected on input     at anytime

;Motor 2 Driver Failure
 
M581 P8 S0 T6 R0 ; invoke trigger 6 when an active-to-inactive edge is detected on input   at anytime
 

M501                                               ; load saved parameters from non-volatile memory
M98 P"0:/sys/AMB/Configuration/AMB_Config_LoadVariables.g" 