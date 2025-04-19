import numpy as np
import matplotlib.pyplot as plt


def inertial_2nd_order(x, t, u, k, T, zeta):
    """
    Prawe strony układu równań dla członu inercyjnego II rzędu.\n
    Równanie: T² d²y/dt² + 2ζT dy/dt + y = ku \n
    Stan: x₁ = y, x₂ = dy/dt \n
    x = [x1, x2] = [y, dy/dt]
    """
    x1, x2 = x
    dx1_dt = x2
    dx2_dt = (k * u - x1 - 2 * zeta * T * x2) / (T**2)  # przekształcenie równania
    return np.array([dx1_dt, dx2_dt])


def integrating_inertial(x, t, u, k, T):
    """
    Prawe strony układu równań dla członu całkującego z inercją. \n
    Równanie: T d²y/dt² + dy/dt = ku \n
    Stan: x₁ = y, x₂ = dy/dt \n
    x = [x1, x2] = [y, dy/dt]
    """
    x1, x2 = x
    dx1_dt = x2
    dx2_dt = (k * u - x2) / T
    return np.array([dx1_dt, dx2_dt])


def sinusoidal_input(t, amplitude, frequency):
    """Pobudzenie sinusoidalne."""
    omega = 2 * np.pi * frequency
    return amplitude * np.sin(omega * t)


def periodic_impulse_input(t, h, impulse_strength, period):
    """
    Okresowe pobudzenie impulsowe. \n
    Impuls o całce 'impulse_strength' co okres 'period' realizowany jako prostokąt o wymiarach 'h' x 'strength/h'.
    """
    time_within_period = t % period
    if 0 <= time_within_period < h:
        # sprawdzenie czy t jest bliskie wielokrotności period (z powodu błędów numerycznych)
        if abs(t - round(t / period) * period) < h / 2.0:
            return impulse_strength / h
        else:
            return 0.0  # przypadek np. t=1.99999, period=2, h=0.1 -> time_within_period=1.9999, ale to nie start
    else:
        return 0.0


def euler_simulation(system_func, system_params, input_func, input_params, t_span, h, x0):
    """
    Wykonuje symulację metodą Eulera.

    Args:
        system_func: Funkcja obliczająca pochodne stanu.
        system_params: Słownik lub krotka z parametrami systemu (k, T, zeta lub k, T).
        input_func: Funkcja generująca sygnał wejściowy.
        input_params: Słownik lub krotka z parametrami sygnału wejściowego.
        t_span: Krotka (t_start, t_end) określająca czas symulacji.
        h: Krok dyskretyzacji.
        x0: Wektor stanu początkowego.

    Returns:
        t_vec: Wektor czasu.
        y_vec: Wektor odpowiedzi systemu (pierwszy element stanu).
        u_vec: Wektor użytego sygnału wejściowego.
    """
    t_start, t_end = t_span
    n_steps = int((t_end - t_start) / h)
    t_vec = np.linspace(t_start, t_end, n_steps + 1)

    num_states = len(x0)
    x_vec = np.zeros((num_states, n_steps + 1))
    u_vec = np.zeros(n_steps + 1)

    x_vec[:, 0] = x0

    # specjalna obsługa dla impulsu okresowego - podajemy h
    if input_func == periodic_impulse_input:
        for i, t in enumerate(t_vec):
            u_vec[i] = input_func(t, h, *input_params)
    else:
         for i, t in enumerate(t_vec):
            u_vec[i] = input_func(t, *input_params)

    # pętla symulacji - jawna metoda Eulera
    for n in range(n_steps):
        t_n = t_vec[n]
        x_n = x_vec[:, n]
        u_n = u_vec[n]  # pobudzenie w chwili t_n

        # obliczenie pochodnych w punkcie (t_n, x_n, u_n)
        if system_func == inertial_2nd_order:
            dx_dt = system_func(x_n, t_n, u_n, *system_params)  # k, T, zeta
        elif system_func == integrating_inertial:
            dx_dt = system_func(x_n, t_n, u_n, *system_params)  # k, T

        # krok Eulera
        x_vec[:, n+1] = x_n + h * dx_dt

    y_vec = x_vec[0, :]  # odpowiedź y(t) to pierwszy element stanu x1
    return t_vec, y_vec, u_vec


# parametry członów
k = 1.0          # wzmocnienie statyczne
T = 1.0          # stała czasowa [s]
zeta = 0.5       # współczynnik tłumienia (dla inercyjnego II rzędu)

# parametry pobudzeń
sin_amplitude = 1.0
sin_frequency = 0.5     # w Hz
impulse_strength = 1.0  # całka impulsu
impulse_period = 5.0    # okres impulsów [s]

# parametry symulacji
t_start = 0.0
t_end = 20.0                # całkowity czas symulacji [s]
x0 = np.array([0.0, 0.0])   # stan początkowy [y(0), dy/dt(0)]
h = 0.1                     # krok dyskretyzacji [s]

print(f"Używany krok dyskretyzacji: h = {h} s")

# symulacje

# 1. Człon inercyjny II rzędu
# pobudzenie sinusoidalne
params_inertial2 = (k, T, zeta)
t1_sin, y1_sin, u1_sin = euler_simulation(
    inertial_2nd_order, params_inertial2,
    sinusoidal_input, (sin_amplitude, sin_frequency),
    (t_start, t_end), h, x0)

# pobudzenie impulsowe (okresowe)
t1_imp, y1_imp, u1_imp = euler_simulation(
    inertial_2nd_order, params_inertial2,
    periodic_impulse_input, (impulse_strength, impulse_period),
    (t_start, t_end), h, x0)

# 2. Człon całkujący z inercją
# pobudzenie sinusoidalne
params_integr_inertial = (k, T)
t2_sin, y2_sin, u2_sin = euler_simulation(
    integrating_inertial, params_integr_inertial,
    sinusoidal_input, (sin_amplitude, sin_frequency),
    (t_start, t_end), h, x0)

# pobudzenie impulsowe (okresowe)
t2_imp, y2_imp, u2_imp = euler_simulation(
    integrating_inertial, params_integr_inertial,
    periodic_impulse_input, (impulse_strength, impulse_period),
    (t_start, t_end), h, x0)

plt.style.use('seaborn-v0_8-whitegrid')  # lepszy wygląd wykresów

# wykresy dla członu inercyjnego II rzędu
fig1, axs1 = plt.subplots(2, 1, figsize=(10, 8))
fig1.suptitle(f'Człon inercyjny II rzędu (T={T}, ζ={zeta}, k={k}) - jawna metoda Eulera (h={h})', fontsize=14)

# pobudzenie sinusoidalne
axs1[0].plot(t1_sin, u1_sin, 'r--', label='Pobudzenie u(t)', alpha=0.7)
axs1[0].plot(t1_sin, y1_sin, 'b-', label='Odpowiedź y(t)')
axs1[0].set_title('Odpowiedź na pobudzenie sinusoidalne')
axs1[0].set_xlabel('Czas [s]')
axs1[0].set_ylabel('Amplituda')
axs1[0].legend()
axs1[0].grid(True)

# pobudzenie impulsowe (okresowe)
axs1[1].plot(t1_imp, u1_imp, 'r--', label='Pobudzenie u(t)', alpha=0.7)
axs1[1].plot(t1_imp, y1_imp, 'b-', label='Odpowiedź y(t)')
axs1[1].set_title(f'Odpowiedź na pobudzenie impulsowe (siła={impulse_strength}, okres={impulse_period}s)')
axs1[1].set_xlabel('Czas [s]')
axs1[1].set_ylabel('Amplituda')
axs1[1].legend()
axs1[1].grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # miejsce na tytuł główny
plt.show()

# wykresy dla członu całkującego z inercją
fig2, axs2 = plt.subplots(2, 1, figsize=(10, 8))
fig2.suptitle(f'Człon całkujący z inercją (T={T}, k={k}) - jawna metoda Eulera (h={h})', fontsize=14)

# pobudzenie sinusoidalne
axs2[0].plot(t2_sin, u2_sin, 'r--', label='Pobudzenie u(t)', alpha=0.7)
axs2[0].plot(t2_sin, y2_sin, 'g-', label='Odpowiedź y(t)')
axs2[0].set_title('Odpowiedź na pobudzenie sinusoidalne')
axs2[0].set_xlabel('Czas [s]')
axs2[0].set_ylabel('Amplituda')
axs2[0].legend()
axs2[0].grid(True)

# pobudzenie impulsowe (okresowe)
axs2[1].plot(t2_imp, u2_imp, 'r--', label='Pobudzenie u(t)', alpha=0.7)
axs2[1].plot(t2_imp, y2_imp, 'g-', label='Odpowiedź y(t)')
axs2[1].set_title(f'Odpowiedź na pobudzenie impulsowe (siła={impulse_strength}, okres={impulse_period}s)')
axs2[1].set_xlabel('Czas [s]')
axs2[1].set_ylabel('Amplituda')
axs2[1].legend()
axs2[1].grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
