import math
import numpy as np
import matplotlib.pyplot as plt

# wczytywanie parametrów od użytkownika
print("Podaj parametry układu(mx'' + bx' + kx = F):")
m = float(input("Masa m (>0): "))
b = float(input("Współczynnik tłumienia b (>0): "))
k = float(input("Stała sprężystości k (>0): "))
F = float(input("Siła zewnętrzna F: "))

# zakładam zerowe warunki początkowe
x0 = 0
v0 = 0

# wyróżnik (delta) równania  mr² + br + k = 0
delta = b**2 - 4 * m * k

# sprawdzenie warunku Δ > 0
if delta > 0:
    r1 = (-b + math.sqrt(delta)) / (2 * m)
    r2 = (-b - math.sqrt(delta)) / (2 * m)

    # rozwiązanie szczególne (pozycja równowagi)
    xp = F / k

    # obliczanie stałych C₁ i C₂ z warunków początkowych
    C1 = (v0 - r2 * (x0 - xp)) / (r1 - r2)
    C2 = (r1 * (x0 - xp) - v0) / (r1 - r2)

    time_constant = 1.0  # wartość domyślna
    t_end = 100 * time_constant  # czas końcowy dla wykresu

    # generowanie punktów
    t_values = np.linspace(0, t_end, 500)

    # obliczanie wartości x(t) dla każdego punktu czasowego
    x_values = C1 * np.exp(r1 * t_values) + C2 * np.exp(r2 * t_values) + xp

    # tworzenie wykresu
    plt.figure(figsize=(10, 6))
    plt.plot(t_values, x_values, label='Pozycja x(t)')

    # dodanie linii dla stanu ustalonego
    plt.axhline(xp, color='red', linestyle='--', linewidth=0.7, label=f'Stan ustalony x = {xp:.4f}')

    plt.title('Pozycja x(t) w czasie (tłumienie silne, Δ > 0)')
    plt.xlabel('Czas t')
    plt.ylabel('Pozycja x(t)')
    plt.legend()
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.show()
else:
    print(f"Delta: {delta} nie jest większa od 0")
