import numpy as np
from pulp import *

# Step 1: Define the simplified RTP curve again
np.random.seed(1)  # Changing the seed for a different RTP curve
rtp_prices = np.random.uniform(low=0.5, high=2.0, size=24)  # Simulated RTP prices
hours = [i for i in range(24)]

# Step 2: Setup for households
# Let's simplify to 30 households, with 15 having an EV
num_households = 30
ev_households = 15  # Half the households have an EV

# Assuming each EV needs to be charged once a day, needing 9.9 kWh
ev_consumption = 9.9

# Define the optimization problem
prob_neighborhood = LpProblem("Minimize_Neighborhood_Energy_Cost", LpMinimize)

# Decision variables for EV charging schedule across households with an EV
x_neighborhood = LpVariable.dicts("EV_schedule", (range(ev_households), hours), 0, 1, LpBinary)

# Objective Function: Minimize total cost for EV charging in the neighborhood
prob_neighborhood += lpSum([rtp_prices[h] * x_neighborhood[i][h] * ev_consumption for i in range(ev_households) for h in hours])

# Constraints: Each EV needs to be charged once a day
for i in range(ev_households):
    prob_neighborhood += lpSum([x_neighborhood[i][h] for h in hours]) == 1

#TODO: Include all appliances, not just EVs

prob_neighborhood.solve()
