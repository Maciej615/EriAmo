# -*- coding: utf-8 -*-
# config.py - EriAmo v5.0 (EMOTIONAL AXES)

# --- KOLORY ---
class Colors:
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    PINK = "\033[95m"
    BLUE = "\033[34m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    BLINK = "\033[5m"
    FAINT = "\033[2m"
    ORANGE = "\033[38;5;208m"

# --- EMOCJE (8-wymiarowy model Plutchika) ---
EMOCJE = {
    "radość":      {"kolor": Colors.YELLOW,  "ikona": "😊", "energia": +15},
    "smutek":      {"kolor": Colors.BLUE,    "ikona": "😢", "energia": -20},
    "strach":      {"kolor": Colors.MAGENTA, "ikona": "😨", "energia": -15},
    "gniew":       {"kolor": Colors.RED,     "ikona": "😡", "energia": -10},
    "miłość":      {"kolor": Colors.PINK,    "ikona": "❤️",  "energia": +20},
    "wstręt":      {"kolor": Colors.GREEN,   "ikona": "🤢", "energia": -5},
    "zaskoczenie": {"kolor": Colors.CYAN,    "ikona": "😮", "energia": +10},
    "akceptacja":  {"kolor": Colors.WHITE,   "ikona": "🕊️",  "energia": +5},
    "neutralna":   {"kolor": Colors.FAINT,   "ikona": "⚪", "energia": 0}
}