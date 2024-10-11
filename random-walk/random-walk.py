# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: la_pip
#     language: python
#     name: python3
# ---

# ## Random Walk Example

# +
import numpy as np
import matplotlib.pyplot as plt 
T = np.array([[ 0 , 0.6 , 0.4], 
              [0.5, 0.1 , 0.4],
              [0.8,  0 ,  0.2]])


# -

#Set x0
x = [1,0,0]
plt.bar( ['A', 'B', 'C'], x)
step = 0

# Run one step of chain
step = step + 1
x = np.matmul(x,T)
print(x) 
plt.bar( ['A', 'B', 'C'], x)
plt.title("Probability Distribution after " + str(step) + " transitions")
plt.savefig('random-walk-1.png')

# Run another step of chain
step = step + 1
x = np.matmul(x,T)
print(x) 
plt.bar( ['A', 'B', 'C'], x)
plt.title("Probability Distribution after " + str(step) + " transitions")
plt.savefig('random-walk-2.png')

# Check the stationary distribution
pi = [2/5, 4/15, 1/3]
print(f"DEBUG: pi: {pi}")

pi_prime = np.matmul(pi,T)
print(f"DEBUG: pi_prime: {pi_prime}")

print(f"Stationary distribution? {pi == pi_prime}")
