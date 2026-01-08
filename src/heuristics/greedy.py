def nearest_neighbor(distance_matrix, start=0):
    """
    Euristica deterministica greedy per il TSP:
    Partendo dal nodo 'start', ogni volta sceglie il nodo più vicino.
    Restituisce:
    - tour (lista di nodi in ordine)
    - costo totale
    """
    n = len(distance_matrix)
    unvisited = set(range(n))
    unvisited.remove(start)

    tour = [start]
    total_cost = 0
    current = start

    while unvisited:
        # trova il nodo più vicino non visitato
        next_city = min(unvisited, key=lambda j: distance_matrix[current][j])
        total_cost += distance_matrix[current][next_city]
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    # ritorno al nodo di partenza
    total_cost += distance_matrix[current][start]
    tour.append(start)

    return tour, total_cost
