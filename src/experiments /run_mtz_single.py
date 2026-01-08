import os
from gurobipy import GRB

from src.utils.tsplib_reader import read_tsplib, distance_matrix
from src.solver.tsp_mtz import solve_tsp_mtz


def main():
    instance_name = "eil51.tsp"
    instance_path = os.path.join("instances", instance_name)

    print(f"Caricamento istanza: {instance_path}")

    coords, n = read_tsplib(instance_path)
    print(f"Città lette: {n}")

    dist = distance_matrix(coords)
    print("Matrice delle distanze creata.")

    # Risolvi TSP con MTZ
    tour, cost, runtime, status = solve_tsp_mtz(
        dist,
        time_limit=60,   # 60 secondi di limite (più che sufficiente per eil51)
        verbose=True     # True per vedere l'output di Gurobi in console
    )

    print("\n=== RISULTATO TSP MTZ (Gurobi) ===")
    print("Status Gurobi:", status)
    if status in [GRB.OPTIMAL, GRB.TIME_LIMIT]:
        print("Tour ottimo (o best found):", tour)
        print(f"Costo totale: {cost:.4f}")
        print(f"Tempo di esecuzione: {runtime:.2f} s")
    else:
        print("Nessuna soluzione valida trovata.")


if __name__ == "__main__":
    main()
