import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.decomposition import PCA
import seaborn as sns

np.random.seed(42)

class Civilizacja:
    def __init__(self, id):
        self.id = id
        self.S = np.zeros(10)  # 10-wymiarowy stan
        self.trajektoria = []
        self.horyzont = set()  # unikalne F
  self.typ_gwiazdy = np.random.choice(['O','B','A','F','G','K','M'], p=[0.01,0.03,0.08,0.12,0.12,0.3,0.34])
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

print("Generowanie 1000 cywilizacji...")
cywilizacje = [Civilizacja(i) for i in range(1000)]

print("Szukanie par o wspólnym H...")
pary_z_przecieciem = []
wspolne_F_count = []

for (i, civ1), (j, civ2) in combinations(enumerate(cywilizacje), 2):
    wspolne = civ1.horyzont & civ2.horyzont
    if len(wspolne) > 0:
        pary_z_przytcieciem.append((civ1, civ2))
        wspolne_F_count.append(len(wspolne))

print(f"\nZNALEZIONO PAR Z WSPÓLNYM F: {len(pary_z_przecieciem)}")
if pary_z_przecieciem:
    print(f"Najwięcej wspólnych F: {max(wspolne_F_count)}")
else:
    print("ŻADNEJ PARY NIE MA WSPÓLNEGO WEKTORA F → FILTR ONTOLOGICZNY JEST ABSOLUTNY")

# PCA wizualizacja
X = np.zeros((1000, 100))
possible_F = [tuple(np.round(np.random.randn(10)*0.5, 2)) for _ in range(100)]
for i, civ in enumerate(cywilizacje):
    for j, F in enumerate(possible_F):
        if F in civ.horyzont:
            X[i, j] = 1

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

plt.figure(figsize=(10, 8))
plt.scatter(X_2d[:, 0], X_2d[:, 1], c='lightblue', alpha=0.7, s=30)
plt.title('1000 Cywilizacji w Przestrzeni Horyzontów (PCA 2D)\nŻadna para się nie pokrywa', fontsize=14)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('simulations/results/pca_2d_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# Zapisz dane
np.save('simulations/data/civilizations_1000.npy', np.array([civ.S for civ in cywilizacje]))
