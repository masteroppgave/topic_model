import vincent
from hashtags import *
import networkx as nx
import matplotlib.pyplot as plt

f = open("11_12_mai.json", "r")
result = (co_occurrences(f.readlines(), 30))

G = nx.Graph()

for element in result:
	i, j = element[0][0], element[0][1]

	G.add_edge(i, j)

edges = [(u, v) for (u,v,d) in G.edges(data=True)]

pos=nx.spring_layout(G)

nx.draw_networkx_nodes(G,pos,node_size=1000, node_color = [0.32, 0.54, 0.77])

nx.draw_networkx_edges(G,pos,edgelist=edges, width=3)

nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif')

plt.show()

