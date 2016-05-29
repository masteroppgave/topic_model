import json
import operator
from collections import Counter
from collections import defaultdict
from stop_hashtags import get_stop_hashtags

stop_hashtags = get_stop_hashtags()

def most_popular(lines, number_of_results):

	lines = [json.loads(line) for line in lines]
	lines = sorted(lines, key=lambda k: k["favorite_count"])

	return [(line["text"], line["favorite_count"]) for line in lines[:number_of_results]]

def length(lines):
	length = 0
	for line in lines:
		tweet = json.loads(line)

		length += len(tweet["text"].split(" "))

	return length/float(len(lines))


def most_common(lines, number_of_results, metadata=False):

	"""
	Takes a json file with tweets and returns
	the most common hashtags.
	"""

	hashtags = []

	for line in lines:

		tweet = json.loads(line) 

		if metadata:
			for hashtag in tweet["entities"]["hashtags"]:
				hashtags.append(hashtag["text"])
		else:
			hashtags.extend([token for token in tweet["text"].split() if (token.startswith("#") and token not in stop_hashtags)])

	return {"most_common": Counter(hashtags).most_common(number_of_results), "number_of_tweets": len(lines)}

def co_occurrences(lines, number_of_results=0, metadata=False):

	"""
	Finds co-occurrences of hashtags in tweets
	"""

	com = defaultdict(lambda: defaultdict(int))
	length = len(lines)

	for i, line in enumerate(lines):
		#if i%2000==0:
		#	print int(i/float(length)*100)
		tweet = json.loads(line)

		if metadata:
			hashtags = [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]]
		else:
			hashtags = [token for token in tweet["text"].split() if (token.startswith("#") and token not in stop_hashtags)]

		if len(hashtags) < 2:
			continue

		# Build co-occurrence matrix

		for i in range(len(hashtags)-1):
			for j in range(i+1, len(hashtags)):
				h1, h2 = sorted([hashtags[i], hashtags[j]])
				if h1 != h2:
					com[h1][h2] += 1

	most_common = []

	for h1 in com:
		h1_max = max(com[h1].items(), key=operator.itemgetter(1))
		for h2 in h1_max:
			most_common.append(((h1, h2), com[h1][h2]))

	max_hashtags = sorted(most_common, key=operator.itemgetter(1), reverse=True)

	if number_of_results>0:
		return([m for m in max_hashtags if m[-1]>0][:number_of_results])
	else:
		return([m for m in max_hashtags if m[-1]>0])



if __name__ == "__main__":
	f = open("11_12_mai.json", "r")

	print (most_common(f.readlines(), 20))
