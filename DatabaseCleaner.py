# Duplicate Cleaner 
# by David Bour
# 
# Used to help remove duplicates/near duplicates in a list
# Requires the users to manually select which one is most likely
# unless a reference list is provided.
#
# Must install fuzzywuzzy to use - pip install fuzzywuzzy

from sys import argv
import re, itertools
from fuzzywuzzy import fuzz
from fuzzywuzzy import process



class DataCluster():

	""" Class acts as a helper to create an object that
	keeps track of similar items using FuzzyWuzzy. This class
	will sort the items using FuzzyWuzzy as the key function 
	in the sorted(<arg>,<key="">) built-in utility. 

	Essentially, each word in the list will have a specific
	"seed" or "key" value associated with it and this is what
	the sorted function will use to sort by. Example:

	<key>     | <value>
	1. JOBS   | JOBS
	2. JOB    | JOBS (same key as #1)
	3. APPLE  | APPLE
	4. APPLES | APPLE

	This grouping works by setting the first encountered word as the
	"seed"/"key" value. This does not take into the account of the scenario
	of given items A,B,C... If A & B are similar, but A is not similar to C,
	but B & C are similar, how do you group them? 

	Only then, the itertools groupby() function can be used 
	to group similar items into array clusters.

	The adapted idea was found from the link below:
	http://stackoverflow.com/questions/11535483/fuzzy-group-by-grouping-similar-words
	"""

	def __init__(self, threshold):

		# This is the unique key for every word that will be used to sort by
		self.seeds = set()

		# This contains all of the words with its value associated with a unique seed
		self.cache = dict()

		# This is the threshold cutoff used by FuzzyWuzzy
		self.threshold = threshold

	def get_seed(self, word):

		seed = self.cache.get(word, None)

		if seed is not None:
			return seed
		for seed in self.seeds:
			if (fuzz.token_set_ratio(seed, word) >= self.threshold):
				self.cache[word] = seed
				return seed
		self.seeds.add(word)
		self.cache[word] = word
		return word

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

			filtered_list = [items_filter for items_filter in self.items if pattern.match(r'%s' % items_filter)]
			self.items[:] = [items for items in self.items if not pattern.match(r'%s' % items)]

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
			clustered list of similar items.

		"""


		cluster = DataCluster(threshold)
		sort_cluster = sorted(self.items, key=cluster.get_seed)
		group_cluster = itertools.groupby(sort_cluster, key=cluster.get_seed)

		return [list(value) for key, value in group_cluster]


	def size_of_list(self):
		print len(self.items)

	def blanket_filter(self):
		""" 
		Iterates through the original db object and removes
		names that meet a set threshold when compared
		to the blanket_filter file. 

		The blanket filter file has a list of names that can be compared
		against the original list of names. FuzzyWuzzy will be used to compare
		both list and remove all items from the original list where 
		the threshold specification is met. 
		"""

		# Blanket list 
		blanket_list = []

		# Keeps track of how many items were removed
		count_removals = 0 

		get_blanket_file = raw_input("Name of filter file? ")

		while(True):
			try:
				with open(get_blanket_file, 'rb') as working_file:
					for lines in working_file:
						names = lines.rstrip().lower()
						blanket_list.append(names)
				break
			except IOError as err:
				print err
				print "Cannot read/find specified file."
				continue
			
		get_threshold_value = raw_input("Set threshold value: ")
		get_threshold_value = int(get_threshold_value)

		for comparators in blanket_list:
			for items in self.items:
				if (fuzz.token_set_ratio(items, comparators) > get_threshold_value):
					self.items.remove(items)
					count_removals += 1

		print "Removed %s" % count_removals

		return None

	def save_to_drive(self):

		"""
		Save current list to save to drive 
		"""

		if self.is_list:
			print "Cannot save list as list of list, please convert back to string using 'rejoin word'"
		else:
			save_as = raw_input("Save file as: ")
			with open(save_as, "w") as saved_file:
				for content in self.items:
					saved_file.write(content+"\n")
					print content

		print "Finished saving."


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

		elif command_prompt == "blanket filter":
			dF.blanket_filter()

		elif command_prompt == "quit":
			break

		elif command_prompt == "clear mod list":
			really_reset = raw_input("Are you sure you'd like to remove all modified lists? (y/n")
			if (really_reset == "y"):
				curr_lists = {}
			else:
				pass

		elif command_prompt == "save":
			dF.save_to_drive()


		elif command_prompt == "save mod":

			selected_list = []

			for key, value in curr_lists.iteritems():
				print "List Name: %s" % key

			list_chosen = raw_input("Please select which list you'd like to save. ")
			selected_list = curr_lists[list_chosen]

			save_mod_as = raw_input("Save file as: ")

			with open(save_mod_as,"w") as save_to_file:

				if (isinstance(selected_list[0], (list))):
					
					for content in selected_list:

						combined_string = ""

						for num, items in enumerate(content):
							if (num == len(content)-1):
								combined_string += items
							else:
								combined_string += items + ","
						
						save_to_file.write(combined_string+"\n")

				else:

					for content in selected_list:

						save_to_file.write(content+"\n")

			print "Jobs Done"
	


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
