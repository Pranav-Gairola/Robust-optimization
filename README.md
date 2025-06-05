# Classical and Robust Combinatorial Optimization Models

![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Issues](https://img.shields.io/github/issues/Pranav-Gairola/Robust-optimization)
![Stars](https://img.shields.io/github/stars/Pranav-Gairola/Robust-optimization?style=social)

This repository implements classical and robust versions of three well-known combinatorial optimization problems using Python and [PuLP](https://coin-or.github.io/pulp/):

- ✅ 0-1 Knapsack Problem (Deterministic and Robust)
- ✅ Set Covering Problem (Deterministic and Robust)
- ✅ p-Median Facility Location Problem (Deterministic and Robust)

These scripts are designed for educational, research, and prototyping purposes.

---

## 📚 Table of Contents

- [📁 Repository Structure](#-repository-structure)
- [📌 Problem Descriptions](#-problem-descriptions)
- [🛠️ Requirements](#️-requirements)
- [🚀 Running the Scripts](#-running-the-scripts)
- [📤 Sample Output](#-sample-output)
- [📚 References](#-references)
- [🙋‍♂️ Author](#-author)
- [📄 License](#-license)
- [🤝 Contributing](#-contributing)

---

## 📁 Repository Structure

.
├── knapsack.py             # 0-1 Knapsack (deterministic and robust)
├── set_covering.py         # Set Covering Problem (deterministic and robust)
├── p_median.py             # p-Median Problem (deterministic and robust)
├── README.md               # Documentation

---

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

---

## 🛠️ Requirements

- Python 3.7+
- PuLP

Install dependencies:

pip install pulp

---

🚀 Running the Scripts
Each script contains a main() function for demonstration.

Run them from the command line:

python knapsack.py
python set_covering.py
python p_median.py

## 📤 Sample Output

1. Example output for the knapsack problem:

=== Deterministic Knapsack ===
Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

Result - Optimal solution found

Objective value:                41.00000000
Enumerated nodes:               0
Total iterations:               0
Time (CPU seconds):             0.00
Time (Wallclock seconds):       0.00

Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.01   (Wallclock seconds):       0.00

Status: Optimal
Objective value: 41.0
Decision variables:
x0 = 1.0
x1 = 1.0
x2 = 1.0
x3 = 1.0
x4 = 1.0

=== Robust Knapsack (Budgeted Uncertainty set) ===
Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

Result - Optimal solution found

Objective value:                30.00000000
Enumerated nodes:               0
Total iterations:               6
Time (CPU seconds):             0.01
Time (Wallclock seconds):       0.01

Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.01   (Wallclock seconds):       0.01

Status: Optimal
Objective value: 30.0
Decision variables:
x0 = 1.0
x1 = 1.0
x2 = 1.0
x3 = 1.0
x4 = 0.0
Gamma value (dual): 0.0
chi0 = 1.0
chi1 = 2.0
chi2 = 1.0
chi3 = 1.0
chi4 = 0.0

2. Example output for the set covering problem:
   
--- Solving Deterministic Set Covering Problem ---
Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

Result - Optimal solution found

Objective value:                30.00000000
Enumerated nodes:               0
Total iterations:               0
Time (CPU seconds):             0.00
Time (Wallclock seconds):       0.01

Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.03   (Wallclock seconds):       0.02

Status: Optimal
Minimum Cost: 30.0
Selected Facilities:
 - Facility at site A
 - Facility at site E
 - Facility at site F

--- Solving Robust Set Covering Problem (Box Uncertainty set) ---
Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

Result - Optimal solution found

Objective value:                60.00000000
Enumerated nodes:               0
Total iterations:               0
Time (CPU seconds):             0.00
Time (Wallclock seconds):       0.00

Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.01   (Wallclock seconds):       0.01

Status: Optimal
Robust Minimum Cost: 60.0
Selected Facilities (Robust):
 - Facility at site A
 - Facility at site B
 - Facility at site D
 - Facility at site E
 - Facility at site F


3. Example output for the p-median problem:
   
--- Solving Deterministic p-Median ---
Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

Result - Optimal solution found

Objective value:                16.00000000
Enumerated nodes:               0
Total iterations:               0
Time (CPU seconds):             0.01
Time (Wallclock seconds):       0.01

Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.03   (Wallclock seconds):       0.03

Status: Optimal
Objective Value: 16.0
Open Facilities: ['B', 'E']
Assignments:
  Demand at A assigned to facility at B
  Demand at B assigned to facility at B
  Demand at C assigned to facility at E
  Demand at D assigned to facility at E
  Demand at E assigned to facility at E
  Demand at F assigned to facility at E

--- Solving Robust p-Median (Polyhedral Uncertainty set)---
Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

Result - Optimal solution found

Objective value:                18.00000000
Enumerated nodes:               0
Total iterations:               0
Time (CPU seconds):             0.01
Time (Wallclock seconds):       0.01

Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.03   (Wallclock seconds):       0.03

Status: Optimal
Objective Value: 18.0
Open Facilities: ['B', 'E']
Assignments:
  Demand at A assigned to facility at B
  Demand at B assigned to facility at B
  Demand at C assigned to facility at B
  Demand at D assigned to facility at E
  Demand at E assigned to facility at E
  Demand at F assigned to facility at E


📚 References
Bertsimas, D., & Sim, M. (2004). The Price of Robustness. Operations Research, 52(1), 35–53.
Optimization examples inspired by classical combinatorial problems in OR literature.

## 🙋‍♂️ Author
Pranav Gairola
PhD, Transportation Engineering |
Feel free to connect: https://www.linkedin.com/in/pranav-gairola-15a76ab3/

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.



