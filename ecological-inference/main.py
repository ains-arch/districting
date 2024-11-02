import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import numpy as np
import pymc as pm
import pandas as pd
from pyei.two_by_two import TwoByTwoEI
from pyei.goodmans_er import GoodmansER
from pyei.io_utils import from_netcdf, to_netcdf

# Code heavily yoinked from chatgpt
# https://chatgpt.com/share/6725cda6-11b4-800f-8b2a-ed5f58067224

# Data points
percent_black = np.array([0.05, 0.1, 0.1, 0.15, 0.2, 0.2]).reshape(-1, 1)
a_support = np.array([0.1, 0.12, 0.15, 0.2, 0.23, 0.28])

# Plot the scatter plot
plt.figure()
plt.scatter(percent_black, a_support)
plt.xlabel('Percent of Voters who are Black')
plt.ylabel('Percentage Voting for Candidate A')
plt.savefig("scatterplot.png")

# Create and fit the model
model = LinearRegression()
model.fit(percent_black, a_support)

# Predict y values for the line of best fit
a_support_pred = model.predict(percent_black)

# Get the equation of the line
slope = model.coef_[0]
intercept = model.intercept_
print(f"Equation of the line: y = {slope:.2f}x + {intercept:.2f}")

# Plot the line of best fit
plt.figure()
plt.plot(percent_black, a_support_pred, color='red',
         label=f'Line of Best Fit: y = {slope:.2f}x + {intercept:.2f}')
plt.legend()
plt.savefig("best_fit.png")

# Create tomography lines for each district
plt.figure()

# Generate x values (possible proportion of Black voters supporting the candidate)
x_vals = np.linspace(0, 1, 100)

# Plot each district's tomography line using the given formula
plt.figure(figsize=(10, 8))
for i in range(len(percent_black)):
    # Calculate y values based on the provided formula
    y_vals = ((percent_black[i] - 1) / percent_black[i]) * x_vals + a_support[i]/percent_black[i]
    
    # Plot the tomography line for this district
    plt.plot(x_vals, y_vals, label=f'District {i+1}')

plt.ylim(0, 1)
plt.xlabel("Proportion of Black Voters Supporting Candidate")
plt.ylabel("Proportion of Non-Black Voters Supporting Candidate")
plt.title("Ecological Inference Tomographic Plot")
plt.legend()
plt.savefig("tomography.png")

waterbury_data = pd.read_csv("WaterburySampleData.csv")
print(waterbury_data.shape)
# (23, 7)
print(waterbury_data.columns)
# Index(['Precinct', 'Total.Votes', 'Tom.Foley', 'Dan.Malloy', 'White.Pct',
       # 'Black.Pct', 'Hispanic.Pct'],
      # dtype='object')
print(waterbury_data.head())
  # Precinct  Total.Votes  Tom.Foley  Dan.Malloy  White.Pct  Black.Pct  Hispanic.Pct
# 0     71-1         1271      0.570       0.402      0.854      0.097         0.114
# 1     71-2          805      0.539       0.432      0.776      0.141         0.214
# 2     71-3         1321      0.568       0.406      0.847      0.096         0.136
# 3     72-1          310      0.223       0.770      0.391      0.530         0.475
# 4     72-2          413      0.148       0.816      0.231      0.686         0.445

group_fraction_2by2 = np.array(waterbury_data["Black.Pct"])
# group_fraction_2by2 = np.array(waterbury_data["Hispanic.Pct"])
votes_fraction_2by2 = np.array(waterbury_data["Dan.Malloy"])
precinct_pops = np.array(waterbury_data["Total.Votes"])

demographic_group_name_2by2 = "Black"
candidate_name_2by2 = "Malloy"
precinct_names = waterbury_data['Precinct']

ei_2by2 = TwoByTwoEI(model_name="king99_pareto_modification", pareto_scale=15, pareto_shape=2)

# Fit the model
ei_2by2.fit(group_fraction_2by2,
       votes_fraction_2by2,
       precinct_pops,
       demographic_group_name=demographic_group_name_2by2,
       candidate_name=candidate_name_2by2,
       precinct_names=precinct_names,
       draws=1200, # optional
       tune=3000, # optional
)

model = ei_2by2.sim_model
pm.model_to_graphviz(model)

plt.figure()
ei_2by2.plot()
plt.savefig("precincts.png")

print(ei_2by2.summary())
print(ei_2by2.polarization_report(percentile=95, reference_group=0, verbose=True))
print(ei_2by2.polarization_report(threshold=0.10, reference_group=0, verbose=True))

# Fitting Goodman's ER - precincts not weighted by population

# Create a GoodmansER object
goodmans_er = GoodmansER()

# Fit the model
goodmans_er.fit(
    group_fraction_2by2,
    votes_fraction_2by2,
    demographic_group_name=demographic_group_name_2by2,
    candidate_name=candidate_name_2by2
)

# Generate a simple report to summarize the results
print(goodmans_er.summary())

# Fitting Goodman's ER - precincts weighted by population
goodmans_er = GoodmansER(is_weighted_regression="True")

goodmans_er.fit(group_fraction_2by2,
    votes_fraction_2by2,
    precinct_pops, # Must include populations if weighting by population
    demographic_group_name=demographic_group_name_2by2,
    candidate_name=candidate_name_2by2
)

print(goodmans_er.summary())

plt.figure()
goodmans_er.plot()
plt.savefig("goodmans.png")
