# Class to aid in farmer-market matching
# Contains easy storage


from math import fabs, sqrt, pow
from types import *

class Coordinate:

	# Constructor
	def __init__(self, lat, long):
		self.lat_ = lat;
		self.long_ = long;

	# Methods
	def compute_distance_between(self, other):
		latDiff = fabs(self.lat_ - other.lat_)
		longDiff = fabs(self.long_ - other.long_)

		distanceBetween = round(sqrt( (pow(latDiff, 2)) + (pow(longDiff, 2)) ), 2)

		return distanceBetween

	def print_coords(self):
		print("Lat: {}  Long: {}".format(self.lat_, self.long_))



if __name__ == '__main__':
	coord1 = Coordinate(0, 0)
	coord1.print_coords();
	coord2 = Coordinate(3, 4)
	coord2.print_coords();
	coord3 = Coordinate(5, 12)
	coord3.print_coords();

	diff_12 = coord1.compute_distance_between(coord2)
	diff_21 = coord2.compute_distance_between(coord1)

	diff_13 = coord1.compute_distance_between(coord3)
	diff_31 = coord3.compute_distance_between(coord1)

	diff_23 = coord2.compute_distance_between(coord3)
	diff_32 = coord3.compute_distance_between(coord2)

	assert(diff_12 == 5)
	assert(diff_21 == 5)
	assert(diff_13 == 13)
	assert(diff_31 == 13)
	assert(diff_23 == 8.25)
	assert(diff_32 == 8.25)

	print("All tests passed, coord.py working as intended")