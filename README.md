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
- Charger le graphe de l'application → numero 999
- Visualiser la matrice de valeurs, les matrices L et P intermédiaires
- Détecter les circuits absorbants
- Afficher les chemins de valeurs minimales

## Structure du projet

```
main.py                  - Programme principal (boucle interactive)
graph.py                 - Classe Graph (chargement, Floyd-Warshall, affichage)
graph_tests/             - Fichiers de graphes de test
  graph_testX.txt        - Graphes de test donnés par EFREI
  graph_test999.txt      - Exemple réel (réseau 10 villes)
traces_execution.txt     - Traces d'exécution sur tous les graphes
rapport_application.pdf  - Rapport (exemple d'application)
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
- Geremy Ruis