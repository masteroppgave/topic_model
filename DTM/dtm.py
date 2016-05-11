from topic_model.twitter_stop_words import get_stop_words
import gensim
import logging
import subprocess

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def dynamic_topic_model(num_topics=5, corpus=None, dictionary=None, passes=1):

	if not dictionary:
		print("USING DEFAULT 29jan_tweets DICTIONARY")
		dictionary = gensim.corpora.Dictionary.load("/tmp/29jan_tweets.dict")
	if not corpus:
		print("USING DEFAULT 29jan_tweets CORPUS")
		corpus = gensim.corpora.MmCorpus("/tmp/29jan_tweets.mm")

	model = gensim.models.wrappers.DtmModel('./dtm-linux64', corpus, [100,100,100,28], num_topics=num_topics, id2word=dictionary)

print dynamic_topic_model()
