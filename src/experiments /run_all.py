import os
import csv
import json
import time

from src.utils.tsplib_reader import read_tsplib, distance_matrix
from src.heuristics.greedy import nearest_neighbor
from src.heuristics.two_opt import two_opt
from src.heuristics.simulated_annealing import simulated_annealing
from src.solver.tsp_mtz import solve_tsp_mtz


def save_tour_json(instance_name, method_name, tour, cost, folder="results/tours"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{instance_name}_{method_name}.json"
    path = os.path.join(folder, filename)

    data = {
        "instance": instance_name,
        "method": method_name,
        "tour": tour,
        "cost": cost
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def run_experiments(instances_folder="instances", output_file="results/output.csv"):

    files = [f for f in os.listdir(instances_folder) if f.endswith(".tsp")]

    print("== AVVIO ESPERIMENTI SU TUTTE LE ISTANZE ==\n")

    os.makedirs("results", exist_ok=True)

    with open(output_file, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Nuova intestazione completa
        writer.writerow([
            "instance",
            "greedy_cost",
            "two_opt_cost",
            "sa_cost",
            "mtz_cost",
            "t_greedy",
            "t_two_opt",
            "t_sa",
            "mtz_time",
            "gap_greedy",
            "gap_two_opt",
            "gap_sa"
        ])

        for filename in files:
            instance_path = os.path.join(instances_folder, filename)
            instance_name = filename.replace(".tsp", "")

            print(f"--- ISTANZA: {instance_name} ---")

            coords, n = read_tsplib(instance_path)
            dist = distance_matrix(coords)


            # -----------------------
            #  EURISTICHE (con tempi)
            # -----------------------

            t0 = time.time()
            greedy_tour, greedy_cost = nearest_neighbor(dist)
            t_greedy = time.time() - t0

            t0 = time.time()
            improved_tour, improved_cost = two_opt(dist, greedy_tour)
            t_two_opt = time.time() - t0

            t0 = time.time()
            sa_tour, sa_cost = simulated_annealing(dist, improved_tour)
            t_sa = time.time() - t0

            print(f"Greedy         : {greedy_cost:.2f}  (time {t_greedy:.4f}s)")
            print(f"2-opt          : {improved_cost:.2f}  (time {t_two_opt:.4f}s)")
            print(f"SA             : {sa_cost:.2f}  (time {t_sa:.4f}s)")

            # -----------------------
            #  MTZ (MODELLO ESATTO)
            # -----------------------
            print(" >> Risoluzione MTZ con Gurobi...")

            mtz_tour, mtz_cost, mtz_runtime, mtz_status = solve_tsp_mtz(
                dist, time_limit=300, verbose=False
            )

            print(f"MTZ optimal    : {mtz_cost:.2f} (time {mtz_runtime:.2f}s)\n")

            # -----------------------
            # GAP rispetto al modello esatto
            # -----------------------
            gap_greedy = (greedy_cost - mtz_cost) / mtz_cost * 100
            gap_twoopt = (improved_cost - mtz_cost) / mtz_cost * 100
            gap_sa     = (sa_cost - mtz_cost) / mtz_cost * 100

            # -----------------------
            # Scrivi CSV
            # -----------------------
            writer.writerow([
                instance_name,
                round(greedy_cost, 4),
                round(improved_cost, 4),
                round(sa_cost, 4),
                round(mtz_cost, 4),
                round(t_greedy, 6),
                round(t_two_opt, 6),
                round(t_sa, 6),
                round(mtz_runtime, 4),
                round(gap_greedy, 4),
                round(gap_twoopt, 4),
                round(gap_sa, 4)
            ])

            # -----------------------
            # Salvataggio tour JSON
            # -----------------------
            save_tour_json(instance_name, "greedy", greedy_tour, greedy_cost)
            save_tour_json(instance_name, "two_opt", improved_tour, improved_cost)
            save_tour_json(instance_name, "sa", sa_tour, sa_cost)
            save_tour_json(instance_name, "mtz", mtz_tour, mtz_cost)

    print("\n== ESPERIMENTI COMPLETATI ==")
    print(f"Risultati salvati in: {output_file}")
    print("Tour salvati in: results/tours/")


if __name__ == "__main__":
    run_experiments()
