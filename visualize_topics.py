import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

NUM_TOPICS = 5

X = np.loadtxt(os.path.join("/tmp/coords.csv"), delimiter="\t")
kmeans = KMeans(NUM_TOPICS).fit(X)
y = kmeans.labels_

colors = ["b", "g", "r", "m", "c"]
for i in range(X.shape[0]):
    plt.scatter(X[i][0], X[i][1], c=colors[y[i]], s=10)    
plt.show()
