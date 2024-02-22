import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

#function to read a file containing a 2d array of numbers delimited by a comma and a space
def read_file(filename):
		file = open(filename, 'r')
		arr = []
		lines = file.readlines()
		info = lines[2:3]
		info = [info[x].split(',') for x in range(len(info))]
		print(info)
		lines = lines[3:]
		for i in range(len(lines)):
			z_values = lines[i].split(', ')

			#remove spaces and the newline character
			for j in range(len(z_values)):
				z_values[j] = z_values[j].strip()
			print(z_values)
			z_values = [float(x) for x in z_values]
			arr.append(z_values)
		file.close()
		return arr

def find_difference_two_arrays(arr1, arr2):
	#find the difference of the two arrays
	diff = []
	for i in range(len(arr_szp)):
		row = []
		for j in range(len(arr_szp[i])):
			row.append(arr_szp[i][j] - arr_blt[i][j])
		diff.append(row)

	#write the difference to a file
	file = open('.\heightmaps\Difference.txt', 'w')
	for i in range(len(diff)):
		for j in range(len(diff[i])):
			diff[i][j] = round(diff[i][j], 4)
			file.write(str(diff[i][j]) + ', ')
		file.write('\n')
	file.close()
	print('done')

#read the file and print result
arr_szp = read_file('.\heightmaps\SZP_HeightMap.txt')
arr_blt = read_file('.\heightmaps\BLTouch_HeightMap.txt')
find_difference_two_arrays(arr_szp, arr_blt)