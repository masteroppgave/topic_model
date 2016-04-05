import logging
import gensim

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def generate_topics(num_topics, corpus=None, dictionary=None, passes=1):
	print("=== GENERATING TOPICS ===")
	print("=========================")
	print("Number of topics: " + str(num_topics))
	print("Number of passes: " + str(passes))

	if not dictionary:
		dictionary = gensim.corpora.Dictionary.load("/tmp/29jan_tweets.dict")
	if not corpus:
		corpus = gensim.corpora.MmCorpus("/tmp/29jan_tweets.mm")

	lda = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=passes)
	topic_list = lda.show_topics(num_topics)

	return dict(topic_list)
