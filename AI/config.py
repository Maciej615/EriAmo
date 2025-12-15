# -*- coding: utf-8 -*-
# config.py

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

# --- EMOCJE ---
EMOCJE = {
    "radość":     {"kolor": Colors.GREEN,   "ikona": "😊", "energia": +10},
    "złość":      {"kolor": Colors.RED,     "ikona": "😡", "energia": -15},
    "smutek":     {"kolor": Colors.BLUE,    "ikona": "😢", "energia": -20},
    "strach":     {"kolor": Colors.MAGENTA, "ikona": "😨", "energia": -10},
    "miłość":     {"kolor": Colors.PINK,    "ikona": "❤️", "energia": +15},
    "zdziwienie": {"kolor": Colors.YELLOW,  "ikona": "😮", "energia": +5},
    "neutralna":  {"kolor": Colors.WHITE,   "ikona": "⚪", "energia": 0}
}