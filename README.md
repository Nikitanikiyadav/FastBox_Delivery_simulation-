# FastBox Delivery Simulation System

This is a Python script I built for a coding assessment. The idea is basically a mini delivery simulation for a fictional company called FastBox — you're given some warehouses, some delivery agents, and a bunch of packages, and the script figures out who delivers what, how far everyone travels, and who did the best job.

## Overview

Given:
- A list of **warehouses**, each with a fixed location
- A list of **delivery agents**, each with a starting location
- A list of **packages**, each linked to a warehouse and a delivery destination

The program:
1. Assigns every package to the delivery agent closest to its warehouse
2. Simulates each agent's route and calculates total distance travelled
3. Scores every agent on an efficiency metric
4. Outputs a full report as JSON, plus a CSV summary of the top performer

## Features

- **Flexible JSON parsing** — handles two different input formats found across the provided test data (warehouses/agents given as a list of objects *or* as a plain key-value dict) without needing separate code paths for each
- **Nearest-agent assignment** using Euclidean (straight-line) distance
- **Full delivery simulation** — computes agent → warehouse → destination distance per package, summed per agent
- **Efficiency scoring** to rank agents and determine a daily "best agent"
- **JSON report generation**, one clean report per input file
- **Bonus CSV export** of the top-performing agent for each run
- **Built-in sanity check** — verifies that every package in the input was delivered exactly once, with no drops or duplicates

## How it works
Input JSON --> load_data() --> assign_packages() --> simulate() --> add_efficiency() --> save_report()

|| Step | Function | What it does |
|-------|----------|----------|
| 1 | **load_data()** | Parses and normalizes warehouses, agents, and packages |
| 2 | **distance()** | Computes straight-line distance between two (x, y) points |
| 3 | **assign_packages()** | Assigns each package to the agent nearest to its warehouse |
| 4 | **simulate()** | Calculates total travel distance per agent |
| 5 | **add_efficiency()** | Scores agents and identifies the best performer |
| 6 | **save_report()** | Writes the final report to a JSON file |
| Bonus | **export_top_performer_csv()** | Writes the best agent's stats to a CSV file |

## Design decisions & assumptions

The original brief left a couple of details open to interpretation. Here's what I decided and why:

- **Distance per package** = distance(agent → warehouse) + distance(warehouse → destination). An agent has to travel to the warehouse to pick up a package before it can be delivered, so both legs are counted.
- **Efficiency formula** = **(packages delivered ÷ total distance) × 100** . This rewards agents who deliver more packages while covering less ground, rather than just rewarding whichever agent happened to get the most packages.

Both are documented directly in code comments next to where they're calculated.

## Project structure
FastBox_Delivery/
│
├── delivery_system.py
├── README.md
├── base_case.json
│
├── Python Assignment(Delivery System Test Cases)/
│   ├── test_case_1.json
│   ├── test_case_2.json
│   ├── ...
│   └── test_case_10.json
│
└── output/
    ├── report_base_case.json
    ├── report_base_case_top_performer.csv
    ├── report_test_case_1.json
    ├── report_test_case_1_top_performer.csv
    ├── ...
    ├── report_test_case_10.json
    └── report_test_case_10_top_performer.csv

## Running it

Requires Python 3.7+, no external dependencies (standard library only: **json**, **math**, **os**, **csv**).

```bash
python delivery_system.py
```

This runs the simulation against **base_case.json** and every file in the test cases folder, printing a result line for each:


## Testing

Validated against 11 total input files (1 base case + 10 provided test cases). Every run passed the delivered-vs-total-packages sanity check with no mismatches:

| Input file | Packages | Result |
|---|---|---|
| base_case.json | 5/5 | OK |
| test_case_1.json | 12/12 |  OK |
| test_case_2.json | 10/10 |  OK |
| test_case_3.json | 6/6 | OK |
| test_case_4.json | 12/12 |  OK |
| test_case_5.json | 10/10 |  OK |
| test_case_6.json | 9/9 |  OK |
| test_case_7.json | 10/10 |  OK |
| test_case_8.json | 11/11 |  OK |
| test_case_9.json | 8/8 |  OK |
| test_case_10.json | 11/11 |  OK |

## Sample output

```json
{
  "A1": { "packages_delivered": 2, "total_distance": 78.28, "efficiency": 2.55 },
  "A2": { "packages_delivered": 2, "total_distance": 72.24, "efficiency": 2.77 },
  "A3": { "packages_delivered": 1, "total_distance": 14.14, "efficiency": 7.07 },
  "best_agent": "A3"
}
```

## Things I'd add if I had more time

Things I'd add if I had more time
Random delivery delays, just to make it feel more like a real day
Some kind of visual/ASCII output showing each agent's actual route
Handling for an agent joining partway through the day
Actual unit tests instead of just the one sanity check

## Tech stack

- **Language:** Python 3
- **Libraries:** Standard library only — **json**, **math**, **os**, **csv**