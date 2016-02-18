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


class DatabaseEntry():

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
			return True
		except IOError as err:
			print err
			print "Cannot read/find specified file."
			return False

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
		Removes all special characters in the words
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

		Args:
			delimiter - character used to rejoin the list.
			Default is white space.
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

		if self.is_list:
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
		Clears out all data entries that are blank or 
		only contains special characters.
		"""

		reg_pattern = re.compile(r'^[\W]+$')

		if not self.is_list:
			self.items = [words for words in self.items if not (words == "" or reg_pattern.match(r'%s' % words))]
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


	def partition(self, key):

		"""
		Uses regex to move specified items to a separate list. Removes
		said items from original list.

		Args:
			key - regex pattern, recommended to add 'r' in the
			parameter for raw string search. i.e. (r'string pattern here')

		return:
			filtered_list - a list containing matches to the regex pattern
		"""

		# Filtered list
		filtered_list = []

		if not self.is_list:
			# Creation of regex
			pattern = re.compile(r'%s' % key)

			for items in self.items:
				if (pattern.match(r'%s' % items)):
					filtered_list.append(items)
					self.items.remove(items)

		else:
			print "Cannot perform action on list of list\
			\nPlease convert list back to list of words."

		return filtered_list


	def cluster(self, threshold):


		""" Use of fuzzywuzzy library to cluster 
		similar items together.


		Args:
			threshold - percent identity to call a match.

		return:
			clustered_list - clustered list of similar items.

		"""

		# List of list of similar items
		clustered_list = []

		# Create a copy of the original list to aid in comparisons.
		is_copy = [z for z in self.items]

		for items in self.items:

			# Holds the similar items together
			temp_cluster = []

			for comparisons in is_copy:

				if (fuzz.token_set_ratio(items, comparisons) > threshold):
					temp_cluster.append(comparisons)
					is_copy.remove(comparisons)

			# Checks if any matches were made, don't add if no clustered made.
			if len(temp_cluster) != 0:
				clustered_list.append(temp_cluster)

		return clustered_list


	def size_of_list(self):
		print len(self.items)

def main():

	db = DatabaseEntry()
	dF = DataFilters(db)

	curr_lists = {}
	curr_file = ""

	in_process = True

	while(in_process):
		print "DATA PROCESSER: To begin... please choose a file to upload."
		curr_file = raw_input("File name: ")
		if (db.set_data(curr_file)):
			in_process = False

	while(True):

		command_prompt = raw_input("Enter Command> ")
		command_prompt = command_prompt.lower()

		if command_prompt == "print":
			dF.print_items()

		elif command_prompt == "lowercase":
			dF.lower_case()

		elif command_prompt == "remove funny":
			dF.remove_funny()

		elif command_prompt == "split word":
			delimiter = raw_input("What delimiter to use to split word? ")
			dF.split_word(delimiter)

		elif command_prompt == "rejoin word":
			rj_delimiter = raw_input("What delimiter to use to rejoin word? ")
			dF.rejoin_word(rj_delimiter)

		elif command_prompt == "filter":
			operation = raw_input("Operation type - greater than\equal(ge),\
				less than\equal(le), or equal to(eq): ")
			length = raw_input("Length limit: ")
			length = int(length)
			dF.filter_list(length, operation)

		elif command_prompt == "clear empty":
			dF.clear_empty()

		elif command_prompt == "remove duplicates":
			dF.remove_duplicates()

		elif command_prompt == "partition":
			regex = raw_input("Enter regex pattern: ")
			name_list = raw_input("Please name the return list: ")
			partition = dF.partition(regex)
			curr_lists[name_list] = partition

		elif command_prompt == "cluster":
			threshold = raw_input("Please enter cluster threshold: ")
			threshold = int(threshold)
			name_cluster = raw_input("Please name the return cluster list:" )
			cluster = dF.cluster(threshold)
			curr_lists[name_cluster] = cluster

		elif command_prompt == "more":
			for key, value in curr_lists.iteritems():
				print key

			do_proceed = raw_input("Would you like to print? (y/n) ")
			if (do_proceed == "y"):
				get_dict_name = raw_input("Which list would you like to print? ")
				get_dict = curr_lists[get_dict_name]
				print get_dict, len(get_dict)
				for items in get_dict:
					print items
			else:
				pass

		elif command_prompt == "reset":
			do_reset = raw_input("Are you sure you'd like to reset the data? (y/n) ")
			if (do_reset == "y"):
				db = DatabaseEntry()
				dF = DataFilters(db)
				db.set_data(curr_file)
			else:
				pass

		elif command_prompt == "quit":
			break


if __name__ == "__main__":
	main()

# q = DatabaseEntry()
# q.set_data(argv[1])

# x = DataFilters(q)
# x.size_of_list()
# x.clear_empty()
# x.size_of_list()
# # x.print_items()
# x.cluster(5)
# # x.print_items()
# # x.partition('.*\\\\.*|.*/.*')
# # x.lower_case()
# # x.print_items()
# # # x.remove_funny()
# # x.print_items()
# # x.clear_empty()
# # x.split_word(" ")
# # x.print_items()
# # # x.remove_funny()
# # # x.size_of_list()
# # x.filter_list(2, "le")
# # # x.size_of_list()
# # x.print_items()
# # x.rejoin_word()
# # # x.clear_empty()
# # # x.print_items()
# # # x.size_of_list()
# # x.remove_duplicates()
# # x.print_items()
# # x.cluster()
