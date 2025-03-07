import matplotlib.pyplot as plt
import numpy as np

# pytanie o przedział x
while True:
    try:
        x_start = float(input("Podaj początek przedziału x: "))
        x_end = float(input("Podaj koniec przedziału x: "))
        if x_start >= x_end:
            print("Początek musi być mniejszy niż koniec przedziału. Spróbuj ponownie.")
        else:
            break
    except ValueError:
        print("Niepoprawny format. Spróbuj ponownie.")

x = np.linspace(x_start, x_end, 100)  # wygładzenie: 10 -> 100 punktów

# pytanie o kolor wykresu
plot_color = input("Podaj kolor wykresu (np. red, blue, green): ")

# pytanie, które funkcje chce wyświetlić
print("\nWybierz funkcje do wyświetlenia:")
print("1 - y=x")
print("2 - y=sin(x)")
print("3 - y=cos(x)")
print("4 - y=x^3")
print("Numery funkcji oddziel przecinkami (np. 1,3):")

while True:
    choices = input().replace(" ", "").split(',')  # usunięcie spacji i rozdzielenie po przecinkach
    function_choices = []
    valid_choices = True
    for choice_str in choices:
        try:
            choice = int(choice_str)
            if 1 <= choice <= 4:
                function_choices.append(choice)
            else:
                print("Wybrano numer funkcji spoza zakresu. Spróbuj ponownie.")
                valid_choices = False
                break
        except ValueError:
            print("Niepoprawny format. Spróbuj ponownie.")
            valid_choices = False
            break
    if valid_choices and function_choices:  # sprawdzamy, czy lista nie jest pusta i numery są poprawne
        break
    elif not valid_choices:
        continue
    else:
        print("Nie wybrano żadnej funkcji. Wybierz przynajmniej jedną funkcję z listy (1, 2, 3 lub 4).")

_, ax = plt.subplots(figsize=(10, 5))

# wyświetlenie wybranych funkcji
if 1 in function_choices:
    ax.plot(x, x, color=plot_color, label='$y=x$')
if 2 in function_choices:
    ax.plot(x, np.sin(x), color='blue', label=r'$y=\sin(x)$')
if 3 in function_choices:
    ax.plot(x, np.cos(x), color='brown', label=r'$y=\cos(x)$')  # funkcja cos(x)
if 4 in function_choices:
    ax.plot(x, x ** 3, color='green', label='$y=x^3$')  # funkcja x^3

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_ylim([-2, 20])  # dla czytelniejszego wykresu
ax.set_title("Wykres")
ax.legend()

plt.show()
