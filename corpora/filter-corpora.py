import json
from random import shuffle

"""

Used for filtering the corpora on length or other attributes

"""

def max_lines(_file, max_lines):
	"""
	Outputs a file including only max_lines number of max_lines
	from the input file. The lines are chosen at random.
	"""
	head = _file.split(".")[0]
	out = open("out_%s.json" % (head), "a")

	_list = [line for line in open(_file).readlines()]
	shuffle(_list)
	for line in _list[:max_lines]:
		out.write(line)

max_lines("experiment.json", 500000)
