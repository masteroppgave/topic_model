from topic.utils import open_relative
from datetime import datetime
import json
import os
from topic.models.corpus import Corpus, create_corpus


"""
This creates the vector space model for the DTM executable without using
the gensim subprocess (gensim.models.wrappers.DtmModel)
"""

def convert_to_date(date):
	"""
	Args: date (string): Date on the form "Tue Apr 26 08:10:11 +0000 2016" (used by default in twitter JSON)
	
	Returns: Datetime object
	"""

	return datetime.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")


def slice_by_time(json_file, interval="day"):
	"""
	Takes a json file containing tweets and produces one file per interval (day, year or month),
	based on the tweets timestamps.
	"""


	with open(json_file, "r") as f:
		for i, line in enumerate(f):
			if i%100000==0:
				print i
			l = json.loads(line)
			date = convert_to_date(l["created_at"])

			# Open file for the specific day
			if interval=="day":
				file_name = "%s_%s_%s_tweets.json" % (date.day, date.year, date.month)
			elif interval=="month":
				file_name = "%s_%s_tweets.json" % (date.year, date.month)
			elif interval=="year":
				file_name = "%s_%s_tweets.json" % (date.year)
			else:
				raise ValueError("Wrong interval type")

			with open(os.path.join("data", file_name), "a") as f:
				f.write(line)

create_corpus("dtm_out.json")
