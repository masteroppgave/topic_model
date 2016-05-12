from utils import open_relative

"""
This creates the vector space model for the DTM executable without using
the gensim subprocess (gensim.models.wrappers.DtmModel)
"""

def slice_by_time(json_file, interval):
	"""
	This splits the json file into several smaller files based on which interval is chosen (year, month, week, day)
	"""

	