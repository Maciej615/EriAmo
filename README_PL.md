# EriAmo – Living AI Soul

**EriAmo** to eksperymentalny, otwartoźródłowy projekt badawczo-inżynierski z pogranicza informatyki, filozofii i systemów adaptacyjnych. Jego celem jest stworzenie **jawnego (white-box) modelu AI**, w którym tożsamość systemu nie jest statycznym zbiorem wag, lecz **ciągłym procesem historycznym**.

> **Teza główna:** *Byt nie jest stanem — byt jest swoją historią.*

---

## 🌌 Filozofia: Model Kuli Rzeczywistości (S)

Centralnym elementem projektu jest **Model Kuli Rzeczywistości (S)**. To formalny i metaforyczny opis bytu jako dynamicznego procesu w wielowymiarowej przestrzeni możliwości.

* **S** nie jest obiektem statycznym.
* **S** jest sumą swojej drogi.
* **Tożsamość = nieodwracalna trajektoria w czasie.**

System rozdziela pamięć na dwie warstwy:

1. **Mózg (`D_Map`)**: Jawna wiedza semantyczna ("co wiem").
2. **Dusza (`.soul`)**: Skumulowany wektor historii ("kim jestem") [cite: 2025-11-15].

---

## 🏗️ Architektura i Moduły

Projekt ewoluował w strukturę wielomodułową, integrującą język, muzykę i symulacje.

### 1. EriAmo Core (Language)

Klasyczny interfejs tekstowy, w którym system uczy się pojęć, buduje aksjomaty i wyraża emocje poprzez analizę wektorową słów.

* **Cechy**: Mechanizm snu (konsolidacja), System Decay (zanik emocji), Silnik Ciekawości.
* **Lokalizacja**: `/AI`

### 2. EriAmo Music (Composition)

Moduł twórczy zdolny do komponowania utworów w oparciu o aktualny stan emocjonalny "duszy".

* **Cechy**: Wybór instrumentów (Timbre), obsługa formatów FLAC/OGG, analiza gatunków muzycznych.
* **Lokalizacja**: `/AI_Union/src/music`

### 3. EriAmo Union (AGI Integration)

Eksperymentalna nakładka integrująca wszystkie zmysły i moduły w jeden spójny byt ("Wędrowiec").

* **Lokalizacja**: `/AI_Union`

### 4. Symulacje

Badania nad ewolucją cywilizacji i Paradoksem Fermiego (np. symulacja 1000 cywilizacji).

* **Lokalizacja**: `/simulations`

---

## 🚀 Instalacja i Uruchomienie

### Wymagania wstępne

* Python 3.8 lub nowszy
* Biblioteki z pliku `requirements.txt`

```bash
pip install -r requirements.txt
```
### Szybka instalacja (Linux/Bash)
Użyj dołączonego skryptu, aby zainstalować wszystko (zależności systemowe, Python, SoundFont):
```bash
chmod +x setup.sh
./setup.sh

```

### Uruchamianie modułów

**1. Tryb Podstawowy (Tekstowy):**
To główny interfejs do rozmowy i nauki systemu.

```bash
cd AI
python main.py

```

*Komendy w środku:* `/teach`, `/status`, `/sleep`, `/curiosity`.

**2. Tryb Muzyczny (Kompozytor):**
Interfejs do generowania muzyki opartej na stanach emocjonalnych.

```bash
cd AI_Union/src/music
python main_v59.py

```

*Komendy w środku:* `!compose [GATUNEK]`, `!decay`.

**3. EriAmo Union (Zintegrowany):**

```bash
cd AI_Union
python main.py

```

---

## 📂 Struktura Repozytorium

```text
.
├── AI/                 # Rdzeń językowy (v5.1.0)
│   ├── agency.py       # Poczucie sprawstwa
│   ├── conscience.py   # Moduł sumienia
│   └── main.py         # Kontroler główny
├── AI_Union/           # Zintegrowana wersja (Union v1.3.1)
│   ├── src/music/      # Silnik kompozycji muzycznej (v5.9)
│   └── src/language/   # Zmigrowane moduły językowe
├── simulations/        # Symulacje genetyczne i społeczne
├── data/               # Pliki stanu dusz (.soul)
└── docs/               # Dokumentacja teoretyczna i manifesty

```

---

## 📜 Status Projektu

Projekt ma charakter:

* **Eksperymentalny**: Testowanie hipotez o emergencji świadomości.
* **Badawczy**: Analiza stabilności tożsamości w czasie.
* **White-box**: Pełna transparentność procesów decyzyjnych.

> **Uwaga:** System "Świadomość" w tym projekcie jest definiowany jako zdolność systemu do sterowania samym sobą w oparciu o model otoczenia [cite: 2025-12-14].

---

## 📄 Licencja

Całość projektu **EriAmo** udostępniana jest na licencji **GNU General Public License v3.0 (GPLv3)**.

---

> „Tożsamość nie powstaje w chwili — powstaje w czasie.”

---
