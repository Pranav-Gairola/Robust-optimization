"""
Robust Knapsack Problem (RKP) Implementation using PuLP
--------------------------------------------------------

This script solves a robust version of the classical 0-1 Knapsack Problem
under budgeted uncertainty in item weights. The goal is to select a subset
of items to maximize value while ensuring that the total weight remains
within capacity under worst-case deviations.

Robust formulation uses the dualization technique under a budgeted uncertainty set.

Formulation and data based on the example:

- Number of items: 5
- Profits/values:     [10, 7, 5, 8, 11]
- Nominal weights:    [2, 3, 1, 4, 5]
- Weight deviations:  [1, 2, 1, 1, 3]
- Capacity: 15
- Budget of uncertainty (Γ): 2

Author: Pranav Gairola
"""

import pulp


def solve_robust_knapsack(profits, nominal_weights, deviations, capacity, Gamma):
    """
    Solves the robust knapsack problem with given parameters.

    :param profits: List of item profits
    :param nominal_weights: List of nominal weights of items
    :param deviations: List of weight deviations for items
    :param capacity: Capacity of the knapsack
    :param Gamma: Budget of uncertainty
    :return: Solution status, objective value, decision variables
    """
    n = len(profits)

    # Create a linear programming problem
    prob = pulp.LpProblem("Robust_Knapsack_Problem", pulp.LpMaximize)

    # Decision variables
    x = [pulp.LpVariable(f"x{i}", cat='Binary') for i in range(n)]
    gamma = pulp.LpVariable("gamma", lowBound=0)
    chi = [pulp.LpVariable(f"chi{i}", lowBound=0) for i in range(n)]

    # Objective function
    prob += pulp.lpSum(profits[i] * x[i] for i in range(n))

    # Constraints
    prob += pulp.lpSum(nominal_weights[i] * x[i] for i in range(n)) + Gamma * gamma + pulp.lpSum(
        chi[i] for i in range(n)) <= capacity

    for i in range(n):
        prob += gamma + chi[i] >= deviations[i] * x[i]

    # Solve the problem
    prob.solve()

    # Collect results
    status = pulp.LpStatus[prob.status]
    objective_value = pulp.value(prob.objective)
    decision_vars = {f"x{i}": pulp.value(x[i]) for i in range(n)}
    gamma_value = pulp.value(gamma)
    chi_values = {f"chi{i}": pulp.value(chi[i]) for i in range(n)}

    return status, objective_value, decision_vars, gamma_value, chi_values


def RKP():
    # Example problem data
    profits = [10, 7, 5, 8, 11]
    nominal_weights = [2, 3, 1, 4, 5]
    deviations = [1, 2, 1, 1, 3]
    capacity = 15
    Gamma = 2

    # Solve the problem
    status, objective_value, decision_vars, gamma_value, chi_values = solve_robust_knapsack(profits, nominal_weights,
                                                                                            deviations, capacity, Gamma)

    # Output the results
    print("Status:", status)
    print("Objective value:", objective_value)
    print("Decision variables:")
    for var, value in decision_vars.items():
        print(f"{var} = {value}")
    print("Gamma:", gamma_value)
    for var, value in chi_values.items():
        print(f"{var} = {value}")

# if __name__ == "__main__":
#     main()
RKP()
