import unittest
from DatabaseCleaner import read_in_file

class file_reading(unittest.TestCase):
	""" Tests for file imports and reading """

	def setUp(self):
		self.file = "test.txt"

	def test_read_in_file(self):
		""" File is opened and outputs correct list"""
		self.assertEqual(read_in_file(self.file), ["apple","oranges"], msg="Did not output correct items.")

if __name__ == '__main__':
	unittest.main()