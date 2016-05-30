import logging
import gensim
import json
import operator
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from topic.twitter_stop_words import get_stop_words

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stop_words = get_stop_words()

def generate_lda_topics(num_topics, corpus=None, dictionary=None, passes=1):
	print("=== GENERATING LDA TOPICS ===")
	print("=============================")
	print("Number of topics: " + str(num_topics))
	print("Number of passes: " + str(passes))

	if not dictionary:
		# For testing
		print("USING DEFAULT 29jan_tweets DICTIONARY")
		dictionary = gensim.corpora.Dictionary.load("/tmp/29jan_tweets.dict")
	else:
		dictionary = gensim.corpora.Dictionary.load("/tmp/%s.dict" % (dictionary))
	if not corpus:
		# For testing
		print("USING DEFAULT 29jan_tweets CORPUS")
		corpus = gensim.corpora.MmCorpus("/tmp/29jan_tweets.mm")
	else:
		corpus = gensim.corpora.MmCorpus("/tmp/%s.mm" % (corpus))

	lda = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=passes, minimum_probability=0.02, gamma_threshold=0.001)
	lda.save("saved_author_original_50p_50t.p")

	# To get topic mixture for document:
	#topic_mixture = lda[dictionary.doc2bow(["love", "write", "inspir", "due", "professor", "date", "essay"])]
	print("===== TOPIC MIXTURE=====")
	#print(topic_mixture)

	# Update model: lda.update(other_corpus)

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

def create_aggregated_author_results(lda_model, author_tweets):
	"""
	lda_model: A saved gensim.models.LdaModel

	author_tweets: json-file with new author tweets that the topic mixture will be inferred for

	"""

	topic_score = {}

	dictionary = gensim.corpora.Dictionary.load("/tmp/aggr.dict")
	ldamodel = gensim.models.LdaModel.load(lda_model)

	new_tweets = []

	for line in open(author_tweets, "r").readlines():
		line = json.loads(line)
		new_tweets.append([token for token in line["text"].split(" ") if token not in stop_words])


	# Add topic mixture of each tweet to a dict
	for tweet in new_tweets:
		topic_mixture = ldamodel[dictionary.doc2bow(tweet)]
		for element in topic_mixture:
			if not element[0] in topic_score:
				topic_score[element[0]] = element[1]
			else:
				topic_score[element[0]] += element[1]
	
	# Normalize
	for key, value in topic_score.items():
		topic_score[key] /= len(new_tweets)

	sorted_topic_score = sorted(topic_score.items(), key=operator.itemgetter(1))[::-1]

	return sorted_topic_score

def plot_aggregated_author_results(sorted_topic_score):
	"""
	Takes a tuple of (topic_id, score) generated from
	create_aggregated_author_results
	"""

	fig = plt.figure(figsize=(16,8))
	num_topics = len(sorted_topic_score)

	plt.bar(range(num_topics), [el[1] for el in sorted_topic_score])
	plt.title("Hello")
	plt.xticks(np.arange(num_topics)+0.4, ["#Topic %s" % el[0] for el in sorted_topic_score])
	plt.ylim(0, 1)

	fig.subplots_adjust(bottom=0.2)

	plt.show()

	print sorted_topic_score




if __name__ == "__main__":
    #print generate_lda_topics(50, corpus="aggr", dictionary="aggr", passes=50)

    #ldamodel = gensim.models.LdaModel.load("saved_author_original_50p_50t.p")

    topic_scores = create_aggregated_author_results("saved_author_original_50p_50t.p", "elonmusk_test.json")
    
    plot_aggregated_author_results(topic_scores)
