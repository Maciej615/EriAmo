import numpy as np
import matplotlib.pyplot as plt

print("Uruchamianie symulacji 'Kuli Rzeczywistości'...")

# --- Definicja Parametrów Modelu ---
steps = 1000  # Liczba "punktów stycznych" w "wędrówce"
wymiary = 2   # Liczba osi Krajobrazu P (dla wizualizacji 2D)

# S(t0) - Stan Początkowy (Początek wędrówki)
pos = np.zeros((steps, wymiary))

# --- Definicja Wektorów Zmian (F) ---
# F_wola: Wewnętrzny wektor determinacji/woli.
# Ustawiamy go jako błądzenie losowe, aby symulować stałą, ale zmienną wolę.
# Używamy cumsum (suma skumulowana) do symulacji 'pamięci' woli.
wektor_woli = np.random.uniform(-0.05, 0.05, size=(steps, wymiary)).cumsum(axis=0)

# F_przypadek: Zewnętrzny wektor Krajobrazu P (np.random.normal)
# To są te "zmienne", "pył kosmiczny", "spotkania".
sila_przypadku = 0.1
wektor_przypadku = np.random.normal(0, sila_przypadku, size=(steps, wymiary))

# --- Symulacja "Wędrówki" (Całka Akumulacji) ---
# S(t) = S(t-1) + F(t)
# Gdzie F(t) = F_wola(t) + F_przypadek(t)

for t in range(1, steps):
    
    # F = F(S(t-1), V(t)) -> W naszym przypadku F = F_wola + F_przypadek
    F_total = wektor_woli[t] + wektor_przypadku[t]
    
    # S(t) = S(t-1) + F_total * dt (dt = 1 krok)
    # To jest nasza Całka (akumulacja historii)
    pos[t] = pos[t-1] + F_total

print("Symulacja zakończona. Generowanie wizualizacji...")

# --- Wizualizacja Trajektorii (Ścieżki C) ---
plt.figure(figsize=(10, 10))
plt.plot(pos[:, 0], pos[:, 1], lw=1, alpha=0.6, label='Ścieżka $\mathcal{C}$ (Wędrówka)')

# Oznaczenie Początku i Końca
plt.scatter(pos[0, 0], pos[0, 1], color='green', s=100, zorder=5, label='Początek $S(t_0)$')
plt.scatter(pos[-1, 0], pos[-1, 1], color='red', s=100, zorder=5, label='Koniec $S(t)$ (Obecność)')

plt.legend()
plt.title("Model Kuli Rzeczywistości ($S$)", fontsize=16)
plt.xlabel("Oś Krajobrazu $P_1$")
plt.ylabel("Oś Krajobrazu $P_2$")
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True, linestyle='--', alpha=0.4)

# Zapisz wykres do pliku. Ten plik też dodasz do GitHub.
plt.savefig('kula_trajektoria.png')
print("Wykres zapisany jako 'kula_trajektoria.png'.")
# plt.show() # Możesz odkomentować, jeśli chcesz zobaczyć wykres lokalnie
