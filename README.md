# Algorithme de Floyd-Warshall

Projet SM601 - Théorie des graphes - EFREI Paris 2025/2026

## Description

Programme Python implémentant l'algorithme de Floyd-Warshall pour la recherche des chemins de valeurs minimales entre tous les couples de sommets d'un graphe orienté et valué.

## Utilisation

```
python main.py
```

Le menu permet de :
- Charger un graphe par numéro (ex: `1` → `graph_tests/graph_test1.txt`)
- Charger un graphe par chemin (ex: `graph_tests/graph_application.txt`)
- Visualiser la matrice de valeurs, les matrices L et P intermédiaires
- Détecter les circuits absorbants
- Afficher les chemins de valeurs minimales

## Structure du projet

```
main.py                  - Programme principal (boucle interactive)
graph.py                 - Classe Graph (chargement, Floyd-Warshall, affichage)
graph_tests/             - Fichiers de graphes de test
  graph_test1.txt        - Exemple du sujet (4 sommets)
  graph_test2.txt        - Graphe avec circuit absorbant
  graph_test3.txt        - 6 sommets, sommets non atteignables
  graph_test4.txt        - Graphe bien connecté (4 sommets)
  graph_test5.txt        - Graphe avec sommet puits
  graph_application.txt  - Exemple réel (réseau 10 villes)
traces_execution.txt     - Traces d'exécution sur tous les graphes
rapport_application.pdf  - Rapport partie 2 (exemple d'application)
```

## Format des fichiers de graphe

```
<nombre de sommets>
<nombre d'arcs>
<sommet_depart> <sommet_arrivee> <poids>
...
```

Les sommets sont numérotés de 0 à n-1. Les valeurs négatives et nulles sont admises.

## Équipe

- Julie Brouet
- Grégoire Boucheroy
- Louis Champigneule
- William Robert