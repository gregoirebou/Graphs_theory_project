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

    def __str__(self):
        result = ""
        for vertex, successors in self.graph.items():
            result += f"{vertex} -> {successors}\n"
        return result

