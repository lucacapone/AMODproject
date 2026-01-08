from src.utils.tsplib_reader import read_tsplib, distance_matrix
from src.heuristics.greedy import nearest_neighbor
from src.heuristics.two_opt import two_opt
from src.utils.tour_utils import tour_cost
import os

def main():
    # scegli un file nella cartella instances
    instance_path = os.path.join("instances", "eil51.tsp")

    print(f"Caricamento istanza: {instance_path}")

    coords, n = read_tsplib(instance_path)
    print(f"Città lette: {n}")

    dist = distance_matrix(coords)
    print("Matrice delle distanze creata.")

    # euristica greedy (Nearest Neighbor)
    greedy_tour, greedy_cost = nearest_neighbor(dist, start=0)

    print("\n== RISULTATO GREEDY ==")
    print("Tour greedy:", greedy_tour)
    print(f"Costo totale greedy: {greedy_cost:.2f}")

    # Miglioriamo la soluzione greedy con 2-opt
    improved_tour, improved_cost = two_opt(dist, greedy_tour)

    print("\n== RISULTATO GREEDY + 2-OPT ==")
    print("Tour migliorato:", improved_tour)
    print(f"Costo totale migliorato: {improved_cost:.2f}")

    # confronto
    improvement = greedy_cost - improved_cost
    print(f"\nMiglioramento rispetto a greedy: {improvement:.2f}")

if __name__ == "__main__":
    main()
