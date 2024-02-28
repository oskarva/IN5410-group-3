from pulp import *
import numpy as np

# Generate a random RTP curve for 24 hours
np.random.seed(0)  # For reproducibility
rtp_prices = np.random.uniform(low=0.5, high=2.0, size=24)  # Simulated RTP prices from 0.5 to 2.0

# Define the problem
prob = LpProblem("Minimize_Energy_Cost", LpMinimize)

# Appliances setup
appliances = ['Dishwasher', 'LaundryMachine', 'ClothDryer', 'EV']
consumption = {'Dishwasher': 1.44, 'LaundryMachine': 1.94, 'ClothDryer': 2.5, 'EV': 9.9}  # kWh per operation

# Decision variables: binary variables indicating whether an appliance runs in a given hour
hours = list(range(24))
x = LpVariable.dicts("schedule", (appliances, hours), 0, 1, LpBinary)

# Objective Function: Minimize total energy cost
prob += lpSum([rtp_prices[h] * x[a][h] * consumption[a] for a in appliances for h in hours])

# Constraints: Each shiftable appliance runs once a day
for a in appliances:
    prob += lpSum([x[a][h] for h in hours]) == 1

# Solve the problem
prob.solve()

# Output the results
schedule = {a: [x[a][h].varValue for h in hours] for a in appliances}
total_cost = value(prob.objective)

print("Optimal Schedule:", schedule)
print("Total Cost:", total_cost)
