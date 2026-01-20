# -*- coding: utf-8 -*-
# lexicon.py v6.0.0-Union Compatible
# Zaktualizowano dla EriAmo Union: Obsługa vector_override

import json
import os
import numpy as np
import unidecode
import re
from config import Colors

class EvolvingLexicon:
    # EMOCJONALNE SEED - słowa jako kotwice dla wspomnień
    SEED_LEXICON = {
        # RADOŚĆ - pozytywne doświadczenia, sukces, piękno
        "radość": [
            "radosc", "szczescie", "wesolo", "uciecha", "zadowolenie", "zabawa",
            "smiech", "entuzjazm", "ekscytacja", "triumf", "zwyciestwo", "sukces",
            "piekno", "wspaniale", "cudownie", "zachwyt", "swietnie", "super"
        ],
        
        # SMUTEK - strata, tęsknota, melancholia, żal
        "smutek": [
            "smutek", "zal", "tesknota", "melancholia", "rozpacz", "bol",
            "placz", "lzy", "utrata", "strata", "samotnosc", "osamotnienie",
            "przygnebienie", "depresja", "zgryzota", "rozpamiętywanie", "zmartwionie"
        ],
        
        # STRACH - zagrożenie, niepewność, lęk, panika
        "strach": [
            "strach", "lek", "obawa", "niepokoj", "trwoga", "panika",
            "goza", "przerazenie", "fobia", "lekowy", "niebezpieczenstwo", "zagrożenie",
            "niepewnosc", "watpliwość", "drżenie", "przestraszyc", "alarm"
        ],
        
        # GNIEW - frustracja, złość, niesprawiedliwość
        "gniew": [
            "gniew", "zlosc", "wscieklosc", "furia", "irytacja", "oburzenie",
            "frustracja", "nienawisc", "kłotnia", "konflikt", "agresja", "wkurw",
            "niesprawiedliwosc", "obraza", "zemsta", "bunt", "protest", "walka"
        ],
        
        # MIŁOŚĆ - przywiązanie, czułość, troska, bliskość
        "miłość": [
            "milosc", "kocham", "czulosc", "uczucie", "serce", "przywarzanie",
            "czułość", "tkliwosc", "namiętnosc", "romans", "bliskosc", "intymnosc",
            "troska", "opiek", "rodzina", "przyjazn", "zaufanie", "oddanie",
            "ukochany", "ukochana", "partner", "dziecko"
        ],
        
        # WSTRĘT - odrzucenie, obrzydzenie, niesmak, niechęć
        "wstręt": [
            "wstret", "obrzydzenie", "niesmak", "wstretny", "obrzydliwy", "fuj",
            "odrzucenie", "niechec", "odraza", "obmierzlosc", "nienawsc",
            "toksyczny", "zgniły", "zepsuty", "brud", "plugawy", "odpychajacy"
        ],
        
        # ZASKOCZENIE - nowość, odkrycie, ciekawość, zdziwienie
        "zaskoczenie": [
            "zaskoczenie", "zdziwienie", "niespodzianka", "wow", "ojej", "szok",
            "nowosc", "odkrycie", "rewelacja", "ciekawosc", "zainteresowanie",
            "nieoczekiwany", "niespodziewany", "dziwny", "niezwykly", "zdumienie",
            "fascynacja", "intrygujący", "tajemnica", "cud", "fenomen"
        ],
        
        # AKCEPTACJA - spokój, pewność, harmonia, rezygnacja
        "akceptacja": [
            "akceptacja", "spokoj", "spokojny", "harmonia", "rownowan", "balans",
            "pewnosc", "zaufanie", "ufnosc", "odprezenie", "relaks", "zen",
            "pogodzenie", "rezygnacja", "zgodna", "tolerancja", "zrozumienie",
            "cierpliwosc", "lagodnosc", "uległosc", "pogodzony", "oswajanje"
        ]
    }
    
    # Progi uczenia
    PRÓG_AKTYWACJI = 0.15
    PRÓG_UCZENIA = 0.20
    WAGA_SEED = 1.0
    WAGA_NAUCZONE = 0.8
    DECAY_RATE = 0.99
    MIN_WORD_LENGTH = 3
    REINFORCEMENT_RATE = 0.08
    
    def __init__(self, lexicon_file="lexicon.soul"):
        self.lexicon_file = lexicon_file
        # Kolejność osi musi być zgodna z AII.AXES_ORDER
        self.axes = ["radość", "smutek", "strach", "gniew", "miłość", "wstręt", "zaskoczenie", "akceptacja"]
        self.words = {}
        self.total_learned = 0
        self.last_learned = []
        self._initialize_from_seed()
        self.load()
    
    def _normalize(self, word):
        word = word.lower().strip()
        try:
            word = unidecode.unidecode(word)
        except: pass # Fallback if unidecode fails or not present
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
            
            if enable_reinforcement and dominant_sector:
                for word in used_known_words:
                    self._reinforce_word(word, dominant_sector)
        
        return total_vec, dominant_sector, unknown_words
    
    def _reinforce_word(self, word, sector):
        if word not in self.words:
            return
        current = self.words[word].get(sector, 0.0)
        self.words[word][sector] = min(1.0, current + self.REINFORCEMENT_RATE)
    
    def learn_from_context(self, unknown_words, context_vector, confidence):
        if confidence < self.PRÓG_UCZENIA:
            return []
        
        learned = []
        for word in unknown_words:
            if len(word) < self.MIN_WORD_LENGTH:
                continue
            
            if word not in self.words:
                self.words[word] = {}
            
            for i, axis in enumerate(self.axes):
                dim_strength = context_vector[i]
                if dim_strength > self.PRÓG_AKTYWACJI:
                    initial_weight = self.WAGA_NAUCZONE * dim_strength * confidence
                    current = self.words[word].get(axis, 0.0)
                    self.words[word][axis] = min(1.0, current + initial_weight)
            
            if any(v > 0 for v in self.words[word].values()):
                learned.append((word, self.words[word].copy()))
                self.total_learned += 1
        
        self.last_learned = learned
        return learned
    
    def learn_from_correction(self, word, correct_sector, strength=0.7, vector_override=None):
        """
        Uczy słowa. Obsługuje ręczną korektę LUB bezpośrednie nadpisanie wektora (dla AII v6.0).
        """
        norm_word = self._normalize(word)
        if norm_word not in self.words:
            self.words[norm_word] = {}
            
        # --- FIX: Obsługa vector_override dla AII v6.0 ---
        if vector_override is not None:
            # Przepisujemy wartości z wektora do słownika osi
            for i, axis in enumerate(self.axes):
                if i < len(vector_override):
                    val = float(vector_override[i])
                    if val > 0:
                        self.words[norm_word][axis] = val
            self.total_learned += 1
            return True
        # -------------------------------------------------

        current = self.words[norm_word].get(correct_sector, 0.0)
        self.words[norm_word][correct_sector] = min(1.0, current + strength)
        self.total_learned += 1
        return True
    
    def decay_unused(self):
        words_to_remove = []
        for word, sectors in self.words.items():
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
            "version": "6.0.0-Union-Compatible",
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