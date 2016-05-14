import pickle
import logging
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from topic.ptm import AuthorTopicModel
from topic.ptm.utils import convert_cnt_to_list, get_top_words

logger = logging.getLogger('AuthorTopicModel')
logger.propagate=False

corpus = pickle.load(open('data/corpus.p'))
doc_author = pickle.load(open('data/doc_author.p', 'rb'))
author_name = pickle.load(open('data/author_name.p', 'rb'))
voca = pickle.load(open('data/vocab.p', 'rb'))

n_doc = len(corpus)
n_topic = 10
n_author = len(author_name)
n_voca = len(voca)
max_iter = 50

model = AuthorTopicModel(n_doc, n_voca, n_topic, n_author)
model.fit(corpus, doc_author, max_iter=max_iter)

for k in range(n_topic):
    top_words = get_top_words(model.TW, voca, k, 10)
    print('topic ', k , ','.join(top_words))

author_id = 6
fig = plt.figure(figsize=(12,6))
plt.bar(range(n_topic), model.AT[author_id]/np.sum(model.AT[author_id]))
plt.title(author_name[author_id])
plt.xticks(np.arange(n_topic)+0.5, ['\n'.join(get_top_words(model.TW, voca, k, 10)) for k in range(n_topic)])
plt.show()
