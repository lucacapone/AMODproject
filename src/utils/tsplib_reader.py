import math

def read_tsplib(filename):
    """
    Legge un file TSPLIB .tsp e restituisce:
    - lista di coordinate [(x1, y1), (x2, y2), ...]
    - numero di città
    """
    coords = []
    with open(filename, 'r') as f:
        lines = f.readlines()

    node_coord_section = False
    for line in lines:
        line = line.strip()

        if line.startswith("NODE_COORD_SECTION"):
            node_coord_section = True
            continue

        if line.startswith("EOF"):
            break

        if node_coord_section:
            parts = line.split()
            if len(parts) >= 3:
                _, x, y = parts
                coords.append((float(x), float(y)))

    return coords, len(coords)


def euclidean_distance(p1, p2):
    """Calcola la distanza euclidea tra due punti."""
    return math.dist(p1, p2)


def distance_matrix(coords):
    """Crea una matrice delle distanze NxN."""
    n = len(coords)
    dist = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            dist[i][j] = euclidean_distance(coords[i], coords[j])

    return dist
