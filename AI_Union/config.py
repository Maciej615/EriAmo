# -*- coding: utf-8 -*-
"""
config.py
Lokalizacja: /eriamo-union/src/language/config.py
"""

class Colors:
    """Paleta kolorów ANSI do terminala."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Kolory podstawowe
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
    # Dodatkowe (Naprawa błędu Genesis)
    PINK = "\033[95m" 

class Config:
    """Główna konfiguracja parametrów Bytu."""
    SOUL_FILE = "eriamo.soul"
    LEXICON_FILE = "lexicon.soul"
    DEFAULT_ENERGY = 100.0
    ENERGY_DECAY = 0.1
    RESONANCE_THRESHOLD = 0.15
    GENESIS_DEF_COUNT = 1111
    ANIMATION_SPEED = 0.03