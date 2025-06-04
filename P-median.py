"""
Title: Deterministic and Robust p-Median Problem Solver using PuLP

Author: Pranav Gairola
Date: June 2025

Description:
This script implements a deterministic and robust formulation of the p-median facility location problem using the PuLP optimization library in Python.

Problem:
Given a set of demand nodes and pairwise distances, the goal is to locate exactly 'p' facilities such that the total assignment distance is minimized. Each demand node must be assigned to one of the open facilities.

Structure:
- Part 1: Solves the deterministic p-median problem.
- Part 2: Solves the robust p-median version using affine dual constraints.

Dependencies:
- PuLP
- NumPy

How to Use:
- Modify the 'nodes', 'distance' matrix, or number of facilities `p` as needed.
- Run the script to view open facilities, assignments, and objective values.

Illustration:
Example network used in this code:
    
        A ——4—— B ——5—— C
        |     /       | \ 
        6   7        3  11
        | /          |   \
        E ——5—— D ——7—— F
         \             /
          ————4——————

    Distances between nodes are symmetric and taken as per the matrix.
    Robust Extension:
    A robust version considers uncertainty in selected arc distances:
    - Uncertain arcs: ('A', 'F'), ('B', 'F'), and ('C', 'E') with deviation ±2 units.
    - A polyhedral uncertainty set is modeled via dualization for worst-case deviation handling.

    Uncertainty applies on arcs: ('A','F'), ('B','F'), and ('C','E') (highlighted with ±2 in the robust version).

"""

import pulp

# Data
nodes = ['A', 'B', 'C', 'D', 'E', 'F']
p = 2  # number of facilities

# Distances
distance = {
    ('A', 'A'): 0, ('A', 'B'): 4, ('A', 'C'): 8, ('A', 'D'): 12, ('A', 'E'): 6, ('A', 'F'): 9,
    ('B', 'A'): 4, ('B', 'B'): 0, ('B', 'C'): 5, ('B', 'D'): 10, ('B', 'E'): 7, ('B', 'F'): 8,
    ('C', 'A'): 8, ('C', 'B'): 5, ('C', 'C'): 0, ('C', 'D'): 6,  ('C', 'E'): 3, ('C', 'F'): 11,
    ('D', 'A'): 12,('D', 'B'):10, ('D', 'C'): 6, ('D', 'D'): 0,  ('D', 'E'): 5, ('D', 'F'): 7,
    ('E', 'A'): 6, ('E', 'B'): 7, ('E', 'C'): 3, ('E', 'D'): 5,  ('E', 'E'): 0, ('E', 'F'): 4,
    ('F', 'A'): 9, ('F', 'B'): 8, ('F', 'C'):11, ('F', 'D'): 7,  ('F', 'E'): 4, ('F', 'F'): 0,
}

model = pulp.LpProblem("Deterministic_p-Median", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Open", nodes, cat="Binary")  # facility open
y = pulp.LpVariable.dicts("Assign", [(i, j) for i in nodes for j in nodes], cat="Binary")

# Objective: Minimize total distance
model += pulp.lpSum(distance[i, j] * y[i, j] for i in nodes for j in nodes)

# Each demand is assigned to one facility
for i in nodes:
    model += pulp.lpSum(y[i, j] for j in nodes) == 1

# Assign only to open facilities
for i in nodes:
    for j in nodes:
        model += y[i, j] <= x[j]

# Open exactly p facilities
model += pulp.lpSum(x[j] for j in nodes) == p

# Solve
model.solve()

# Output
print("Status:", pulp.LpStatus[model.status])
print("Objective Value:", pulp.value(model.objective))
print("Open Facilities:", [j for j in nodes if pulp.value(x[j]) > 0.5])
print("Assignments:")
for i in nodes:
    for j in nodes:
        if pulp.value(y[i, j]) > 0.5:
            print(f"  Demand at {i} assigned to facility at {j}")

# Now add uncertainty on arcs: ('A', 'F'), ('B', 'F'), ('C', 'E') with deviation up to ±2.
# We use dualization for the worst-case distance deviations.

import numpy as np

# Uncertain arcs and dimension of uncertainty
uncertain_arcs = [('A', 'F'), ('B', 'F'), ('C', 'E')]
num_uncertain = len(uncertain_arcs)

# Polyhedral set: |ξ_k| <= 2 -> Dξ + q >= 0
D = np.vstack([np.eye(num_uncertain), -np.eye(num_uncertain)])
q = np.array([2.0] * (2 * num_uncertain))

# Sensitivity matrix P[(i,j)][k]
P = {}
for i in nodes:
    for j in nodes:
        P[(i, j)] = np.zeros(num_uncertain)
        for k, (iu, ju) in enumerate(uncertain_arcs):
            if (i, j) == (iu, ju):
                P[(i, j)][k] = 1.0  # distance changes by ξ_k

# Build robust model
model = pulp.LpProblem("Robust_p-Median", pulp.LpMinimize)

x = pulp.LpVariable.dicts("Open", nodes, cat="Binary")
y = pulp.LpVariable.dicts("Assign", [(i, j) for i in nodes for j in nodes], cat="Binary")
w = pulp.LpVariable.dicts("w", range(2 * num_uncertain), lowBound=0)

# Objective = Nominal + max deviation (dualized)
nominal = pulp.lpSum(distance[i, j] * y[i, j] for i in nodes for j in nodes)
robust = pulp.lpSum(q[k] * w[k] for k in range(2 * num_uncertain))
model += nominal + robust

# Same constraints as before
for i in nodes:
    model += pulp.lpSum(y[i, j] for j in nodes) == 1
for i in nodes:
    for j in nodes:
        model += y[i, j] <= x[j]
model += pulp.lpSum(x[j] for j in nodes) == p

# Robust dual constraints: Dᵀw = -Pᵀ y
for l in range(num_uncertain):
    lhs = pulp.lpSum(D[k, l] * w[k] for k in range(2 * num_uncertain))
    rhs = -pulp.lpSum(P[(i, j)][l] * y[i, j] for i in nodes for j in nodes)
    model += lhs == rhs

# Solve
model.solve()

# Output
print("Status:", pulp.LpStatus[model.status])
print("Objective Value:", pulp.value(model.objective))
print("Open Facilities:", [j for j in nodes if pulp.value(x[j]) > 0.5])
print("Assignments:")
for i in nodes:
    for j in nodes:
        if pulp.value(y[i, j]) > 0.5:
            print(f"  Demand at {i} assigned to facility at {j}")
