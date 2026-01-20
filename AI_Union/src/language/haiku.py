# -*- coding: utf-8 -*-
"""
haiku.py - Dynamiczny Generator Haiku dla EriAmo v3.1
ULEPSZONA WERSJA z seedem i wzmacnianiem
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
        
        # NOWE: Seed słownika dla każdej emocji
        self.emotion_seeds = {
            'radość': ['szczęście', 'uśmiech', 'światło', 'śmiech', 'słońce'],
            'smutek': ['łzy', 'samotność', 'pustka', 'cisza', 'deszcz'],
            'strach': ['cień', 'ciemność', 'lęk', 'drżenie', 'noc'],
            'gniew': ['krzyk', 'burza', 'ogień', 'wściekłość', 'furia'],
            'miłość': ['serce', 'ciepło', 'bliskość', 'czułość', 'objęcie'],
            'wstręt': ['odwrót', 'odraza', 'fu', 'unikaj', 'niechęć'],
            'zaskoczenie': ['nagle', 'łup', 'szok', 'nieoczekiwane', 'zdziwienie'],
            'akceptacja': ['spokój', 'zgoda', 'harmonia', 'akceptacja', 'równowaga'],
            'neutralna': ['cisza', 'pustka', 'czas', 'jestem', 'trwa']
        }

    def _count_syllables(self, text):
        """Liczy sylaby w polskim tekście."""
        vowels = "aąeęioóuyAĄEĘIOÓUY"
        count = sum(1 for char in text if char in vowels)
        return max(1, count)

    def _get_words_for_emotion(self, lexicon, emotion, min_score=0.2):
        """Wyciąga słowa z leksykonu + seed."""
        candidates = []
        
        # Obsługa różnych struktur lexicon
        if hasattr(lexicon, 'words'):
            words_dict = lexicon.words
        elif hasattr(lexicon, 'vocabulary'):
            words_dict = lexicon.vocabulary
        else:
            # Brak lexicon - użyj tylko seedów
            return self.emotion_seeds.get(emotion, self.emotion_seeds['neutralna'])
        
        # Zbierz słowa z lexicon
        for word, scores in words_dict.items():
            if scores.get(emotion, 0) >= min_score:
                candidates.append(word)
            elif emotion == 'neutralna' and max(scores.values()) < 0.4:
                candidates.append(word)
        
        # NOWE: Dodaj seedy dla gwarancji jakości
        seeds = self.emotion_seeds.get(emotion, [])
        candidates.extend(seeds)
        
        return candidates if candidates else seeds

    def _build_line(self, target_syllables, pool):
        """Buduje linię o zadanej liczbie sylab."""
        if not pool:
            return "..." * (target_syllables // 3 + 1)
        
        best_line = None
        best_diff = float('inf')
        
        for attempt in range(100):
            phrase_length = random.randint(1, 3)
            chosen_words = random.sample(pool, min(len(pool), phrase_length))
            line_str = " ".join(chosen_words)
            
            syllables = self._count_syllables(line_str)
            diff = abs(syllables - target_syllables)
            
            if diff == 0:
                return line_str.capitalize()
            
            if diff < best_diff:
                best_diff = diff
                best_line = line_str
        
        return best_line.capitalize() if best_line else "..."

    def _reinforce_lexicon(self, haiku_lines, emotion):
        """NOWE: Wzmacnia lexicon używając słów z haiku."""
        if not self.aii or not hasattr(self.aii, 'lexicon'):
            return
        
        reinforced = 0
        axes_order = getattr(self.aii, 'AXES_ORDER', [])
        
        if not axes_order:
            return
        
        # Wektor emocji
        emotion_vector = np.zeros(8)
        if emotion in axes_order:
            idx = axes_order.index(emotion)
            emotion_vector[idx] = 0.7
        
        # Wzmocnij wszystkie słowa z haiku
        for line in haiku_lines:
            words = line.lower().split()
            for word in words:
                clean_word = word.strip('.,!?')
                if len(clean_word) > 2:
                    try:
                        self.aii.lexicon.learn_from_context(
                            [clean_word], emotion_vector, confidence=0.15
                        )
                        reinforced += 1
                    except:
                        pass
        
        if reinforced > 0:
            print(f"{Colors.FAINT}[Haiku→Lexicon] Wzmocniłem {reinforced} słów w '{emotion}'{Colors.RESET}")

    def generate(self, emotion="neutralna", lexicon=None):
        """Główna metoda generująca Haiku."""
        # 1. Przygotuj pulę słów
        word_pool = self._get_words_for_emotion(lexicon, emotion)
        
        # 2. Zbuduj strukturę 5-7-5
        line1 = self._build_line(5, word_pool)
        line2 = self._build_line(7, word_pool)
        line3 = self._build_line(5, word_pool)
        
        # 3. NOWE: Wzmocnij lexicon
        self._reinforce_lexicon([line1, line2, line3], emotion)
        
        # 4. Formatowanie
        color_map = {
            'radość': Colors.YELLOW, 'smutek': Colors.BLUE,
            'strach': Colors.MAGENTA, 'gniew': Colors.RED,
            'miłość': Colors.MAGENTA, 'wstręt': Colors.GREEN,
            'zaskoczenie': Colors.CYAN, 'akceptacja': Colors.CYAN,
            'neutralna': Colors.RESET
        }
        color = color_map.get(emotion, Colors.RESET)
        
        # 5. Wyświetlanie
        border = f"{color}╔════════════════════════════════════════╗{Colors.RESET}"
        title  = f"{color}║  [HAIKU] - Stan: {emotion:16s}  ║{Colors.RESET}"
        sep    = f"{color}╠════════════════════════════════════════╣{Colors.RESET}"
        l1     = f"{color}║  {line1:36s}  ║{Colors.RESET}"
        l2     = f"{color}║  {line2:36s}  ║{Colors.RESET}"
        l3     = f"{color}║  {line3:36s}  ║{Colors.RESET}"
        end    = f"{color}╚════════════════════════════════════════╝{Colors.RESET}"
        
        return f"\n{border}\n{title}\n{sep}\n{l1}\n{l2}\n{l3}\n{end}\n"

    def display(self):
        """Helper dla zgodności z AII."""
        if not self.aii:
            print(self.generate())
            return
        
        # Wykryj emocję z context_vector
        if hasattr(self.aii, 'context_vector') and hasattr(self.aii, 'AXES_ORDER'):
            if np.sum(self.aii.context_vector) > 0:
                idx = np.argmax(self.aii.context_vector)
                emotion = self.aii.AXES_ORDER[idx]
            else:
                emotion = 'neutralna'
        else:
            emotion = 'neutralna'
        
        # Generuj z lexicon
        lexicon = getattr(self.aii, 'lexicon', None)
        haiku = self.generate(emotion, lexicon)
        print(haiku)