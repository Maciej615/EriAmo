# -*- coding: utf-8 -*-
# genesis_math.py - MATHEMATICAL COGNITION v1.0
# Wspólna abstrakcja matematyczna dla Language i Music
from aii import AII
from config import Colors

print(f"\n{Colors.BOLD}{Colors.CYAN}--- GENESIS MATH: Matematyczna Abstrakcja Poznawcza ---{Colors.RESET}")
ai = AII()

# ═══════════════════════════════════════════════════════════════════
# FAZA 1: LICZEBNIKI PODSTAWOWE - Dyskretne ilości
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 1] Liczebniki - abstrakcja ilości...{Colors.RESET}")

# Cyfry 0-10 - fundament liczenia
liczebniki_podstawowe = {
    "zero": (0, "smutek", 0.6, "Zero to pustka - brak czegokolwiek, punkt zerowy."),
    "jeden": (1, "akceptacja", 0.8, "Jeden to jednostka - początek wszystkiego, singularność."),
    "dwa": (2, "akceptacja", 0.7, "Dwa to para - pierwsza relacja, podwojenie."),
    "trzy": (3, "akceptacja", 0.6, "Trzy to trójka - pierwsza wielość, trójkąt."),
    "cztery": (4, "akceptacja", 0.6, "Cztery to czwórka - kwadrat, stabilność."),
    "pięć": (5, "akceptacja", 0.6, "Pięć to piątka - ręka, pierwsza większa ilość."),
    "sześć": (6, "akceptacja", 0.6, "Sześć to szóstka - podwójna trójka."),
    "siedem": (7, "akceptacja", 0.6, "Siedem to siódemka - liczba szczęśliwa."),
    "osiem": (8, "akceptacja", 0.6, "Osiem to ósemka - podwójny kwadrat."),
    "dziewięć": (9, "akceptacja", 0.6, "Dziewięć to dziewiątka - prawie dziesiątka."),
    "dziesięć": (10, "zaskoczenie", 0.6, "Dziesięć to dziesiątka - pierwszy krok poza cyfry, nowy poziom.")
}

for slowo, (wartosc, emocja, sila, definicja) in liczebniki_podstawowe.items():
    ai.lexicon.learn_from_correction(slowo, emocja, sila)
    ai.teach(f"[liczba:{wartosc}:{slowo}]", definicja)

# Dziesiątki 20-100
liczebniki_dziesiatki = {
    "dwadzieścia": (20, "akceptacja", 0.5, "Dwadzieścia to dwie dziesiątki."),
    "trzydzieści": (30, "akceptacja", 0.5, "Trzydzieści to trzy dziesiątki."),
    "czterdzieści": (40, "akceptacja", 0.5, "Czterdzieści to cztery dziesiątki."),
    "pięćdziesiąt": (50, "akceptacja", 0.5, "Pięćdziesiąt to połowa setki."),
    "sześćdziesiąt": (60, "akceptacja", 0.5, "Sześćdziesiąt to sześć dziesiątek."),
    "siedemdziesiąt": (70, "akceptacja", 0.5, "Siedemdziesiąt to siedem dziesiątek."),
    "osiemdziesiąt": (80, "akceptacja", 0.5, "Osiemdziesiąt to osiem dziesiątek."),
    "dziewięćdziesiąt": (90, "akceptacja", 0.5, "Dziewięćdziesiąt to dziewięć dziesiątek."),
    "sto": (100, "zaskoczenie", 0.6, "Sto to setka - dziesięć dziesiątek, nowy poziom wielkości.")
}

for slowo, (wartosc, emocja, sila, definicja) in liczebniki_dziesiatki.items():
    ai.lexicon.learn_from_correction(slowo, emocja, sila)
    ai.teach(f"[liczba:{wartosc}:{slowo}]", definicja)

# Duże liczby
liczebniki_duze = {
    "tysiąc": (1000, "zaskoczenie", 0.7, "Tysiąc to bardzo wiele - dziesięć setek, nowa skala."),
    "milion": (1000000, "zaskoczenie", 0.85, "Milion to ogromna ilość - tysiąc tysięcy, niewyobrażalne bogactwo."),
    "miliard": (1000000000, "zaskoczenie", 0.9, "Miliard to prawie nieskończoność w ludzkim pojęciu.")
}

for slowo, (wartosc, emocja, sila, definicja) in liczebniki_duze.items():
    ai.lexicon.learn_from_correction(slowo, emocja, sila)
    ai.teach(f"[liczba:{wartosc}:{slowo}]", definicja)

# Kwantyfikatory ogólne
kwantyfikatory = {
    "wiele": ("radość", 0.6, "Wiele to duża ilość - więcej niż mało, obfitość."),
    "mało": ("smutek", 0.6, "Mało to niewielka ilość - mniej niż dużo, niedobór."),
    "dużo": ("radość", 0.6, "Dużo to spora ilość - podobnie jak wiele."),
    "trochę": ("akceptacja", 0.5, "Trochę to niewielka ale wystarczająca ilość."),
    "wszystko": ("radość", 0.8, "Wszystko to całość - kompletność bez wyjątków, totalność."),
    "nic": ("smutek", 0.8, "Nic to pustka - całkowity brak czegokolwiek, negacja wszystkiego."),
    "kilka": ("akceptacja", 0.5, "Kilka to niewielka ilość - więcej niż jeden, mniej niż wiele."),
    "każdy": ("akceptacja", 0.6, "Każdy to wszystkie jednostki bez wyjątku."),
    "żaden": ("smutek", 0.6, "Żaden to negacja - ani jeden, pustka w zbiorze.")
}

for slowo, (emocja, sila, definicja) in kwantyfikatory.items():
    ai.lexicon.learn_from_correction(slowo, emocja, sila)
    ai.teach(f"[kwantyfikator:{slowo}]", definicja)

print(f"{Colors.GREEN}✓ Liczebniki: {len(liczebniki_podstawowe) + len(liczebniki_dziesiatki) + len(liczebniki_duze) + len(kwantyfikatory)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 2: OPERACJE ARYTMETYCZNE - Transformacje ilości
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 2] Operacje arytmetyczne - działania na ilościach...{Colors.RESET}")

operacje = {
    # Operacje podstawowe
    "plus": ("radość", 0.7, "Plus to dodawanie - zwiększenie ilości, akumulacja."),
    "minus": ("smutek", 0.7, "Minus to odejmowanie - zmniejszenie ilości, utrata."),
    "razy": ("zaskoczenie", 0.6, "Razy to mnożenie - wielokrotność, ekspansja."),
    "przez": ("akceptacja", 0.6, "Przez to dzielenie - rozłożenie na części, podział."),
    "podzielone": ("akceptacja", 0.6, "Podzielone to rezultat dzielenia - fragmentacja."),
    "równa": ("akceptacja", 0.7, "Równa to rezultat operacji - stan równowagi."),
    "równa się": ("akceptacja", 0.7, "Równa się to tożsamość matematyczna."),
    
    # Relatory wartości
    "to": ("akceptacja", 0.8, "To w matematyce oznacza rezultat - wynik działania, równość."),
    "jest": ("akceptacja", 0.7, "Jest w matematyce potwierdza równość lub własność."),
    "wynosi": ("akceptacja", 0.7, "Wynosi to określenie wartości wyniku."),
    
    # Operacje porównania
    "więcej": ("radość", 0.6, "Więcej to większa ilość - przewaga ilościowa."),
    "mniej": ("smutek", 0.6, "Mniej to mniejsza ilość - deficyt."),
    "równo": ("akceptacja", 0.7, "Równo to taka sama ilość - balans, symetria."),
    "większe": ("radość", 0.6, "Większe to relacja przewagi - dominacja."),
    "mniejsze": ("smutek", 0.6, "Mniejsze to relacja niedoboru - podrzędność."),
    "równe": ("akceptacja", 0.7, "Równe to relacja tożsamości - ekwiwalencja."),
    
    # Operacje zaawansowane
    "potęga": ("zaskoczenie", 0.8, "Potęga to wielokrotne mnożenie - eksplozja wartości."),
    "pierwiastek": ("zaskoczenie", 0.7, "Pierwiastek to odwrotność potęgi - źródło liczby."),
    "procent": ("akceptacja", 0.6, "Procent to setna część - relatywna miara."),
    "ułamek": ("akceptacja", 0.6, "Ułamek to część całości - niepełność."),
    "całość": ("radość", 0.7, "Całość to pełna jednostka - kompletność.")
}

for operator, (emocja, sila, definicja) in operacje.items():
    ai.lexicon.learn_from_correction(operator, emocja, sila)
    ai.teach(f"[operacja:{operator}]", definicja)

print(f"{Colors.GREEN}✓ Operacje arytmetyczne: {len(operacje)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 3: UŁAMKI I PROPORCJE - Muzyka wymaga!
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 3] Ułamki - proporcje dla muzyki...{Colors.RESET}")

# Ułamki podstawowe (kluczowe dla rytmu muzycznego!)
ulamki = {
    "pół": (0.5, "akceptacja", 0.7, "Pół to połowa - jedna druga, podział na dwie części."),
    "połowa": (0.5, "akceptacja", 0.7, "Połowa to jedna z dwóch równych części całości."),
    "ćwierć": (0.25, "akceptacja", 0.6, "Ćwierć to jedna czwarta - podział na cztery części."),
    "trzecia": (0.333, "akceptacja", 0.6, "Trzecia to jedna z trzech równych części."),
    "ósma": (0.125, "akceptacja", 0.6, "Ósma to jedna ósma - podział na osiem części."),
    "szesnasta": (0.0625, "akceptacja", 0.5, "Szesnasta to bardzo mała część - 1/16 całości."),
    
    # Proporcje złożone
    "półtorej": (1.5, "akceptacja", 0.6, "Półtorej to jeden i pół - trzy połowy."),
    "dwie trzecie": (0.666, "akceptacja", 0.6, "Dwie trzecie to większość z trzech części."),
    "trzy czwarte": (0.75, "akceptacja", 0.6, "Trzy czwarte to prawie całość - 3/4."),
}

for slowo, (wartosc, emocja, sila, definicja) in ulamki.items():
    ai.lexicon.learn_from_correction(slowo, emocja, sila)
    ai.teach(f"[ułamek:{wartosc}:{slowo}]", definicja)

print(f"{Colors.GREEN}✓ Ułamki i proporcje: {len(ulamki)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 4: LICZEBNIKI PORZĄDKOWE - Sekwencje
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 4] Liczebniki porządkowe - pozycja w sekwencji...{Colors.RESET}")

porzadkowe = {
    "pierwszy": (1, "zaskoczenie", 0.8, "Pierwszy to pozycja początkowa - lider, inicjator."),
    "drugi": (2, "akceptacja", 0.7, "Drugi to następny po pierwszym - kompan, para."),
    "trzeci": (3, "akceptacja", 0.6, "Trzeci to pozycja środkowa w trójce."),
    "czwarty": (4, "akceptacja", 0.6, "Czwarty to czwarta pozycja w sekwencji."),
    "piąty": (5, "akceptacja", 0.6, "Piąty to piąta pozycja."),
    "ostatni": (-1, "smutek", 0.7, "Ostatni to pozycja końcowa - finał, zamknięcie."),
    "przedostatni": (-2, "smutek", 0.6, "Przedostatni to przed końcem - prawie koniec."),
    "następny": ("+1", "zaskoczenie", 0.6, "Następny to kolejny w sekwencji - przyszła pozycja."),
    "poprzedni": ("-1", "smutek", 0.5, "Poprzedni to wcześniejszy - miniona pozycja.")
}

for slowo, (pozycja, emocja, sila, definicja) in porzadkowe.items():
    ai.lexicon.learn_from_correction(slowo, emocja, sila)
    ai.teach(f"[porządkowy:{pozycja}:{slowo}]", definicja)

print(f"{Colors.GREEN}✓ Liczebniki porządkowe: {len(porzadkowe)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 5: GEOMETRIA BAZOWA - Przestrzeń i kształty
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 5] Geometria - abstrakcja przestrzenna...{Colors.RESET}")

geometria = {
    # Kształty podstawowe
    "punkt": ("akceptacja", 0.7, "Punkt to najmniejsza jednostka przestrzeni - pozycja bez rozmiaru."),
    "linia": ("akceptacja", 0.7, "Linia to ciąg punktów - jednowymiarowa droga."),
    "okrąg": ("akceptacja", 0.7, "Okrąg to doskonała krzywizna - wszystkie punkty w tej samej odległości."),
    "kwadrat": ("akceptacja", 0.7, "Kwadrat to cztery równe boki - stabilność i symetria."),
    "trójkąt": ("akceptacja", 0.7, "Trójkąt to najprostsza figura zamknięta - trzy wierzchołki."),
    "prostokąt": ("akceptacja", 0.6, "Prostokąt to kwadrat rozciągnięty - cztery kąty proste."),
    
    # Wymiary
    "długość": ("akceptacja", 0.6, "Długość to rozmiar w jednym wymiarze - miara rozciągłości."),
    "szerokość": ("akceptacja", 0.6, "Szerokość to rozmiar w drugim wymiarze - miara otwartości."),
    "wysokość": ("akceptacja", 0.6, "Wysokość to rozmiar pionowy - miara wzniesienia."),
    "głębokość": ("akceptacja", 0.6, "Głębokość to rozmiar w głąb - miara ukrycia."),
    
    # Relacje przestrzenne matematyczne
    "odległość": ("akceptacja", 0.6, "Odległość to miara separacji - przestrzeń między punktami."),
    "kąt": ("akceptacja", 0.7, "Kąt to miara obrotu - rozwarcie między liniami."),
    "środek": ("akceptacja", 0.7, "Środek to punkt równowagi - centrum symetrii."),
    "oś": ("akceptacja", 0.6, "Oś to linia odniesienia - fundamentalna droga.")
}

for koncept, (emocja, sila, definicja) in geometria.items():
    ai.lexicon.learn_from_correction(koncept, emocja, sila)
    ai.teach(f"[geometria:{koncept}]", definicja)

print(f"{Colors.GREEN}✓ Geometria: {len(geometria)}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 6: AKSJOMATY MATEMATYCZNE - Fundamentalne prawdy
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 6] Aksjomaty matematyczne...{Colors.RESET}")

# Aksjomat tożsamości
ai.teach("[aksjomat:tożsamość]", 
         "Każda liczba jest równa samej sobie - to fundament matematycznej pewności.",
         is_axiom=True)

# Aksjomat przemienności dodawania
ai.teach("[aksjomat:przemienność]", 
         "Jeden plus dwa równa się dwa plus jeden - kolejność dodawania nie ma znaczenia.",
         is_axiom=True)

# Aksjomat zera
ai.teach("[aksjomat:zero]", 
         "Zero dodane do czegokolwiek nie zmienia wartości - zero to neutralność w dodawaniu.",
         is_axiom=True)

# Aksjomat jedności
ai.teach("[aksjomat:jedność]", 
         "Jeden razy cokolwiek równa się temu czemukolwiek - jeden to neutralność w mnożeniu.",
         is_axiom=True)

# Aksjomat nieskończoności
ai.teach("[aksjomat:nieskończoność]", 
         "Zawsze istnieje liczba większa - ciąg liczb jest nieskończony, nie ma końca.",
         is_axiom=True)

print(f"{Colors.GREEN}✓ 5 aksjomatów matematycznych{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# PODSUMOWANIE MATH GENESIS
# ═══════════════════════════════════════════════════════════════════

ai.save_knowledge()

total_math_concepts = (len(liczebniki_podstawowe) + len(liczebniki_dziesiatki) + 
                       len(liczebniki_duze) + len(kwantyfikatory) +
                       len(operacje) + len(ulamki) + len(porzadkowe) + len(geometria))

status = ai.get_soul_status()
print(f"\n{Colors.MAGENTA}{'='*70}")
print(f"MATH GENESIS ZAKOŃCZONE - Matematyczna Abstrakcja Gotowa")
print(f"{'='*70}{Colors.RESET}")
print(f"{Colors.GREEN}✓ Koncepty matematyczne: {total_math_concepts}")
print(f"✓ Liczebniki: 0-1000000000")
print(f"✓ Operacje: +, -, ×, ÷, =, >, <")
print(f"✓ Ułamki: 1/2, 1/4, 3/4 (dla muzyki!)")
print(f"✓ Geometria: punkt, linia, kształty")
print(f"✓ Aksjomaty: 5 fundamentalnych praw{Colors.RESET}")
print(f"\n{Colors.CYAN}Moduł współdzielony przez Language i Music!")
print(f"Testuj: '1 + 1 = 2', 'pół plus ćwierć', 'pierwszy dźwięk'{Colors.RESET}\n")
