class Graph:
    def __init__(self):
        # On utilise un dictionnaire pour stocker le graphe
        # Format : {sommet_depart: [(sommet_arrivee, poids), ...]}
        self.graph = {}

    def load(self, file):
        self.graph = {}
        with open(file, 'r') as f:
            lines = f.readlines()
            clean_lines = [line.strip() for line in lines if line.strip()]

            if not clean_lines:
                print("Le fichier est vide")
                return

            num_nodes = int(clean_lines[0])

            for i in range(num_nodes):
                self.add_vertex(i)

            num_edges = int(clean_lines[1])

            for i in range(2, len(clean_lines)):
                parts = clean_lines[i].split()

                # Vérification simple qu'on a bien 3 valeurs
                if len(parts) >= 3:
                    start = int(parts[0])
                    end = int(parts[1])
                    weight = int(parts[2])

                    self.add_edge(start, end, weight)
            print(f"Graphe chargé depuis '{file}' : {num_nodes} sommets, {num_edges} arcs déclarés.")




    def adjacency_matrix(self):
        nodes = sorted(self.graph.keys())
        n = len(nodes)

        matrix = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            matrix[i][i] = 0

        for u_index, u_label in enumerate(nodes):
            for v_label, weight in self.graph[u_label]:
                if v_label in nodes:
                    v_index = nodes.index(v_label)
                    matrix[u_index][v_index] = weight

        return matrix, nodes

    def add_vertex(self, vertex):
        # Ajoute un sommet au graphe s'il n'existe pas déjà.
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, start, end, weight=1):
        # Ajoute un arc orienté et valué.
        if start not in self.graph:
            self.add_vertex(start)
        if end not in self.graph:
            self.add_vertex(end)
        self.graph[start].append((end, weight))

    def get_successors(self, vertex):
        # Retourne la liste des successeurs
        if vertex not in self.graph:
            return []
        else:
            return [successor for successor, weight in self.graph[vertex]]

    def __str__(self):
        # Affichage standard.
        result = ""
        # On trie les clés pour un affichage propre
        for vertex in sorted(self.graph.keys()):
            successors = self.get_successors(vertex)
            result += f"{vertex} -> {successors}\n"
        return result
