import time
import gurobipy as gp
from gurobipy import GRB


def solve_tsp_mtz(distance_matrix, time_limit=None, verbose=False):
    """
    Risolve il TSP simmetrico con formulazione MTZ usando Gurobi.

    Parametri:
    - distance_matrix: matrice NxN delle distanze (lista di liste)
    - time_limit: limite di tempo in secondi (opzionale)
    - verbose: se True mostra l'output di Gurobi

    Restituisce:
    - tour: lista di nodi [0, i2, i3, ..., 0]
    - cost: costo totale del tour
    - runtime: tempo di esecuzione in secondi
    - status: codice di stato di Gurobi (GRB.Status.OPTIMAL, GRB.Status.TIME_LIMIT, ecc.)
    """
    n = len(distance_matrix)
    if n == 0:
        return [], 0.0, 0.0, None

    # Modello
    m = gp.Model("tsp_mtz")

    # Output Gurobi
    if not verbose:
        m.Params.OutputFlag = 0
    if time_limit is not None:
        m.Params.TimeLimit = time_limit

    # Variabili x[i,j] binarie: 1 se si va da i a j
    x = m.addVars(n, n, vtype=GRB.BINARY, name="x")

    # Variabili u[i] per vincoli MTZ (ordini di visita)
    # u[0] può essere fissata implicitamente a 0 dai vincoli, usiamo [0, n-1]
    u = m.addVars(n, vtype=GRB.CONTINUOUS, lb=0.0, ub=n - 1, name="u")

    # Niente auto-anelli
    for i in range(n):
        m.addConstr(x[i, i] == 0, name=f"no_loop_{i}")

    # Vincoli di grado: 1 arco uscente e 1 entrante per ogni nodo
    for i in range(n):
        m.addConstr(gp.quicksum(x[i, j] for j in range(n)) == 1, name=f"out_{i}")
        m.addConstr(gp.quicksum(x[j, i] for j in range(n)) == 1, name=f"in_{i}")

    # Vincoli MTZ per evitare sottocicli
    # solo per nodi 1..n-1 (0 è il deposito di riferimento)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                m.addConstr(
                    u[i] - u[j] + n * x[i, j] <= n - 1,
                    name=f"mtz_{i}_{j}"
                )

    # Funzione obiettivo: minimizzare costo totale del tour
    m.setObjective(
        gp.quicksum(
            distance_matrix[i][j] * x[i, j]
            for i in range(n)
            for j in range(n)
        ),
        GRB.MINIMIZE
    )

    # Risoluzione
    start_time = time.time()
    m.optimize()
    runtime = time.time() - start_time

    status = m.Status

    if status not in [GRB.OPTIMAL, GRB.TIME_LIMIT]:
        # Nessuna soluzione valida
        return None, None, runtime, status

    # Ricostruzione del tour dalla soluzione di x
    successor = {}
    for i in range(n):
        for j in range(n):
            if x[i, j].X > 0.5:
                successor[i] = j
                break

    # Seguiamo il tour partendo da 0
    tour = [0]
    current = 0
    while True:
        nxt = successor[current]
        tour.append(nxt)
        current = nxt
        if current == 0:
            break

    cost = m.ObjVal

    return tour, cost, runtime, status
