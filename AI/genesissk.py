# -*- coding: utf-8 -*-
# genesis_skladnia.py - Szkielety Składniowe Języka Polskiego
# Gramatyka: zdania proste, złożone, spójniki, konstrukcje
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
║           GENESIS SKŁADNIA - Szkielety Gramatyczne                    ║
║                                                                       ║
║   Podstawy konstrukcji zdań: proste, złożone, spójniki               ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
""")

ai = AII()

# ═══════════════════════════════════════════════════════════════════════════
# ZDANIA PROSTE - podmiot + orzeczenie
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 1] ZDANIA PROSTE - podstawowe konstrukcje...{Colors.RESET}")

zdania_proste = [
    # Ja + czasownik
    "Ja jestem",
    "Ja idę",
    "Ja mam",
    "Ja robię",
    "Ja wiem",
    "Ja chcę",
    "Ja myślę",
    "Ja czuję",
    "Ja mówię",
    "Ja widzę",
    
    # Ty + czasownik
    "Ty jesteś",
    "Ty idziesz",
    "Ty masz",
    "Ty robisz",
    "Ty wiesz",
    "Ty chcesz",
    
    # On/Ona + czasownik
    "On jest",
    "On idzie",
    "On ma",
    "Ona jest",
    "Ona idzie",
    "Ona ma",
    
    # My/Wy/Oni
    "My jesteśmy",
    "Wy jesteście",
    "Oni są",
    
    # To + jest
    "To jest",
    "To nie jest",
    "Czy to jest?",
]

for zdanie in zdania_proste:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Zdania proste: {len(zdania_proste)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# KONSTRUKCJE "X ROBI Y" - akcje podstawowe
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 2] KONSTRUKCJE AKCJI 'X robi Y'...{Colors.RESET}")

konstrukcje_akcji = [
    # Podstawowe akcje
    "Ja robię to",
    "Ty robisz to",
    "On robi to",
    "Ja daję ci to",
    "Ty dajesz mi to",
    "On daje jej to",
    "Ja biorę to",
    "Ty bierzesz to",
    "On bierze to",
    
    # Z dopełnieniem miejsca
    "Ja idę tam",
    "Ty idziesz tam",
    "On idzie tam",
    "Ja jestem tutaj",
    "Ty jesteś tutaj",
    "On jest tutaj",
    
    # Z dopełnieniem celu
    "Ja idę do domu",
    "Ty idziesz do domu",
    "On idzie do domu",
    "Ja przychodzę z pracy",
    "Ty przychodzisz z pracy",
    
    # Posiadanie
    "Ja mam książkę",
    "Ty masz książkę",
    "On ma książkę",
    "Ja nie mam książki",
    "Ty nie masz książki",
]

for zdanie in konstrukcje_akcji:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Konstrukcje akcji: {len(konstrukcje_akcji)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# SPÓJNIKI WSPÓŁRZĘDNE - łączenie równorzędnych zdań
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 3] SPÓJNIKI WSPÓŁRZĘDNE - 'i', 'ale', 'lub'...{Colors.RESET}")

spojniki_wspolrzedne = [
    # I - łączenie
    "Ja idę i ty idziesz",
    "On jest i ona jest",
    "Mam to i chcę to",
    "Robię to i lubię to",
    
    # Ale - przeciwstawienie
    "Ja chcę ale nie mogę",
    "On jest ale ty nie jesteś",
    "Mam to ale nie używam tego",
    "Wiem to ale nie rozumiem tego",
    "Jest trudno ale da się",
    "Jest zimno ale jest pięknie",
    
    # Lub/Albo - alternatywa
    "To lub tamto",
    "Ja lub ty",
    "Teraz albo nigdy",
    "Tu albo tam",
    
    # Więc/Zatem - wnioskowanie
    "Myślę więc jestem",
    "Jest zimno więc noszę kurtkę",
    "Jestem głodny więc jem",
    "Pada deszcz więc biorę parasol",
    
    # Bo - przyczyna (potoczna)
    "Nie idę bo jestem zmęczony",
    "Cieszę się bo udało się",
    "Płaczę bo jest mi smutno",
]

for zdanie in spojniki_wspolrzedne:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Spójniki współrzędne: {len(spojniki_wspolrzedne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZDANIA WARUNKOWE - jeśli..., to...
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 4] ZDANIA WARUNKOWE - 'jeśli..., to...'...{Colors.RESET}")

zdania_warunkowe = [
    # Jeśli, to
    "Jeśli pada deszcz, to biorę parasol",
    "Jeśli jestem głodny, to jem",
    "Jeśli jest zimno, to noszę kurtkę",
    "Jeśli jest ciemno, to zapalę światło",
    "Jeśli mam czas, to przyjdę",
    
    # Gdy/Kiedy (warunek czasowy)
    "Gdy pada deszcz, zostaję w domu",
    "Kiedy jestem szczęśliwy, śpiewam",
    "Gdy jest ciepło, otwieram okno",
    "Kiedy mam problem, pytam o pomoc",
    
    # Gdyby (tryb warunkowy)
    "Gdyby padał deszcz, wziąłbym parasol",
    "Gdyby było ciepło, poszedłbym na spacer",
    "Gdybym miał czas, zrobiłbym to",
    "Gdybyś mógł, czy pomógłbyś mi?",
]

for zdanie in zdania_warunkowe:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Zdania warunkowe: {len(zdania_warunkowe)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZDANIA PRZYCZYNOWE - ponieważ, dlatego że, bo
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 5] ZDANIA PRZYCZYNOWE - 'ponieważ', 'dlatego że'...{Colors.RESET}")

zdania_przyczynowe = [
    # Ponieważ
    "Nie idę, ponieważ jestem zmęczony",
    "Cieszę się, ponieważ udało się",
    "Noszę kurtkę, ponieważ jest zimno",
    "Jem, ponieważ jestem głodny",
    
    # Dlatego że
    "Nie idę, dlatego że jestem zmęczony",
    "Cieszę się, dlatego że wygrałem",
    "Zostaję w domu, dlatego że pada",
    
    # Bo (potoczne)
    "Nie mogę, bo nie mam czasu",
    "Idę, bo muszę",
    "Płaczę, bo jest mi smutno",
    "Śmieję się, bo jest zabawnie",
    
    # Z tego powodu
    "Jest zimno, z tego powodu noszę kurtkę",
    "Jestem zmęczony, z tego powodu odpoczywam",
]

for zdanie in zdania_przyczynowe:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Zdania przyczynowe: {len(zdania_przyczynowe)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZDANIA CELOWE - żeby, aby, po to żeby
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 6] ZDANIA CELOWE - 'żeby', 'aby'...{Colors.RESET}")

zdania_celowe = [
    # Żeby
    "Idę do sklepu, żeby kupić chleb",
    "Uczę się, żeby zdać egzamin",
    "Pracuję, żeby zarobić pieniądze",
    "Jem, żeby żyć",
    "Ćwiczę, żeby być zdrowym",
    
    # Aby (formalne)
    "Przyszedłem, aby ci pomóc",
    "Mówię to, aby cię ostrzec",
    "Robię to, aby było dobrze",
    
    # Po to żeby
    "Uczę się po to, żeby wiedzieć",
    "Pracuję po to, żeby mieć pieniądze",
    
    # W celu (bardzo formalne)
    "Przyszedłem w celu pomocy",
    "Robię to w celu sukcesu",
]

for zdanie in zdania_celowe:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Zdania celowe: {len(zdania_celowe)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZDANIA CZASOWE - kiedy, zanim, po tym jak
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 7] ZDANIA CZASOWE - 'kiedy', 'zanim', 'po'...{Colors.RESET}")

zdania_czasowe = [
    # Kiedy
    "Kiedy pada deszcz, zostaję w domu",
    "Kiedy jestem zmęczony, śpię",
    "Kiedy mam czas, czytam książkę",
    
    # Zanim
    "Zanim wyjdę, sprawdzam pogodę",
    "Zanim zasnę, myję zęby",
    "Zanim podejmę decyzję, zastanawiam się",
    
    # Po tym jak / Po
    "Po tym jak zjem, idę na spacer",
    "Po pracy idę do domu",
    "Po deszczu wychodzi słońce",
    
    # Nim (literackie)
    "Nim przyjdę, zadzwonię",
    "Nim zasnę, pomyślę o tobie",
    
    # Dopóki / Póki
    "Dopóki żyję, będę walczyć",
    "Póki jest czas, działam",
    
    # Odkąd / Od kiedy
    "Odkąd cię poznałem, jestem szczęśliwy",
    "Od kiedy tu jestem, czuję się dobrze",
]

for zdanie in zdania_czasowe:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Zdania czasowe: {len(zdania_czasowe)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZDANIA PRZYZWALAJĄCE - mimo że, chociaż, choć
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 8] ZDANIA PRZYZWALAJĄCE - 'mimo że', 'choć'...{Colors.RESET}")

zdania_przyzwalajace = [
    # Mimo że
    "Mimo że pada deszcz, idę na spacer",
    "Mimo że jest zimno, nie noszę kurtki",
    "Mimo że jestem zmęczony, pracuję dalej",
    
    # Chociaż / Choć
    "Chociaż jest trudno, nie poddam się",
    "Choć jest późno, jeszcze pracuję",
    "Chociaż boli, wytrzymam",
    
    # Pomimo
    "Pomimo problemów, jestem szczęśliwy",
    "Pomimo wszystko, wierzę w ciebie",
]

for zdanie in zdania_przyzwalajace:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Zdania przyzwalające: {len(zdania_przyzwalajace)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PYTANIA - kto, co, gdzie, kiedy, dlaczego, jak
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 9] PYTANIA - 'kto', 'co', 'gdzie'...{Colors.RESET}")

pytania = [
    # Kto?
    "Kto to jest?",
    "Kto to zrobił?",
    "Kto przyszedł?",
    "Kto tam jest?",
    
    # Co?
    "Co to jest?",
    "Co robisz?",
    "Co się stało?",
    "Co mówisz?",
    "Co masz?",
    
    # Gdzie?
    "Gdzie jesteś?",
    "Gdzie idziesz?",
    "Gdzie to jest?",
    "Gdzie mieszkasz?",
    
    # Kiedy?
    "Kiedy przyjdziesz?",
    "Kiedy to było?",
    "Kiedy wyjdziesz?",
    
    # Dlaczego?
    "Dlaczego to robisz?",
    "Dlaczego tak jest?",
    "Dlaczego nie przyszedłeś?",
    
    # Jak?
    "Jak się masz?",
    "Jak to działa?",
    "Jak się nazywasz?",
    "Jak to zrobić?",
    
    # Czyj?
    "Czyj to jest?",
    "Czyja to książka?",
    
    # Ile?
    "Ile to kosztuje?",
    "Ile masz lat?",
    "Ile czasu?",
    
    # Czy? (pytanie zamknięte)
    "Czy to prawda?",
    "Czy jesteś gotowy?",
    "Czy masz czas?",
]

for zdanie in pytania:
    ai.teach("[zaskoczenie]", zdanie)

print(f"{Colors.GREEN}✓ Pytania: {len(pytania)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PRZECZENIA - nie, ani, wcale, nigdy
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 10] PRZECZENIA - 'nie', 'ani', 'nigdy'...{Colors.RESET}")

przeczenia = [
    # Nie
    "Ja nie jestem",
    "Nie idę",
    "Nie mam",
    "Nie wiem",
    "Nie mogę",
    "Nie chcę",
    "To nie jest prawda",
    
    # Ani
    "Ani to ani tamto",
    "Ani ja ani ty",
    "Nie mam ani czasu ani pieniędzy",
    
    # Nigdy
    "Nigdy nie zapomnę",
    "Nigdy więcej",
    "Nigdy tego nie robiłem",
    
    # Wcale
    "Wcale nie jestem zmęczony",
    "Wcale tego nie chciałem",
    
    # Nic
    "Nic nie wiem",
    "Nic nie mam",
    "Nic się nie stało",
    
    # Nikt
    "Nikt nie przyszedł",
    "Nikt tego nie wie",
    
    # Nigdzie
    "Nigdzie nie idę",
    "Nigdzie cię nie ma",
]

for zdanie in przeczenia:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Przeczenia: {len(przeczenia)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# TRYB ROZKAZUJĄCY - rozkazy, prośby, sugestie
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 11] TRYB ROZKAZUJĄCY - rozkazy, prośby...{Colors.RESET}")

tryb_rozkazujacy = [
    # Rozkazy (2 osoba)
    "Idź tam!",
    "Zrób to!",
    "Przyjdź tutaj!",
    "Daj mi to!",
    "Weź to!",
    "Zostaw to!",
    
    # Prośby (uprzejme)
    "Proszę przyjdź",
    "Proszę zrób to",
    "Proszę pomóż mi",
    "Proszę poczekaj",
    
    # Niech (3 osoba)
    "Niech przyjdzie",
    "Niech to zrobi",
    "Niech będzie",
    "Niech tak zostanie",
    
    # Nie (zakazy)
    "Nie idź tam!",
    "Nie rób tego!",
    "Nie mów nic!",
    "Nie dotykaj tego!",
]

for zdanie in tryb_rozkazujacy:
    ai.teach("[gniew]", zdanie)

print(f"{Colors.GREEN}✓ Tryb rozkazujący: {len(tryb_rozkazujacy)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# ZDANIA WZGLĘDNE - który, która, które
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{Colors.CYAN}[KATEGORIA 12] ZDANIA WZGLĘDNE - 'który', 'która'...{Colors.RESET}")

zdania_wzgledne = [
    # Który
    "To jest człowiek, który mi pomógł",
    "Widzę psa, który biegnie",
    "Mam książkę, którą lubię",
    "To jest dom, w którym mieszkam",
    
    # Co (potoczne)
    "To, co mówisz, jest prawdą",
    "Wszystko, co mam, jest twoje",
    "Robię to, co mogę",
    
    # Jakie
    "Jakie masz pytania?",
    "Jakie to jest?",
    "W jakim jesteś wieku?",
]

for zdanie in zdania_wzgledne:
    ai.teach("[akceptacja]", zdanie)

print(f"{Colors.GREEN}✓ Zdania względne: {len(zdania_wzgledne)} przykładów{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════════════════
# PODSUMOWANIE
# ═══════════════════════════════════════════════════════════════════════════

ai.save_knowledge()

total = (len(zdania_proste) + len(konstrukcje_akcji) + len(spojniki_wspolrzedne) +
         len(zdania_warunkowe) + len(zdania_przyczynowe) + len(zdania_celowe) +
         len(zdania_czasowe) + len(zdania_przyzwalajace) + len(pytania) +
         len(przeczenia) + len(tryb_rozkazujacy) + len(zdania_wzgledne))

status = ai.get_soul_status()

print(f"\n{Colors.MAGENTA}{'='*70}")
print(f"GENESIS SKŁADNIA ZAKOŃCZONE")
print(f"{'='*70}{Colors.RESET}")
print(f"{Colors.GREEN}✓ Szkielety składniowe: {total} przykładów")
print(f"✓ Kategorie: 12")
print(f"✓ Wspomnienia łącznie: {status['memories']}")
print(f"✓ Masa duszy: {status['radius']:.4f}")
print(f"✓ Słowa w leksykonie: {status['lexicon']['total']}{Colors.RESET}")

print(f"\n{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
print(f"║  System nauczony konstrukcji gramatycznych języka polskiego       ║")
print(f"║  Wie jak budować zdania proste i złożone.                        ║")
print(f"║                                                                   ║")
print(f"║  Uruchom: python main.py                                         ║")
print(f"╚═══════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
