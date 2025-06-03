"""
This script solves the Set Covering Problem (SCP) for a small network example
with both deterministic and robust versions using PuLP.

Author: [Pranav Gairola]
Date: [03-06-2025]
"""

import pulp

# --------------------------
# Input Data
# --------------------------

# Candidate facility sites: A, B, C, D, E, F
sites = ['A', 'B', 'C', 'D', 'E', 'F']

# Cost of opening facility at each site
costs = {
    'A': 10,
    'B': 10,
    'C': 20,
    'D': 20,
    'E': 10,
    'F': 10
}

# Coverage matrix (a_ij): which sites can cover which demand nodes
# Sets N_i for each demand node
coverage = {
    'A': ['A', 'B', 'C'],
    'B': ['A', 'B', 'D'],
    'C': ['A', 'C', 'D'],
    'D': ['B', 'C', 'D', 'E'],
    'E': ['D', 'E'],
    'F': ['F']
}

# Uncertainty in a_ij: δ_ij, assumed only for robust model
delta = 0.5  # box uncertainty with δ_ij = 1 for all i,j pairs

# --------------------------
# Deterministic SCP Model
# --------------------------

print("\n--- Solving Deterministic Set Covering Problem ---")

# Create the problem
det_model = pulp.LpProblem("Deterministic_Set_Covering", pulp.LpMinimize)

# Decision variables: x_j ∈ {0,1}
x = pulp.LpVariable.dicts("x", sites, cat='Binary')

# Objective function: minimize total facility opening cost
det_model += pulp.lpSum([costs[j] * x[j] for j in sites])

# Constraints: for every demand node i, at least one facility covering i must be open
for i, Nj in coverage.items():
    det_model += pulp.lpSum([x[j] for j in Nj]) >= 1, f"Cover_{i}"

# Solve the deterministic model
det_model.solve()
print(f"Status: {pulp.LpStatus[det_model.status]}")
print(f"Minimum Cost: {pulp.value(det_model.objective)}")
print("Selected Facilities:")
for j in sites:
    if x[j].value() == 1:
        print(f" - Facility at site {j}")

# --------------------------
# Robust SCP Model (Box Uncertainty in a_ij)
# --------------------------

print("\n--- Solving Robust Set Covering Problem (Box Uncertainty) ---")

# Create a new problem
rob_model = pulp.LpProblem("Robust_Set_Covering", pulp.LpMinimize)

# New decision variables: x_j ∈ {0,1}
xr = pulp.LpVariable.dicts("x", sites, cat='Binary')

# Objective function remains the same
rob_model += pulp.lpSum([costs[j] * xr[j] for j in sites])

# Robust constraints: ∑_j ((ā_ij - δ_ij) * x_j) ≥ 1
# Since nominal ā_ij = 1 → (1 - δ) = 0 when δ = 1 → only exact cover ensures robustness
for i, Nj in coverage.items():
    rob_model += pulp.lpSum([(1 - delta) * xr[j] for j in Nj]) >= 1, f"Robust_Cover_{i}"

# Solve the robust model
rob_model.solve()
print(f"Status: {pulp.LpStatus[rob_model.status]}")
print(f"Robust Minimum Cost: {pulp.value(rob_model.objective)}")
print("Selected Facilities (Robust):")
for j in sites:
    if xr[j].value() == 1:
        print(f" - Facility at site {j}")
