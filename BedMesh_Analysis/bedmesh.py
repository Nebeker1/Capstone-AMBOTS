import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

#class to hold the heightmap points and info
class Heightmap(object):
		
	def __init__(self, filename):
		super(Heightmap, self).__init__()
		self.filename = filename
		self.heightmap = []
		self.z_points = []
		self.min_x = 0
		self.max_x = 0
		self.min_y = 0
		self.max_y = 0
		self.spacing_x = 0
		self.spacing_y = 0
		self.cols = 0
		self.rows = 0

	
	def read_z_points(self):
			file = open(self.filename, 'r')
			arr = []
			lines = file.readlines()
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
			self.z_points = arr
	
	def read_info(self):
		file = open(self.filename, 'r')
		lines = file.readlines()
		info = lines[2:3]

		info = info[0].split(',')
		self.min_x = float(info[2])
		self.max_x = float(info[3])
		self.min_y = float(info[4])
		self.max_y = float(info[5])	
		self.spacing_x = float(info[7])
		self.spacing_y = float(info[8])
		self.cols = int(info[9])
		self.rows = int(info[10])

	def generate_heightmap(self):
		#generate the heightmap
		x = np.linspace(self.min_x, self.max_x, self.cols)
		y = np.linspace(self.min_y, self.max_y, self.rows)
		X, Y = np.meshgrid(x, y)
		Z = np.array(self.z_points)
		self.heightmap = [X, Y, Z]
		#plot the heightmap
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.plot_surface(X, Y, Z, cmap='viridis')
		plt.show()
		pass

def find_difference_two_arrays(arr1, arr2):
	#find the difference of the two arrays
	diff = []
	for i in range(len(arr1)):
		row = []
		for j in range(len(arr1[i])):
			row.append(arr1[i][j] - arr2[i][j])
		diff.append(row)

	#write the difference to a file
	file = open('.\heightmaps\Difference.txt', 'w')
	for i in range(len(diff)):
		for j in range(len(diff[i])):
			diff[i][j] = round(diff[i][j], 4)
			file.write(str(diff[i][j]) + ', ')
		file.write('\n')
	#find the average difference
	avg = 0
	for i in range(len(diff)):
		for j in range(len(diff[i])):
			avg += abs(diff[i][j])
	avg = avg / (len(diff) * len(diff[0]))
	file.write('Average: ' + str(avg))
	file.close()
	print('done')

absolute_path = os.path.dirname(__file__)

#add heightmap files
BLTouch_relative_path = "heightmaps/heightmap1.csv"
SZP_relative_path = "heightmaps/heightmap3.csv"
BLTouch_hm_path = os.path.join(absolute_path, BLTouch_relative_path)
SZP_hm_path = os.path.join(absolute_path, SZP_relative_path)

heightmap_blt = Heightmap(BLTouch_hm_path)
heightmap_szp = Heightmap(SZP_hm_path)
heightmap_blt.read_z_points()
heightmap_blt.read_info()
heightmap_szp.read_z_points()
heightmap_szp.read_info()
find_difference_two_arrays(heightmap_blt.z_points, heightmap_szp.z_points)
heightmap_szp.generate_heightmap()

#read the file and print result
# arr_szp = read_file('.\heightmaps\SZP_HeightMap.txt')
# arr_blt = read_file('.\heightmaps\BLTouch_HeightMap.txt')
# find_difference_two_arrays(arr_szp, arr_blt)