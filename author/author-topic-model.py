import pickle
import logging
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from topic.ptm import AuthorTopicModel
from topic.ptm.utils import convert_cnt_to_list, get_top_words

logger = logging.getLogger('AuthorTopicModel')
logger.propagate=False

corpus = pickle.load(open('data/corpus3.p'))
doc_author = pickle.load(open('data/doc_author3.p', 'rb'))
author_name = pickle.load(open('data/author_name3.p', 'rb'))
voca = pickle.load(open('data/vocab3.p', 'rb'))

n_doc = len(corpus)
n_topic = 10
n_author = len(author_name)
n_voca = len(voca)
max_iter = 50

def create_model(output_file):
	"""
	Trains the author-topic model and pickles it
	"""

	model = AuthorTopicModel(n_doc, n_voca, n_topic, n_author)
	model.fit(corpus, doc_author, max_iter=max_iter)

	with open(output_file, "wb") as out:
		pickle.dump(model, out)


def graph_distribution(model_file, author_id=1):

	model = open(model_file, "rb")
	model = pickle.load(model)

	for k in range(n_topic):
	    top_words = get_top_words(model.TW, voca, k, 10)
	    print('topic ', k , ','.join(top_words))

	fig = plt.figure(figsize=(16,8))

	print "BARSTART"
	print range(n_topic), model.AT[author_id]/np.sum(model.AT[author_id])
	print "BAREND"

	plt.bar(range(n_topic), model.AT[author_id]/np.sum(model.AT[author_id]))
	plt.title(author_name[author_id])
	plt.xticks(np.arange(n_topic)+0.5, ['\n'.join(get_top_words(model.TW, voca, k, 10)) for k in range(n_topic)])
	plt.ylim(0, 1)

	fig.subplots_adjust(bottom=0.2)

	plt.show()

if __name__ == "__main__":
	print author_name
	#create_model("modelw.p")
	graph_distribution("model3.p")
