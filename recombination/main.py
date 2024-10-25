#Needed for gerrychain
from functools import partial
# For making plots
import matplotlib.pyplot as plt
# Needed for gerrychain
from gerrychain import Graph, Partition, constraints, MarkovChain
from gerrychain.updaters import Tally
from gerrychain.tree import recursive_tree_part
from gerrychain.proposals import recom
from gerrychain.accept import always_accept
import geopandas as gpd

# Read shapefile data into a geo data frame, rather than creating a graph
pa_gdf = gpd.read_file("PA/PA.shp")
pa_graph = Graph.from_file("PA/PA.shp")

NUM_DIST = 18 # Number of Congressional Districts in PA (when redistricting lawsuit happened)
tot_pop = sum(pa_graph.nodes()[v]['TOTPOP'] for v in pa_graph.nodes())
ideal_pop = tot_pop/NUM_DIST
POP_TOLERANCE = 0.02
initial_plan = recursive_tree_part(pa_graph,
                                   range(NUM_DIST),
                                   ideal_pop,
                                   'TOTPOP',
                                   POP_TOLERANCE,
                                   10)

# Set up random walk

# Set up partition object
initial_partition = Partition(
    pa_graph, # dual graph
    assignment = initial_plan, # initial districting plan
    updaters = {
        "district population": Tally("TOTPOP", alias = "district population"), 
        "Pres R Votes": Tally("T16PRESR", alias = "Pres R Votes"), 
        "Pres D Votes": Tally("T16PRESD", alias = "Pres D Votes"),
        "Sen R Votes": Tally("T16SENR", alias = "Sen R Votes"), 
        "Sen D Votes": Tally("T16SEND", alias = "Sen D Votes")
    }
)

rw_proposal = partial(recom,                   # How you choose a next districting plan
                      pop_col = "TOTPOP",      # What data describes population
                      pop_target = ideal_pop,  # Target/ideal population is for each district
                                               # (we calculated ideal pop above)
                      epsilon = POP_TOLERANCE, # How far from ideal population you can deviate
                                               # (we set POP_TOLERANCE above)
                      node_repeats = 1         # Number of times to repeat bipartition.
                                               # Can increase if you get a BipartitionWarning
                      )

# Constraint on population: stay within POP_TOLERANCE of ideal

population_constraint = constraints.within_percent_of_ideal_population(
    initial_partition,
    POP_TOLERANCE,
    pop_key = "district population"
    )

# Creating the chain

# The following sets up the chain, but doesn't run it
our_random_walk = MarkovChain(
    proposal = rw_proposal,
    constraints = [population_constraint],
    accept = always_accept, # accepts every proposed plan that meets population criteria
    initial_state = initial_partition,
    total_steps = 100
)

# What ensembles we want to build:  We'll calculate number of R majority districts in the
# 2016 Presidential and Senate elections

# This actually runs the random walk
r_pres_ensemble = []
r_sen_ensemble = []

for part in our_random_walk:
    # Calculate number of districts with more Republican votes than Democratic votes in the 2016
    # Presidential election
    r_pres = 0
    for i in range(NUM_DIST):
        if part["Pres R Votes"][i] > part["Pres D Votes"][i]:
            r_pres = r_pres + 1
    r_pres_ensemble.append(r_pres)

    # Calculate number of districts with more Republican votes than Democratic votes in the 2016
    # Senate election
    r_sen = 0
    for i in range(NUM_DIST):
        if part["Sen R Votes"][i] > part["Sen D Votes"][i]:
            r_sen = r_sen + 1
    r_sen_ensemble.append(r_sen)

# Histogram of number of Republican Districts from the 2016 Presidential Election
plt.figure()
plt.hist(r_pres_ensemble)
plt.savefig("histogram-presidential-republicans.jpg")

# Can specify boundaries between bins to make your plot look a bit nicer
plt.figure()
plt.hist(r_pres_ensemble, bins=[9.5, 10.5, 11.5, 12.5, 13.5], edgecolor='black', color='red')
plt.xticks([10, 11, 12, 13])
plt.xlabel("Republican majority districts", fontsize=12)
plt.ylabel("Ensembles", fontsize=12)
plt.title("Histogram of Republican Districts by Votes in the 2016 Presidential Election",
          fontsize=14)
plt.savefig("histogram-presidential-republicans-clean.jpg", bbox_inches='tight')

# And now a Histogram of number of Republican Districts from the 2016 Presidential Election
plt.figure()
plt.hist(r_sen_ensemble, bins=[9.5, 10.5, 11.5, 12.5, 13.5], edgecolor='black', color='red')
plt.xticks([10, 11, 12, 13])
plt.xlabel("Republican majority districts", fontsize=12)
plt.ylabel("Ensembles", fontsize=12)
plt.title("Histogram of Republican Districts by Votes in the 2016 Senate Election",
          fontsize=14)
plt.savefig("histogram-senate-republicans-clean.jpg", bbox_inches='tight')
