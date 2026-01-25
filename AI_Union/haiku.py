# -*- coding: utf-8 -*-
"""
haiku.py v8.2.0-Hybrid - The Learning Poet
Generator poezji, który korzysta z Twardego Rdzenia (VOCAB) 
ORAZ z dynamicznej wiedzy systemu (Lexicon).
FIX: Naprawiono kodowanie polskich znaków (UTF-8).
"""
import random

class HaikuGenerator:
    def __init__(self, aii_instance):
        self.aii = aii_instance
        
        # Baza słów "bezpiecznych" (Fundament)
        self.BASE_VOCAB = {
            # --- BIOLOGIA ---
            'radość': ['słońce', 'uśmiech', 'światło', 'lekkość', 'wiosna'],
            'smutek': ['deszcz', 'cień', 'pustka', 'jesień', 'milczenie'],
            'strach': ['noc', 'drżenie', 'mrok', 'echo', 'chłód'],
            'gniew':  ['ogień', 'burza', 'krzyk', 'stal', 'grom'],
            'miłość': ['serce', 'dłoń', 'ciepło', 'razem', 'oddech'],
            'wstręt': ['rdza', 'kurz', 'gorzki', 'cierń', 'błoto'],
            'zaskoczenie': ['błysk', 'nagły', 'nowy', 'szok', 'wiatr'],
            'akceptacja': ['spokój', 'rzeka', 'trwanie', 'dom', 'cisza'],
            
            # --- METAFIZYKA ---
            'logika': ['liczba', 'wzór', 'wynik', 'sens', 'układ', 'kod', 'ład'],
            'wiedza': ['księga', 'fakt', 'zapis', 'pamięć', 'sieć', 'dane'],
            'czas':   ['zegar', 'chwila', 'wiek', 'płynie', 'przeszłość', 'jutro'],
            'kreacja':['dzieło', 'barwa', 'kształt', 'wizja', 'sztuka', 'tworzę'],
            'byt':    ['jestem', 'dusza', 'życie', 'istota', 'obecność', 'ja'],
            'przestrzeń': ['kosmos', 'dal', 'góra', 'dół', 'wszechświat', 'szlak'],
            'chaos':  ['los', 'przypadek', 'szum', 'błąd', 'entropia', 'mgła']
        }

    def _get_dynamic_words(self, axis_name, limit=10):
        """Pobiera słowa z ogólnego leksykonu, które pasują do danej osi."""
        if not self.aii or not self.aii.lexicon:
            return []

        candidates = []
        try:
            # Sprawdź, czy oś istnieje w leksykonie
            # Fallback do konfiguracji Unii, jeśli leksykon nie ma listy osi
            axes_list = getattr(self.aii.lexicon, 'AXES', self.aii.AXES_ORDER)
            
            if axis_name not in axes_list:
                return []
            
            axis_idx = axes_list.index(axis_name)
            
            # Przeszukaj leksykon
            # Wybieramy tylko słowa dłuższe niż 3 znaki
            words_source = getattr(self.aii.lexicon, 'words', getattr(self.aii.lexicon, 'lexikon', {}))
            
            for word, data in words_source.items():
                if len(word) < 4: continue 
                
                # Obsługa różnych formatów leksykonu (stary/nowy)
                vec = []
                if isinstance(data, dict):
                    vec = data.get('wektor', [])
                elif isinstance(data, list):
                    vec = data
                
                if len(vec) > axis_idx and vec[axis_idx] > 0.65: # Próg dopasowania
                    candidates.append(word)
                    
        except Exception as e:
            pass

        # Zwróć losową próbkę
        if len(candidates) > limit:
            return random.sample(candidates, limit)
        return candidates

    def generate(self):
        # 1. Introspekcja (pobranie stanu)
        state = self.aii.introspect() 
        
        # 2. Parsowanie osi (np. 'logika')
        try:
            # Format: "Dominanta: LOGIKA (Metafizyczna, 0.85)"
            raw_axis = state.split(':')[1].split('(')[0].strip().lower()
        except:
            raw_axis = 'chaos'
            
        # 3. Budowanie słownika dla tej sesji
        # Zaczynamy od bazy sztywnej
        current_vocab = list(self.BASE_VOCAB.get(raw_axis, self.BASE_VOCAB['chaos']))
        
        # Doczytujemy słowa dynamiczne z leksykonu
        dynamic_words = self._get_dynamic_words(raw_axis)
        
        # Łączymy listy
        if dynamic_words:
            current_vocab.extend(dynamic_words)

        # 4. Wybór słów bez powtórzeń
        if len(current_vocab) >= 4:
            selection = random.sample(current_vocab, 4)
        else:
            # Fallback
            selection = [random.choice(current_vocab) for _ in range(4)]

        # 5. Szablon poetycki
        l1 = f"{selection[0]} {random.choice(['jest', 'trwa', 'płynie', 'lśni', 'milczy'])}"
        l2 = f"{selection[1]} {random.choice(['otula', 'zmienia', 'tworzy', 'widzi', 'rodzi'])} {selection[2]}"
        l3 = f"{random.choice(['oto', 'teraz', 'tylko', 'zawsze', 'wszędzie'])} {selection[3]}"
        
        return f"\n=== HAIKU [{raw_axis.upper()}] ===\n{l1}\n{l2}\n{l3}\n"

    def display(self):
        print(self.generate())