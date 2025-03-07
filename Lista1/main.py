# zaimportuj bibliotekę ’pyplot’ z pakietu ’matplotlib’
# nazwij ją ’plt’
# dalej można z niej korzystać w kodzie pod nazwą ’plt’
import matplotlib.pyplot as plt

# utwórz wykres
# funkcja ’plt.subplots’ zwraca dwa argumenty
# pierwszy ignorujemy, drugi zapisujemy do zmiennej ’axes’
_, axes = plt.subplots()

# tworzymy wykres z punktów (0, 0), (1, 2), (2, 4), itd.
axes.plot([0, 1, 2, 3, 4, 5, 6], [0, 2, 4, 6, 4, 2, 0])

# wyświetlamy wykres
plt.show()
