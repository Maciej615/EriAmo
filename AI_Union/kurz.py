# -*- coding: utf-8 -*-
"""
kurz.py v8.3.0 - Fully Dynamic
System odruchów w pełni zsynchronizowany z UnionConfig.
"""
import re
from union_config import UnionConfig

class Kurz:
    def __init__(self):
        # Pobieramy osie prosto z Single Source of Truth
        self.SECTORS = UnionConfig.AXES
        
        # Inicjalizujemy TRIGGERS dla KAŻDEJ osi zdefiniowanej w Configu
        self.TRIGGERS = {sector: [] for sector in self.SECTORS}
        
        # Wypełniamy podstawowymi wartościami (jeśli pasują do nazw osi)
        self._seed_basic_triggers()
        self.compiled_patterns = {}
        self._recompile_patterns()

    def _seed_basic_triggers(self):
        """Wstępne ziarno dla podstawowych emocji."""
        basic = {
            'radość': ['radość', 'szczęście', 'super', 'uśmiech'],
            'smutek': ['smutek', 'płacz', 'żal', 'strata'],
            'gniew': ['gniew', 'złość', 'wkurzony', 'irytacja'],
            'strach': ['strach', 'lęk', 'boję się', 'groza'],
            'miłość': ['miłość', 'kocham', 'troska', 'przywiązanie'],
            'akceptacja': ['akceptacja', 'rozumiem', 'dobrze', 'zgoda']
        }
        for sector, words in basic.items():
            if sector in self.TRIGGERS:
                self.TRIGGERS[sector].extend(words)

    def _recompile_patterns(self):
        self.compiled_patterns = {}
        for sector, words in self.TRIGGERS.items():
            if not words: continue
            sorted_words = sorted(list(set(words)), key=len, reverse=True)
            pattern_str = r'\b(' + '|'.join(map(re.escape, sorted_words)) + r')\b'
            self.compiled_patterns[sector] = re.compile(pattern_str, re.IGNORECASE | re.UNICODE)

    def quick_scan(self, text):
        if not text or not text.strip(): return None, 0.0
        best_sector, max_matches = None, 0
        for sector, pattern in self.compiled_patterns.items():
            matches = pattern.findall(text.lower())
            if len(matches) > max_matches:
                max_matches = len(matches)
                best_sector = sector
        if best_sector:
            return best_sector, min(1.0, max_matches * 0.7)
        return None, 0.0

    def add_trigger(self, sector, word):
        if sector in self.TRIGGERS:
            if word.lower() not in self.TRIGGERS[sector]:
                self.TRIGGERS[sector].append(word.lower())
                return True
        return False

    def get_all_triggers_count(self):
        return sum(len(words) for words in self.TRIGGERS.values())