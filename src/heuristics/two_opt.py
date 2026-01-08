from src.utils.tour_utils import tour_cost

def two_opt_swap(tour, i, k):
    """
    Applica una mossa 2-opt al tour:
    - mantiene i nodi [0:i]
    - inverte l'ordine dei nodi [i:k]
    - mantiene i nodi [k+1:]
    Restituisce un nuovo tour.
    """
    new_tour = tour[0:i] + tour[i:k + 1][::-1] + tour[k + 1:]
    return new_tour


def two_opt(distance_matrix, initial_tour):
    """
    Local search 2-opt:
    - parte da un tour iniziale
    - esplora tutte le mosse 2-opt
    - accetta la prima mossa che migliora
    - ripete finché non ci sono miglioramenti

    Restituisce:
    - best_tour: tour migliorato
    - best_cost: costo del tour migliorato
    """
    best_tour = initial_tour[:]
    best_cost = tour_cost(best_tour, distance_matrix)
    n = len(best_tour)

    improved = True
    while improved:
        improved = False
        # Non tocchiamo il primo e l'ultimo nodo (0 e n-1), per preservare il ciclo
        for i in range(1, n - 2):
            for k in range(i + 1, n - 1):
                new_tour = two_opt_swap(best_tour, i, k)
                new_cost = tour_cost(new_tour, distance_matrix)

                if new_cost < best_cost - 1e-9:
                    best_tour = new_tour
                    best_cost = new_cost
                    improved = True
                    # usciamo dai cicli per ricominciare dalla nuova soluzione
                    break
            if improved:
                break

    return best_tour, best_cost
