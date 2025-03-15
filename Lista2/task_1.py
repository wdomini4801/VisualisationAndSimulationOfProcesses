import matplotlib.pyplot as plt
import numpy as np

# pobierz dane od użytkownika
r = float(input("Podaj rozstaw kół (r): "))
up = float(input("Podaj prędkość liniową prawego koła (up): "))
ul = float(input("Podaj prędkość liniową lewego koła (ul): "))

# oblicz stałą prędkość kątową (ze wzoru)
omega = (1/r) * (up - ul)

# zakres czasu (od 0 do 10 sekund)
time = np.linspace(0, 10, 100)

# kąt obrotu w czasie (zakładając kąt początkowy 0) w radianach
x3 = omega * time

# wyświetl wykres
plt.figure(figsize=(8, 6))
plt.plot(time, x3)
plt.xlabel("Czas (s)")
plt.ylabel("Kąt obrotu x3 (rad)")
plt.title("Wykres kąta obrotu robota w czasie")
plt.grid(True)  # siatka dla lepszej czytelności
plt.show()
