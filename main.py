import argparse
from bag_of_words import create_bag_of_words
from lda import generate_topics
from num_topics import create_lsi_model
from num_topics import find_number_of_topics

"""

Takes a .json file with tweets and produces topics.
If number of topics are not specicied, it is calculated by Vincent Granvilles method:
http://www.analyticbridge.com/profiles/blogs/identifying-the-number-of-clusters-finally-a-solution

"""

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, help='JSON file containing tweets.', required=True)
parser.add_argument('--topics', type=int, help='Number of topics to use.', required=False, default=0)
args = parser.parse_args()

dictionary, corpus = create_bag_of_words(args.file)
num_topics = 5 # default

if (args.topics==0):
	create_lsi_model(args.file)
	num_topics = find_number_of_topics(args.file)
	print "=== Using " + str(num_topics) + " topics ==="

print generate_topics(num_topics, corpus, dictionary)
