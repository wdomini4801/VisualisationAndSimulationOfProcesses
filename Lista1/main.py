# zaimportuj bibliotekę ’pyplot’ z pakietu ’matplotlib’
# nazwij ją ’plt’
# dalej można z niej korzystać w kodzie pod nazwą ’plt’
import matplotlib.pyplot as plt

# utwórz wykres
# funkcja ’plt.subplots’ zwraca dwa argumenty
# pierwszy ignorujemy, drugi zapisujemy do zmiennej ’axes’
# _, axes = plt.subplots() <- dlaczego tak deklarujemy? bo nie potrzebujemy zmiennej figure

# tworzymy wykres z punktów (0, 0), (1, 2), (2, 4), itd.
plt.plot([0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 6, 4, 2, 0])  # trójkąt
# plt.plot([0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 4, 4, 2, 0]) <- trapez

# wyświetlamy wykres
plt.show()
