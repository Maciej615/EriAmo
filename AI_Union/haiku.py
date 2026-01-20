# -*- coding: utf-8 -*-
"""
haiku.py v4.0 - Zen Structure Engine
Algorytm: Obserwacja (Fizyka) -> Ruch (Proces) -> Konkluzja (Metafizyka)
"""

import random
import numpy as np

try:
    from config import Colors
except ImportError:
    class Colors:
        CYAN = '\033[96m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        RED = '\033[91m'; RESET = '\033[0m'; BLUE = '\033[94m'
        MAGENTA = '\033[95m'; FAINT = '\033[2m'

class HaikuGenerator:
    def __init__(self, aii_instance=None):
        self.aii = aii_instance
        
        # Słownik Zen - Podział na 3 sfery rzeczywistości
        self.zen_db = {
            'radość': {
                'obraz': ['słońce', 'promień', 'poranek', 'kwiat', 'ptak', 'niebo', 'ogród'],
                'ruch': ['tańczy', 'wznosi się', 'rozkwita', 'płynie', 'jaśnieje', 'budzi się', 'śpiewa'],
                'istota': ['ciepło', 'uśmiech', 'światło', 'życie', 'oddech', 'błysk', 'dar']
            },
            'smutek': {
                'obraz': ['deszcz', 'szyba', 'kamień', 'mgła', 'cień', 'pusty dom', 'zmrok'],
                'ruch': ['opada', 'milczy', 'gaśnie', 'czeka', 'płacze', 'odchodzi', 'stoi'],
                'istota': ['pustka', 'cisza', 'tęsknota', 'brak', 'dal', 'chłód', 'koniec']
            },
            'strach': {
                'obraz': ['noc', 'przepaść', 'ściana', 'szmer', 'kruk', 'wiatr', 'mrok'],
                'ruch': ['drży', 'ucieka', 'skrada się', 'patrzy', 'zastyga', 'szepcze', 'kryje'],
                'istota': ['lęk', 'niepewność', 'ciężar', 'dreszcz', 'zguba', 'szok', 'nikt']
            },
            'gniew': {
                'obraz': ['ogień', 'piorun', 'burza', 'pięść', 'krew', 'iskra', 'stal'],
                'ruch': ['uderza', 'pali', 'krzyczy', 'niszczy', 'łamie', 'grzmi', 'wrze'],
                'istota': ['ból', 'bunt', 'siła', 'furia', 'szkoda', 'fałsz', 'wrzask']
            },
            'miłość': {
                'obraz': ['dłoń', 'oczy', 'most', 'dom', 'puls', 'drzewo', 'gniazdo'],
                'ruch': ['tuli', 'łączy', 'trzyma', 'chroni', 'trwa', 'słucha', 'tętni'],
                'istota': ['jedność', 'spokój', 'razem', 'my', 'sens', 'więź', 'dom']
            },
            'akceptacja': {
                'obraz': ['rzeka', 'góra', 'liść', 'staw', 'obłok', 'droga', 'horyzont'],
                'ruch': ['płynie', 'jest', 'trwa', 'mija', 'niesie', 'oddycha', 'leży'],
                'istota': ['harmonia', 'balans', 'teraz', 'byt', 'zgoda', 'czas', 'rytm']
            },
            'zaskoczenie': {
                'obraz': ['błysk', 'znak', 'nagły ruch', 'drzwi', 'echo', 'lustro'],
                'ruch': ['zmienia', 'otwiera', 'budzi', 'łamie', 'odwraca'],
                'istota': ['nowe', 'zagadka', 'pytanie', 'zmiana', 'szansa']
            }
        }

    def _count_syllables(self, text):
        vowels = "aąeęioóuyAĄEĘIOÓUY"
        count = sum(1 for char in text if char in vowels)
        return max(1, count)

    def _get_words(self, emotion, category, mix_vector=None, axes=None):
        """
        Pobiera słowa z danej kategorii (obraz/ruch/istota).
        Obsługuje mieszanie emocji (Hybrid Moods) jeśli podano wektor.
        """
        # Baza słów dla dominującej emocji
        pool = self.zen_db.get(emotion, self.zen_db['akceptacja'])[category].copy()
        
        # Jeśli mamy wektor mieszany, domieszaj słowa z innej silnej emocji
        if mix_vector is not None and axes is not None:
            sorted_indices = np.argsort(mix_vector)[::-1]
            # Sprawdź drugą najsilniejszą emocję
            second_idx = sorted_indices[1]
            if mix_vector[second_idx] > 0.3: # Jeśli jest istotna
                second_emotion = axes[second_idx]
                second_pool = self.zen_db.get(second_emotion, {}).get(category, [])
                # Dodaj 3 losowe słowa z drugiej emocji
                if second_pool:
                    pool.extend(random.sample(second_pool, min(3, len(second_pool))))
        
        return pool

    def _assemble_line(self, target_syl, vocabulary):
        """Składa linię starając się trafić w sylaby."""
        for _ in range(50):
            word = random.choice(vocabulary)
            
            # Czasem dodajemy "i", "w", "to" dla płynności (hardcoded grammar glue)
            prefix = ""
            if target_syl == 7 and random.random() < 0.3:
                prefix = random.choice(["i ", "tu ", "tam ", "gdzie "])
            
            line = f"{prefix}{word}"
            
            current_syl = self._count_syllables(line)
            
            if current_syl == target_syl:
                return line
            
            # Jeśli brakuje sylab, dobierz drugie słowo
            if current_syl < target_syl:
                diff = target_syl - current_syl
                # Szukaj słowa o długości 'diff'
                candidates = [w for w in vocabulary if self._count_syllables(w) == diff]
                if candidates:
                    line += " " + random.choice(candidates)
                    return line
        
        # Fallback
        return random.choice(vocabulary)

    def generate(self, vector=None, axes_order=None):
        """Generuje Haiku Zen."""
        if vector is None: vector = np.zeros(8)
        if axes_order is None: axes_order = ['radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt', 'zaskoczenie', 'akceptacja']

        # 1. Ustal dominującą emocję
        if np.sum(vector) > 0:
            dom_idx = np.argmax(vector)
            emotion = axes_order[dom_idx]
        else:
            emotion = 'akceptacja'

        # 2. Buduj strukturalnie
        # Linia 1: OBRAZ (5 sylab) - Co widzę?
        pool_img = self._get_words(emotion, 'obraz', vector, axes_order)
        l1 = self._assemble_line(5, pool_img)

        # Linia 2: RUCH (7 sylab) - Co się dzieje?
        pool_act = self._get_words(emotion, 'ruch', vector, axes_order)
        l2 = self._assemble_line(7, pool_act)
        
        # Linia 3: ISTOTA (5 sylab) - Jaki to ma sens?
        pool_meaning = self._get_words(emotion, 'istota', vector, axes_order)
        l3 = self._assemble_line(5, pool_meaning)

        # 3. Formatowanie
        color_map = {
            'radość': Colors.YELLOW, 'smutek': Colors.BLUE,
            'strach': Colors.MAGENTA, 'gniew': Colors.RED,
            'miłość': Colors.MAGENTA, 'wstręt': Colors.GREEN,
            'zaskoczenie': Colors.CYAN, 'akceptacja': Colors.CYAN
        }
        c = color_map.get(emotion, Colors.RESET)
        r = Colors.RESET

        return (f"\n{c}   {l1}      (Obraz){r}\n"
                f"{c}   {l2}    (Ruch){r}\n"
                f"{c}   {l3}      (Istota){r}\n")

    def display(self):
        if self.aii:
            vec = getattr(self.aii, 'context_vector', np.zeros(8))
            axes = getattr(self.aii, 'AXES_ORDER', None)
            print(self.generate(vec, axes))
        else:
            print(self.generate())