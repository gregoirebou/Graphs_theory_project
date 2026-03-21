class Graph:
    """
    Classe représentant un graphe orienté et valué.
    Format : {sommet: [(successeur, poids), ...]}
    """

    def __init__(self):
        self.graph = {}
        self.num_vertices = 0
        self.num_edges = 0

    # CHARGEMENT DEPUIS UN FICHIER
    def load(self, file):
        """
        Charge un graphe depuis un fichier texte.
        Format attendu :
            Ligne 1 : nombre de sommets
            Ligne 2 : nombre d'arcs
            Lignes suivantes : sommet_depart sommet_arrivee poids
        """
        self.graph = {}
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Erreur : le fichier '{file}' n'existe pas.")
            return False

        clean_lines = [line.strip() for line in lines if line.strip()]

        if not clean_lines:
            print("Erreur : le fichier est vide.")
            return False

        try:
            self.num_vertices = int(clean_lines[0])
            self.num_edges = int(clean_lines[1])
        except (ValueError, IndexError):
            print("Erreur : format de fichier invalide (en-tête).")
            return False

        # Création de tous les sommets (numérotés de 0 à n-1)
        for i in range(self.num_vertices):
            self.add_vertex(i)

        # Lecture des arcs
        arcs_lus = 0
        for i in range(2, len(clean_lines)):
            parts = clean_lines[i].split()
            if len(parts) < 3:
                print(f"Attention : ligne {i + 1} ignorée (format incorrect).")
                continue
            try:
                start = int(parts[0])
                end = int(parts[1])
                weight = int(parts[2])
            except ValueError:
                print(f"Attention : ligne {i + 1} ignorée (valeurs non entières).")
                continue

            self.add_edge(start, end, weight)
            arcs_lus += 1

        if arcs_lus != self.num_edges:
            print(f"Attention : {self.num_edges} arcs déclarés mais {arcs_lus} arcs lus.")

        print(f"Graphe chargé depuis '{file}' : {self.num_vertices} sommets, {arcs_lus} arcs.")
        return True

    # STRUCTURE DU GRAPHE
    def add_vertex(self, vertex):
        """Ajoute un sommet s'il n'existe pas déjà."""
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, start, end, weight):
        """
        Ajoute un arc orienté et valué.
        Si un arc (start -> end) existe déjà, il est remplacé.
        """
        if start not in self.graph:
            self.add_vertex(start)
        if end not in self.graph:
            self.add_vertex(end)

        # Vérifier si l'arc existe déjà (au plus un arc de x vers y)
        for idx, (dest, _) in enumerate(self.graph[start]):
            if dest == end:
                self.graph[start][idx] = (end, weight)
                return

        self.graph[start].append((end, weight))

    def get_sorted_vertices(self):
        """Retourne la liste triée des sommets."""
        return sorted(self.graph.keys())

    # MATRICE D'ADJACENCE
    def adjacency_matrix(self):
        """
        Construit la matrice de valeurs (matrice d'adjacence pondérée).
        Retourne (matrix, nodes, node_to_index).
        """
        nodes = self.get_sorted_vertices()
        n = len(nodes)
        node_to_index = {node: idx for idx, node in enumerate(nodes)}

        INF = float('inf')
        matrix = [[INF] * n for _ in range(n)]

        # Diagonale à 0
        for i in range(n):
            matrix[i][i] = 0

        # Remplissage avec les poids des arcs
        for u in nodes:
            u_idx = node_to_index[u]
            for v, weight in self.graph[u]:
                v_idx = node_to_index[v]
                matrix[u_idx][v_idx] = weight

        return matrix, nodes, node_to_index

    # AFFICHAGE DES MATRICES
    @staticmethod
    def display_matrix(matrix, nodes, title="", symbol_inf="inf"):
        """
        Affiche une matrice avec un alignement propre.
        Les lignes et colonnes sont identifiées par les noms des sommets.
        """
        n = len(nodes)

        if title:
            print(f"\n{'=' * 60}")
            print(f"  {title}")
            print(f"{'=' * 60}")

        # Déterminer la largeur maximale des cellules
        col_width = max(len(str(symbol_inf)), len(str(max(nodes)))) + 1
        for row in matrix:
            for val in row:
                if val == float('inf'):
                    col_width = max(col_width, len(symbol_inf) + 1)
                elif val == float('-inf'):
                    col_width = max(col_width, len("-" + symbol_inf) + 1)
                else:
                    col_width = max(col_width, len(str(val)) + 1)

        col_width = max(col_width, 5)  # minimum 5 pour la lisibilité

        # En-tête : noms des colonnes
        header = " " * (col_width + 1) + "|"
        for node in nodes:
            header += str(node).rjust(col_width)
        print(header)

        # Séparateur
        separator = "-" * (col_width + 1) + "+" + "-" * (col_width * n)
        print(separator)

        # Lignes de la matrice
        for i, node in enumerate(nodes):
            row_str = str(node).rjust(col_width) + " |"
            for j in range(n):
                val = matrix[i][j]
                if val == float('inf'):
                    cell = symbol_inf
                elif val == float('-inf'):
                    cell = "-" + symbol_inf
                else:
                    cell = str(val)
                row_str += cell.rjust(col_width)
            print(row_str)

        print()

    # FLOYD-WARSHALL
    def floyd_warshall(self, verbose=True):
        """
        Exécute l'algorithme de Floyd-Warshall.

        Retourne :
            L   : matrice des distances minimales
            P   : matrice des prédécesseurs
            nodes : liste ordonnée des sommets
            has_negative_cycle : booléen
        """
        matrix, nodes, node_to_index = self.adjacency_matrix()
        n = len(nodes)
        INF = float('inf')

        # Initialisation de L (distances) et P (prédécesseurs)
        L = [row[:] for row in matrix]  # copie profonde
        P = [[None] * n for _ in range(n)]

        for i in range(n):
            for j in range(n):
                P[i][j] = i

        if verbose:
            self.display_matrix(L, nodes, title="L(0) - Matrice initiale des distances")
            self.display_matrix_P(P, nodes, title="P(0) - Matrice initiale des prédécesseurs")

        # Boucle principale : k est le sommet intermédiaire
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if L[i][k] != INF and L[k][j] != INF:
                        new_dist = L[i][k] + L[k][j]
                        if new_dist < L[i][j]:
                            L[i][j] = new_dist
                            P[i][j] = P[k][j]

            if verbose:
                self.display_matrix(L, nodes,
                                    title=f"L({k + 1}) - Après passage par le sommet {nodes[k]}")
                self.display_matrix_P(P, nodes,
                                      title=f"P({k + 1}) - Après passage par le sommet {nodes[k]}")

        # Détection de circuit absorbant : diagonale de L
        has_negative_cycle = False
        for i in range(n):
            if L[i][i] < 0:
                has_negative_cycle = True
                break

        return L, P, nodes, has_negative_cycle

    @staticmethod
    def display_matrix_P(P, nodes, title=""):
        """
        Affiche la matrice des prédécesseurs P.
        Les valeurs None sont affichées comme '-'.
        """
        n = len(nodes)

        if title:
            print(f"\n{'=' * 60}")
            print(f"  {title}")
            print(f"{'=' * 60}")

        col_width = 5

        # En-tête
        header = " " * (col_width + 1) + "|"
        for node in nodes:
            header += str(node).rjust(col_width)
        print(header)

        separator = "-" * (col_width + 1) + "+" + "-" * (col_width * n)
        print(separator)

        for i, node in enumerate(nodes):
            row_str = str(node).rjust(col_width) + " |"
            for j in range(n):
                val = P[i][j]
                if val is None:
                    cell = "-"
                else:
                    cell = str(nodes[val]) if isinstance(val, int) and val < len(nodes) else str(val)
                row_str += cell.rjust(col_width)
            print(row_str)

        print()

    # RECONSTRUCTION DES CHEMINS
    @staticmethod
    def reconstruct_path(P, nodes, start_idx, end_idx):
        """
        Reconstruit le chemin de start_idx à end_idx en utilisant la matrice P.
        Retourne la liste des indices des sommets du chemin, ou None si pas de chemin.
        """
        if P[start_idx][end_idx] is None:
            return None

        path = [end_idx]
        current = end_idx
        visited = set()

        while current != start_idx:
            pred = P[start_idx][current]
            if pred is None:
                return None
            if pred in visited:
                # Boucle détectée dans la reconstruction
                return None
            visited.add(current)
            path.append(pred)
            current = pred

        path.reverse()
        return path

    @staticmethod
    def display_path(L, P, nodes, start_idx, end_idx):
        """Affiche le chemin de valeur minimale entre deux sommets."""
        INF = float('inf')

        dist = L[start_idx][end_idx]

        if dist == INF:
            print(f"  Pas de chemin de {nodes[start_idx]} vers {nodes[end_idx]}.")
            return

        path_indices = Graph.reconstruct_path(P, nodes, start_idx, end_idx)

        if path_indices is None:
            print(f"  Impossible de reconstruire le chemin de {nodes[start_idx]} vers {nodes[end_idx]}.")
            return

        path_labels = [str(nodes[idx]) for idx in path_indices]
        print(f"  Chemin de {nodes[start_idx]} vers {nodes[end_idx]} : "
              f"{' -> '.join(path_labels)}  (valeur = {dist})")

    @staticmethod
    def display_all_paths(L, P, nodes):
        """Affiche tous les chemins de valeurs minimales."""
        n = len(nodes)
        INF = float('inf')

        print(f"\n{'=' * 60}")
        print("  Tous les chemins de valeurs minimales")
        print(f"{'=' * 60}")

        for i in range(n):
            for j in range(n):
                if i != j:
                    Graph.display_path(L, P, nodes, i, j)

    # AFFICHAGE DU GRAPHE                           #
    def __str__(self):
        """Affichage sous forme de liste d'adjacence avec poids."""
        result = ""
        for vertex in self.get_sorted_vertices():
            successors = self.graph[vertex]
            if successors:
                arcs = ", ".join(f"{dest}(val={w})" for dest, w in successors)
                result += f"  {vertex} -> {arcs}\n"
            else:
                result += f"  {vertex} -> (aucun successeur)\n"
        return result