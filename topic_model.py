import logging
import gensim

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def generate_lda_topics(num_topics, corpus=None, dictionary=None, passes=1):
	print("=== GENERATING LDA TOPICS ===")
	print("=============================")
	print("Number of topics: " + str(num_topics))
	print("Number of passes: " + str(passes))

	if not dictionary:
		print("USING DEFAULT 29jan_tweets DICTIONARY")
		dictionary = gensim.corpora.Dictionary.load("/tmp/29jan_tweets.dict")
	if not corpus:
		print("USING DEFAULT 29jan_tweets CORPUS")
		corpus = gensim.corpora.MmCorpus("/tmp/29jan_tweets.mm")

	lda = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=passes)
	topic_list = lda.show_topics(num_topics)

	return (dict(topic_list))

def generate_hdp_topics(num_topics, corpus=None, dictionary=None):

	if not dictionary:
		print("USING DEFAULT 29jan_tweets DICTIONARY")
		dictionary = gensim.corpora.Dictionary.load("/tmp/29jan_tweets.dict")
	if not corpus:
		print("USING DEFAULT 29jan_tweets CORPUS")
		corpus = gensim.corpora.MmCorpus("/tmp/29jan_tweets.mm")

	hdp = gensim.models.HdpModel(corpus, dictionary)
	topic_list = hdp.show_topics(topics=num_topics)

	_dict = {}

	for element in topic_list:
		index, element = element.split(":")
		index = int(index[-1])
		element = element.strip()

		_dict[index] = element

	return _dict


if __name__ == "__main__":
    print generate_hdp_topics(2)
