from graph import Graph


def display_menu():
    """Affiche le menu principal."""
    print("\n" + "=" * 60)
    print("  ALGORITHME DE FLOYD-WARSHALL")
    print("  Recherche des chemins de valeurs minimales")
    print("=" * 60)
    print("  1. Charger et analyser un graphe")
    print("  0. Quitter")
    print("-" * 60)


def get_graph_filepath(graph_number):
    """Retourne le chemin du fichier pour un numéro de graphe donné."""
    return f"graph_test{graph_number}.txt"


def path_query_loop(L, P, nodes):
    """
    Boucle interactive pour interroger les chemins de valeurs minimales.
    L'utilisateur peut demander un chemin spécifique ou tous les afficher.
    """
    n = len(nodes)
    node_to_index = {node: idx for idx, node in enumerate(nodes)}

    while True:
        print("\n" + "-" * 40)
        print("  Options chemins :")
        print("    1. Afficher un chemin spécifique")
        print("    2. Afficher tous les chemins")
        print("    0. Retour au menu principal")
        print("-" * 40)

        choice = input("  Votre choix : ").strip()

        if choice == "0":
            break

        elif choice == "2":
            Graph.display_all_paths(L, P, nodes)

        elif choice == "1":
            print(f"  Sommets disponibles : {nodes}")

            try:
                start = int(input("  Sommet de départ : ").strip())
                end = int(input("  Sommet d'arrivée : ").strip())
            except ValueError:
                print("  Erreur : veuillez entrer des entiers.")
                continue

            if start not in node_to_index:
                print(f"  Erreur : le sommet {start} n'existe pas dans le graphe.")
                continue
            if end not in node_to_index:
                print(f"  Erreur : le sommet {end} n'existe pas dans le graphe.")
                continue

            if start == end:
                print(f"  Le sommet de départ et d'arrivée sont identiques ({start}).")
                continue

            start_idx = node_to_index[start]
            end_idx = node_to_index[end]
            Graph.display_path(L, P, nodes, start_idx, end_idx)

        else:
            print("  Choix invalide.")


def process_graph():
    """
    Traitement complet d'un graphe :
    chargement, affichage, Floyd-Warshall, détection circuit absorbant,
    affichage des chemins.
    """
    try:
        graph_number = int(input("  Numéro du graphe à analyser : ").strip())
    except ValueError:
        print("  Erreur : veuillez entrer un entier.")
        return

    filepath = get_graph_filepath(graph_number)

    g = Graph()
    if not g.load(filepath):
        return

    # Affichage sous forme de liste adjacence
    print(f"\n{'=' * 60}")
    print("  Liste d'adjacence du graphe")
    print(f"{'=' * 60}")
    print(g)

    # Affichage sous forme matricielle
    matrix, nodes, _ = g.adjacency_matrix()
    Graph.display_matrix(matrix, nodes, title="Matrice de valeurs du graphe")

    # Exécution de Floyd-Warshall (avec affichage des étapes intermédiaires)
    print(f"\n{'#' * 60}")
    print("  EXÉCUTION DE L'ALGORITHME DE FLOYD-WARSHALL")
    print(f"{'#' * 60}")

    L, P, nodes, has_negative_cycle = g.floyd_warshall(verbose=True)

    # Détection de circuit absorbant
    print(f"\n{'=' * 60}")
    print("  RÉSULTAT : DÉTECTION DE CIRCUIT ABSORBANT")
    print(f"{'=' * 60}")

    if has_negative_cycle:
        print("  ⚠  Le graphe contient au moins un circuit absorbant !")
        print("  Les distances calculées ne sont pas fiables.")
        # On identifie les sommets concernés
        for i, node in enumerate(nodes):
            if L[i][i] < 0:
                print(f"     → Circuit absorbant passant par le sommet {node} "
                      f"(L[{node}][{node}] = {L[i][i]})")
        return

    print("  ✓  Le graphe ne contient aucun circuit absorbant.")

    # Affichage des matrices finales
    Graph.display_matrix(L, nodes, title="L finale — Distances minimales")
    Graph.display_matrix_P(P, nodes, title="P finale — Prédécesseurs")

    # Affichage des chemins de valeurs minimales
    path_query_loop(L, P, nodes)


def main():
    """Boucle principale du programme."""
    print("\n" + "#" * 60)
    print("  PROJET SM601 — THÉORIE DES GRAPHES")
    print("  Algorithme de Floyd-Warshall")
    print("#" * 60)

    while True:
        display_menu()
        choice = input("  Votre choix : ").strip()

        if choice == "1":
            process_graph()
        elif choice == "0":
            print("\n  Au revoir !")
            break
        else:
            print("  Choix invalide. Veuillez entrer 1 ou 0.")


if __name__ == "__main__":
    main()