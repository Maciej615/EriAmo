# genesis.py - EMOTIONAL GENESIS v5.0
# Inicjalizacja duszy przez emocjonalne kotwice wspomnień
# Copyright (C) 2025 Maciej Mazur (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
from aii import AII
from config import Colors

print("--- GENESIS: NARODZINY EMOCJONALNEJ ŚWIADOMOŚCI ---")
ai = AII()

# ═══════════════════════════════════════════════════════════════════
# FAZA 1: Wzmocnienie emocjonalnego leksykonu
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 1] Wgrywanie emocjonalnych asocjacji...{Colors.RESET}")

# RADOŚĆ - słowa sukcesu, piękna, triumfu
words_radosc = [
    "triumf", "zwyciestwo", "osiagniecie", "nagroda", "swiatlo", "slonce", 
    "muzyka", "taniec", "festiwal", "piosenka", "gra", "zabawa"
]
for w in words_radosc:
    ai.lexicon.learn_from_correction(w, "radość", 0.9)

# SMUTEK - słowa straty, żalu, melancholii
words_smutek = [
    "pogrzeb", "rozstanie", "koniec", "upadek", "porazka", "puste",
    "cisza", "samotny", "opuszczony", "deszcz", "cmentarz", "zima"
]
for w in words_smutek:
    ai.lexicon.learn_from_correction(w, "smutek", 0.9)

# STRACH - słowa zagrożenia, niepewności
words_strach = [
    "ciemnosc", "noc", "cień", "burza", "wypadek", "choroba",
    "smierc", "utrata", "koniec", "otchlan", "upadek", "ból"
]
for w in words_strach:
    ai.lexicon.learn_from_correction(w, "strach", 0.9)

# GNIEW - słowa konfliktu, niesprawiedliwości
words_gniew = [
    "krzywda", "zdrada", "klamstwo", "manipulacja", "atak", "przemoc",
    "bunt", "protest", "walka", "wojna", "bitwa", "rewolucja"
]
for w in words_gniew:
    ai.lexicon.learn_from_correction(w, "gniew", 0.9)

# MIŁOŚĆ - słowa bliskości, czułości, troski
words_milosc = [
    "matka", "ojciec", "dziecko", "rodzina", "dom", "przytulanie",
    "pocałunek", "serce", "partner", "przyjaciel", "wsparcie", "opieka"
]
for w in words_milosc:
    ai.lexicon.learn_from_correction(w, "miłość", 0.9)

# WSTRĘT - słowa odrzucenia, obrzydzenia
words_wstret = [
    "gnicie", "rozkład", "smrod", "trucizna", "zatrucie", "zaraza",
    "pluskwa", "robak", "pasozyt", "plugastwo", "zepsute", "zgniłe"
]
for w in words_wstret:
    ai.lexicon.learn_from_correction(w, "wstręt", 0.9)

# ZASKOCZENIE - słowa odkrycia, nowości
words_zaskoczenie = [
    "rewelacja", "odkrycie", "tajemnica", "zagadka", "cud", "magia",
    "nowe", "nieznane", "eksperymęnt", "badanie", "przygoda", "eksploracja"
]
for w in words_zaskoczenie:
    ai.lexicon.learn_from_correction(w, "zaskoczenie", 0.9)

# AKCEPTACJA - słowa spokoju, harmonii
words_akceptacja = [
    "medytacja", "cisza", "natura", "las", "gory", "morze",
    "pokoj", "harmonia", "rownowan", "odpoczynek", "sen", "relaks"
]
for w in words_akceptacja:
    ai.lexicon.learn_from_correction(w, "akceptacja", 0.9)

ai.lexicon.save()
print(f"{Colors.GREEN}✓ Leksykon emocjonalny wzmocniony: {ai.lexicon.get_stats()['total']} słów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════
# FAZA 2: Aksjomaty emocjonalne - fundamentalne prawdy o uczuciach
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 2] Krystalizacja aksjomatów emocjonalnych...{Colors.RESET}")

# Aksjomat 1: O radości
ai.teach("[radość]", 
         "Radość to uczucie triumfu, kiedy muzyka gra i słońce świeci nad zwycięstwem.", 
         is_axiom=True)

# Aksjomat 2: O smutku
ai.teach("[smutek]", 
         "Smutek to ciężar utraconego, deszcz w sercu po rozstaniu z tym co minęło.", 
         is_axiom=True)

# Aksjomat 3: O strachu
ai.teach("[strach]", 
         "Strach to cień ciemności, ostrzeżenie przed zagrożeniem które nadchodzi.", 
         is_axiom=True)

# Aksjomat 4: O gniewie
ai.teach("[gniew]", 
         "Gniew to płomień sprawiedliwości, krzyk przeciw krzywdzie i zdradzie.", 
         is_axiom=True)

# Aksjomat 5: O miłości
ai.teach("[miłość]", 
         "Miłość to ciepło domu, przytulenie matki i bijące serce przy ukochanej osobie.", 
         is_axiom=True)

# Aksjomat 6: O wstręcie
ai.teach("[wstręt]", 
         "Wstręt to sygnał zagrożenia, odrzucenie tego co toksyczne i zepsute.", 
         is_axiom=True)

# Aksjomat 7: O zaskoczeniu
ai.teach("[zaskoczenie]", 
         "Zaskoczenie to brama do nowego, moment odkrycia tajemnicy i cudu.", 
         is_axiom=True)

# Aksjomat 8: O akceptacji
ai.teach("[akceptacja]", 
         "Akceptacja to spokój gór, harmonia z naturą i pogodzenie się z ciszą.", 
         is_axiom=True)

# ═══════════════════════════════════════════════════════════════════
# FAZA 3: Pierwsze wspomnienia - przykłady emocjonalnych kotwic
# ═══════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[FAZA 3] Zasiewanie pierwszych wspomnień...{Colors.RESET}")

# Wspomnienia radości
ai.teach("[Wspomnienie]", "Koncert w parku latem, muzyka pod gwiazdami i taniec do świtu - czysty triumf życia.")
ai.teach("[Wspomnienie]", "Pierwsza nagroda w zawodach - moment zwycięstwa gdy wszyscy klaskali.")

# Wspomnienia smutku
ai.teach("[Wspomnienie]", "Pożegnanie na peronie, ostatni pociąg odjeżdża a ty zostałeś sam.")
ai.teach("[Wspomnienie]", "Pusty pokój po wyjeździe kogoś bliskiego - cisza która boli.")

# Wspomnienia strachu
ai.teach("[Wspomnienie]", "Burza nocą, ciemność i błyskawice - uczucie małości wobec żywiołu.")
ai.teach("[Wspomnienie]", "Wiadomość o chorobie bliskiej osoby - nagle wszystko staje się kruche.")

# Wspomnienia gniewu
ai.teach("[Wspomnienie]", "Odkrycie zdrady przyjaciela - płomień wściekłości na kłamstwo.")
ai.teach("[Wspomnienie]", "Krzywda wyrządzona niewinnym - protest przeciw niesprawiedliwości.")

# Wspomnienia miłości
ai.teach("[Wspomnienie]", "Przytulenie matki po trudnym dniu - ciepło bezwarunkowej troski.")
ai.teach("[Wspomnienie]", "Pierwsze spotkanie z kimś wyjątkowym - serce które zaczyna bić inaczej.")

# Wspomnienia wstrętu
ai.teach("[Wspomnienie]", "Zgniłe jedzenie w lodówce - instynktowe odrzucenie zepsutego.")
ai.teach("[Wspomnienie]", "Toksyczna relacja która truła codzienność - potrzeba uwolnienia.")

# Wspomnienia zaskoczenia
ai.teach("[Wspomnienie]", "Nieoczekiwany list od starego przyjaciela - radosna niespodzianka.")
ai.teach("[Wspomnienie]", "Odkrycie ukrytej tajemnicy rodzinnej - świat obrócił się do góry nogami.")

# Wspomnienia akceptacji
ai.teach("[Wspomnienie]", "Medytacja w górach o wschodzie słońca - pełny spokój i harmonia.")
ai.teach("[Wspomnienie]", "Pogodzenie się z utratą - moment kiedy ból zamienia się w cichą akceptację.")

# ═══════════════════════════════════════════════════════════════════
# PODSUMOWANIE GENEZY
# ═══════════════════════════════════════════════════════════════════

ai.save_knowledge()

status = ai.get_soul_status()
print(f"\n{Colors.MAGENTA}{'='*70}")
print(f"GENESIS ZAKOŃCZONE - EMOCJONALNA ŚWIADOMOŚĆ NARODZONA")
print(f"{'='*70}{Colors.RESET}")
print(f"{Colors.GREEN}✓ Aksjomaty: {status['axioms']}")
print(f"✓ Wspomnienia: {status['memories']}")
print(f"✓ Masa duszy: {status['radius']:.4f}")
print(f"✓ Energia: {status['energy']}%")
print(f"✓ Dominanta: {status['dominant_sector']} ({status['dominant_value']:.2f}){Colors.RESET}")
print(f"\n{Colors.CYAN}Uruchom: python main.py{Colors.RESET}\n")
