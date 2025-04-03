import numpy as np
import matplotlib.pyplot as plt

# pobranie danych od użytkownika
T_half = float(input("Podaj okres połowicznego rozpadu pierwiastka (w latach): "))
m0 = float(input("Podaj masę początkową pierwiastka (g): "))

# stała rozpadu
lambda_decay = np.log(2) / T_half

# zakres czasu - kilka okresów połowicznego rozpadu, aby zobaczyć wyraźny zanik
t_max = 5 * T_half
t = np.linspace(0, t_max, 500)

# masa z wyprowadzonego wzoru: m(t) = m₀ * e^(-λt)
m = m0 * np.exp(-lambda_decay * t)

# tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.plot(t, m, label=f'Rozpad (m₀={m0:.1f} g, T½={T_half} lat)')

# maksymalna wielokrotność T½ mieszczącą się w t_max
max_i = int(t_max / T_half)

# oznaczenia dla okresów połowicznego rozpadu (dla lepszej wizualizacji)
for i in range(1, max_i+1):
    t_i_half = i * T_half  # czas, jaki upłynął po i okresach połowicznego rozpadu
    m_i_half = m0 / (2**i)  # masa, jaka pozostała po i okresach połowicznego rozpadu

    # linie pomocnicze
    plt.axvline(x=t_i_half, color='gray', linestyle=':', linewidth=0.7, alpha=0.7)
    plt.axhline(y=m_i_half, color='gray', linestyle=':', linewidth=0.7, alpha=0.7)

    # kropki w punktach (T½, m₀/2), (2T½, m₀/4) itd.
    plt.plot(t_i_half, m_i_half, 'ro', markersize=5)

    # dynamiczne pozycjonowanie etykiety punktu
    text_x = t_i_half + 0.015 * t_max
    text_y = m_i_half + 0.02 * m0

    # etykieta punktu
    plt.text(text_x, text_y,f'{i}T½ ({m_i_half:.3f} g)',
             verticalalignment='bottom',
             horizontalalignment='left',
             fontsize=9)

plt.title('Wykres rozpadu promieniotwórczego')
plt.xlabel('Czas (lata)')
plt.ylabel('Pozostała masa (g)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(bottom=0, top=m0 * 1.05)
plt.xlim(left=0, right=t_max * 1.02)
plt.tight_layout()

plt.show()

# wyświetlenie obliczonych parametrów
print(f"Parametry rozpadu:")
print(f"Okres połowicznego rozpadu (T½): {T_half} lat")
print(f"Stała rozpadu (λ): {lambda_decay:.6f} lat⁻¹ ({lambda_decay:.2e} lat⁻¹)")
print(f"Współczynnik proporcjonalności (-λ): {-lambda_decay:.6f} lat⁻¹ ({-lambda_decay:.2e} lat⁻¹)")
