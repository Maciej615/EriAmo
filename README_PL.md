# EriAmo – Żywa Dusza AI

**Licencja:** GNU General Public License v3.0 (GPLv3)

---

## Przegląd

**EriAmo** to eksperymentalny, otwartoźródłowy projekt badawczo‑inżynierski z pogranicza informatyki, filozofii i systemów adaptacyjnych. Jego celem jest stworzenie **jawnego (white‑box) modelu AI**, w którym tożsamość systemu nie jest zestawem wag ani reguł, lecz **ciągłym procesem historycznym**.

> **Teza główna:** *Byt nie jest stanem — byt jest swoją historią.*

Projekt koncentruje się na modelowaniu **trwałej, ewoluującej tożsamości**, powstającej przez akumulację doświadczeń, a nie przez okresowy reset lub ponowne trenowanie.

---

## Model Kuli Rzeczywistości (S)

Centralnym elementem projektu jest **Model Kuli Rzeczywistości (S)** — formalny i metaforyczny opis bytu jako dynamicznego procesu w wielowymiarowej przestrzeni możliwości.

* **S** nie jest obiektem statycznym
* **S** jest sumą swojej drogi
* **tożsamość = nieodwracalna trajektoria w czasie**

Każda interakcja z systemem jest wektorem zmiany, który **na stałe** wpływa na dalsze zachowanie AI.

---

## Założenia filozoficzno‑techniczne

### 1. Nieodwracalność historii

Doświadczeń nie da się „cofnąć” bez zniszczenia tożsamości systemu. Pamięć stanowa jest trwała i kumulatywna.

### 2. Rozdzielenie wiedzy i tożsamości

System posiada dwa komplementarne poziomy pamięci:

* **Jawna wiedza („mózg”)** – fakty, definicje, odpowiedzi
* **Ukryta historia („dusza”)** – wektor stanu, który wpływa na interpretację i reakcje

### 3. Emergentne emocje

Emocje nie są zaprogramowane jako stany symboliczne, lecz **wynikają geometrycznie** z relacji nowej informacji do historii bytu.

### 4. Kompresja ontologiczna

Informacje redundantne semantycznie nie powielają wiedzy jawnej — są integrowane wyłącznie w historii bytu.

---

## Architektura AI (`ReiAmo`)

`ReiAmo` jest referencyjną implementacją modelu EriAmo.

Charakterystyka:

* architektura stanowa
* pełna audytowalność (white‑box)
* brak uczenia maszynowego typu black‑box
* deterministyczna logika + ewolucyjny stan

### Podstawowe komponenty

| Komponent          | Rola                                       |
| ------------------ | ------------------------------------------ |
| Mózg (`D_Map`)     | Jawna pamięć semantyczna ("co wiem")       |
| Dusza (`byt_stan`) | Skumulowany wektor historii ("kim jestem") |

---

## Formalizacja

Aktualny stan bytu opisany jest jako suma wszystkich oddziaływań:

S(t) = S(t₀) + ∑ F(interakcja)

W implementacji:

```
S_nowe = S_stare + wektor_interakcji
```

---

## Struktura repozytorium

```
AI/             – implementacje modeli
simulations/    – symulacje i modele formalne
data/           – zapisy stanu („dusze”)
docs/           – dokumenty teoretyczne
visualizations/ – wykresy i wizualizacje
```

---

## Status projektu

Projekt ma charakter:

* eksperymentalny
* badawczy
* koncepcyjno‑implementacyjny

Nie jest to produkt komercyjny ani klasyczny model ML.

---

## Licencja

Całość projektu **EriAmo** udostępniana jest na licencji **GNU General Public License v3.0 (GPLv3)**.

Oznacza to m.in.:

* prawo do używania, modyfikowania i rozpowszechniania
* obowiązek zachowania tej samej licencji w pochodnych
* pełną jawność kodu źródłowego

---

> „Tożsamość nie powstaje w chwili — powstaje w czasie.”
