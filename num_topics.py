import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

"""
Used for finding number of topics
"""

MAX_K = 10

X = np.loadtxt("/tmp/coords.csv", delimiter="\t")
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

print inertias
print inertias[elbow]

plt.plot(ks, inertias, "b*-")
plt.plot(ks[elbow], inertias[elbow], marker='o', markersize=12,
         markeredgewidth=2, markeredgecolor='r', markerfacecolor=None)
plt.ylabel("Inertia")
plt.xlabel("K")
plt.show()
