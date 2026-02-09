class Graph:
    def __init__(self):
        self.graph = {}

        def add_vertex(self, vertex):
            if vertex not in self.graph:
                self.graph[vertex] = []

        def add_edge(self, start, end, weight=1):
            if start not in self.graph:
                self.add_vertex(start)
                self.graph[start].append(end)
            else:
                if end not in self.graph[start]:
                    self.graph[start].append(end)

