"""
robust_set_covering.py

This script solves the Set Covering Problem (SCP) for a small example network using both
deterministic and robust optimization formulations with PuLP.

Problem Description:
--------------------
You are given a set of candidate facility sites and their associated opening costs.
Each demand node must be covered by at least one open facility. The coverage is based
on a predefined coverage matrix (i.e., each demand node is covered by a subset of facilities).

The goal is to minimize the total facility opening cost while ensuring every demand
node is covered. A robust version of the model is also considered, where coverage
availability is uncertain and modeled with box uncertainty.

Coverage Network (Example):
---------------------------
The network includes both facilities and demand nodes, which in this simplified example
are labeled with the same names ('A' to 'F'). Each demand node i is associated with a set N_i of
facilities that can cover it:

    Demand Node A ← {A, B, C}
    Demand Node B ← {A, B, D}
    Demand Node C ← {A, C, D}
    Demand Node D ← {B, C, D, E}
    Demand Node E ← {D, E}
    Demand Node F ← {F}

This structure defines a bipartite coverage graph between demand nodes and facility sites.

Robust Formulation:
-------------------
Robust optimization is used to hedge against uncertainty in the coverage matrix (a_ij).
A box uncertainty model assumes each entry in a_ij can be reduced by a δ factor (e.g., 0.5),
leading to conservative constraints that ensure coverage even under worst-case deviations.

Author: [Your Name]
Date: [Today’s Date]
"""

import pulp

# --------------------------
# Input Data
# --------------------------

sites = ['A', 'B', 'C', 'D', 'E', 'F']

costs = {
    'A': 10, 'B': 10, 'C': 20, 'D': 20, 'E': 10, 'F': 10
}

coverage = {
    'A': ['A', 'B', 'C'],
    'B': ['A', 'B', 'D'],
    'C': ['A', 'C', 'D'],
    'D': ['B', 'C', 'D', 'E'],
    'E': ['D', 'E'],
    'F': ['F']
}

delta = 0.5


# --------------------------
# Function Definitions
# --------------------------

def solve_deterministic_scp(sites, costs, coverage):
    """
    Solves the deterministic Set Covering Problem (SCP) using linear programming.

    Args:
        sites (list): List of candidate facility sites.
        costs (dict): Dictionary of opening costs for each site.
        coverage (dict): Dictionary mapping each demand node to its covering sites.

    Prints:
        Optimal status, total cost, and selected facilities.
    """
    print("\n--- Solving Deterministic Set Covering Problem ---")
    model = pulp.LpProblem("Deterministic_Set_Covering", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", sites, cat='Binary')
    model += pulp.lpSum([costs[j] * x[j] for j in sites])
    for i, Nj in coverage.items():
        model += pulp.lpSum([x[j] for j in Nj]) >= 1, f"Cover_{i}"
    model.solve()
    print(f"Status: {pulp.LpStatus[model.status]}")
    print(f"Minimum Cost: {pulp.value(model.objective)}")
    print("Selected Facilities:")
    for j in sites:
        if x[j].value() == 1:
            print(f" - Facility at site {j}")


def solve_robust_scp(sites, costs, coverage, delta):
    """
    Solves the robust Set Covering Problem under box uncertainty.

    Args:
        sites (list): List of candidate facility sites.
        costs (dict): Dictionary of opening costs for each site.
        coverage (dict): Dictionary mapping each demand node to its covering sites.
        delta (float): Box uncertainty parameter (e.g., 0.5).

    Prints:
        Robust optimal status, total cost, and selected facilities.
    """
    print("\n--- Solving Robust Set Covering Problem (Box Uncertainty) ---")
    model = pulp.LpProblem("Robust_Set_Covering", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", sites, cat='Binary')
    model += pulp.lpSum([costs[j] * x[j] for j in sites])
    for i, Nj in coverage.items():
        model += pulp.lpSum([(1 - delta) * x[j] for j in Nj]) >= 1, f"Robust_Cover_{i}"
    model.solve()
    print(f"Status: {pulp.LpStatus[model.status]}")
    print(f"Robust Minimum Cost: {pulp.value(model.objective)}")
    print("Selected Facilities (Robust):")
    for j in sites:
        if x[j].value() == 1:
            print(f" - Facility at site {j}")


# --------------------------
# Main Execution
# --------------------------

if __name__ == "__main__":
    solve_deterministic_scp(sites, costs, coverage)
    solve_robust_scp(sites, costs, coverage, delta)
