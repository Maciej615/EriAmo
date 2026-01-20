# -*- coding: utf-8 -*-
# kurz.py (v5.2.0-Fusion) - Warstwa Odruchowa

import re
from config import Colors

class Kurz:
    def __init__(self):
        # Puste kontenery - zostaną zasilone przez AII._sync_kurz_with_lexicon()
        self.TRIGGERS = {
            "radość": [], "smutek": [], "strach": [], "gniew": [],
            "miłość": [], "wstręt": [], "zaskoczenie": [], "akceptacja": []
        }
        self.patterns = {}
        self._recompile_patterns()

    def _recompile_patterns(self):
        """Kompiluje regexy dla słów nauczonych w Leksykonie."""
        for sector, words in self.TRIGGERS.items():
            if words:
                # Tworzymy wzorzec: szukamy rdzeni słów dla lepszej generalizacji
                pattern_str = r"|".join([re.escape(w) for w in words])
                self.patterns[sector] = re.compile(pattern_str, re.IGNORECASE)
            else:
                self.patterns[sector] = None

    def quick_scan(self, text):
        """Szybki skan intencji (Odruch Adama)."""
        best_sector = None
        max_strength = 0
        
        for sector, pattern in self.patterns.items():
            if pattern:
                matches = pattern.findall(text)
                if matches:
                    strength = len(matches)
                    if strength > max_strength:
                        max_strength = strength
                        best_sector = sector
                        
        return best_sector, max_strength