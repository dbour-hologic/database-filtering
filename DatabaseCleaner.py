# Duplicate Cleaner 
# by David Bour
# 
# Used to help remove duplicates/near duplicates in a list
# Requires the users to manually select which one is most likely
# unless a reference list is provided.
#
# Must install fuzzywuzzy to use - pip install fuzzywuzzy

from sys import argv
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class DatabaseEntry:

	""" 

	DatabaseEntry Class ---

	The DatabaseEntry class converts a text file in the following
	format into a list that can be modified by applying filters.

	Example:

	content
	-----
	item1\n
	item2\n
	item3\n

	"""

	def __init__(self):
		self.data = []

	def set_data(self, filename):

		"""
		Initializes the data structure.

		Args:
			filename - The filename that is to be read and converted
			to a list of items.
		"""

		try:
			with open(filename, 'r') as working_file:
				for lines in working_file:
					names = lines.rstrip()
					self.data.append(names)
		except IOError as err:
			print err
			print "Cannot read/find specified file."


class DataFilters():

	def __init__(self, database_object):
		self.items = database_object.data

	def print_items(self):
		for items in self.items:
			print items

	def lower_case(self):

		"""
		Lower cases all characters
		"""
		self.items = [words.lower() for words in self.items]

	def remove_funny(self):

		""" 
		Removes all special characters
		"""
		for number, check in enumerate(self.items):
			self.items[number] = re.sub('[^A-Za-z0-9\s]+','',check)



q = DatabaseEntry()
q.set_data(argv[1])

x = DataFilters(q)
x.print_items()
x.lower_case()
x.print_items()
x.remove_funny()
x.print_items()



# def read_in_file(list_file):

# 	""" 
# 		read_in_file(list_file): reads in a text file line by 
# 		line to be used for further processing by other downstream
# 		applications. File must be in the format described as shown
# 		below.

# 		file
# 		----
# 		file_example.txt

# 		content
# 		-------
# 		item1
# 		item2
# 		item3

# 		Args:
# 			list_file(file): name of file to read from.

# 		Returns:
# 			list: a list of lines read by the file scanner.
# 	"""

# 	# holds all of the lines in a list
# 	name_list = []

# 	try:
# 		with open(list_file, "r") as working_file:
# 			for lines in working_file:
# 				names = lines.rstrip()
# 				name_list.append(names)
# 	except IOError as err:
# 		print err
# 		pass

# 	return name_list