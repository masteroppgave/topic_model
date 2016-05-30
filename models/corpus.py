from topic.twitter_stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import gensim
from nltk.stem.porter import PorterStemmer
import json
import logging
from topic.utils import open_relative

"""
Presents the tweet as a bag of words model
saves corpus and dictionary to /tmp
"""

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
p_stemmer = PorterStemmer()
stop_words = get_stop_words()

class Corpus:
	def __init__(self, json_file, stemming=False):
		self.tweets = []
		self.file = json_file.split(".")[0]

		for line in open(open_relative(json_file)).readlines():
			try:
				self.tweets.append(json.loads(line)["text"])
			except:
				print("Failed to add the following tweet:")
				print(line)

		if stemming:
			self.tokenized_tweets = [[p_stemmer.stem(token) for token in tokenizer.tokenize(doc.lower()) if not token in stop_words] for doc in self.tweets]
		else:
			self.tokenized_tweets = [[token for token in tokenizer.tokenize(doc.lower()) if not token in stop_words] for doc in self.tweets]

		self.dictionary = gensim.corpora.Dictionary(self.tokenized_tweets)

	def __iter__(self):
		"""
		Converts bag of words to vector.
		Iterable to avoid keeping all documents in memory.
		"""

		for tokens in self.tokenized_tweets:
			yield self.dictionary.doc2bow(tokens)

class AggregatedCorpus:

	"""
	This corpus is used for the Author-Topic model where we
	combine every tweet by the same user into one large document
	"""

	def __init__(self, text_files, stemming=False):
		self.docs = []

		for file_name in text_files:
			f = open("aggr/" + file_name, "r")

			self.docs.append(" ".join(l.replace("\n", "") for l in f.readlines()))

		if stemming:
			self.tokenized_tweets = [[p_stemmer.stem(token) for token in tokenizer.tokenize(doc.lower()) if not token in stop_words] for doc in self.docs]
		else:
			self.tokenized_tweets = [[token for token in tokenizer.tokenize(doc.lower()) if not token in stop_words] for doc in self.docs]

		self.dictionary = gensim.corpora.Dictionary(self.tokenized_tweets)

	def __iter__(self):
		"""
		Converts bag of words to vector.
		Iterable to avoid keeping all documents in memory.
		"""

		for tokens in self.tokenized_tweets:
			yield self.dictionary.doc2bow(tokens)


def create_aggregated_author_corpus(text_files):
	print("=== CREATING BAG OF WORDS MODEL FOR AGGREGATED AUTHOR TWEETS ===")
	print("================================================================")
	print("                                                                ")

	corpus = AggregatedCorpus(text_files)
	corpus.dictionary.save("/tmp/aggr.dict")
	gensim.corpora.MmCorpus.serialize("/tmp/aggr.mm", corpus)

	return corpus.dictionary, gensim.corpora.MmCorpus("/tmp/aggr.mm")


def create_corpus(json_file):
	print("=== CREATING BAG OF WORDS MODEL ===")
	print("===================================")
	print("                                   ")

	corpus = Corpus(json_file)
	corpus.dictionary.save("/tmp/" + corpus.file + ".dict")
	gensim.corpora.MmCorpus.serialize("/tmp/" + corpus.file + ".mm", corpus)

	return corpus.dictionary, gensim.corpora.MmCorpus("/tmp/" + corpus.file + ".mm")

if __name__=="__main__":
	aggregated_author_list = ["aggregated_barack_w.txt", "aggregated_elonmusk.txt", "aggregated_justinbieber.txt", "aggregated_neiltyson.txt" \
	, "aggregated_realDonaldTrump.txt", "aggregated_taylorswift13.txt"]

	create_aggregated_author_corpus(aggregated_author_list)

	#create_aggregated_author_corpus()
	#create_corpus("out_experiment.json")
	#print stop_words

	#c = Corpus("29jan_tweets.json")

	#c.dictionary.save_as_text("corpus.txt")
