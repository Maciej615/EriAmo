# -*- coding: utf-8 -*-
# genesis_definicje.py - Szkielety Definicji Strukturalnych
# Konstrukcje gramatyczne typu "X to Y" - wiedza faktograficzna
# Copyright (C) 2025 Maciej Mazur (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from aii import AII
from config import Colors

print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║           GENESIS DEFINICJE - Szkielety Strukturalne                  ║
║                                                                       ║
║   Konstrukcje "X to Y" - budowanie wiedzy o świecie                  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")

ai = AII()

# ═══════════════════════════════════════════════════════════════════════════
# KOLORY - definicje podstawowe
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 1] KOLORY - definicje podstawowe...{Colors.RESET}")

definicje_kolory = [
    "Czerwony to kolor",
    "Niebieski to kolor",
    "Żółty to kolor",
    "Zielony to kolor",
    "Czarny to kolor",
    "Biały to kolor",
    "Pomarańczowy to kolor",
    "Fioletowy to kolor",
    "Różowy to kolor",
    "Brązowy to kolor",
    "Szary to kolor",
    "Złoty to kolor",
    "Srebrny to kolor",
    "Czerwony to kolor krwi",
    "Niebieski to kolor nieba",
    "Zielony to kolor trawy",
    "Żółty to kolor słońca",
    "Biały to kolor śniegu",
    "Czarny to kolor nocy",
]

for definicja in definicje_kolory:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Kolory: {len(definicje_kolory)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZWIERZĘTA - klasyfikacja
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 2] ZWIERZĘTA - klasyfikacja...{Colors.RESET}")

definicje_zwierzeta = [
    "Pies to zwierzę",
    "Kot to zwierzę",
    "Ptak to zwierzę",
    "Ryba to zwierzę",
    "Koń to zwierzę",
    "Krowa to zwierzę",
    "Świnia to zwierzę",
    "Owca to zwierzę",
    "Pies to ssak",
    "Kot to ssak",
    "Koń to ssak",
    "Wieloryb to ssak",
    "Delfin to ssak",
    "Nietoperz to ssak",
    "Pszczoła to owad",
    "Mrówka to owad",
    "Motyl to owad",
    "Mucha to owad",
    "Pająk to pajęczak",
    "Wąż to gad",
    "Jaszczurka to gad",
    "Krokodyl to gad",
    "Żaba to płaz",
    "Salamandra to płaz",
    "Orzeł to ptak",
    "Wróbel to ptak",
    "Pingwin to ptak",
    "Struś to ptak",
    "Rekin to ryba",
    "Łosoś to ryba",
    "Karp to ryba",
]

for definicja in definicje_zwierzeta:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Zwierzęta: {len(definicje_zwierzeta)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ROŚLINY - klasyfikacja
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 3] ROŚLINY - klasyfikacja...{Colors.RESET}")

definicje_rosliny = [
    "Drzewo to roślina",
    "Kwiat to roślina",
    "Trawa to roślina",
    "Dąb to drzewo",
    "Sosna to drzewo",
    "Brzoza to drzewo",
    "Jabłoń to drzewo",
    "Róża to kwiat",
    "Tulipan to kwiat",
    "Słonecznik to kwiat",
    "Stokrotka to kwiat",
    "Kaktus to roślina",
    "Mech to roślina",
    "Paproć to roślina",
    "Grzyb to organizm",
    "Alga to roślina",
]

for definicja in definicje_rosliny:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Rośliny: {len(definicje_rosliny)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# JEDZENIE - kategorie
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 4] JEDZENIE - kategorie...{Colors.RESET}")

definicje_jedzenie = [
    "Jabłko to owoc",
    "Gruszka to owoc",
    "Banan to owoc",
    "Pomarańcza to owoc",
    "Truskawka to owoc",
    "Arbuz to owoc",
    "Winogrono to owoc",
    "Marchew to warzywo",
    "Pomidor to warzywo",
    "Ogórek to warzywo",
    "Ziemniak to warzywo",
    "Kapusta to warzywo",
    "Sałata to warzywo",
    "Chleb to pieczywo",
    "Bułka to pieczywo",
    "Rogal to pieczywo",
    "Mleko to napój",
    "Sok to napój",
    "Woda to napój",
    "Herbata to napój",
    "Kawa to napój",
    "Ser to nabiał",
    "Jogurt to nabiał",
    "Masło to nabiał",
    "Mięso to białko",
    "Ryba to białko",
    "Jajko to białko",
]

for definicja in definicje_jedzenie:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Jedzenie: {len(definicje_jedzenie)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PRZEDMIOTY - kategorie codzienne
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 5] PRZEDMIOTY - kategorie codzienne...{Colors.RESET}")

definicje_przedmioty = [
    "Krzesło to mebel",
    "Stół to mebel",
    "Łóżko to mebel",
    "Szafa to mebel",
    "Fotel to mebel",
    "Samochód to pojazd",
    "Rower to pojazd",
    "Autobus to pojazd",
    "Pociąg to pojazd",
    "Samolot to pojazd",
    "Książka to przedmiot",
    "Długopis to narzędzie",
    "Ołówek to narzędzie",
    "Nóż to narzędzie",
    "Młotek to narzędzie",
    "Telefon to urządzenie",
    "Komputer to urządzenie",
    "Telewizor to urządzenie",
    "Lodówka to urządzenie",
    "Kuchenka to urządzenie",
]

for definicja in definicje_przedmioty:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Przedmioty: {len(definicje_przedmioty)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# POJĘCIA ABSTRAKCYJNE - definicje podstawowe
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 6] POJĘCIA ABSTRAKCYJNE...{Colors.RESET}")

definicje_pojecia = [
    "Czas to wymiar",
    "Przestrzeń to wymiar",
    "Miłość to uczucie",
    "Strach to uczucie",
    "Radość to uczucie",
    "Smutek to uczucie",
    "Matematyka to nauka",
    "Fizyka to nauka",
    "Biologia to nauka",
    "Chemia to nauka",
    "Historia to nauka",
    "Język to narzędzie komunikacji",
    "Muzyka to sztuka",
    "Malarstwo to sztuka",
    "Taniec to sztuka",
    "Teatr to sztuka",
    "Prawda to wartość",
    "Dobro to wartość",
    "Piękno to wartość",
    "Sprawiedliwość to wartość",
]

for definicja in definicje_pojecia:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Pojęcia: {len(definicje_pojecia)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# CIAŁO I ZDROWIE - anatomia podstawowa
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 7] CIAŁO I ZDROWIE...{Colors.RESET}")

definicje_cialo = [
    "Serce to organ",
    "Płuco to organ",
    "Wątroba to organ",
    "Nerka to organ",
    "Mózg to organ",
    "Oko to organ zmysłu",
    "Ucho to organ zmysłu",
    "Nos to organ zmysłu",
    "Język to organ smaku",
    "Skóra to organ",
    "Ręka to kończyna",
    "Noga to kończyna",
    "Głowa to część ciała",
    "Tułów to część ciała",
    "Kość to część szkieletu",
    "Mięsień to tkanka",
    "Krew to płyn ustrojowy",
]

for definicja in definicje_cialo:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Ciało: {len(definicje_cialo)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# NATURA I ŚRODOWISKO - elementy podstawowe
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 8] NATURA I ŚRODOWISKO...{Colors.RESET}")

definicje_natura = [
    "Słońce to gwiazda",
    "Księżyc to satelita",
    "Ziemia to planeta",
    "Mars to planeta",
    "Woda to ciecz",
    "Lód to ciało stałe",
    "Para to gaz",
    "Powietrze to gaz",
    "Góra to forma terenu",
    "Rzeka to zbiornik wodny",
    "Jezioro to zbiornik wodny",
    "Morze to zbiornik wodny",
    "Ocean to zbiornik wodny",
    "Las to ekosystem",
    "Pustynia to ekosystem",
    "Burza to zjawisko atmosferyczne",
    "Tęcza to zjawisko optyczne",
    "Deszcz to opad atmosferyczny",
    "Śnieg to opad atmosferyczny",
    "Wiatr to ruch powietrza",
]

for definicja in definicje_natura:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Natura: {len(definicje_natura)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# MATEMATYKA I LICZBY - podstawy
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 9] MATEMATYKA I LICZBY...{Colors.RESET}")

definicje_matematyka = [
    "Jeden to liczba",
    "Dwa to liczba",
    "Trzy to liczba",
    "Zero to liczba",
    "Koło to figura",
    "Kwadrat to figura",
    "Trójkąt to figura",
    "Prostokąt to figura",
    "Plus to działanie matematyczne",
    "Minus to działanie matematyczne",
    "Razy to działanie matematyczne",
    "Dzielić to działanie matematyczne",
    "Równa się to znak równości",
    "Większe to porównanie",
    "Mniejsze to porównanie",
]

for definicja in definicje_matematyka:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Matematyka: {len(definicje_matematyka)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# RELACJE I PRZECIWIEŃSTWA - logika podstawowa
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 10] RELACJE I PRZECIWIEŃSTWA...{Colors.RESET}")

definicje_relacje = [
    "Duży to przeciwieństwo małego",
    "Wysoki to przeciwieństwo niskiego",
    "Gorący to przeciwieństwo zimnego",
    "Jasny to przeciwieństwo ciemnego",
    "Szybki to przeciwieństwo wolnego",
    "Dobry to przeciwieństwo złego",
    "Prawda to przeciwieństwo kłamstwa",
    "Góra to przeciwieństwo dołu",
    "Początek to przeciwieństwo końca",
    "Dzień to przeciwieństwo nocy",
    "Lato to pora roku",
    "Zima to pora roku",
    "Wiosna to pora roku",
    "Jesień to pora roku",
    "Poniedziałek to dzień tygodnia",
    "Wtorek to dzień tygodnia",
    "Środa to dzień tygodnia",
    "Styczeń to miesiąc",
    "Luty to miesiąc",
    "Marzec to miesiąc",
]

for definicja in definicje_relacje:
    ai.teach("[akceptacja]", definicja)

print(f"{Colors.GREEN}✓ Relacje: {len(definicje_relacje)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# DEFINICJE Z ZASKOCZENIEM - ciekawe fakty
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 11] CIEKAWE FAKTY (zaskoczenie)...{Colors.RESET}")

definicje_ciekawe = [
    "Wieloryb to ssak, nie ryba",
    "Pomidor to owoc, nie warzywo",
    "Truskawka to orzech, nie jagoda",
    "Banan to zioło, nie drzewo",
    "Pingwin to ptak, który nie lata",
    "Nietoperz to ssak, który lata",
    "Ośmiornica ma trzy serca",
    "Karaluch może żyć bez głowy",
    "Miód nigdy nie psuje się",
    "Diamenty to węgiel pod ciśnieniem",
]

for definicja in definicje_ciekawe:
    ai.teach("[zaskoczenie]", definicja)

print(f"{Colors.GREEN}✓ Ciekawe fakty: {len(definicje_ciekawe)} definicji{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PODSUMOWANIE
# ═══════════════════════════════════════════════════════════════════════════

ai.save_knowledge()

total = (len(definicje_kolory) + len(definicje_zwierzeta) + len(definicje_rosliny) +
         len(definicje_jedzenie) + len(definicje_przedmioty) + len(definicje_pojecia) +
         len(definicje_cialo) + len(definicje_natura) + len(definicje_matematyka) +
         len(definicje_relacje) + len(definicje_ciekawe))

status = ai.get_soul_status()

print(f"\n{Colors.MAGENTA}{'='*70}")
print(f"GENESIS DEFINICJE ZAKOŃCZONE")
print(f"{'='*70}{Colors.RESET}")
print(f"{Colors.GREEN}✓ Definicje strukturalne: {total} przykładów")
print(f"✓ Kategorie: 11")
print(f"✓ Wspomnienia łącznie: {status['memories']}")
print(f"✓ Masa duszy: {status['radius']:.4f}")
print(f"✓ Słowa w leksykonie: {status['lexicon']['total']}{Colors.RESET}")

print(f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
print(f"║  System nauczony definicji strukturalnych 'X to Y'                ║")
print(f"║  Wie co jest czym - podstawowa wiedza o świecie.                 ║")
print(f"║                                                                   ║")
print(f"║  Uruchom: python main.py                                         ║")
print(f"╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
