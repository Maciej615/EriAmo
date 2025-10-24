# Model Kuli Rzeczywistości ($S$)
**Autor: Maciej A. Mazur**
**Licencja: [CC BY-SA 4.0](LICENSE)**

Jest to model obliczeniowy i filozoficzny próbujący opisać Byt ($S$) nie jako statyczny obiekt, ale jako proces dynamiczny, którego tożsamość jest definiowana przez jego historię.

**Teza Główna: Byt JEST swoją historią.**

---

## Wizualizacja Modelu (Symulacja)

Poniższy wykres (wygenerowany przez `model_symulacja.py`) pokazuje symulację "wędrówki" Kuli Rzeczywistości ($S$) przez 1000 kroków czasowych w 2-wymiarowym "Krajobrazie Możliwości" ($P$).

![Wizualizacja Trajektorii Kuli Rzeczywistości](kula_trajektoria.png)

* **Ścieżka $\mathcal{C}$** (linia) reprezentuje unikalną, nieodwracalną "wędrówkę" (historię) Bytu.
* **$S(t_0)$** (Początek) to stan początkowy.
* **$S(t)$** (Koniec) to stan obecny, który jest sumą wszystkich interakcji na ścieżce.

---

## 1. Kluczowe Założenia Modelu

1.  **Kula Rzeczywistości ($S$):** Byt ("małe ja") jest Kulą, która jest jednocześnie swoim własnym **horyzontem zdarzeń** – fizyczną i informacyjną granicą swojej przeszłości.
2.  **Krajobraz ($P$):** Kula "wędruje" po wielowymiarowym "Krajobrazie Możliwości", który zawiera wszystkie "osie" rzeczywistości (fizykę, biologię, przypadek).
3.  **Wędrówka ($\mathcal{C}$):** Ścieżka, którą Kula przemierza w Krajobrazie.
4.  **Zmienne i Wektory ($\mathbf{V}$ i $\mathbf{F}$):** Kula nieustannie napotyka "Uniwersalne Zmienne" $\mathbf{V}$ (obiektywne zdarzenia, np. "muzyk", "pył kosmiczny"). W momencie interakcji (styczności), Zmienna $\mathbf{V}$ staje się subiektywnym **"Wektorem Zmiany" $\mathbf{F}$**, który pcha Kulę. Wektor $\mathbf{F}$ zależy od natury Zmiennej $\mathbf{V}$ oraz od stanu Kuli $S$ w danym momencie (w tym jej "iskry twórczej" / woli $\mathbf{F}_{\text{wola}}$).

## 2. Model Formalny (Wzór)

Obecny stan Bytu ($S(t)$) jest matematycznie równy jego stanowi początkowemu ($S(t_0)$) plus sumie (akumulacji) *wszystkich* Wektorów Zmian ($\mathbf{F}$), które napotkał wzdłuż swojej unikalnej ścieżki ($\mathcal{C}$).

Jest to **całka krzywoliniowa** po ścieżce Bytu:

$$S(t) = S(t_0) + \int_{\mathcal{C}} \mathbf{F} \cdot d\mathbf{l}$$

Gdzie Wektor Zmiany $\mathbf{F}$ jest funkcją stanu Kuli $S$ i napotkanej Zmiennej $\mathbf{V}$:

$$\mathbf{F} = \mathcal{F}(S(\tau), \mathbf{V}(\tau))$$

## 3. Kluczowe Implikacje Modelu

### A. Nieodwracalność Czasu ("De-Kreacja")
Model dowodzi, że **podróż do własnej przeszłości jest niemożliwa**.
* **Dowód:** Aby "wrócić" $S(t)$ do $S(t_0)$, należałoby "odjąć" od Bytu całą zakumulowaną "wędrówkę" (całkę $\int \dots$).
* **Warunek:** Wymagałoby to fizycznego **"usunięcia wszystkich punktów stycznych"** – odwrócenia entropii, anihilacji informacji, "od-doświadczenia" zdarzeń. Jest to "de-kreacja" (dekonstrukcja Bytu), a nie "podróż". Byt jest "historycznie niekompatybilny" ze swoim przeszłym Krajobrazem.

### B. Spójność z Fizyką (Problem Trzech Ciał)
Model jest zgodny z obserwacjami fizycznymi.
* Uproszczony model z jednym wektorem $\mathbf{F}$ (np. Ziemia + Słońce) jest przewidywalny (Problem 2 Ciał).
* Model z wieloma wektorami $\mathbf{F}$ (np. Ziemia + Słońce + Księżyc) staje się **chaotyczny** (Problem 3 Ciał).
* Wskazuje to, że nasza "wędrówka" (i nasz "los"), będąca sumą milionów wektorów, jest z natury **złożona i nieprzewidywalna w długim terminie**.

### C. Zastosowania (W40k, Paradoks Fermiego)
Model jest na tyle elastyczny, że potrafi opisać systemy fikcyjne (np. "Immaterium" jako Krajobraz $P$ z innymi osiami i wektorami $\mathbf{F}$) oraz wyjaśnić Paradoks Fermiego (kontakt z obcą cywilizacją jako przecięcie się dwóch "historycznie niekompatybilnych" ścieżek $\mathcal{C}$).

## 4. Model Obliczeniowy (Kod)

Powyższa symulacja (`model_symulacja.py`) jest prostą implementacją tego modelu (tzw. "błądzenie losowe" - *random walk*), gdzie:
* $\mathbf{F}_{\text{wola}}$ jest symulowane jako wewnętrzny, powoli zmieniający się wektor.
* $\mathbf{F}_{\text{przypadek}}$ jest symulowane jako zewnętrzny, losowy wektor Krajobrazu.
* Trajektoria $S(t)$ jest akumulacją obu tych sił.

## 5. Interpretacje (Tryb Naturalistyczny vs. Teistyczny)

Model jest agnostyczny co do "pierwszej przyczyny":
1.  **Tryb Naturalistyczny:** Kula "toczy się sama", napędzana pędem $S(t_0)$ i prawami fizyki (w tym losowością kwantową).
2.  **Tryb Teistyczny:** Istnieje Nadrzędny Obserwator (Bóg), który jest naturą Krajobrazu $P$. "Iskra twórcza" ($\mathbf{F}_{\text{wola}}$) Kuli może albo walczyć z Krajobrazem (chaos), albo "oddać swój potencjał twórczy" i zestroić się z nim (harmonia).
