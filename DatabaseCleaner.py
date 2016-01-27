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

		self.items = database_object.data 		# initializes the data structure
		self.is_list = False					# if split_word() used, word is now a list.

	def print_items(self):

		for number, items in enumerate(self.items):
			print number,") ",items

	def lower_case(self):

		"""
		Lower cases all characters
		"""

		if not self.is_list:
			self.items = [words.lower() for words in self.items]
		else:
			print "Cannot perform action on list of list\
			\nPlease convert list back to list of words."

	def remove_funny(self):

		""" 
		Removes all special characters
		"""

		if not self.is_list:
			for number, check in enumerate(self.items):
				self.items[number] = re.sub('[^A-Za-z0-9\s]+','',check)
		else:
			print "Cannot perform action on list of list\
			\nPlease convert list back to list of words."

	def split_word(self, delimiter):

		""" 
		Splits word on selected delimiter. 
		Default is whitespace.

		Args:
			delimiter - Character to divide word on.

		"""

		if not self.is_list:
			self.items = [words.split(delimiter) for words in self.items]
			self.is_list = True
		else:
			print "Cannot perform action on list of list\
			\nPlease convert list back to list of words."


	def rejoin_word(self, delimiter=" "):

		"""
		Rejoins the split words back to a string, connecting
		each word by the specified delimiter.
		"""
		if not self.is_list:
			print "Cannot perform action on list of words.\
			\nPlease convert list to list of list with split_word()."
		else:
			self.items = [delimiter.join(words) for words in self.items]
			self.is_list = False


	def filter_list(self, length, operation):

		"""
		Filters the list depending on length input.

		Args:
			length - length to filter by.

			operation - greater/equal(ge) to, equal to(eq), less/equal to(le)
			Default is equal to.

		"""

		if not self.is_list:
			if (operation == "ge"):
				self.items = [words for words in self.items if len(words) >= length]
			elif (operation == "le"):
				self.items = [words for words in self.items if len(words) <= length]
			else: 
				self.items = [words for words in self.items if len(words) == length]
		else:
			print "Cannot perform action on list of words.\
			\nPlease convert list to list of list with split_word()."

	def clear_empty(self):

		"""
		Clears out all data entries that are blank
		"""

		if not self.is_list:
			self.items = [words for words in self.items if not words == ""]
		else:
			print "Cannot perform action on list of list\
			\nPlease convert list back to list of words."


	def remove_duplicates(self):

		"""
		Scans the list to remove duplicates.
		"""

		unique_set = []

		if not self.is_list:
			for items in self.items:
				if items not in unique_set:
					unique_set.append(items)
			
			self.items = unique_set
		else:
			print "Cannot perform action on list of words.\
			\nPlease convert list to list of list with split_word()."



	def size_of_list(self):
		print len(self.items)



q = DatabaseEntry()
q.set_data(argv[1])

x = DataFilters(q)
x.print_items()
x.lower_case()
x.print_items()
x.remove_funny()
x.print_items()
x.split_word(" ")
x.print_items()
x.remove_funny()
# x.size_of_list()
x.filter_list(2, "ge")
# x.size_of_list()
x.print_items()
x.rejoin_word()
x.clear_empty()
x.print_items()
x.size_of_list()
x.remove_duplicates()
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