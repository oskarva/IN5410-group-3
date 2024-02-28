from pulp import *

# Define the problem
prob = LpProblem("Minimize_Energy_Cost_with_RTP", LpMinimize)

APPLIANCES = ['lighting', 'heating', 'refrigerator-freezer', 'electric_stove', 'TV', 'computer', 'dishwasher', 'laundry_machine', 'cloth_dryer', 'EV']
HOURS = [i for i in range(0, 24)]
CONSUMPTION_AVERAGE = {
    'lighting':1.5,
    'heating':8,
    'refrigerator-freezer':2.64,
    'electric_stove':3.9,
    'TV':0.6,
    'computer':0.6,
    'dishwasher':1.44,
    'laundry_machine':1.94,
    'cloth_dryer':2.5,
    'EV':9.9,
}

# Define your RTP pricing curve here
price_t = [i for i in range(1, 25)]  # This should be a list of 24 prices, one for each hour

# Define decision variables
x_it = LpVariable.dicts("ApplianceRun", (APPLIANCES, HOURS), 0, 1, LpBinary)


# Objective function
prob += lpSum([x_it[i][t] * CONSUMPTION_AVERAGE[i] * price_t[t] for i in APPLIANCES for t in HOURS]), "TotalCost"

# Add constraints for non-shiftable and shiftable appliances

# Solve the problem
prob.solve()

# Output results
print(x_it)
print(value(prob.objective))