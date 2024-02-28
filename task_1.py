from pulp import LpProblem, LpMinimize, LpVariable, LpBinary, value

# Define the problem
prob = LpProblem("Minimize_Energy_Cost", LpMinimize)

# Decision variables for whether each appliance runs during peak hours (binary: 0 or 1)
x1 = LpVariable("WashingMachineDuringPeak", 0, 1, LpBinary)
x2 = LpVariable("EVDuringPeak", 0, 1, LpBinary)
x3 = LpVariable("DishwasherDuringPeak", 0, 1, LpBinary)

# Define the objective function (total cost)
prob += (x1 * 1 + (1 - x1) * 0.5) * 1.94 + (x2 * 1 + (1 - x2) * 0.5) * 9.9 + (x3 * 1 + (1 - x3) * 0.5) * 1.44

# Solve the problem
prob.solve()

# Output the results
print("Total Cost:", value(prob.objective))
