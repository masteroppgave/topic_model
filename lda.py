import logging
import gensim

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = gensim.corpora.Dictionary.load("/tmp/27jan_tweets.dict")
corpus = gensim.corpora.MmCorpus("/tmp/27jan_tweets.mm")

lda = gensim.models.LdaModel(corpus, id2word=dictionary, num_topics=5, passes=2)
lda.print_topics(5)
