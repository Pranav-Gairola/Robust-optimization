"""
p_median_facility_location.py

This script solves the classical p-median facility location problem using both
a deterministic formulation and a robust optimization formulation.

Problem Description:
--------------------
Given a set of demand nodes, the goal of the p-median problem is to open `p` facilities
such that the total distance from demand nodes to their assigned open facilities is minimized.

In the **deterministic model**, it is assumed that all distances are known with certainty.

In the **robust model**, certain arcs (i.e., distances between node pairs) are considered uncertain.
The model incorporates a robust optimization approach using a budgeted uncertainty set to safeguard
against worst-case deviations in these uncertain distances.

Key Features:
-------------
- Uses `pulp` for solving MILP problems.
- Demonstrates classical and robust optimization paradigms.
- Ideal for teaching, research, and prototyping in facility location problems.

Author: [Pranav Gairola]
Date: [June 2025]
"""

import pulp
import numpy as np

# ----------------------------
# Input Data
# ----------------------------
nodes = ['A', 'B', 'C', 'D', 'E', 'F']
p = 2  # number of facilities to open

# Distance matrix: symmetric and complete
distance = {
    ('A', 'A'): 0, ('A', 'B'): 4, ('A', 'C'): 8, ('A', 'D'): 12, ('A', 'E'): 6, ('A', 'F'): 9,
    ('B', 'A'): 4, ('B', 'B'): 0, ('B', 'C'): 5, ('B', 'D'): 10, ('B', 'E'): 7, ('B', 'F'): 8,
    ('C', 'A'): 8, ('C', 'B'): 5, ('C', 'C'): 0, ('C', 'D'): 6,  ('C', 'E'): 3, ('C', 'F'): 11,
    ('D', 'A'): 12,('D', 'B'):10, ('D', 'C'): 6, ('D', 'D'): 0,  ('D', 'E'): 5, ('D', 'F'): 7,
    ('E', 'A'): 6, ('E', 'B'): 7, ('E', 'C'): 3, ('E', 'D'): 5,  ('E', 'E'): 0, ('E', 'F'): 4,
    ('F', 'A'): 9, ('F', 'B'): 8, ('F', 'C'):11, ('F', 'D'): 7,  ('F', 'E'): 4, ('F', 'F'): 0,
}

# Uncertain arcs (those with possible distance perturbations)
uncertain_arcs = [('A', 'F'), ('B', 'F'), ('C', 'E')]


def solve_deterministic_p_median(nodes, p, distance):
    """Solves the deterministic p-median problem."""
    print("\n--- Solving Deterministic p-Median ---")
    model = pulp.LpProblem("Deterministic_p-Median", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("Open", nodes, cat="Binary")
    y = pulp.LpVariable.dicts("Assign", [(i, j) for i in nodes for j in nodes], cat="Binary")

    model += pulp.lpSum(distance[i, j] * y[i, j] for i in nodes for j in nodes)

    for i in nodes:
        model += pulp.lpSum(y[i, j] for j in nodes) == 1
    for i in nodes:
        for j in nodes:
            model += y[i, j] <= x[j]
    model += pulp.lpSum(x[j] for j in nodes) == p

    model.solve()

    print("Status:", pulp.LpStatus[model.status])
    print("Objective Value:", pulp.value(model.objective))
    print("Open Facilities:", [j for j in nodes if pulp.value(x[j]) > 0.5])
    print("Assignments:")
    for i in nodes:
        for j in nodes:
            if pulp.value(y[i, j]) > 0.5:
                print(f"  Demand at {i} assigned to facility at {j}")


def solve_robust_p_median(nodes, p, distance, uncertain_arcs):
    """Solves the robust p-median problem with budgeted uncertainty."""
    print("\n--- Solving Robust p-Median ---")
    num_uncertain = len(uncertain_arcs)
    D = np.vstack([np.eye(num_uncertain), -np.eye(num_uncertain)])
    q = np.array([2.0] * (2 * num_uncertain))  # Budget weights

    P = {}
    for i in nodes:
        for j in nodes:
            P[(i, j)] = np.zeros(num_uncertain)
            for k, (iu, ju) in enumerate(uncertain_arcs):
                if (i, j) == (iu, ju):
                    P[(i, j)][k] = 1.0

    model = pulp.LpProblem("Robust_p-Median", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("Open", nodes, cat="Binary")
    y = pulp.LpVariable.dicts("Assign", [(i, j) for i in nodes for j in nodes], cat="Binary")
    w = pulp.LpVariable.dicts("w", range(2 * num_uncertain), lowBound=0)

    nominal = pulp.lpSum(distance[i, j] * y[i, j] for i in nodes for j in nodes)
    robust = pulp.lpSum(q[k] * w[k] for k in range(2 * num_uncertain))
    model += nominal + robust

    for i in nodes:
        model += pulp.lpSum(y[i, j] for j in nodes) == 1
    for i in nodes:
        for j in nodes:
            model += y[i, j] <= x[j]
    model += pulp.lpSum(x[j] for j in nodes) == p

    for l in range(num_uncertain):
        lhs = pulp.lpSum(D[k, l] * w[k] for k in range(2 * num_uncertain))
        rhs = -pulp.lpSum(P[(i, j)][l] * y[i, j] for i in nodes for j in nodes)
        model += lhs == rhs

    model.solve()

    print("Status:", pulp.LpStatus[model.status])
    print("Objective Value:", pulp.value(model.objective))
    print("Open Facilities:", [j for j in nodes if pulp.value(x[j]) > 0.5])
    print("Assignments:")
    for i in nodes:
        for j in nodes:
            if pulp.value(y[i, j]) > 0.5:
                print(f"  Demand at {i} assigned to facility at {j}")



if __name__ == "__main__":
    """Runs both deterministic and robust models."""
    solve_deterministic_p_median(nodes, p, distance)
    solve_robust_p_median(nodes, p, distance, uncertain_arcs)

