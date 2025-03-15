# zaimportuj bibliotekę ’networkx’ do rysowania grafów
# nazwij ją ’nx’
# dalej można z niej korzystać w kodzie pod nazwą ’nx’
import networkx as nx

# zaimportuj bibliotekę ’pyplot’ z pakietu ’matplotlib’
# nazwij ją ’plt’
# dalej można z niej korzystać w kodzie pod nazwą ’plt’
import matplotlib.pyplot as plt

# utwórz obiekt reprezentujący graf ’nx.Graph()’
# przypisz go do zmiennej ’G’
G = nx.Graph()

# wykorzystaj funkcję ’add_edge’ obiektu/grafu ’G’
# funkcja dodaje do grafu krawędź między dwoma wierzchołkami
# nazwy wierzchołków podane są w argumentach funkcji
G.add_edge('A', 'B')
G.add_edge('B', 'D')
G.add_edge('A', 'C')
G.add_edge('C', 'D')

# wybierz typ układu wierzchołków ’spring_layout’
# przypisz go do zmiennej ’pos’
pos = nx.spring_layout(G)  # dlaczego przy każdym uruchomieniu otrzymujemy inne rozmieszczenie?

# wyświetl wierzchołki
# wierzchołki są w pozycjach zadanych przez ’pos’
# wierzchołki mają rozmiar ’500’
nx.draw_networkx_nodes(G, pos, node_size=500)

# wyświetl etykiety wierzchołków
# etykiety są w pozycjach zadanych przez ’pos’
nx.draw_networkx_labels(G, pos)

# wyświetl krawędzie grafu
# wierzchołki są w pozycjach zadanych przez ’pos’
nx.draw_networkx_edges(G, pos)

# wyświetl graf
plt.show()
