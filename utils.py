import os.path

def open_relative(json_file, path = '/corpora/'):
	return os.path.dirname(__file__) + path + json_file
