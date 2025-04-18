import numpy as np
import matplotlib.pyplot as plt

# parametry symulacji i obiektu
T = 1.0      # stała czasowa
k = 1.0      # wzmocnienie statyczne
y0 = 0.0     # warunek początkowy
t_start = 0.0  # czas początkowy symulacji
t_end = 5 * T  # czas końcowy symulacji

# kroki czasowe do przetestowania
# h_values = [0.8 * T, 0.5 * T, 0.2 * T, 0.05 * T]
h_values = [2.5, 1.5, 0.5, 0.1]


# funkcje pobudzeń
def step_input(t):
    """Pobudzenie skokowe jednostkowe."""
    return 1.0 if t >= 0 else 0.0


def impulse_input(t, h):
    """Przybliżone pobudzenie impulsowe (delta Diraca)."""
    return 1.0 / h if 0 <= t < h else 0.0


# symulacja metodą Eulera
def euler_simulation(h, input_type):
    """Wykonuje symulację jawną metodą Eulera dla danego h i typu pobudzenia."""
    n_steps = int(t_end / h)
    t = np.linspace(t_start, t_end, n_steps + 1)
    y = np.zeros(n_steps + 1)
    u = np.zeros(n_steps + 1)

    y[0] = y0  # wstawienie warunku początkowego

    # generowanie sygnału wejściowego
    if input_type == 'step':
        for i in range(n_steps + 1):
            u[i] = step_input(t[i])
    elif input_type == 'impulse':
        # impuls niezerowy tylko na początku
        if n_steps > 0:
            u[0] = 1.0 / h  # impuls o całce 1
    else:
        raise ValueError("Nieznany typ pobudzenia")

    # pętla symulacji - jawna metoda Eulera
    for n in range(n_steps):
        dy_dt = (k * u[n] - y[n]) / T
        y[n+1] = y[n] + h * dy_dt

    return t, y


# 1. Wykres odpowiedzi na skok jednostkowy
plt.figure(figsize=(10, 6))
plt.title(f'Odpowiedź skokowa członu inercyjnego (T={T}, k={k})\njawna metoda Eulera')

# rozwiązanie analityczne dla skoku jednostkowego (dla porównania)
t_analytical = np.linspace(t_start, t_end, 200)
y_analytical_step = k * (1 - np.exp(-t_analytical / T))  # z poprzedniej listy
plt.plot(t_analytical, y_analytical_step, 'k--', label='rozwiązanie analityczne', linewidth=2)

# symulacje dla różnych h
for h in h_values:
    t_sim, y_sim = euler_simulation(h, 'step')
    plt.plot(t_sim, y_sim, '-', label=f'jawny Euler, h={h:.2f} s', markersize=3, linewidth=1)

plt.xlabel('Czas [s]')
plt.ylabel('Odpowiedź y(t)')
plt.legend()
plt.grid(True)
plt.ylim(bottom=min(y0, 0)-0.1, top=k*1.1)  # dostosowanie zakresu osi y
plt.show()

# 2. Wykres odpowiedzi na impuls jednostkowy
plt.figure(figsize=(10, 6))
plt.title(f'Odpowiedź impulsowa członu inercyjnego (T={T}, k={k})\njawna metoda Eulera (przybliżona delta Diraca)')

# rozwiązanie analityczne dla impulsu jednostkowego (delta Diraca)
y_analytical_impulse = (k / T) * np.exp(-t_analytical / T)  # z poprzedniej listy
plt.plot(t_analytical, y_analytical_impulse, 'k--', label='rozwiązanie analityczne', linewidth=2)

# symulacje dla różnych h
for h in h_values:
    t_sim, y_sim = euler_simulation(h, 'impulse')
    if h >= 2*T:
        # jeśli wartości są bardzo duże, ograniczamy oś Y dla czytelności
        if np.any(np.abs(y_sim) > 10 * (k/T)):
             plt.ylim(top=10*(k/T), bottom=min(0,-0.1*(k/T)))

    plt.plot(t_sim, y_sim, '-', label=f'jawny Euler, h={h:.2f} s', markersize=3, linewidth=1)

plt.xlabel('Czas [s]')
plt.ylabel('Odpowiedź y(t)')
plt.legend()
plt.grid(True)
plt.show()
