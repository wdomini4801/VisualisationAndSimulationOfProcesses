import matplotlib.pyplot as plt
import numpy as np

# pobranie danych od użytkownika
T = float(input("Podaj wartość parametru T: "))
k = float(input("Podaj wartość parametru k: "))

if T == 0:
    print("T nie może być równe 0")
    exit()

# zakres czasu
time = np.linspace(0, 5 * T if T > 0 else 5, 500)


# odpowiedź na pobudzenie jednostkowe
def odpowiedz_jednostkowa(t, T, k):
    return k * (1 - np.exp(-t / T)) * (t >= 0)  # mnożenie przez (t>=0) aby odpowiedź była zero dla t<0


# odpowiedź na deltę Diraca
def odpowiedz_diraca(t, T, k):
    return (k / T) * np.exp(-t / T) * (t >= 0)  # mnożenie przez (t>=0) aby odpowiedź była zero dla t<0


y_jedn = odpowiedz_jednostkowa(time, T, k)
y_dirac = odpowiedz_diraca(time, T, k)

# wyświetlanie wykresów
plt.figure(figsize=(12, 6))

# wykres odpowiedzi na pobudzenie jednostkowe
plt.subplot(1, 2, 1)
plt.plot(time, y_jedn)
plt.title('Odpowiedź na pobudzenie jednostkowe')
plt.xlabel('Czas')
plt.ylabel('y(t)')
plt.grid(True)

# wykres odpowiedzi na deltę Diraca
plt.subplot(1, 2, 2)
plt.plot(time, y_dirac)
plt.title('Odpowiedź na deltę Diraca')
plt.xlabel('Czas')
plt.ylabel('y(t)')
plt.grid(True)

plt.tight_layout()  # dopasowanie wykresów, żeby się nie nakładały
plt.show()
