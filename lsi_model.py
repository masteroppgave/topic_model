import os
import logging
import gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = gensim.corpora.Dictionary.load("/tmp/27jan_tweets.dict")
corpus = gensim.corpora.MmCorpus("/tmp/27jan_tweets.mm")

tfidf = gensim.models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)

fcoords = open("/tmp/coords.csv", 'wb')
for vector in lsi[corpus]:
    if len(vector) != 2:
        continue
    fcoords.write("%6.4f\t%6.4f\n" % (vector[0][1], vector[1][1]))
fcoords.close()
