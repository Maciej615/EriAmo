#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_lexicon.py - Dodaje SEED_LEXICON do lexicon.soul

Problem: lexicon.soul ma tylko 11 słów z haiku
Rozwiązanie: Dodaj ~150 podstawowych słów dla każdej emocji
"""

import json
import sys
from pathlib import Path

# Kolory
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
print(f"{Colors.CYAN}Rebuild Lexicon - Dodawanie SEED_LEXICON{Colors.RESET}")
print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")

# Znajdź lexicon.soul
lexicon_path = None
# Fix paths relative to project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

candidates = [
    os.path.join(project_root, 'src', 'language', 'lexicon.soul'),
    os.path.join(project_root, 'lexicon.soul'),
    os.path.join(project_root, 'data', 'lexicon.soul')
]
for p in candidates:
    if Path(p).exists():
        lexicon_path = p
        break

if not lexicon_path:
    print(f"{Colors.RED}✗ Nie znaleziono lexicon.soul{Colors.RESET}")
    sys.exit(1)

print(f"Plik: {lexicon_path}")

# Wczytaj obecny lexicon
with open(lexicon_path, 'r', encoding='utf-8') as f:
    lexicon = json.load(f)

print(f"Obecny stan: {len(lexicon['words'])} słów")

# SEED_LEXICON - podstawowe słowa dla każdej emocji
SEED_LEXICON = {
    # RADOŚĆ - ~25 słów
    "radość": {
        "radosc": 0.9, "radość": 0.9, "szczescie": 0.9, "szczęście": 0.9,
        "usmiech": 0.8, "uśmiech": 0.8, "smiech": 0.8, "śmiech": 0.8,
        "zabawa": 0.75, "taniec": 0.7, "wesele": 0.8, "swietnie": 0.85,
        "wspaniale": 0.85, "cudownie": 0.85, "super": 0.8, "fajnie": 0.75,
        "genialnie": 0.8, "bomba": 0.75, "git": 0.7, "ekstra": 0.75,
        "wow": 0.7, "hura": 0.85, "brawo": 0.8, "sukces": 0.85, "zwyciestwo": 0.85
    },
    
    # SMUTEK - ~20 słów
    "smutek": {
        "smutek": 0.9, "zal": 0.8, "żal": 0.8, "tesknota": 0.85, "tęsknota": 0.85,
        "placz": 0.85, "płacz": 0.85, "lzy": 0.85, "łzy": 0.85,
        "samotnosc": 0.8, "samotność": 0.8, "strata": 0.85, "utrata": 0.85,
        "rozstanie": 0.85, "smutno": 0.8, "przygnebienie": 0.75, "przygnębienie": 0.75,
        "melancholia": 0.7, "depresja": 0.85, "rozpacz": 0.9, "cierpienie": 0.85
    },
    
    # STRACH - ~20 słów
    "strach": {
        "strach": 0.9, "lek": 0.9, "lęk": 0.9, "obawa": 0.8, "panika": 0.95,
        "przerazenie": 0.95, "przerażenie": 0.95, "przestrach": 0.9,
        "niepokój": 0.85, "niepokój": 0.85, "grozba": 0.85, "groźba": 0.85,
        "niebezpieczenstwo": 0.9, "niebezpieczeństwo": 0.9, "zagrożenie": 0.85,
        "panicznie": 0.9, "strasznie": 0.8, "przerazajace": 0.85, "przerażające": 0.85,
        "boję": 0.85, "lekam": 0.8, "lękam": 0.8
    },
    
    # GNIEW - ~20 słów
    "gniew": {
        "gniew": 0.9, "zlosc": 0.85, "złość": 0.85, "wscieklosc": 0.95, "wściekłość": 0.95,
        "irytacja": 0.75, "denerwuje": 0.75, "frustracja": 0.8,
        "wkurzenie": 0.8, "wkurza": 0.8, "wkurzam": 0.8,
        "nienawisc": 0.95, "nienawiść": 0.95, "nienawidze": 0.95, "nienawidzę": 0.95,
        "furia": 0.9, "szal": 0.85, "szał": 0.85, "agresja": 0.85,
        "krzywda": 0.8, "niesprawiedliwosc": 0.8, "niesprawiedliwość": 0.8
    },
    
    # MIŁOŚĆ - ~25 słów
    "miłość": {
        "milosc": 0.95, "miłość": 0.95, "kocham": 0.95, "ukochany": 0.9,
        "czulosc": 0.85, "czułość": 0.85, "namiętność": 0.9, "namietnosc": 0.9,
        "serce": 0.8, "przyjazn": 0.8, "przyjaźń": 0.8, "bliskosc": 0.85, "bliskość": 0.85,
        "troska": 0.8, "opieka": 0.75, "wsparcie": 0.75, "empatia": 0.8,
        "zrozumienie": 0.75, "akceptacja": 0.7, "rodzina": 0.85, "przyjaciel": 0.8,
        "ukochana": 0.9, "kochanie": 0.9, "kochany": 0.9, "drogie": 0.85
    },
    
    # WSTRĘT - ~15 słów
    "wstręt": {
        "wstret": 0.9, "wstręt": 0.9, "obrzydzenie": 0.9, "obrzydliwe": 0.85,
        "fuj": 0.85, "obrzydza": 0.85, "niedobrze": 0.75, "mdli": 0.8,
        "odpychajace": 0.8, "odpychające": 0.8, "obrzydliwy": 0.85,
        "ohyda": 0.85, "plugastwo": 0.85, "plugastwo": 0.85, "wstrętne": 0.85
    },
    
    # ZASKOCZENIE - ~20 słów
    "zaskoczenie": {
        "zaskoczenie": 0.85, "zdziwienie": 0.8, "niespodzianka": 0.85,
        "wow": 0.75, "ojej": 0.75, "niesamowite": 0.8, "niewiarygodne": 0.85,
        "szok": 0.9, "zaskakujace": 0.8, "zaskakujące": 0.8,
        "ciekawe": 0.7, "intrygujace": 0.75, "intrygujące": 0.75,
        "fascynujace": 0.75, "fascynujące": 0.75, "odkrycie": 0.8,
        "rewelacja": 0.85, "nieoczekiwane": 0.85, "niespodziewane": 0.85
    },
    
    # AKCEPTACJA - ~25 słów
    "akceptacja": {
        "akceptacja": 0.85, "spokoj": 0.85, "spokój": 0.85, "harmonia": 0.8,
        "rownowaga": 0.8, "równowaga": 0.8, "balans": 0.75, "zgoda": 0.75,
        "rozumiem": 0.75, "wiem": 0.75, "jasne": 0.7, "ok": 0.7, "okej": 0.7,
        "dobrze": 0.75, "porzadku": 0.7, "porządku": 0.7, "zgadzam": 0.75,
        "przyjmuje": 0.7, "akceptuje": 0.8, "akceptuję": 0.8,
        "godzę": 0.75, "pewny": 0.7, "oczywiste": 0.7, "logiczne": 0.7
    }
}

# Dodaj podstawowe słowa
added_count = 0
for sektor, slowa in SEED_LEXICON.items():
    for slowo, sila in slowa.items():
        if slowo not in lexicon['words']:
            lexicon['words'][slowo] = {sektor: sila}
            added_count += 1
        else:
            # Słowo już jest - dodaj tylko nowy sektor jeśli nie ma
            if sektor not in lexicon['words'][slowo]:
                lexicon['words'][slowo][sektor] = sila
                added_count += 1

print(f"Dodano: {added_count} nowych asocjacji")

# Dodaj podstawowe słowa strukturalne (gramatyka)
STRUCTURAL = {
    "ja": ("akceptacja", 0.6),
    "ty": ("akceptacja", 0.6),
    "on": ("akceptacja", 0.5),
    "ona": ("akceptacja", 0.5),
    "my": ("radość", 0.5),
    "wy": ("akceptacja", 0.5),
    "oni": ("akceptacja", 0.5),
    "jestem": ("akceptacja", 0.7),
    "jestes": ("akceptacja", 0.7),
    "jesteś": ("akceptacja", 0.7),
    "jest": ("akceptacja", 0.7),
    "i": ("akceptacja", 0.3),
    "ale": ("zaskoczenie", 0.4),
    "co": ("zaskoczenie", 0.5),
    "jak": ("zaskoczenie", 0.5),
    "gdzie": ("zaskoczenie", 0.5),
    "kiedy": ("zaskoczenie", 0.5),
    "dlaczego": ("zaskoczenie", 0.6),
    "tak": ("akceptacja", 0.6),
    "dobrze": ("radość", 0.7),
    "źle": ("smutek", 0.7),
    "zle": ("smutek", 0.7),
}

for slowo, (sektor, sila) in STRUCTURAL.items():
    if slowo not in lexicon['words']:
        lexicon['words'][slowo] = {sektor: sila}
        added_count += 1

print(f"Dodano: {len(STRUCTURAL)} słów strukturalnych")

# Aktualizuj total_learned
lexicon['total_learned'] = len(lexicon['words'])

# Backup
backup = Path(lexicon_path).with_suffix('.soul.before_rebuild')
Path(lexicon_path).rename(backup)
print(f"Backup: {backup}")

# Save
with open(lexicon_path, 'w', encoding='utf-8') as f:
    json.dump(lexicon, f, ensure_ascii=False, indent=2)

print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
print(f"{Colors.GREEN}✓ LEXICON PRZEBUDOWANY!{Colors.RESET}")
print(f"{Colors.GREEN}{'='*60}{Colors.RESET}\n")

print(f"Statystyki:")
print(f"  Przed: 11 słów (tylko z haiku)")
print(f"  Po: {len(lexicon['words'])} słów (SEED + strukturalne + nauczone)")
print(f"  Backup: {backup.name}")

print(f"\n{Colors.CYAN}Teraz uruchom:{Colors.RESET}")
print(f"  {Colors.CYAN}python main.py{Colors.RESET}\n")

print(f"Test:")
print(f"  Ty > jestem szczęśliwy")
print(f"  [System rozpozna 'szczęśliwy' → radość]")
print()
