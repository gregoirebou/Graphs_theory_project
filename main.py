from graph import Graph  # Assure-toi que ton fichier s'appelle bien graphe.py

# Graph creation
my_graph = Graph()


my_graph.add_edge("A", "B", 1)
my_graph.add_edge("A", "C", 2)
my_graph.add_edge("B", "D", 4)
my_graph.add_edge("C", "D", 1)

# Printing
print("--- My Graph ---")
print(my_graph)