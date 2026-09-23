import json
import math
import os
import csv

# ---------- STEP 1: Load and normalize JSON ----------
def load_data(filepath):
    """Reads the JSON file and converts it into a consistent internal format,
    regardless of whether warehouses/agents are lists of objects or dicts."""
    with open(filepath, "r") as f:
        raw = json.load(f)

    # Normalize warehouses into {id: (x, y)}
    if isinstance(raw["warehouses"], dict):
        warehouses = {k: tuple(v) for k, v in raw["warehouses"].items()}
    else:
        warehouses = {w["id"]: tuple(w["location"]) for w in raw["warehouses"]}

    # Normalize agents into {id: (x, y)}
    if isinstance(raw["agents"], dict):
        agents = {k: tuple(v) for k, v in raw["agents"].items()}
    else:
        agents = {a["id"]: tuple(a["location"]) for a in raw["agents"]}

    # Normalize packages, handling both "warehouse" and "warehouse_id" keys
    packages = []
    for p in raw["packages"]:
        wid = p.get("warehouse") or p.get("warehouse_id")
        packages.append({
            "id": p["id"],
            "warehouse": wid,
            "destination": tuple(p["destination"])
        })

    return warehouses, agents, packages


# ---------- STEP 2: Euclidean distance ----------
def distance(p1, p2):
    """Straight-line distance between two (x, y) points."""
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# ---------- STEP 3: Assign each package to nearest agent ----------
def assign_packages(warehouses, agents, packages):
    """For each package, find the agent closest to that package's warehouse."""
    assignments = {aid: [] for aid in agents}
    for pkg in packages:
        wh_loc = warehouses[pkg["warehouse"]]
        nearest_agent = min(agents, key=lambda aid: distance(agents[aid], wh_loc))
        assignments[nearest_agent].append(pkg)
    return assignments


# ---------- STEP 4: Simulate delivery, compute distance ----------
def simulate(warehouses, agents, assignments):
    """For each agent: travel from agent -> warehouse -> destination,
    for every package assigned to them. Sum total distance traveled."""
    results = {}
    for aid, pkgs in assignments.items():
        total_dist = 0
        for pkg in pkgs:
            wh_loc = warehouses[pkg["warehouse"]]
            total_dist += distance(agents[aid], wh_loc)          # agent -> warehouse
            total_dist += distance(wh_loc, pkg["destination"])   # warehouse -> destination
        results[aid] = {
            "packages_delivered": len(pkgs),
            "total_distance": round(total_dist, 2)
        }
    return results


# ---------- STEP 5: Efficiency + best agent ----------
def add_efficiency(results):
    """Efficiency = packages delivered per unit distance, scaled to a readable number.
    Higher efficiency = more packages delivered per distance traveled."""
    for aid, data in results.items():
        if data["total_distance"] > 0:
            eff = (data["packages_delivered"] / data["total_distance"]) * 100
        else:
            eff = 0
        data["efficiency"] = round(eff, 2)

    best_agent = max(results, key=lambda aid: results[aid]["efficiency"])
    results["best_agent"] = best_agent
    return results


# ---------- STEP 6: Save report ----------
def save_report(results, out_path="report.json"):
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)


# ---------- BONUS: export top performer to CSV ----------
def export_top_performer_csv(results, out_path="top_performer.csv"):
    best = results["best_agent"]
    data = results[best]
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["agent_id", "packages_delivered", "total_distance", "efficiency"])
        writer.writerow([best, data["packages_delivered"], data["total_distance"], data["efficiency"]])


# ---------- Main pipeline ----------
def main(filepath, out_path="report.json"):
    warehouses, agents, packages = load_data(filepath)
    assignments = assign_packages(warehouses, agents, packages)
    results = simulate(warehouses, agents, assignments)
    results = add_efficiency(results)
    save_report(results, out_path)
    export_top_performer_csv(results, out_path.replace(".json", "_top_performer.csv"))

    # Sanity check: every package must be accounted for
    delivered = sum(v["packages_delivered"] for k, v in results.items() if k != "best_agent")
    status = "OK" if delivered == len(packages) else "MISMATCH!"
    print(f"{filepath}: delivered {delivered}/{len(packages)} packages [{status}], best agent: {results['best_agent']}")


if __name__ == "__main__":
    # Run on the base case
    main("base_case.json", "report_base_case.json")

    # Run on every test case file
    test_folder = "Python Assignment(Delivery System Test Cases)"
    if os.path.isdir(test_folder):
        for fname in sorted(os.listdir(test_folder)):
            path = os.path.join(test_folder, fname)
            out_name = f"report_{fname}"
            main(path, out_name)