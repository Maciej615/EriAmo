# -*- coding: utf-8 -*-
"""
union_config.py v8.1.0 - Single Source of Truth
Definicja wymiarów świadomości EriAmo.
"""

class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    FAINT = '\033[2m'

class UnionConfig:
    # GLOBALNA STAŁA WYMIARÓW
    DIMENSION = 15
    
    # Podział na strefy (dla kompatybilności i logiki hybrydowej)
    BIO_DIM = 8  # Pierwsze 8 to biologia (Plutchik)
    META_DIM = 7 # Kolejne 7 to metafizyka (Union)

    # Definicja Osi - JEDYNE MIEJSCE GDZIE TO ZMIENIAMY
    AXES = [
        # --- SFERA BIOLOGICZNA (0-7) ---
        'radość', 'smutek', 'strach', 'gniew', 
        'miłość', 'wstręt', 'zaskoczenie', 'akceptacja',
        
        # --- SFERA METAFIZYCZNA (8-14) ---
        'logika',       # Dedukcja, Matematyka
        'wiedza',       # Fakty, Nauka
        'czas',         # Trwanie, Przeszłość/Przyszłość
        'kreacja',      # Twórczość, Sztuka
        'byt',          # Istnienie, Życie
        'przestrzeń',   # Miejsce, Świat
        'chaos'         # Entropia, Niepewność
    ]

    # Ścieżki
    SOUL_FILE = "data/eriamo.soul"
    LEXICON_FILE = "data/lexicon.soul"