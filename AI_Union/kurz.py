# -*- coding: utf-8 -*-
"""
kurz.py v8.1.0 - Config Aware
System odruchów w pełni zintegrowany z union_config.py.
"""
import re
from union_config import UnionConfig

class Kurz:
    def __init__(self):
        # POBIERZ OSIE Z JEDNEGO ŹRÓDŁA PRAWDY
        self.SECTORS = UnionConfig.AXES
        
        # Inicjalizacja pustych triggerów dla każdej osi
        self.TRIGGERS = {sector: [] for sector in self.SECTORS}
        self.compiled_patterns = {}

    def _recompile_patterns(self):
        """Kompiluje regexy dla wszystkich osi zdefiniowanych w Configu."""
        self.compiled_patterns = {}
        for sector, words in self.TRIGGERS.items():
            if not words: continue
            sorted_words = sorted(words, key=len, reverse=True)
            pattern_str = r'\b(' + '|'.join(map(re.escape, sorted_words)) + r')\b'
            try:
                self.compiled_patterns[sector] = re.compile(pattern_str, re.IGNORECASE)
            except re.error: pass

    def quick_scan(self, text):
        best_sector = None
        max_matches = 0
        
        for sector, pattern in self.compiled_patterns.items():
            matches = len(pattern.findall(text))
            if matches > max_matches:
                max_matches = matches
                best_sector = sector
        
        if best_sector:
            return best_sector, min(1.0, max_matches * 0.4)
        return None, 0.0