# -*- coding: utf-8 -*-
# lexicon.py v1.1 - FIXED: Multi-dimensional learning + reinforcement
import json
import os
import numpy as np
import unidecode
import re
from config import Colors

class EvolvingLexicon:
    SEED_LEXICON = {
        "logika": ["logika", "logiczny", "sens", "rozum", "dlaczego", "poniewaz", "wynik", "fakt", "analiza", "system", "wniosek", "dowod"],
        "emocje": ["czuje", "emocja", "milosc", "zlosc", "smutek", "radosc", "strach", "uczucie", "nastroj", "bol", "szczescie"],
        "byt": ["byt", "istnienie", "ja", "ty", "jestem", "kula", "rzeczywistosc", "historia", "ontologia", "imie", "dusza", "swiadomosc", "zycie", "smierc", "eriamo"],
        "walka": ["walka", "dzialanie", "konflikt", "wojna", "sila", "wrog", "chaos", "wola", "atak", "obrona", "przystosowanie", "sterowanie", "bitwa"],
        "kreacja": ["tworzyc", "sztuka", "budowac", "muzyka", "pisac", "nowy", "piekno", "wyobraznia", "projekt", "dzielo", "kompozycja"],
        "wiedza": ["wiedza", "nauka", "uczyc", "dane", "informacja", "co", "kto", "jak", "definicja", "model", "teoria", "prawda"],
        "czas": ["czas", "kiedy", "przeszlosc", "teraz", "przyszlosc", "historia", "krok", "sciezka", "moment", "wiecznosc", "chwila"],
        "przestrzen": ["gdzie", "miejsce", "krajobraz", "droga", "swiat", "kierunek", "polozenie", "sektor", "otoczenie", "biosfera", "dom", "tu"]
    }
    
    # ✅ FIX 1: Zmniejszony próg uczenia
    PRÓG_AKTYWACJI = 0.3
    PRÓG_UCZENIA = 0.3        # Było 0.5 - teraz bardziej tolerancyjne
    WAGA_SEED = 1.0
    WAGA_NAUCZONE = 0.5
    DECAY_RATE = 0.99
    MIN_WORD_LENGTH = 3
    REINFORCEMENT_RATE = 0.05  # ✅ NEW: Wzmocnienie przy użyciu
    
    def __init__(self, lexicon_file="lexicon.soul"):
        self.lexicon_file = lexicon_file
        self.axes = ["logika", "emocje", "byt", "walka", "kreacja", "wiedza", "czas", "przestrzen"]
        self.words = {}
        self.total_learned = 0
        self.last_learned = []
        self._initialize_from_seed()
        self.load()
    
    def _normalize(self, word):
        word = word.lower().strip()
        word = unidecode.unidecode(word)
        word = re.sub(r'[^\w]', '', word)
        return word
    
    def _initialize_from_seed(self):
        for sector, words in self.SEED_LEXICON.items():
            for word in words:
                norm_word = self._normalize(word)
                if norm_word not in self.words:
                    self.words[norm_word] = {}
                self.words[norm_word][sector] = self.WAGA_SEED
    
    def get_word_vector(self, word):
        norm_word = self._normalize(word)
        vec = np.zeros(len(self.axes))
        if norm_word in self.words:
            for i, axis in enumerate(self.axes):
                vec[i] = self.words[norm_word].get(axis, 0.0)
        return vec
    
    # ✅ FIX 2: Dodano reinforcement dla używanych słów
    def analyze_text(self, text, enable_reinforcement=True):
        words = text.lower().split()
        words = [self._normalize(w) for w in words if len(w) >= self.MIN_WORD_LENGTH]
        
        if not words:
            return np.zeros(len(self.axes)), None, []
        
        total_vec = np.zeros(len(self.axes))
        unknown_words = []
        used_known_words = []
        
        for word in words:
            if word in self.words:
                total_vec += self.get_word_vector(word)
                used_known_words.append(word)
            else:
                unknown_words.append(word)
        
        norm = np.linalg.norm(total_vec)
        if norm > 0:
            total_vec = total_vec / norm
        
        dominant_sector = None
        if np.max(total_vec) > self.PRÓG_AKTYWACJI:
            dominant_idx = np.argmax(total_vec)
            dominant_sector = self.axes[dominant_idx]
            
            # ✅ NEW: Wzmocnij znane słowa w dominującym sektorze
            if enable_reinforcement and dominant_sector:
                for word in used_known_words:
                    self._reinforce_word(word, dominant_sector)
        
        return total_vec, dominant_sector, unknown_words
    
    # ✅ FIX 3: Nowa metoda wzmacniania
    def _reinforce_word(self, word, sector):
        """Wzmacnia połączenie słowo-sektor przy każdym użyciu."""
        if word not in self.words:
            return
        current = self.words[word].get(sector, 0.0)
        # Wzmocnienie z ceiling na 1.0
        self.words[word][sector] = min(1.0, current + self.REINFORCEMENT_RATE)
    
    # ✅ FIX 4: Multi-dimensional learning z progiem
    def learn_from_context(self, unknown_words, context_vector, confidence):
        """
        Uczy nowe słowa na podstawie PEŁNEGO wektora kontekstu, nie tylko dominanty.
        Przypisuje wymiary które przekraczają próg aktywacji.
        """
        if confidence < self.PRÓG_UCZENIA:
            return []
        
        learned = []
        for word in unknown_words:
            if len(word) < self.MIN_WORD_LENGTH:
                continue
            
            if word not in self.words:
                self.words[word] = {}
            
            # ✅ NEW: Przypisz WSZYSTKIE wymiary powyżej progu
            for i, axis in enumerate(self.axes):
                dim_strength = context_vector[i]
                if dim_strength > self.PRÓG_AKTYWACJI:
                    initial_weight = self.WAGA_NAUCZONE * dim_strength * confidence
                    current = self.words[word].get(axis, 0.0)
                    self.words[word][axis] = min(1.0, current + initial_weight)
            
            # Jeśli nauczono chociaż jeden wymiar
            if any(v > 0 for v in self.words[word].values()):
                learned.append((word, self.words[word].copy()))
                self.total_learned += 1
        
        self.last_learned = learned
        return learned
    
    def learn_from_correction(self, word, correct_sector, strength=0.7):
        """Manualna korekta - zwiększa wagę w danym sektorze."""
        norm_word = self._normalize(word)
        if norm_word not in self.words:
            self.words[norm_word] = {}
        current = self.words[norm_word].get(correct_sector, 0.0)
        self.words[norm_word][correct_sector] = min(1.0, current + strength)
        self.total_learned += 1
        return True
    
    def decay_unused(self):
        """Zanik nieużywanych słów (oprócz SEED)."""
        words_to_remove = []
        for word, sectors in self.words.items():
            # Nie dotykaj seeda
            is_seed = False
            for s_words in self.SEED_LEXICON.values():
                if word in [self._normalize(w) for w in s_words]:
                    is_seed = True
                    break
            if is_seed:
                continue
            
            for sector in list(sectors.keys()):
                sectors[sector] *= self.DECAY_RATE
                if sectors[sector] < 0.1:
                    del sectors[sector]
            
            if not sectors:
                words_to_remove.append(word)
        
        for word in words_to_remove:
            del self.words[word]
        return len(words_to_remove)
    
    def get_stats(self):
        total = len(self.words)
        seed = sum(len(x) for x in self.SEED_LEXICON.values())
        per_sec = {ax: 0 for ax in self.axes}
        for w, secs in self.words.items():
            for s, v in secs.items():
                if v >= self.PRÓG_AKTYWACJI:
                    per_sec[s] += 1
        return {
            "total": total,
            "seed": seed,
            "learned": max(0, total - seed),
            "per_sector": per_sec,
            "last_learned": self.last_learned
        }

    def display_word_info(self, word):
        norm = self._normalize(word)
        if norm not in self.words:
            print(f"{Colors.FAINT}[Lexicon] '{word}' - Nieznane{Colors.RESET}")
            return
        print(f"{Colors.CYAN}[Lexicon] '{word}':{Colors.RESET}")
        for s, v in sorted(self.words[norm].items(), key=lambda x: -x[1]):
            bar = "█" * int(v * 10)
            print(f"  {s:12} {bar} {v:.2f}")

    def save(self):
        learned_only = {}
        for w, secs in self.words.items():
            is_seed = False
            for sw in self.SEED_LEXICON.values():
                if w in [self._normalize(x) for x in sw]:
                    is_seed = True
                    break
            if not is_seed:
                learned_only[w] = secs
        
        data = {
            "version": "1.1-fixed",
            "words": learned_only,
            "total_learned": self.total_learned
        }
        try:
            with open(self.lexicon_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Błąd zapisu lexiconu: {e}")

    def load(self):
        if not os.path.exists(self.lexicon_file):
            return
        try:
            with open(self.lexicon_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for w, secs in data.get("words", {}).items():
                if w not in self.words:
                    self.words[w] = {}
                for s, v in secs.items():
                    self.words[w][s] = v
            self.total_learned = data.get("total_learned", 0)
        except Exception:
            pass