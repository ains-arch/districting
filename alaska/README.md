Data: Connected Alaska Block Group dual graph from
[MGGG](http://data.mggg.org.s3-website.us-east-2.amazonaws.com/dual-graphs/). One edit made to move
a single node's longitude from positive something to negative something >180 so that the dual graph
would plot correctly.

Code uses the `gerrychain` library to
* make a districting plan with 20 districts (the number of seats in Alaska's State Senate) using the `recursive_tree_part` function
* prints the number of cutedges in this districting plan
* computes and prints the number of districts in the true districting plan that have more than half their population being Native American and Alaska Native
* Draw our plan's dual graph such that the colors of the nodes describe which district they're in, and the positions of the nodes reflect the latitude and longitude of the geographic region represented by that node
