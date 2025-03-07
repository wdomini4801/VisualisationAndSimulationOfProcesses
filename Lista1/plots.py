import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 20, 10)

_, ax = plt.subplots(figsize=(10, 5))

ax.plot(x, x, color='black', label='y=x')
ax.plot(x, np.sin(x), label='y=sin(x)')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title("Wykres")
ax.legend()

plt.show()
