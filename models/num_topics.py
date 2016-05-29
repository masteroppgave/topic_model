import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import logging
import gensim
import argparse

"""
Used for finding the optimal number of topics.
"""

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def create_lsi_model(_file):
	print("=== CREATING LSI MODEL ===")
	print("==========================")
	print("                          ")

	if "." in _file:
		_file = _file.split(".")[0]

	dictionary = gensim.corpora.Dictionary.load("/tmp/" + _file + ".dict")
	corpus = gensim.corpora.MmCorpus("/tmp/" + _file + ".mm")

	tfidf = gensim.models.TfidfModel(corpus, normalize=True)
	corpus_tfidf = tfidf[corpus]

	lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)

	fcoords = open("/tmp/coords_" + _file + ".csv", 'wb')
	for vector in lsi[corpus]:
	    if len(vector) != 2:
	        continue
	    fcoords.write("%6.4f\t%6.4f\n" % (vector[0][1], vector[1][1]))
	fcoords.close()


def plot_graph(_file):
	X = np.loadtxt("/tmp/coords_" + _file + ".csv", delimiter="\t")

	x = [X[i][0] for i in range(len(X))]
	y = [X[i][1] for i in range(len(X))]

	plt.scatter(x, y, alpha=0.5)
	plt.show()



def find_number_of_topics(_file, draw=0):
	print("=== FINDING OPTIMAL NUMBER OF TOPICS (CLUSTERS) ===")
	print("===================================================")
	print("                                                   ")

	if "." in _file:
		_file = _file.split(".")[0]

	MAX_K = 10

	X = np.loadtxt("/tmp/coords_" + _file + ".csv", delimiter="\t")
	ks = range(1, MAX_K + 1)

	inertias = np.zeros(MAX_K)
	diff = np.zeros(MAX_K)
	diff2 = np.zeros(MAX_K)
	diff3 = np.zeros(MAX_K)

	for k in ks:
	    kmeans = KMeans(k).fit(X)
	    inertias[k - 1] = kmeans.inertia_
	    if k > 1:
	        diff[k - 1] = inertias[k - 1] - inertias[k - 2]
	    if k > 2:
	        diff2[k - 1] = diff[k - 1] - diff[k - 2]
	    if k > 3:
	        diff3[k - 1] = diff2[k - 1] - diff2[k - 2]

	elbow = np.argmin(diff3[3:]) + 3

	print "Elbow: " + str(elbow+1)

	if draw:
		plt.plot(ks, inertias, "b*-")
		plt.plot(ks[2], inertias[2], marker='o', markersize=15)
		plt.ylabel("SSE")
		plt.xlabel("k")
		plt.show()

	return (elbow+1)

if __name__=="__main__":
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', type=str, help='JSON file containing tweets.', required=True)
	parser.add_argument('--draw', type=str, help='1 if you want to draw diagram', default=0, required=False)
	parser.add_argument('--skip_lsi', type=int, help='If you already have the LSI data, you can skip it by setting skip_lsi to 1.', default=0, required=False)
	args = parser.parse_args()

	if not args.skip_lsi:
		create_lsi_model(args.file)
	else:
		print("Skipping LSI model")

	find_number_of_topics(args.file, args.draw)
	"""

	create_lsi_model("out_experiment")
	print find_number_of_topics("out_experiment")
