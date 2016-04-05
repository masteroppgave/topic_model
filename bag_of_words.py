from twitter_stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import gensim
from nltk.stem.porter import PorterStemmer
import json
import logging

"""
Presents the tweet as a bag of words model
saves corpus and dictionary to /tmp
"""

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
p_stemmer = PorterStemmer()
stop_words = get_stop_words()

class Corpus:
	def __init__(self, json_file):
		self.tweets = []
		self.file = json_file.split(".")[0]

		for line in open(json_file).readlines():
			try:
				self.tweets.append(json.loads(line)["text"])
			except:
				print("Failed to add the following tweet:")
				print(line)

		self.tokenized_tweets = [[p_stemmer.stem(token) for token in tokenizer.tokenize(doc.lower()) if not token in stop_words] for doc in self.tweets]
		self.dictionary = gensim.corpora.Dictionary(self.tokenized_tweets)

	def __iter__(self):
		for tokens in self.tokenized_tweets:
			yield self.dictionary.doc2bow(tokens)


corpus = Corpus("27jan_tweets.json")
corpus.dictionary.save("/tmp/" + corpus.file + ".dict")
gensim.corpora.MmCorpus.serialize("/tmp/" + corpus.file + ".mm", corpus)
