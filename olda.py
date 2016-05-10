from twitter_stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import gensim
from nltk.stem.porter import PorterStemmer
import json
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
p_stemmer = PorterStemmer()
stop_words = get_stop_words()
"""
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

corpus.dictionary.save("online_27.dict")
gensim.corpora.MmCorpus.serialize("online27.mm", corpus)

"""


# Extract 10 LDA topics, using 1 pass and updating once every 1 cunk (100 documents)

dictionary = gensim.corpora.Dictionary.load("online_27.dict")
mm = gensim.corpora.MmCorpus("online27.mm")

lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=10, update_every=1, \
	chunksize = 100, passes=1)

print lda.show_topics(10)
