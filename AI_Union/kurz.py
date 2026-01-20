# -*- coding: utf-8 -*-
"""
kurz.py v8.0.0-Hybrid
System odruchów obsługujący 15 osi (Biologia + Metafizyka).
"""
import re

class Kurz:
    def __init__(self):
        # Definicja 15 sektorów
        self.SECTORS = [
            'radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt', 'zaskoczenie', 'akceptacja',
            'logika', 'wiedza', 'czas', 'kreacja', 'byt', 'przestrzeń', 'chaos'
        ]
        
        # Słownik triggerów
        self.TRIGGERS = {sector: [] for sector in self.SECTORS}
        self.compiled_patterns = {}

    def _recompile_patterns(self):
        """Kompiluje regexy dla wszystkich 15 osi."""
        self.compiled_patterns = {}
        for sector, words in self.TRIGGERS.items():
            if not words: continue
            # Sortujemy od najdłuższych, żeby uniknąć dopasowania częściowego
            sorted_words = sorted(words, key=len, reverse=True)
            # Regex z granicami słów (\b) dla precyzji
            pattern_str = r'\b(' + '|'.join(map(re.escape, sorted_words)) + r')\b'
            try:
                self.compiled_patterns[sector] = re.compile(pattern_str, re.IGNORECASE)
            except re.error:
                pass

    def quick_scan(self, text):
        """
        Szybki skan tekstu. Zwraca (Sektor, Siła).
        Działa na zasadzie 'pierwszy silny sygnał'.
        """
        best_sector = None
        max_matches = 0
        
        for sector, pattern in self.compiled_patterns.items():
            matches = len(pattern.findall(text))
            if matches > max_matches:
                max_matches = matches
                best_sector = sector
        
        if best_sector:
            # Siła sygnału zależy od liczby trafień (limit 1.0)
            strength = min(1.0, max_matches * 0.4)
            return best_sector, strength
            
        return None, 0.0