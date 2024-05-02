# Capstone-AMBOTS 2024

## Description

[TODO]

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)
- [Acknowledgements](#acknowledgements)

## Installation

To install and use this project, you need to have Python 3 installed on your system. If you don't have Python 3 installed, you can download it from the official Python website (https://www.python.org/downloads/).

Once you have Python 3 installed, you can follow these steps to install and use the project:

1. Clone the project repository to your local machine.
2. Open a terminal or command prompt and navigate to the project directory.
3. Install the project dependencies by running the following command:
    ```
    pip install -r requirements.txt
    ```
4. You're now ready to use the project! Run your desired script or execute any other commands as needed.

## Usage

This project has a variety of python scripts each with their own usage. A lot of them were test scripts that we used to aid ourselves while developing the hardware.
In the **BedMesh_Analysis** directory there are two important scripts of note. 
1. abl_tests.py
2. duet_http.py

> [!IMPORTANT]
> Ensure you are connected to the printer WiFi before proceeding.

abl_tests.py was used to extract bulk data from the sensors. This greatly aided in our efforts to optimize the SZP configuration as well as compare it against existing sensors.
simply run the script from it's directory using. 
```    
python abl_tests.py
```
By default this program will perform ABL 10 times using the SZP and save the heightmaps to the heightmaps directory. It will also gather the standard deviation and range for each point across the heightmaps.

duet_http.py is a library that is used by all of the programs that communicate via HTTP with the printer. This file is not meant to be run directly, rather it supplies a variety of helpful functions that enable the user to interact with the printer in various ways using python

---

In the **FirstLayer_Analysis** directory there are another two important scripts of note.
1. ir_convert.py
2. print_file.py

ir_convert.py is a script used to prepare a GCODE file produced by prusaslicer to include first layer analysis. What this program will do is take a file as an input and then create a new file that has injected GCODE that will perform some neccessary commands for first layer analysis. 

the usage of ir_convert.py is as follows. 
```
python ir_convert.py filename.gcode
```
> [!NOTE]
> Ensure that the file you are converting is in the same directory as the python script.

print_file.py will connect to the duet_printer using the DUET_IP global variable. This program will then upload an GCODE file to the printer and immediately execute it. The program
will then continue to poll the printer every second for an update and print to the console if an update is recieved. If the key phrases "Preliminary Scan Complete" or "First Layer Scan Complete" are recieved from the printer, the program will download the corresponding heightmap. 

"First Layer Scan Complete" will also trigger the program to send a blocking pop up message to the printer dashboard informing the user of the heighmap data, and prompting them if they would like to continue. 

the usage of print_file.py is as follows.
```
python print_file.py filename.gcode
``` 
> [!NOTE]
> Again, Ensure that the file you are using is in the same directory as the python script.

## Authors 
- Waeland Elder
- Ryan Espejo
- Jarrett Hobbs
- Joshua Hollis
- Kaden Nebeker

## Acknowledgements 
Thank you to our sponsors at AMBOTS, and Dr. Patitz at University of Arkansas


