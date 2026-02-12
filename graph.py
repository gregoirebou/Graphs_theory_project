import copy


class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, start, end, weight=1):
        if start not in self.graph:
            self.add_vertex(start)
        if end not in self.graph:
            self.add_vertex(end)
        self.graph[start].append((end, weight))

    def get_successors(self, vertex):
        if vertex not in self.graph:
            return []
        else:
            return [successor for successor, weight in self.graph[vertex]]

    def get_predecessors(self, vertex):
        predecessors = []
        if vertex not in self.graph:
            return []
        else:
            for predecessor in self.graph:
                if vertex in self.get_successors(predecessor):
                    predecessors.append(predecessor)
        return predecessors

    def clone(self):
        g = Graph()
        g.graph = copy.deepcopy(self.graph)
        return g

    def contains_cycle(self):
        g = self.clone()
        while g.graph:
            deleted = False
            for vertex in g.graph:
                if not g.get_predecessors(vertex):
                    deleted = True
                    del g.graph[vertex]
                    break
            if not deleted:
                return True
        return False

    def compute_ranks(self):
        g = self.clone()
        rank = {}
        k = 0
        while g.graph:
            vertices = []
            for vertex in g.graph:
                if not g.get_predecessors(vertex):
                    vertices.append(vertex)
            if not vertices:
                raise ValueError("Circuit détecté")
            for vertex in vertices:
                rank[vertex] = k
                del g.graph[vertex]
            k = k + 1
        return rank

    # def compute_earliest_start(self):
    #     g = self.clone()
    #     rank = self.compute_ranks()

    def get_weight_path(self, start, end):
        if (start not in self.graph) or (end not in self.graph):
            raise ValueError(f"Le(s) sommet(s) {start} et/ou {end} ne sont pas dans le graphe")
        neighbors = self.graph[start]
        for (vertex, weight) in neighbors:
            if vertex == end:
                return weight
        return float("inf")

    def dijkstra(self, start):
        if start not in self.graph:
            raise ValueError(f"Le sommet {start} n'est pas dans le graphe")
        distances = {node: float("inf") for node in self.graph}
        distances[start] = 0
        predecessors = {node: None for node in self.graph}
        unvisited = list(self.graph.keys())

        while unvisited:
            current_node = None
            min_dist = float("inf")

            for node in unvisited:
                if distances[node] < min_dist:
                    min_dist = distances[node]
                    current_node = node
            if current_node is None:
                break

            unvisited.remove(current_node)

            for neighbor, weight in self.graph[current_node]:
                new_distance = distances[current_node] + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node
        return distances, predecessors

    def __str__(self):
        result = ""
        for vertex, successors in self.graph.items():
            result += f"{vertex} -> {self.get_successors(vertex)}\n"
        return result
