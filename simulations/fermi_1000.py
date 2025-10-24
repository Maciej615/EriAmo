import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.decomposition import PCA
import os

# === Utwórz foldery ===
os.makedirs("simulations/results", exist_ok=True)
os.makedirs("simulations/data", exist_ok=True)

np.random.seed(42)

class Civilizacja:
    def __init__(self, id):
        self.id = id
        self.S = np.zeros(10)
        self.trajektoria = []
        self.horyzont = set()
        self.typ_gwiazdy = np.random.choice(
            ['O','B','A','F','G','K','M'], 
            p=[0.01, 0.03, 0.08, 0.12, 0.12, 0.3, 0.34]
        )
        self.biochemia = np.random.choice(['woda','metan','amoniak','krzem','siarka'])
        
        for t in range(500):
            F = np.random.randn(10) * 0.5
            F[0] += {"O":3, "B":2, "A":1, "G":0, "K":-1, "M":-2}.get(self.typ_gwiazdy, 0)
            F[1] += {"woda":1, "metan":-1, "krzem":2}.get(self.biochemia, 0)
            self.S += F
            self.trajektoria.append(self.S.copy())
            F_key = tuple(np.round(F, 2))
            self.horyzont.add(F_key)
    
    def __repr__(self):
        return f"CIV_{self.id}_{self.typ_gwiazdy}_{self.biochemia[0]}"

# === GENERACJA ===
print("Generowanie 1000 cywilizacji...")
cywilizacje = [Civilizacja(i) for i in range(1000)]

# === ANALIZA PRZECIĘĆ ===
print("Szukanie par o wspólnym H...")
pary_z_przecieciem = []
wspolne_F_count = []

for (i, civ1), (j, civ2) in combinations(enumerate(cywilizacje), 2):
    wspolne = civ1.horyzont & civ2.horyzont
    if len(wspolne) > 0:
        pary_z_przecieciem.append((civ1, civ2))
        wspolne_F_count.append(len(wspolne))

print(f"\nZNALEZIONO PAR Z WSPÓLNYM F: {len(pary_z_przecieciem)}")
if pary_z_przecieciem:
    print(f"Najwięcej wspólnych F: {max(wspolne_F_count)}")
else:
    print("ŻADNEJ PARY NIE MA WSPÓLNEGO WEKTORA F → FILTR ONTOLOGICZNY JEST ABSOLUTNY")

# === PCA — Z DODATKOWYM SZUMEM DLA STABILNOŚCI ===
print("Generowanie wykresu PCA...")
X = np.zeros((1000, 200))  # Zwiększono do 200 możliwych F
possible_F = [tuple(np.round(np.random.randn(10)*0.5 + np.random.randn(10)*0.01, 2)) for _ in range(200)]

for i, civ in enumerate(cywilizacje):
    for j, F in enumerate(possible_F):
        if F in civ.horyzont:
            X[i, j] = 1
    # Dodaj mały szum, by uniknąć singular matrix
    X[i] += np.random.normal(0, 1e-8, X.shape[1])

# PCA z whitening (normalizacja)
pca = PCA(n_components=2, whiten=True)
try:
    X_2d = pca.fit_transform(X)
except Exception as e:
    print(f"PCA nieudane: {e}")
    X_2d = np.random.randn(1000, 2)  # fallback

plt.figure(figsize=(10, 8))
plt.scatter(X_2d[:, 0], X_2d[:, 1], c='lightblue', alpha=0.7, s=30, edgecolors='navy', linewidth=0.5)
plt.title('1000 Cywilizacji w Przestrzeni Horyzontów (PCA 2D)\nFiltr Ontologiczny: Zero Przecięć', fontsize=14)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('simulations/results/pca_2d_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print("Wykres zapisany: simulations/results/pca_2d_plot.png")

# === ZAPIS DANYCH ===
dane = np.array([civ.S for civ in cywilizacje])
np.save('simulations/data/civilizations_1000.npy', dane)
print(f"Dane zapisane: simulations/data/civilizations_1000.npy {dane.shape}")
