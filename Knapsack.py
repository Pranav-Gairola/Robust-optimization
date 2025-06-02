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

Author: Your Name
"""

from pulp import LpProblem, LpVariable, LpMaximize, LpBinary, LpContinuous, lpSum, value

# ------------------------------
# Problem Data
# ------------------------------
values = [10, 7, 5, 8, 11]         # Profits (v_i)
weights = [2, 3, 1, 4, 5]          # Nominal weights (w_i)
deviations = [1, 2, 1, 1, 3]       # Weight deviations (δ_i)
capacity = 15                     # Knapsack capacity (W)
Gamma = 2                         # Uncertainty budget (Γ)
n = len(values)                   # Number of items

# ------------------------------
# Create Optimization Problem
# ------------------------------
model = LpProblem("Robust_Knapsack", LpMaximize)

# ------------------------------
# Decision Variables
# ------------------------------
x = [LpVariable(f"x_{i}", cat=LpBinary) for i in range(n)]            # Item selection variables
chi = [LpVariable(f"chi_{i}", lowBound=0, cat=LpContinuous) for i in range(n)]  # Dual variables
gamma = LpVariable("gamma", lowBound=0, cat=LpContinuous)             # Uncertainty dual variable

# ------------------------------
# Objective Function
# ------------------------------
model += lpSum(values[i] * x[i] for i in range(n)), "Total_Profit"

# ------------------------------
# Robust Capacity Constraint (RC)
#   ∑ w_i x_i + Γγ + ∑ χ_i ≤ W
#   s.t. γ + χ_i ≥ δ_i x_i
# ------------------------------
model += (
    lpSum(weights[i] * x[i] for i in range(n)) +
    Gamma * gamma +
    lpSum(chi[i] for i in range(n))
    <= capacity,
    "Robust_Capacity"
)

for i in range(n):
    model += gamma + chi[i] >= deviations[i] * x[i], f"Dual_Constraint_{i}"

# ------------------------------
# Solve the Problem
# ------------------------------
model.solve()

# ------------------------------
# Display Results
# ------------------------------
print("\nRobust Knapsack Problem (RKP) Results")
print("======================================")
print(f"Status         : {model.status}, {model.solver.__class__.__name__}")
print(f"Total Profit   : {value(model.objective)}")
print(f"Selected Items :")

for i in range(n):
    if x[i].varValue == 1:
        print(f"  Item {i + 1}: Value = {values[i]}, Weight = {weights[i]}, Deviation = {deviations[i]}")

print("\nRobust Terms:")
print(f"  Gamma (γ)  : {gamma.varValue:.4f}")
for i in range(n):
    print(f"  χ_{i + 1}      : {chi[i].varValue:.4f}")

