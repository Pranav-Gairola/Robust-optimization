"""
Knapsack Problem Solver: Deterministic and Robust Versions
-----------------------------------------------------------

This script provides implementations for both the deterministic and robust 0-1 Knapsack Problems using PuLP.

1. Deterministic Knapsack Problem (DKP):
   - Select a subset of items to maximize profit without exceeding knapsack capacity.

2. Robust Knapsack Problem (RKP):
   - Solves under budgeted uncertainty in item weights using Bertsimas and Sim’s robust optimization approach.
   - Accounts for worst-case deviations with a parameter Γ (Gamma) that limits the number of items with worst-case deviations.

Example data:
- Number of items: 5
- Profits/values:     [10, 7, 5, 8, 11]
- Nominal weights:    [2, 3, 1, 4, 5]
- Weight deviations:  [1, 2, 1, 1, 3]
- Capacity: 15
- Budget of uncertainty (Γ): 2

Author: Pranav Gairola
"""

import pulp


def solve_deterministic_knapsack(profits, weights, capacity):
    """
    Solves the classical deterministic 0-1 knapsack problem.

    :param profits: List of item profits/values
    :param weights: List of item weights
    :param capacity: Capacity of the knapsack
    :return: Solution status, objective value, decision variables
    """
    n = len(profits)
    prob = pulp.LpProblem("Deterministic_Knapsack", pulp.LpMaximize)

    # Decision variables
    x = [pulp.LpVariable(f"x{i}", cat='Binary') for i in range(n)]

    # Objective function
    prob += pulp.lpSum(profits[i] * x[i] for i in range(n))

    # Capacity constraint
    prob += pulp.lpSum(weights[i] * x[i] for i in range(n)) <= capacity

    # Solve
    prob.solve()

    status = pulp.LpStatus[prob.status]
    objective_value = pulp.value(prob.objective)
    decision_vars = {f"x{i}": pulp.value(x[i]) for i in range(n)}

    return status, objective_value, decision_vars


def solve_robust_knapsack(profits, nominal_weights, deviations, capacity, Gamma):
    """
    Solves the robust 0-1 knapsack problem with budgeted uncertainty in weights.

    :param profits: List of item profits
    :param nominal_weights: List of nominal weights of items
    :param deviations: List of weight deviations for items
    :param capacity: Capacity of the knapsack
    :param Gamma: Budget of uncertainty
    :return: Solution status, objective value, decision variables, gamma, chi values
    """
    n = len(profits)
    prob = pulp.LpProblem("Robust_Knapsack", pulp.LpMaximize)

    # Decision variables
    x = [pulp.LpVariable(f"x{i}", cat='Binary') for i in range(n)]
    gamma = pulp.LpVariable("gamma", lowBound=0)
    chi = [pulp.LpVariable(f"chi{i}", lowBound=0) for i in range(n)]

    # Objective
    prob += pulp.lpSum(profits[i] * x[i] for i in range(n))

    # Robust capacity constraint
    prob += pulp.lpSum(nominal_weights[i] * x[i] for i in range(n)) + Gamma * gamma + pulp.lpSum(chi[i] for i in range(n)) <= capacity

    for i in range(n):
        prob += gamma + chi[i] >= deviations[i] * x[i]

    # Solve
    prob.solve()

    status = pulp.LpStatus[prob.status]
    objective_value = pulp.value(prob.objective)
    decision_vars = {f"x{i}": pulp.value(x[i]) for i in range(n)}
    gamma_value = pulp.value(gamma)
    chi_values = {f"chi{i}": pulp.value(chi[i]) for i in range(n)}

    return status, objective_value, decision_vars, gamma_value, chi_values


def run_knapsack_examples():
    """
    Runs both deterministic and robust knapsack examples with predefined data.
    """
    profits = [10, 7, 5, 8, 11]
    nominal_weights = [2, 3, 1, 4, 5]
    deviations = [1, 2, 1, 1, 3]
    capacity = 15
    Gamma = 2

    print("=== Deterministic Knapsack ===")
    status_d, obj_d, x_d = solve_deterministic_knapsack(profits, nominal_weights, capacity)
    print("Status:", status_d)
    print("Objective value:", obj_d)
    print("Decision variables:")
    for var, val in x_d.items():
        print(f"{var} = {val}")

    print("\n=== Robust Knapsack ===")
    status_r, obj_r, x_r, gamma_r, chi_r = solve_robust_knapsack(profits, nominal_weights, deviations, capacity, Gamma)
    print("Status:", status_r)
    print("Objective value:", obj_r)
    print("Decision variables:")
    for var, val in x_r.items():
        print(f"{var} = {val}")
    print("Gamma value (dual):", gamma_r)
    for var, val in chi_r.items():
        print(f"{var} = {val}")


if __name__ == "__main__":
    run_knapsack_examples()
