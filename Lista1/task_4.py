import networkx as nx
import matplotlib.pyplot as plt

# do operacji pierwiastkowania
import numpy as np

G = nx.Graph()  # czy potrzebne? NIE, bo nie korzystamy w ogóle z tego grafu, tylko z małego g (niżej)

# nazwy wierzchołków
VV = [1, 2, 3, 4, 5]

# lista krawędzi
WW = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 3), (3, 5)]

# słownik, pozycje wierzchołków
Vx = {1: -5, 2: 1, 3: 2, 4: 3, 5: 4}
Vy = {1: 0, 2: 1, 3: 0, 4: -1, 5: 0}

g = nx.Graph()  # o z tego

# pusty słownik
gpos = {}

# wypełnienie słownika wierzchołkami
# pętla for przechodzi przez wszystkie elementy ’VV’
for v in VV:
    g.add_node(v)
    gpos[v] = [Vx[v], Vy[v]]

# zagnieżdżone pętle for
for v1 in VV:
    for v2 in VV:
        # sprawdzenie czy krawędź istnieje w ’WW’
        if (v1, v2) in WW:
            # jeśli istnieje, to ustaw etykietę na odległość euklidesową
            # funkcja ’str’ zwraca ciąg znaków
            # funkcja ’np.sqrt’ zwraca pierwiastek
            # symbol ’**’ oznacza potęgowanie

            label = str(np.sqrt((Vx[v1] - Vx[v2]) ** 2 + (Vy[v1] - Vy[v2]) ** 2))
            # label = str(round(np.sqrt((Vx[v1] - Vx[v2]) ** 2 + (Vy[v1] - Vy[v2]) ** 2), ndigits=2)) <- zaokr

            # dodaj wagi do krawędzi
            g.add_weighted_edges_from([(v1, v2, label)])

# wyświetl żółte wierzchołki z etykietami w ustalonych wcześniej pozycjach
nx.draw(g, gpos, with_labels=True, node_color='yellow')
# nx.draw(g, gpos, with_labels=True, node_color='yellow', node_size=2000) <- większy rozmiar wierzchołków

# pobierz i wyświetl etykiety
labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, gpos, edge_labels=labels)

# wyświetl graf
plt.show()
