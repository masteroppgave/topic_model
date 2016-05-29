import json
from topic.twitter_stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import gensim
from nltk.stem.porter import PorterStemmer
import json
import logging
import pickle
import os
import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
p_stemmer = PorterStemmer()
stop_words = get_stop_words()
path_to_tweet_file = "data/tweets/weird.json"

def create_author_name(tweet_file):
	authors = {}
	authors[0] = ""
	key = 1

	with open(tweet_file, "r") as f:
		for line in f:
			line = json.loads(line)
			if not line["screen_name"] in authors.values():
				authors[key] = line["screen_name"]
				key+=1

	return authors

def find_key_by_name(search_name, author_dict):
	for key, name in author_dict.iteritems():
		if name==search_name:
			return key

def create_doc_author(tweet_file, author_name):

	_list = []

	with open(tweet_file, "r") as f:
		for line in f:
			author = json.loads(line)["screen_name"]
			_list.append([find_key_by_name(author, author_name)])

	return _list


def create_vocab(tweet_file):
	vocab = []

	with open(tweet_file, "r") as f:
		for line in f:
			text = json.loads(line)["text"]
			tokens = vocab.extend([token for token in tokenizer.tokenize(text.lower()) if not token in stop_words and not token.isdigit() and not len(token) < 3])

	vocab = list(set(vocab))

	return vocab


def create_corpus(tweet_file, vocab):
	"""

	Each item is a document holding the ids for each word it includes.

	E.g. [1023, 192, 3982, 3982] means that it includes token 1023 followed by 192 and then 3982 twice.

	The IDs correspond to the tokens index in the vocab list.

	"""

	docs = []

	with open(tweet_file, "r") as f:
		for line in f:
			text = json.loads(line)["text"]
			docs.append([token for token in tokenizer.tokenize(text.lower()) if not token in stop_words and not token.isdigit() and not len(token) < 3])

	for i in range(len(docs)):
		doc = docs[i]
		for j in range(len(doc)):
			token = doc[j]

			doc[j] = vocab.index(token)

	return docs

def pickle_file(filename, obj):
	with open(os.path.join("data", filename), "wb") as f:
		pickle.dump(obj, f)

if __name__=="__main__":

	vocab = create_vocab(path_to_tweet_file)
	corpus = create_corpus(path_to_tweet_file, vocab)
	author_name = create_author_name(path_to_tweet_file)
	doc_author = create_doc_author(path_to_tweet_file, author_name)

	pickle_file('vocabw.p', vocab)
	pickle_file('corpusw.p', corpus)
	pickle_file('doc_authorw.p', doc_author)
	pickle_file('author_namew.p', author_name)
