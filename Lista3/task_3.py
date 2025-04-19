import numpy as np
import matplotlib.pyplot as plt


def euler_step(x, w, h):
    """
    Wykonuje jeden krok jawnej metody Eulera dla modelu robota.

    Args:
        x (np.array): Aktualny wektor stanu [x1, x2, x3].
        w (np.array): Aktualny wektor sterowań [w1, w2].
        h (float): Krok czasowy.

    Returns:
        np.array: Wektor stanu w następnym kroku czasowym.
    """
    x1, x2, x3 = x
    w1, w2 = w

    # Układ równań różniczkowych opisujących robota (wymnożenie macierzy):
    # ẋ₁(t) = cos(x₃(t)) * w₁(t)
    # ẋ₂(t) = sin(x₃(t)) * w₁(t)
    # ẋ₃(t) = w₂(t)

    x1_next = x1 + h * np.cos(x3) * w1  # wzory zgodne z metodą Eulera: (x₁[n+1] - x₁[n]) / h = cos(x₃[n]) * w₁[n]
    x2_next = x2 + h * np.sin(x3) * w1
    x3_next = x3 + h * w2  # x3 jest w radianach

    return np.array([x1_next, x2_next, x3_next])


# parametry początkowe
x1_0 = float(input("Podaj początkową pozycję x₁ [m]: "))
x2_0 = float(input("Podaj początkową pozycję x₂ [m]: "))
x3_0_deg = float(input("Podaj początkowy kąt obrotu x₃ [stopnie]: "))
x3_0 = np.radians(x3_0_deg)  # konwersja na radiany dla obliczeń

h = float(input("Podaj krok dyskretyzacji h [s] (np. 0.1): "))

phases = []
num_phases = int(input("Podaj liczbę faz ruchu (segmentów trajektorii): "))

x_initial = np.array([x1_0, x2_0, x3_0])

total_simulation_time = 0
for i in range(num_phases):
    print(f"\n--- Definicja Fazy {i + 1} ---")
    print("Podaj parametry ruchu dla tej fazy:")
    w1 = float(input(" Prędkość liniowa w₁ [m/s]: "))
    w2_deg = float(input(" Prędkość kątowa w₂ [stopnie/s]: "))
    w2 = np.radians(w2_deg)  # konwersja na radiany/s dla obliczeń
    duration = float(input(" Czas trwania fazy [s]: "))
    phases.append({'w1': w1, 'w2': w2, 'duration': duration})
    total_simulation_time += duration

print(f"\nCałkowity czas symulacji: {total_simulation_time:.2f} s")
print(f"Krok czasowy h: {h} s")

x_current = x_initial.copy()
t_current = 0.0

# historie stanu do wykresu
t_history = [t_current]
x1_history = [x_current[0]]
x2_history = [x_current[1]]
# x3_history = [x_current[2]]

# pętla symulacji
total_steps = 0
for i, phase in enumerate(phases):
    w_phase = np.array([phase['w1'], phase['w2']])
    # iterujemy dopóki czas fazy nie minie
    t_phase_start = t_history[-1]  # czas na początku tej fazy
    t_phase_end = t_phase_start + phase['duration']

    # mała tolerancja, by uniknąć problemów z precyzją floata
    epsilon = h / 100.0
    while t_current < t_phase_end - epsilon:
        # sprawdzenie czy następny krok nie przekroczy czasu fazy
        time_to_end_phase = t_phase_end - t_current
        current_h = min(h, time_to_end_phase)

        if current_h <= epsilon:  # unikanie bardzo małych kroków na końcu
            break

        x_next = euler_step(x_current, w_phase, current_h)
        t_current += current_h
        x_current = x_next

        # zapis pozycji
        t_history.append(t_current)
        x1_history.append(x_current[0])
        x2_history.append(x_current[1])
        # x3_history.append(x_current[2])
        total_steps += 1

    t_current = t_phase_end

print(f"\nSymulacja zakończona. Wykonano {total_steps} kroków Eulera.")

# wykres pozycji robota
plt.figure(figsize=(10, 8))
# linia łącząca punkty i markery w każdym punkcie
plt.plot(x1_history, x2_history, '-', label=f'Pozycja robota (Euler, h={h} s)', markersize=4, linewidth=1)

# punkt startowy i końcowy
plt.plot(x1_history[0], x2_history[0], 'go', markersize=12, label='Pozycja początkowa')
plt.plot(x1_history[-1], x2_history[-1], 'ro', markersize=10, label='Pozycja końcowa')

# strzałki wskazujące kierunek ruchu
arrow_interval_time = 1  # czas [s] pomiędzy rysowaniem kolejnych strzałek
arrow_step = max(1, int(arrow_interval_time / h))  # liczba kroków symulacji pomiędzy strzałkami
start_arrow_index = arrow_step  # indeks, od którego zacząć rysować strzałki (pomijamy początek)
for i in range(start_arrow_index, len(x1_history) - 1, arrow_step):
    # wektor przesunięcia (do określenia kierunku i długości strzałki)
    dx = x1_history[i+1] - x1_history[i]
    dy = x2_history[i+1] - x2_history[i]
    # nie rysuj strzałek o zerowej długości
    if abs(dx) > 1e-6 or abs(dy) > 1e-6:
        plt.arrow(x1_history[i], x2_history[i], dx, dy, head_width=0.05, head_length=0.1,
                  fc='blue', ec='blue', length_includes_head=True)

plt.title(f'Pozycja robota (x1, x2) - jawna metoda Eulera (h={h})')
plt.xlabel('x1 [m]')
plt.ylabel('x2 [m]')
plt.legend()
plt.grid(True)
plt.axis('equal')  # równe proporcje osi, aby dobrze zwizualizować ruch po okręgu i kąty
plt.show()
