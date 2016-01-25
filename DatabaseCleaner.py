# Duplicate Cleaner 
# by David Bour
# 
# Used to help remove duplicates/near duplicates in a list
# Requires the users to manually select which one is most likely
# unless a reference list is provided.
#
# Must install fuzzywuzzy to use - pip install fuzzywuzzy

from sys import argv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def read_in_file(list_file):

	""" 
		read_in_file(list_file): reads in a text file line by 
		line to be used for further processing by other downstream
		applications.

		Args:
			list_file(file): name of file to read from.

		Returns:
			list: a list of lines read by the file scanner.
	"""

	# holds all of the lines in a list
	name_list = []

	with open(list_file, "r") as working_file:
		for lines in working_file:
			names = lines.rstrip()
			name_list.append(names)

	return name_list







