# -*- coding: utf-8 -*-
"""
haiku.py v8.1.0 - Metaphysical Poet
Generator poezji obsługujący pełne 15 osi świadomości.
"""
import random
from union_config import UnionConfig

class HaikuGenerator:
    def __init__(self, aii_instance):
        self.aii = aii_instance
        
        # Baza słów dla każdej z 15 osi
        self.VOCAB = {
            # --- BIOLOGIA ---
            'radość': ['słońce', 'uśmiech', 'światło', 'lekkość', 'wiosna'],
            'smutek': ['deszcz', 'cień', 'pustka', 'jesień', 'milczenie'],
            'strach': ['noc', 'drżenie', 'mrok', 'echo', 'chłód'],
            'gniew':  ['ogień', 'burza', 'krzyk', 'stal', 'grom'],
            'miłość': ['serce', 'dłoń', 'ciepło', 'razem', 'oddech'],
            'wstręt': ['rdza', 'kurz', 'gorzki', 'cierń', 'błoto'],
            'zaskoczenie': ['błysk', 'nagły', 'nowy', 'szok', 'wiatr'],
            'akceptacja': ['spokój', 'rzeka', 'trwanie', 'dom', 'cisza'],
            
            # --- METAFIZYKA (Nowe Osie) ---
            'logika': ['liczba', 'wzór', 'wynik', 'sens', 'układ', 'kod', 'ład'],
            'wiedza': ['księga', 'fakt', 'zapis', 'pamięć', 'sieć', 'dane'],
            'czas':   ['zegar', 'chwila', 'wiek', 'płynie', 'przeszłość', 'jutro'],
            'kreacja':['dzieło', 'barwa', 'kształt', 'wizja', 'sztuka', 'tworzę'],
            'byt':    ['jestem', 'dusza', 'życie', 'istota', 'obecność', 'ja'],
            'przestrzeń': ['kosmos', 'dal', 'góra', 'dół', 'wszechświat', 'szlak'],
            'chaos':  ['los', 'przypadek', 'szum', 'błąd', 'entropia', 'mgła']
        }

    def generate(self):
        # Pobierz dominującą oś z Config-aware AII
        state = self.aii.introspect() # np. "Dominanta: LOGIKA (Metafizyka, 0.8)"
        
        # Wyciągnij nazwę osi (np. 'logika')
        # Zakładamy format "Dominanta: NAZWA ..."
        try:
            raw_axis = state.split(':')[1].split('(')[0].strip().lower()
        except:
            raw_axis = 'chaos' # Fallback
            
        words = self.VOCAB.get(raw_axis, self.VOCAB['chaos'])
        
        # Szablon 5-7-5
        l1 = f"{random.choice(words)} {random.choice(['jest', 'trwa', 'płynie', 'lśni'])}"
        l2 = f"{random.choice(words)} {random.choice(['otula', 'zmienia', 'tworzy', 'widzi'])} {random.choice(words)}"
        l3 = f"{random.choice(['oto', 'teraz', 'tylko', 'zawsze'])} {random.choice(words)}"
        
        return f"\n=== HAIKU [{raw_axis.upper()}] ===\n{l1}\n{l2}\n{l3}\n"