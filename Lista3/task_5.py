import numpy as np
import matplotlib.pyplot as plt


def robot_dynamics(x, w):
    """
    Oblicza pochodne stanu [dx1/dt, dx2/dt, dx3/dt] dla danego stanu x i sterowań w.

    Args:
        x (np.array): Aktualny wektor stanu [x1, x2, x3 (rad)].
        w (np.array): Aktualny wektor sterowań [w1 (m/s), w2 (rad/s)].

    Returns:
        np.array: Wektor pochodnych stanu.
    """
    x1, x2, x3 = x
    w1, w2 = w
    dx1_dt = np.cos(x3) * w1
    dx2_dt = np.sin(x3) * w1
    dx3_dt = w2
    return np.array([dx1_dt, dx2_dt, dx3_dt])


def euler_step(x, w, h):
    """Jeden krok jawnej metody Eulera dla danego stanu, sterowań oraz kroku dyskretyzacji. \n
    (x[n+1]-x[n]) / h = dx/dt"""
    return x + h * robot_dynamics(x, w)


def rk2_step(x, w, h):
    """Jeden krok metody RK-2 (punktu środkowego) dla danego stanu, sterowań oraz kroku dyskretyzacji. \n
    k₁ = h * f(x_n, w_n) \n
    k₂ = h * f(x_n + k₁/2, w_n) (zakładamy, że sterowanie w jest stałe w kroku h) \n
    x[n+1] = x[n] + k₂
    """
    k1 = h * robot_dynamics(x, w)
    k2 = h * robot_dynamics(x + 0.5 * k1, w)
    return x + k2


def rk4_step(x, w, h):
    """Jeden krok klasycznej metody RK-4 dla danego stanu, sterowań oraz kroku dyskretyzacji. \n
    k₁ = h * f(x_n, w_n) \n
    k₂ = h * f(x_n + k₁/2, w_n) \n
    k₃ = h * f(x_n + k₂/2, w_n) \n
    k₄ = h * f(x_n + k₃, w_n) \n
    x[n+1] = x[n] + (k₁ + 2k₂ + 2k₃ + k₄) / 6"""
    k1 = h * robot_dynamics(x, w)
    k2 = h * robot_dynamics(x + 0.5 * k1, w)
    k3 = h * robot_dynamics(x + 0.5 * k2, w)
    k4 = h * robot_dynamics(x + k3, w)
    return x + (k1 + 2*k2 + 2*k3 + k4) / 6.0


def run_simulation(x_initial, phases, h, step_function, method_name):
    """
    Wykonuje symulację dla zadanej metody kroku.

    Args:
        x_initial (np.array): Początkowy stan robota.
        phases (list): Lista słowników definiujących fazy ruchu.
        h (float): Krok dyskretyzacji.
        step_function (callable): Funkcja wykonująca jeden krok (w zależności od metody).
        method_name (str): Nazwa metody do wyświetlania postępu.

    Returns:
        tuple: (t_history, x1_history, x2_history)
    """

    x_current = x_initial.copy()
    t_current = 0.0
    t_history = [t_current]
    x1_history = [x_current[0]]
    x2_history = [x_current[1]]
    total_steps = 0
    phase_start_indices = [0]  # indeks startowy pierwszej fazy

    for i, phase in enumerate(phases):
        w_phase = np.array([phase['w1'], phase['w2']])  # sterowanie dla tej fazy
        t_phase_start = t_history[-1]
        t_phase_end = t_phase_start + phase['duration']
        epsilon = h / 100.0  # tolerancja dla porównań zmiennoprzecinkowych

        # pętla kroków wewnątrz fazy
        while t_current < t_phase_end - epsilon:
            time_to_end_phase = t_phase_end - t_current
            current_h = min(h, time_to_end_phase)
            if current_h <= epsilon:
                break  # unikaj bardzo małych kroków na końcu

            x_next = step_function(x_current, w_phase, current_h)

            t_current += current_h
            x_current = x_next

            t_history.append(t_current)
            x1_history.append(x_current[0])
            x2_history.append(x_current[1])
            total_steps += 1

        t_current = t_phase_end  # dokładny czas końca fazy (może być pominięty przez epsilon)
        if i < len(phases) - 1:  # indeks końca tej fazy (startu następnej)
            phase_start_indices.append(len(t_history))

    print(f"  Symulacja {method_name} zakończona. Wykonano {total_steps} kroków.")
    return t_history, x1_history, x2_history, phase_start_indices


# parametry początkowe
x1_0 = float(input("Podaj początkową pozycję x₁ [m]: "))
x2_0 = float(input("Podaj początkową pozycję x₂ [m]: "))
x3_0_deg = float(input("Podaj początkowy kąt obrotu x₃ [stopnie]: "))
x3_0 = np.radians(x3_0_deg)  # konwersja na radiany dla obliczeń
x_initial = np.array([x1_0, x2_0, x3_0])

h = float(input("Podaj krok dyskretyzacji h [s] (np. 0.1): "))

phases = []
num_phases = int(input("Podaj liczbę faz ruchu (segmentów trajektorii): "))

total_simulation_time = 0
for i in range(num_phases):
    print(f"\n--- Definicja Fazy {i + 1} ---")
    print("Podaj parametry ruchu dla tej fazy:")
    w1 = float(input(" Prędkość liniowa w₁ [m/s]: "))
    w2_deg = float(input(" Prędkość kątowa w₂ [stopnie/s]: "))
    w2 = np.radians(w2_deg)  # konwersja na rad/s dla obliczeń
    duration = float(input(" Czas trwania fazy [s]: "))
    phases.append({'w1': w1, 'w2': w2, 'duration': duration})
    total_simulation_time += duration

print(f"\nCałkowity czas symulacji: {total_simulation_time:.2f} s")
print(f"Krok dyskretyzacji h: {h} s")

# uruchomienie symulacji dla każdej metody
t_euler, x1_euler, x2_euler, _ = run_simulation(x_initial, phases, h, euler_step, "jawna metoda Eulera")
t_rk2, x1_rk2, x2_rk2, _ = run_simulation(x_initial, phases, h, rk2_step, "metoda RK-2")
t_rk4, x1_rk4, x2_rk4, phase_indices = run_simulation(x_initial, phases, h, rk4_step, "metoda RK-4")

# wykres porównawczy
plt.figure(figsize=(12, 9))

# Euler
plt.plot(x1_euler, x2_euler, 'o-', label='Euler', markersize=3, linewidth=1, color='red', alpha=0.8)
# RK-2
plt.plot(x1_rk2, x2_rk2, 's-', label='RK-2', markersize=3, linewidth=1, color='blue', alpha=0.8)
# RK-4
plt.plot(x1_rk4, x2_rk4, '^-', label=f'RK-4', markersize=3, linewidth=1, color='green', alpha=0.8)

# punkt startowy (wspólny dla wszystkich)
plt.plot(x1_euler[0], x2_euler[0], 'ko', markersize=10, label='Start')

# punkty końcowe dla każdej metody (mogą się różnić)
plt.plot(x1_euler[-1], x2_euler[-1], 'rs', markersize=10, label='Koniec Euler')
plt.plot(x1_rk2[-1], x2_rk2[-1], 'bs', markersize=10, label='Koniec RK-2')
plt.plot(x1_rk4[-1], x2_rk4[-1], 'gs', markersize=10, label='Koniec RK-4')

plt.title(f'Porównanie wyznaczonych trajektorii robota - metody numeryczne (h={h} s)')
plt.xlabel('Pozycja x1 [m]')
plt.ylabel('Pozycja x2 [m]')
plt.legend()
plt.grid(True)
plt.axis('equal')  # do wizualizacji ruchu po okręgu
plt.show()
