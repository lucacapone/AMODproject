import math
import random
from src.utils.tour_utils import tour_cost
from src.heuristics.two_opt import two_opt_swap


def simulated_annealing(distance_matrix, initial_tour,
                        T0=10000, alpha=0.9993, iterations=50000):
    """
    Simulated Annealing per TSP usando mosse 2-opt.

    Parametri:
    - T0: temperatura iniziale
    - alpha: fattore di raffreddamento (0.99 - 0.999)
    - iterations: numero totale di iterazioni

    Restituisce:
    - best_tour: migliore soluzione trovata
    - best_cost: costo della migliore soluzione
    """

    current_tour = initial_tour[:]
    current_cost = tour_cost(current_tour, distance_matrix)

    best_tour = current_tour[:]
    best_cost = current_cost

    T = T0  # temperatura iniziale
    n = len(current_tour)

    for step in range(iterations):

        # scegli random due indici per la mossa 2-opt
        i = random.randint(1, n - 3)
        k = random.randint(i + 1, n - 2)

        new_tour = two_opt_swap(current_tour, i, k)
        new_cost = tour_cost(new_tour, distance_matrix)

        delta = new_cost - current_cost

        # Se migliora, accetta
        if delta < 0:
            current_tour = new_tour
            current_cost = new_cost

            if current_cost < best_cost:
                best_tour = current_tour[:]
                best_cost = current_cost

        else:
            # Accettazione probabilistica
            prob = math.exp(-delta / T)
            if random.random() < prob:
                current_tour = new_tour
                current_cost = new_cost

        # Raffreddamento
        T *= alpha

        if T < 1e-8:
            break

    return best_tour, best_cost
