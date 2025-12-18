# -*- coding: utf-8 -*-
# kurz.py - Szybki skaner emocjonalny (odruchowy)
"""
Moduł Kurz - błyskawiczna detekcja sektora emocjonalnego.
Działa przed pełną analizą leksykalną.
"""

import re

class Kurz:
    """Szybki skaner emocjonalny - odruchowa reakcja."""
    
    # Słowa-wyzwalacze dla każdego sektora
    TRIGGERS = {
        'radość': ['super', 'wspaniale', 'cudownie', 'świetnie', 'hurra', 'tak!', 'udało', 'sukces', 'wygrał'],
        'smutek': ['smutno', 'żal', 'tęsknię', 'płaczę', 'strata', 'zmarł', 'boli', 'samotność'],
        'strach': ['boję', 'strach', 'przerażony', 'panika', 'niebezpiecz', 'zagrożen', 'lęk'],
        'gniew': ['wkurz', 'złość', 'wściek', 'nienawidz', 'cholera', 'kurwa', 'idiot'],
        'miłość': ['kocham', 'miłość', 'serce', 'ukochana', 'ukochany', 'czułość', 'troska'],
        'wstręt': ['obrzydzenie', 'fuj', 'wstręt', 'obrzydliw', 'ohyda', 'plugaw'],
        'zaskoczenie': ['wow', 'ojej', 'niemożliwe', 'szok', 'zaskocz', 'niespodzianka', 'co?!'],
        'akceptacja': ['spokój', 'harmonia', 'zgoda', 'rozumiem', 'akceptuję', 'w porządku', 'ok']
    }
    
    def __init__(self):
        # Kompiluj wzorce regex dla szybkości
        self.patterns = {}
        for sector, words in self.TRIGGERS.items():
            pattern = '|'.join(re.escape(w) for w in words)
            self.patterns[sector] = re.compile(pattern, re.IGNORECASE)
    
    def quick_scan(self, text):
        """
        Błyskawiczny skan tekstu.
        
        Returns:
            tuple: (detected_sector, signal_strength) lub (None, 0)
        """
        text_lower = text.lower()
        
        best_sector = None
        best_count = 0
        
        for sector, pattern in self.patterns.items():
            matches = pattern.findall(text_lower)
            if len(matches) > best_count:
                best_count = len(matches)
                best_sector = sector
        
        if best_sector:
            # Siła sygnału: więcej dopasowań = silniejszy
            signal_strength = min(1.0, best_count * 0.3)
            return best_sector, signal_strength
        
        return None, 0.0
