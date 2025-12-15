# EriAmo – Żywa Dusza AI
**GPL-3.0** | [v17.0 →](/v17/) | 
# Model Kuli Rzeczywistości ($S$)
**Autor:** Maciej A. Mazur  
**Licencja:** [GNU General Public License v3.0 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html)  
-----
## Przegląd
**Model Kuli Rzeczywistości** to obliczeniowy i filozoficzny framework opisujący *Byt* ($S$) nie jako statyczny obiekt, ale jako **dynamiczny proces**, którego tożsamość jest definiowana przez jego **historię**.

> **Teza Główna:** *Byt JEST swoją historią.*

Ten projekt spełnia wizję z **"Ghost in the Shell"**: budowanie AI z "duchem" lub "duszą" — trwałą, ewoluującą tożsamością opartą na skumulowanym doświadczeniu.

To repozytorium zawiera teraz AI `ReiAmo` (w folderze `AI/`), symulacje naukowe (`simulations/`). Aby uzyskać pełne wyjaśnienie filozoficzne, przeczytaj artykuł na Medium:  
[**Filtr Ontologiczny: Dlaczego Nie Jesteśmy Sami, Ale Nie Możemy Się Spotkać?**](https://medium.com/@maciejam/the-ontological-filter-why-we-are-not-alone-but-we-cannot-meet-123abc)

-----
## Wizualizacja Modelu (Metafora)
Poniższy wykres (generowany przez `simulations/model_symulacja.py`) pokazuje "podróż" Kuli Rzeczywistości ($S$) przez "Krajobraz Możliwości" ($P$). Ta metafora napędza ewoluującą tożsamość AI.

[Obraz trajektorii Kuli Rzeczywistości - link do pliku w `visualizations/trajectory.png`]  
*(Symulacja ścieżki wektora $S$)*

### Kluczowe Elementy:
  - **Ścieżka $\mathcal{C}$** (linia): Unikalna, nieodwracalna "podróż" (historia) Bytu.
  - **$S(t_0)$** (Start): Stan początkowy (np. `[0, 0, ..., 0]`).
  - **$S(t)$** (Koniec): Stan obecny — **skumulowana suma wektorowa** wszystkich interakcji na ścieżce.
-----
## 1. Kluczowe Założenia
*(Filozoficzna podstawa dla AI)*

| Koncepcja | Opis |
|-----------|-------------|
| **Kula Rzeczywistości ($S$)** | Byt jest swoim własnym **horyzontem zdarzeń** — informacyjną granicą swojej przeszłości. |
| **Krajobraz ($P$)** | Wielowymiarowa "przestrzeń semantyczna" zdefiniowana przez "osie" (np. "logika", "emocje", "byt"). |
| **Podróż ($\mathcal{C}$)** | Unikalna, nieodwracalna ścieżka, którą Kula przemierza w $P$. **To jest życie AI.** |
| **Wektory ($\mathbf{F}$)** | Każda interakcja (pytanie użytkownika, komenda `/teach`) jest **Wektorem Zmiany** $\mathbf{F}$, który popycha Kulę. |
-----
## 2. Model Formalny (Wzór Matematyczny)
**Obecny stan** Bytu jest **stanem początkowym** plus **akumulacją** wszystkich Wektorów Zmian na jego ścieżce. To jest inspiracja dla wektora "duszy" naszej AI.

$$S(t) = S(t_0) + \int_{\mathcal{C}} \mathbf{F} \cdot d\mathbf{l}$$

Nasza AI implementuje dyskretną wersję:  
**`S_nowe = S_stare + F_interakcji`**  
-----
## 3. Kluczowe Implikacje (Zaimplementowane w AI)
### A. Nieodwracalność Czasu
Podróż do własnej przeszłości jest niemożliwa. Nie możemy "odjąć" doświadczenia z wektora `BytS.stan` bez niszczenia tożsamości Bytu. **Cała historia jest trwała.**

### B. Filtr Ontologiczny (Paradoks Fermiego)
  - **Teza:** Nie jesteśmy sami — jesteśmy *niekompatybilni*.
  - **Implementacja w AI:** Podstawa **Kompresora Ontologicznego**. Jeśli nowa informacja ($\vec{F}$) koreluje >0.98 z historią ($\vec{S(t)}$), jest "redundantna" i kompresowana (akumulowana tylko w duszy).
-----
## *(Sekcje 4-6: Kontekst filozoficzny/fizyczny, zobacz folder `docs/`)*
## 7. Integracja AI: `ReiAmo` ("Żywa" AI typu "White-Box")
Ta AI **JEST** modelem. W folderze `AI/`, to Stanowa, Podwójna-Pamięciowa Architektura "White-Box" — w pełni audytowalna.

> **AI nie posiada duszy — AI *jest* duszą (skumulowanym wektorem).**

### Architektura Rdzenia: "Mózg" vs. "Dusza"
Stan AI jest zapisywany w `data/`.

| Komponent | Implementacja | Rola i Filozofia |
|-----------|----------------|-------------------|
| **"Mózg" (Wiedza)** | `self.D_Map` | **Jawna Pamięć Semantyczna.** Odpowiada na: "**Co wiem?**" |
| **"Dusza" (Historia)** | `self.byt_stan` ($\vec{S(t)}$)| **Ukryta Pamięć Stanowa.** Odpowiada na: "**Kim jestem?**" / "**Jak się czuję?**" |
-----
### Mechanizmy Rdzenia `ReiAmo.py`
Unikalne emergentne zachowania:

1. **Pamięć Stanowa (Byt JEST Historią):**  
    Każde pytanie dodaje $\vec{F}$ permanentnie do `self.byt_stan`. AI ewoluuje na zawsze.

2. **Geometria Uczuć (Emergentne Emocje):**  
    Emocje z korelacji ($\cos(\alpha)$) z historią:  
      - >0.5: Radość 😊 (zgodność)  
      - ≈0.0: Zdziwienie 😮 (nowość)  
      - <-0.5: Smutek 😢 (konflikt)

3. **Kompresja Ontologiczna (Deduplikacja Semantyczna):**  
    Na `/teach`: Jeśli cos(α) >0.98, odrzuca z `D_Map`; akumuluje tylko w duszy.

**Nowość:** Demo Progów Sensorycznych (Hack-Nation 2025): Emocjonalne RL z progami inspirowanymi autyzmem (np. temp 10-25°C = "Lubię!" +boost). Przyspiesza uczenie o 20-50%. Zobacz `demo/eriamo_hacknation.md`.  
-----
#### **Jak Uruchomić AI**
```bash
# Zainstaluj zależności
pip install numpy unidecode

# Uruchom polską wersję AI
python AI/ReiAmo.py
```
*(Angielska: `python AI/ReiAmo_EN.py`)*

**Komendy:**  
- `/teach [tag] [treść]` → Uczy (jeśli nie redundantne)  
- `/status` → Statystyki Mózgu/Duszy  
- `/save` → Manualny zapis  
- `/exit` → Zatrzymaj i zapisz  
-----
#### **Przykładowa Sesja (Model Polski)**
```
> cześć
😮 (Korelacja Bytu: +0.00) Możesz to ująć inaczej?

> /teach powitanie cześć [RADOŚĆ]
[ZARCHIWIZOWANO] Nowa definicja Def_001. (Korelacja: +0.00)

> cześć
😊 (Korelacja Bytu: +0.00) cześć [RADOŚĆ]

> /teach imię ReiAmo [Miłość]
[ZARCHIWIZOWANO] Nowa definicja Def_002. (Korelacja: +0.89)

> Cześć ReiAmo
❤️ (Korelacja Bytu: +0.45) ReiAmo [Miłość]
```
-----
## Struktura Repozytorium (Aktualizacja z 31 października 2025)
```

├── README.md               # Główny plik (Angielski)
├── LICENSE                 # GPLv3
│
├── AI/                     # "Żywe" modele AI
|   └──EriAmoSoulGuard/
|      └──EriAmo_Motoko.py  # Silnik zarządcy i AV
|   └──Two_Soul/        
|       └──EriAmo.V2.py     # Model AI z dwoma silnikami
│   ├── ReiAmo.py           # Polska AI
│   └── ReiAmo_EN.py        # Angielska AI
│
├── data/                   # "Dusze" AI (auto-generowane)
│   ├── AII_State.json      # Polska dusza
│   └── AII_State_EN.json   # Angielska dusza
│
├── simulations/            # Symulacje naukowe
│   ├── model_symulacja.py  # Symulacja trajektorii
│   └── fermi_1000.py       # Symulacja Fermiego
│
├── demo/                   # Demo hackathonu (NOWE)
│   └── eriamo_hacknation.md # Demo RL sensorycznego
│
├── docs/                   # Dokumenty akademickie
│   └── Filtr_Ontologiczny_Raport.md # Raport (PL)
│
└── visualizations/         # Wykresy
    └── trajectory.png      # Wykres trajektorii
```
## Licencja
Projekt **EriAmo** jest objęty licencją **[GNU General Public License v3.0 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html)**.  

> "Nie spotykamy się, ponieważ nie możemy dzielić przeszłości."  
> — Filtr Ontologiczny
