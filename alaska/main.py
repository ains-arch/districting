import warnings
import matplotlib.pyplot as plt
from gerrychain import Graph
from gerrychain.tree import recursive_tree_part
import networkx as nx

warnings.filterwarnings("ignore") # Suppress bipartition warning

# Make a districting plan with 20 districts (the number of seats in Alaska's State Senate) using the
# recursive_tree_part function

ak_graph = Graph.from_json("ak-bg-connected.json")
# print(ak_graph.nodes()[0].keys())
# dict_keys(['boundary_node', 'area', 'NWBHPOP20', 'AWATER20', 'VAP20', 'APAMIPOP20', 'FUNCSTAT20',
# 'SUMLEV', 'NHPIPOP20', 'OTHERPOP20', 'WVAP20', 'STATEFP20', 'APAMIVAP20', 'OTHERVAP20', 'BPOP20',
# 'HVAP20', 'WPOP20', '2MOREVAP20', 'MTFCC20', 'CHARITER', 'APAVAP20', 'ASIANVAP20', 'AMINVAP20',
# 'CIFSN', 'GEOCODE', 'AMINPOP20', 'BVAP20', 'FILEID', 'DOJBVAP20', 'TOTPOP20', 'COUNTYFP20',
# '2MOREPOP20', 'INTPTLON20', 'ASIANPOP20', 'LOGRECNO', 'APAPOP20', 'STUSAB', 'BLKGRPCE20',
# 'HISP20', 'TRACTCE20', 'APBPOP20', 'NAMELSAD20', 'ALAND20', 'NHPIVAP20', 'INTPTLAT20',
# 'NWBHVAP20', 'APBVAP20', 'GEOID20'])

# TOTPOP20: Total population according to the 2020 census
# AMINPOP20: American Indian and Alaska Native population
# INTPTLAT20: Latitude of districts
# INTPTLON20: Longitude of districts

# List of populations at each node
list_of_pop = [ak_graph.nodes()[v]['TOTPOP20'] for v in ak_graph.nodes()]

# Total population
total_pop = sum(list_of_pop)

# ak_graph = the dual graph we're using
# range(NUM_DIST) = how many districts to make
# ideal_pop = target population within each district
# 'TOTPOP20' = what node attribute you should use for population
# 0.02 = tolerance for deviation from ideal pop
# 10 = number of times you try one step of the process before giving up

NUM_DIST = 20 # number of seats in Alaska's State Senate
ideal_pop = total_pop/NUM_DIST

# Try until a valid partition is found
initial_plan = None

while initial_plan is None:
    try:
        initial_plan = recursive_tree_part(ak_graph,
                                           range(NUM_DIST),
                                           ideal_pop,
                                           'TOTPOP20',
                                           0.02,
                                           10)
    except RuntimeError as e:
        print(f"Error encountered: {e}. Retrying...")

print("Successfully found a valid partition.")

print(f"Districting plan: {initial_plan}")

# Print the number of cutedges in this districting plan you've made

cutedges = 0

for e in ak_graph.edges():
    if initial_plan[e[0]] != initial_plan[e[1]]:
        cutedges = cutedges + 1

print(f"Number of cutedges in redistricting plan: {cutedges}")

# Compute and print the number of districts in their districting plan that have more than half their
# population being Native American and Alaska Native

AMIN_dists = 0
for v in ak_graph.nodes():
    dist = initial_plan[v]
    if ak_graph.nodes()[v]['AMINPOP20'] > 0.5 * ak_graph.nodes()[v]['TOTPOP20']:
        AMIN_dists += 1

print(f"Number of Native American and Alaska Native Majority Districts: {AMIN_dists}")

# Draw their dual graph such that the colors of the nodes describe which district they're in, and
# the positions of the nodes reflect the latitude and longitude of the geographic region represented
# by that node.

# Get lat/lon to be fed into nx.draw
node_locations = { v : ( float(ak_graph.nodes()[v]["INTPTLON20"]),
                        float(ak_graph.nodes()[v]["INTPTLAT20"])) for v in ak_graph.nodes() }

plt.figure()
nx.draw(ak_graph, node_size = 10, node_color = [initial_plan[v] for v in ak_graph.nodes()],
        pos = node_locations, cmap="tab20")
plt.savefig("initial-plan.jpg")
print("Saved initial-plan.jpg")
