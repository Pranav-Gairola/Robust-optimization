# Classical and Robust Combinatorial Optimization Models

This repository implements classical and robust versions of three well-known combinatorial optimization problems using Python and [PuLP](https://coin-or.github.io/pulp/):

- ✅ 0-1 Knapsack Problem (Deterministic and Robust)
- ✅ Set Covering Problem (Deterministic and Robust)
- ✅ p-Median Facility Location Problem (Deterministic and Robust)

These scripts are designed for educational, research, and prototyping purposes.

---

## 📁 Repository Structure

```text
.
├── knapsack.py             # 0-1 Knapsack (deterministic and robust)
├── set_covering.py         # Set Covering Problem (deterministic and robust)
├── p_median.py             # p-Median Problem (deterministic and robust)
├── README.md               # Documentation

📌 Problem Descriptions
1. 0-1 Knapsack Problem
Goal: Select a subset of items to maximize total profit without exceeding a weight capacity.

Deterministic: Uses nominal weights.

Robust: Handles uncertainty in item weights using the Bertsimas-Sim budgeted uncertainty model.

🔢 Example:

Profits: [10, 7, 5, 8, 11]

Weights: [2, 3, 1, 4, 5]

Deviations: [1, 2, 1, 1, 3]

Capacity: 15, Budget Γ: 2

2. Set Covering Problem
Goal: Select a subset of facilities to cover all required demand nodes at minimum cost.

Deterministic: Each demand node must be covered by at least one facility.

Robust: Handles uncertainty in demand node coverage (e.g., disruptions) using dualization of budgeted uncertainty.

🧩 Example: Coverage matrix, costs, and demand data defined in-code.

3. p-Median Facility Location Problem
Goal: Choose p facility locations to minimize the total distance from demand points to the nearest open facility.

Deterministic: All data is fixed and known.

Robust: Demand or cost matrix can vary within an uncertainty budget, using robust dual constraints.

📍 Example: Solves a toy p-median instance with demand and cost matrix embedded.

