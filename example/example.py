#Math 195: Math of Political Districting
#Test that correct packages have been set up
#Sarah Cannon
#Claremont McKenna College

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import random
import pandas as pd
import geopandas as gpd
import gerrychain   
from gerrychain import Graph, Partition, GeographicPartition
from gerrychain.tree import recursive_tree_part

## Testing networkx
g = nx.Graph() # Make an empty graph
g.add_node("A") # Add a node named A; can gives nodes labels that are strings
g.add_node(2) # Add a node named 2; can also give nodes labels that are integers
g.add_nodes_from([3,4,5]) # Add nodes 3,4,5

g.add_edge("A",2) #Add an edge from A to 2
g.add_edges_from([(2,3), (2,4), (2,5)]) #Add 3 more edges
g.add_edge("A","B") # If B is not already a node, node B is automatically added

# Testing matplotlib by attempting to draw the graph we just made
print("A drawing of our graph:")
plt.figure() # start a figure
nx.draw(g, node_size = 1000, node_color = 'pink', with_labels = True)
plt.savefig('graph.png')

# Testing numpy by making a matrix and printing it
print("A numpy matrix:")
a = np.matrix('1 2; 3 4')
print(a)

# Testing gerrychain by importaing a dual graph and printing the attributes of one node
dual_graph = Graph.from_json("PA.json")
print("The data stored at one vertex of the imported dual graph (PA's Voting Tabulation Districts):")
print(dual_graph.nodes[0])
## Print the number of nodes
print("Number of Nodes: ", len(dual_graph.nodes()))
## Print the total population of the first vertex of the dual graph
print("Population of Node 0: ", (dual_graph.nodes[0])['TOTPOP'])






    


