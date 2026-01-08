def tour_cost(tour, distance_matrix):
    """
    Calcola il costo totale di un tour dato e una matrice delle distanze.
    Il tour può essere:
    - chiuso (primo nodo uguale all'ultimo)
    - aperto (in tal caso chiudiamo il ciclo aggiungendo l'arco finale)
    """
    if len(tour) < 2:
        return 0.0

    cost = 0.0
    for i in range(len(tour) - 1):
        cost += distance_matrix[tour[i]][tour[i + 1]]

    # se il tour non è chiuso, chiudiamolo
    if tour[0] != tour[-1]:
        cost += distance_matrix[tour[-1]][tour[0]]

    return cost
