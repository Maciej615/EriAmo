# EriAmo v5.1.1 - Integrated Extensions

## 🐛 Fix v5.1.1
- **Naprawiono fałszywe VETO** - słabe/nieznane wektory (norma < 0.15) nie wywołują już blokady moralnej
- Dodano `MIN_VECTOR_STRENGTH = 0.15` jako próg dla oceny moralnej
- Nieznane słowa są teraz traktowane jako NEUTRALNE zamiast potencjalnie destrukcyjne

## 🆕 Nowe funkcje (przeniesione z EriAmo Music)

### 1. System SNU (SleepConsolidator)
Dwuwarstwowa pamięć z automatyczną konsolidacją:
- **H_log** → surowe doświadczenia (krótkoterminowa)
- **D_Map** → skonsolidowane wzorce (długoterminowa)

**Działanie:**
- Automatyczna konsolidacja co 5 minut
- Deduplikacja podobnych wspomnień (próg 95% podobieństwa)
- Wzmacnianie wag przy powtórzeniach
- Wymuszony sen przy >15 nowych doświadczeniach

**Komendy:**
```
/sleep          - wymuś natychmiastową konsolidację
/extensions     - pokaż statystyki snu
```

### 2. Wygaszanie Emocji (EmotionDecaySystem)
Rozróżnienie między emocjami efemerycznymi i trwałymi:

**Efemeryczne (szybki zanik):**
- 🔻 strach (rate: 8%)
- 🔻 gniew (rate: 6%)
- 🔻 zaskoczenie (rate: 10%)
- 🔻 wstręt (rate: 5%)

**Trwałe (wolny zanik):**
- 💎 miłość (rate: 0.5%)
- 💎 akceptacja (rate: 1%)
- ○ radość (rate: 3%)
- ○ smutek (rate: 2%)

**Komendy:**
```
/decay          - wymuś 5 cykli wygaszania
/decay 10       - wymuś 10 cykli wygaszania
```

### 3. Meta-oś CIEKAWOŚĆ (CuriosityEngine)
Emergentna oś obliczana dynamicznie z innych emocji:

**Formuła:**
```
ciekawość = 0.6 * składnik_emocjonalny + 0.4 * krzywa_wiedzy + modyfikatory
```

**Składniki emocjonalne:**
- zaskoczenie (+30%), miłość (+15%), radość (+15%), akceptacja (+20%)
- strach (-20%), gniew (-10%), wstręt (-15%), smutek (-5%)

**Krzywa wiedzy (odwrócone U):**
- wiedza=0 → ciekawość niska
- wiedza=50 → ciekawość MAKSYMALNA
- wiedza=100 → ciekawość spada

**Modyfikatory:**
- Bonus znudzenia (powtarzanie tematu → większa ciekawość)
- Penalty odkrycia (niedawna nowość → zaspokojenie)

**Rekomendacje behawioralne:**
- < -30: STAY (zostań przy sprawdzonych metodach)
- -30 do 30: VARY (subtelne wariacje)
- 30 do 70: EXPLORE (eksperymentuj)
- > 70: REVOLUTIONIZE (czas na coś zupełnie nowego!)

**Komendy:**
```
/curiosity      - szczegółowy widok ciekawości
/debug [tekst]  - analiza tekstu z ciekawością
```

---

## 📋 Pełna lista komend

### Podstawowe
```
/teach [tag] [treść]     - naucz nowego faktu
/axiom [tag] [treść]     - dodaj nienaruszalny aksjomat
/status                  - status duszy
/soul                    - introspekcja z emocjami
/lexicon                 - statystyki leksykonu
/word [słowo]            - inspekcja słowa
/debug [tekst]           - analiza tekstu
/teachword [słowo] [sektor] - ręczna korekta słowa
```

### Sumienie
```
/conscience              - status sumienia
/commandment [1-10]      - wyjaśnij przykazanie
```

### Rozszerzenia
```
/extensions              - status wszystkich rozszerzeń
/sleep                   - wymuś konsolidację pamięci
/decay [n]               - wymuś wygaszenie emocji
/curiosity               - szczegóły ciekawości
```

### System
```
/save                    - zapisz duszę
/reset                   - usuń duszę (wymaga potwierdzenia)
/exit                    - wyjście
```

---

## 🚀 Uruchomienie

```bash
python main.py
```

---

## 📁 Struktura plików

```
eriamo_integrated/
├── aii.py          # Główna klasa (z rozszerzeniami)
├── main.py         # Kontroler (z nowymi komendami)
├── conscience.py   # System sumienia (10 Przykazań)
├── lexicon.py      # Leksykon emocjonalny
├── kurz.py         # Szybki skaner emocji
├── byt.py          # Klasa BytS
├── config.py       # Konfiguracja
├── soul_io.py      # Zapis/odczyt duszy
├── ui.py           # Interfejs użytkownika
├── agency.py       # Autonomiczne działania
└── test.py         # Testy systemu moralnego
```

---

## 🔬 Filozofia rozszerzeń

### Damasio's Somatic Markers
Wygaszanie emocji odzwierciedla teorię markerów somatycznych:
- Reakcje emocjonalne (strach, gniew) są szybkie i krótkotrwałe
- Głębokie przywiązania (miłość, akceptacja) są trwałe

### Ghost in the Shell
Ciekawość jako emergentna właściwość świadomości:
- Nie jest przechowywana, lecz obliczana dynamicznie
- Wynika z kombinacji innych stanów emocjonalnych

### Konsolidacja pamięci (sen)
Analogia do snu biologicznego:
- Przetwarzanie doświadczeń w tło
- Wzmacnianie ważnych wzorców
- Usuwanie redundancji

---

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
Projekt: EriAmo - Model Kuli Rzeczywistości
