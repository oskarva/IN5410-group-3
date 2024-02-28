import numpy as np
from pulp import *

# Define the RTP prices for 24 hours, similar to previous examples
rtp_prices = [0.5 if i < 7 or i > 22 else 1.5 for i in range(24)]  # Lower prices at night, higher during the day

# Define the total energy consumption for non-shiftable appliances (simplified)
#TODO: Calculate based on individual appliances
non_shiftable_consumption = [1.5 for _ in range(24)]  # Constant for simplicity

# Define a single shiftable appliance for this example, e.g., an EV with a requirement of 9.9 kWh
ev_consumption = 9.9

# Initial peak load limit (high to ensure feasibility)
peak_load_limit = 10  # Arbitrary high value to start with

# Setup the optimization problem
prob_peak = LpProblem("Minimize_Cost_and_Peak_Load", LpMinimize)

# Decision variables for scheduling the charging of the EV (binary: charge or not charge at each hour)
ev_schedule = LpVariable.dicts("Charge_EV", range(24), 0, 1, LpBinary)

# Objective Function: Minimize the total energy cost considering only the EV for simplicity
prob_peak += lpSum([rtp_prices[h] * ev_schedule[h] * ev_consumption for h in range(24)])

# Constraint: EV must be charged 9.9 kWh throughout the day
prob_peak += lpSum([ev_schedule[h] * ev_consumption for h in range(24)]) == ev_consumption

# Constraint: Total consumption (non-shiftable + EV charging) must not exceed peak load limit at any hour
for h in range(24):
    prob_peak += (non_shiftable_consumption[h] + ev_schedule[h] * ev_consumption) <= peak_load_limit

# Note: This setup is simplified

prob_peak.solve()
