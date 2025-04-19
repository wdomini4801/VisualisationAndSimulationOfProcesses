import numpy as np
import matplotlib.pyplot as plt


def get_float_sequence(prompt, length):
    """Pobiera od użytkownika ciąg liczb zmiennoprzecinkowych."""
    sequence = []
    print(prompt)
    for i in range(length):
        while True:
            try:
                value = float(input(f" Podaj wartość dla dnia {i + 1}/{length}: "))
                sequence.append(value)
                break  # przejdź do następnej liczby
            except ValueError:
                print(" Nieprawidłowa wartość. Proszę podać liczbę.")
    return np.array(sequence)


# pobieranie parametrów od użytkownika
H = int(input("Podaj horyzont czasowy H (liczba dni): "))
x0 = float(input("Podaj początkowe saldo konta x(0) [PLN]: "))
y0 = float(input("Podaj początkowy stan pszenicy y(0) [t] (> 0): "))
r_daily = float(input("Podaj dzienną stopę zysku na koncie r (np. 0.0001 dla 0.01% dziennie): "))
h_daily = float(input("Podaj dzienny koszt składowania tony pszenicy h [PLN/(t*dzień)]: "))

# pobieranie ciągów v(t) i p(t)
v_daily = get_float_sequence(f"Podaj prędkość skupu/sprzedaży v(t) [t/dzień] dla kolejnych {H} dni (<0 to sprzedaż):",
                             H)
p_daily = get_float_sequence(f"Podaj cenę tony pszenicy p(t) [PLN/t] dla kolejnych {H} dni:", H)

t = np.arange(H + 1)  # wektor czasu (dni), od 0 do H włącznie
x_history = np.zeros(H + 1)
y_history = np.zeros(H + 1)

# warunki początkowe
x_history[0] = x0
y_history[0] = y0

# pętla symulacji - jawna metoda Eulera (dla Δt = 1 dzień)
# (x[n+1] - x[n]) / Δt = r * x[n] - h * y[n] - p[n] * v[n]
# (y[n+1] - y[n]) / Δt = v[n]

for n in range(H):  # pętla od dnia 0 do H-1
    # pobranie wartości v i p dla dnia n (indeks n w tablicach v_daily, p_daily)
    vn = v_daily[n]
    pn = p_daily[n]

    # odczyt stanu na początku dnia n (koniec dnia n-1)
    xn = x_history[n]
    yn = y_history[n]

    # stan na koniec dnia n (początek dnia n+1) - indeks n+1 w historii
    x_history[n + 1] = xn + r_daily * xn - h_daily * yn - pn * vn  # podstawienie do wzoru Δt = 1
    y_history[n + 1] = vn + yn

    # sprawdzenie czy stan pszenicy nie spadł poniżej zera
    if y_history[n + 1] < -1e-9:  # mała tolerancja dla błędów
        print(f"Ostrzeżenie: W dniu {n + 1} obliczony stan pszenicy ({y_history[n + 1]:.2f}) jest ujemny.")

# przygotowanie danych v(t) i p(t) do wykresu typu step
v_plot = np.append(v_daily, v_daily[-1])  # powtórz ostatnią wartość dla pełnego przedziału H
p_plot = np.append(p_daily, p_daily[-1])

# wykresy
fig, axs = plt.subplots(4, 1, figsize=(10, 12))
fig.suptitle('Symulacja modelu sprzedaży i skupu pszenicy (jawna metoda Eulera)', fontsize=16)

# 1. Saldo konta x(t)
axs[0].plot(t, x_history, 'b-o', markersize=4, label='Saldo konta x(t)')
axs[0].set_xlabel('Czas [dni]')
axs[0].set_ylabel('Saldo [PLN]')
axs[0].grid(True)
axs[0].legend()

# 2. Składowana pszenica y(t)
axs[1].plot(t, y_history, 'g-o', markersize=4, label='Składowana pszenica y(t)')
axs[1].set_xlabel('Czas [dni]')
axs[1].set_ylabel('Pszenica [t]')
axs[1].grid(True)
axs[1].legend()
axs[1].axhline(0, color='gray', linestyle='--', linewidth=0.8)  # linia y=0 dla odniesienia

# 3. Prędkość skupu/sprzedaży v(t)
axs[2].step(t, v_plot, 'r-', where='post', label='Prędkość skupu v(t)')
axs[2].set_xlabel('Czas [dni]')
axs[2].set_ylabel('Skup/Sprzedaż [t/dzień]')
axs[2].grid(True)
axs[2].legend()
axs[2].axhline(0, color='gray', linestyle='--', linewidth=0.8)  # linia v=0 dla odniesienia

# 4. Cena pszenicy p(t)
axs[3].step(t, p_plot, 'm-', where='post', label='Cena p(t)')
axs[3].set_xlabel('Czas [dni]')
axs[3].set_ylabel('Cena [PLN/t]')
axs[3].grid(True)
axs[3].legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.96])  # miejsce na suptitle
plt.show()
