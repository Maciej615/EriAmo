# Model Kuli Rzeczywistości (Sphere of Reality Model)
# Autor: Maciej A. Mazur
# Licencja: CC BY-SA 4.0
# Opis: Symulacja 2D wędrówki Kuli Rzeczywistości po Krajobrazie P

import matplotlib.pyplot as plt
import numpy as np

# Symulacja ścieżki kuli w 2D krajobrazie (emergentna, nie pojedyncza)
np.random.seed(42)  # Dla powtarzalności
steps = 50  # Liczba kroków (interakcji)
x = np.cumsum(np.random.randn(steps))  # Losowa ścieżka x (np. oś historia/percepcja)
y = np.cumsum(np.random.randn(steps))  # Losowa ścieżka y (np. oś biologiczna/przypadek)

# Przykładowe wektory interakcji F (5 losowych, niezależnych)
vec_starts = np.random.choice(range(steps), 5)  # Punkty startowe wektorów
vec_dx = np.random.uniform(-2, 2, 5)  # Składowe x (np. siła historii)
vec_dy = np.random.uniform(-2, 2, 5)  # Składowe y (np. siła zapachu/bólu)

# Wizualizacja
fig, ax = plt.subplots(figsize=(10, 7))
ax.plot(x, y, 'b-', linewidth=2, label='Emergentna Ścieżka C (Wędrówka Kuli)')
ax.scatter(x[0], y[0], color='green', s=150, label='Start S(t₀) – Początek Bytu')
ax.scatter(x[-1], y[-1], color='red', s=150, label='Obecny S(t) – Akumulacja Interakcji')

# Dodaj wektory F jako strzałki (reprezentujące punkty styczne)
for i, start in enumerate(vec_starts):
    ax.arrow(x[start], y[start], vec_dx[i], vec_dy[i], 
             head_width=0.5, head_length=0.7, fc='orange', ec='orange', 
             label='Wektor F (Interakcja)' if i == 0 else None)

# Etykiety i styl
ax.set_title('Wizualizacja Kuli Rzeczywistości: Wędrówka po Wieloosiowym Krajobrazie P', fontsize=14)
ax.set_xlabel('Oś X (np. Czas/Historia/Zapach)', fontsize=12)
ax.set_ylabel('Oś Y (np. Biologia/Ból/Przypadek)', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_xlim(min(x)-3, max(x)+3)
ax.set_ylim(min(y)-3, max(y)+3)
plt.savefig("kula_rzeczywistosci.png", dpi=300)
plt.tight_layout()
plt.show()  # Wyświetl wykres (lub plt.savefig('kula_rzeczywistosci.png') do zapisu)
