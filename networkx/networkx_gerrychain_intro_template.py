# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Intro to Networkx and GerryChain
# @author: scannon, with edits by eveomett <br>
# Math of Political Districting, Claremont McKenna College, Fall 2024 <br>
# Introduction to graphs & partitions with networkx and gerrychain

# ### Import necessary packages

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import random
import pandas as pd
import geopandas as gpd
import gerrychain   
from gerrychain import Graph, Partition, GeographicPartition
from gerrychain.tree import recursive_tree_part

# ## Section 1: Networkx

# Main python class for working with graphs: documentation at [https://networkx.org/](https://networkx.org/)

# You can build graphs node-by-node and edge-by-edge, see example.py/example.ipynb <br>
# (In this class, we'll build graphs from real-world data)

# We can also make special types of graphs, such as a grid graph (will use as an example) <br>
# Other types of graphs can be found at [https://networkx.org/documentation/networkx-1.9/reference/generators.html](https://networkx.org/documentation/networkx-1.9/reference/generators.html)

# +
grid = nx.grid_graph([4,4]) # this makes a 4 x 4 grid graph 

print("A drawing of our grid graph:")
plt.figure()
nx.draw(grid, node_size = 1000, node_color = "pink", with_labels = True)
plt.savefig("grid_graph.png")
# -

# When drawing, positions are chosen automatically<br>
# We can also specify the positions of the nodes manually (for example, using latitutde/longitude) <br>
# You can find more drawing options at [https://networkx.org/documentation/stable/reference/drawing.html](https://networkx.org/documentation/stable/reference/drawing.html)

# Sometimes we need to access nodes or edges from a graph we've imported.
#  <br>
# `grid.nodes()` returns a list of all nodes in the graph<br>
# `grid.edges()` returns a list of all edges in the graph<br>

# We can check whether a graph is connected. <br>
# `nx.is_connected(graph)` returns true if graph connected, false otherwise

# +
nx.is_connected(grid)
# -

# We can create an *induced subgraph*.  <br>
# `nx.subgraph(graph, list_of_nodes)` returns a new networkx graph that contains all nodes in list_of_nodes and all edges between them 
# <br>
# (In grid graphs, the 'names' of nodes are ordered pairs; this isn't the case in other graphs)

# +
grid_subgraph = nx.subgraph(grid, [(0,0),(1,1),(1,0),(2,1),(3,3)])
plt.figure()
nx.draw(grid_subgraph, node_size = 1000, node_color = "pink", with_labels = True)
plt.savefig("grid_subgraph.png")
# +

# ### Districting plans: a dictionary on nodes
# Let's make a plan where each node's district is its x-coordinate

# +
distplan = { v:v[0] for v in grid.nodes()}
print(f"DEBUG: distplan: {distplan}")
# - 

# We can visualize the districts by coloring the nodes within a district by the same color. <br>
# Here we use `nx.draw()` to color: specify color by giving a list.

# +
# Make a list of the colors each node should have
node_color_list = [ distplan[v] for v in grid.nodes()]

# Plot graph with these colors for nodes
plt.figure()
nx.draw(grid, node_size = 1000, node_color = node_color_list, with_labels = True)
plt.savefig("grid_graph_color.png")
# -

# Here's another districting plan

# +
distplan2 = distplan
distplan2[(0,0)] = 2
distplan2[(2,3)] = 3
# Plot graph with these colors for nodes
plt.figure()
nx.draw(grid, node_size = 1000, node_color = [distplan2[v] for v in grid.nodes()], with_labels = True)
plt.savefig("grid_graph_distplan.png")
# -

# The one above looks funny: the districts are not all connected. <br>
# Let's verify that:

# +
for i in range(4):
    verts_in_dist = [v for v in grid.nodes() if distplan2[v] == i]
    district = nx.subgraph(grid, verts_in_dist)
    print(f"Is district {i} connected? {nx.is_connected(district)}")
# -

# ### Cut edges can be used as a compactness score.  
# Below we count the cut edges.  Note that `e[0]` and `e[1]` access the endpoints of each edge.

# +
#Let's go back to our original districitng plan
distplan = {v:v[0] for v in grid.nodes()}

# Counting cutedges
cutedges = 0
for e in grid.edges():
    if distplan[e[0]] != distplan[e[1]]:
        cutedges = cutedges + 1 #TODO: fix this

print("Number of cutedges in distplan: ", cutedges)
# -

#  ### Accessing attributes to nodes

# Let's first create random populations for each node and add to graph<br>
# (Shouldn't need to do this; our graphs will come with attributes from real world data)

np.random.seed(123456)
population_dict = {v:random.randint(100) for v in grid.nodes()}
nx.set_node_attributes(grid, population_dict, "population")

# Access all the populations at once



# Access the populations of each node individually



# # Section 2: Graphs and Partitions in Gerrychain

#
# <br>
# Gerrychain has a Graph class, that is based on a networkx graph<br>
# Gerrychain has methods to read a graph in from a .json file or construct a graph from a shapefile<br>
# <br>
# Note that there are more dual graphs at: http://data.mggg.org.s3-website.us-east-2.amazonaws.com/dual-graphs/ if you'd like to play with those. <br>
# Caution:  have not been carefully checked/vetted/investigated <br>
# Maine - have different total populations on BGs and VTDs
# <br>

# ### Pennsylvania Example
# Let's create a dual graph of Pennsylvania's voting tabulation districts using a json. <br>
# Now we can check whether the graph is planar, connected, etc. <br>
# Note that this is an example of a non-planar dual graph! 

pa_graph = Graph.from_json("PA.json")
print("Is this dual graph connected? ")
print("Is this dual graph planar? ")
print("Number of Nodes: ")
print("Number of Edges: ")

# Note that drawing the dual graph isn't that useful with this many nodes.  (It also takes a minute).

plt.figure() 
nx.draw(pa_graph, node_size = 10,  node_color = "pink")
plt.show()

# What information is there on the nodes? 



#
# <br>
# 'TOTPOP': Total population according to the 2010 census<br>
# 'SEN10D': Number of votes for Democratic candidate in 2010 Senate race<br>
# 'ATG12R' : Number of votes for Republican candidate in 2012 Attorney General race <br>
# 'HVAP': Hispanic voting-age population according to the 2010 census<br>
# 'NH_AMIN': Non-Hispanic American Indian and Alaska Native Population, according to the 2010 census<br>
# 'INTPTLAT10': Lattitude of an point inside the VTD<br>
# 'INTPTLON10': Latitude of a point inside the VTD<br>
# 'CD_2011': District Assignment for Congressional Districts in the 2011 plan<br>
# etc.<br>
#

# Let's get total population

# +
# Population at node 0 (Note nodes are 'named' 0, 1, 2, 3, etc.)


# List of populations at each node


# Total population

print("Total Population: ")
# -

# Let's draw the vertices at a location given by their latitude/longitude, colored by 2011 district

# List of node colors


# +
# Dictionary of node positions
# Longitude of node 0: 


# Format needed for positions: dictionary where key is v and value is ordered pair (x-coord, y-coord)
# Location for node 0 


# Getting these values for every node



# -

#Drawing a figure with these colors and locations
# cmap = "tab20" changes the color scheme so that districts are easier to see
plt.figure()
nx.draw(pa_graph, node_size = 10,  node_color = node_colors, cmap="tab20")
plt.show()

# ## Importing From Shapefiles
#
# Some data, but not all, has already been turned into dual graphs and stored in .json format<br>
# But, this is not always the case <br>
# Can also import data directly from shapefiles (we'll learn a lot more about shapefiles later)<br> 
# You may want to do this for your miniproject<br>
# Shapefiles for many states at: https://github.com/mggg-states <br>
# Use gerrychain's `Graph.from_file()`

graph = Graph.from_file("E:/Math 195 Fall 2024/PA/PA.shp")

# Should get the same graph. Check has same number of nodes and same total population. 
#

# +
print("Total Nodes: ")

print("Total Population: ")
# -

# Note that the graph nodes have one additional attribute: ``` `geometry` ```.  This is because we got it from a shapefile.



# Can also read shapefiles into geodataframes rather than graphs (More on this later) <br>
# This lets you do a lot of additional things, such as visualizing the map (and more) <br>
# This data is from the map that has the *Goofy Kicking Donald Duck* district.   <br>

# +
# Read shapefile data into a geo data frame, rather than creating a graph

# Make a districting plan, using the "CD_2011" column

# Draw the map 

# -

# ### Make an initial districting plan using recursive_tree_part

# This makes a random districting plan. This plan will be the starting point for random walks that build our ensemble<br>
# Arguments in the recursive_tree_part function: 
# ```
# pa_graph = the dual graph we're using
# range(num_dist) = how many districts to make
# ideal_pop = target population within each district
# 'TOTPOP' = what node attribute you should use for population
# 0.02 = tolerance for deviation from ideal pop
# 10 = number of times you try one step of the process before giving up (we usually don't need to worry about this)
# ```
#

# +
 # in the example plan we drew, there were 18 districts; as of 2020, PA only has 17



# -

# This initial plan is a dictionary
# node:district
# Node 8551 is in district 0, etc. 


# We can draw this districting plan like we did above

plt.figure()
nx.draw(pa_graph, node_size = 10,  node_color = "pink", pos = node_locations, cmap="tab20")
plt.show()

# We can count the cut edges of the partition

# +
cutedges = 0

print("Number of cutedges in initial_plan: ", cutedges)
# -

# We can see how this compares to the number of cutedges in the 2011 plan. <br>
# (Need to access differently - 2011 plan is a node attribute, rather than a separate deictionary)

# +
cutedges = 0 

print("Number of cutedges in CD_2011 Plan: ", cutedges)
# -

# Our random initial plan has fewer cutedges than the 2011 plan!

#  Find the population of each district:

# +

    
print("Populations of Districts: ")
# -

# # Activity
# ## 1. Networkx
# a.  Make a 5x5 grid graph



#
# b. Make a districting plan for it with 5 districts (manually or with some other method)
#
#



# c. Check whether your districting plan has connected districts



# d. Draw your districting plan, with colors for the nodes that show the districts



# ## 2. Gerrychain
#
# a. Pick a different state and download a (connected) dual graph from http://data.mggg.org.s3-website.us-east-2.amazonaws.com/dual-graphs/ or a shapefile from https://github.com/mggg-states. 
#

# b. Import your dual graph and see how many nodes and edges it has; double-check that it's connected



# c. Find the total population in your state



# d. Decide on a number of districts to use and calculate the ideal population per district 
# (tip: if the number of districts is too large or the population tolerance is too small, recursive_tree_part can take a long time to run)



# e. Use recursive_tree_part to make a districting plan.



# f. Find the number of cutedges your districting plan has



# ## BONUS ACTIVITY 1
#
# For both the distriting plan we created above for Pensylvania and the plan given by "CD_2011", sum up across districts the total Democratic votes in the 2016 presidential election and the total Republican votes in the 2016 presidential election ('T16PRESD', 'T16PRESR'). In each plan, how many districts have more Democratic votes and how many districts have more Repuiblican votes? 



# ## BONUS ACTIVITY 2
#  
# For the dual graph you chose, find out whether it has latitude/longitude at each vertex, and if so what those attributes are called (if it doesn't have latitutde/longitude, try another state). Draw your districting plan with the vertices at locations given by longitude/latitude


