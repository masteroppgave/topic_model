from topic.twitter_stop_words import get_stop_words
import gensim
import logging
import subprocess
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

"""

The DtmModel module in gensim is quite new and contains some bugs.
Since DTM is not implemented natively in gensim, it runs a dtm executable (dtm-linux64) performing
the computations in a subprocess.

"""



def dynamic_topic_model(num_topics=5, corpus=None, dictionary=None, passes=1):

	if not dictionary:
		print("USING DEFAULT 29jan_tweets DICTIONARY")
		dictionary = gensim.corpora.Dictionary.load("/tmp/29jan_tweets.dict")
	if not corpus:
		print("USING DEFAULT 29jan_tweets CORPUS")
		corpus = gensim.corpora.MmCorpus("/tmp/29jan_tweets.mm")


	time_seq = [100,100,100,28]
	model = gensim.models.wrappers.DtmModel('./dtm-linux64', corpus, time_seq, num_topics=num_topics, id2word=dictionary, initialize_lda=True)

	topic1 = model.show_topic(topicid=1, time=1, topn=10)
	topic2 = model.show_topic(topicid=1, time=2, topn=10)

	print "TIME 1\n"
	print topic1
	print "TIME 2\n"
	print topic2

print dynamic_topic_model()
