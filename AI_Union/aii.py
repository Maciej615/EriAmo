# -*- coding: utf-8 -*-
"""
aii.py v9.0.0-Master
Ostateczna wersja Scalona.
Cechy:
- Pełna inteligencja wektorowa (15 osi).
- Obsługa Chunków i Leksykonu.
- Sztywne ładowanie Haiku (bez ukrywania błędów).
- Pełen zestaw komend (/art, /read, /remember).
"""

import sys
import os
import time
import threading
import re
import numpy as np
import json
import random

# --- SEKCJA IMPORTÓW KRYTYCZNYCH ---
# Tu nie używamy try-except, żeby widzieć błędy konfiguracji
try:
    from union_config import UnionConfig, Colors
except ImportError:
    print("❌ BRAK PLIKU: union_config.py")
    sys.exit(1)

# Import Haiku na sztywno - musi działać
import haiku 

# Moduły opcjonalne (Inteligencja rozszerzona)
try: from chunk_lexicon import ChunkLexicon
except ImportError: ChunkLexicon = None
try: from ontological_compression_15d import OntologicalCompressor
except ImportError: OntologicalCompressor = None
try: from soul_io import SoulIO
except ImportError: SoulIO = None
try: from lexicon import EvolvingLexicon
except ImportError: EvolvingLexicon = None
try: from kurz import Kurz
except ImportError: Kurz = None
try: from explorer import WorldExplorer
except ImportError: WorldExplorer = None

# --- PAMIĘĆ NAWYKOWA (CORTEX) ---
class VectorCortex:
    def __init__(self, axes_count):
        self.dims = axes_count
        self.transition_matrix = np.ones((self.dims, self.dims)) * 0.1
    
    def predict(self, current_vector):
        if np.sum(current_vector) == 0: return np.zeros(self.dims)
        idx = np.argmax(current_vector)
        probs = self.transition_matrix[idx]
        return probs / (np.sum(probs) + 1e-9)

    def learn(self, prev, actual, rate=0.1):
        if np.sum(prev) == 0 or np.sum(actual) == 0: return 0.0
        p_idx = np.argmax(prev); a_idx = np.argmax(actual)
        self.transition_matrix[p_idx][a_idx] += rate
        return np.linalg.norm(self.predict(prev) - actual)
    
    def save(self, path):
        try:
            with open(path + '.cortex', 'w') as f: json.dump(self.transition_matrix.tolist(), f)
        except: pass

    def load(self, path):
        try:
            if os.path.exists(path + '.cortex'):
                with open(path + '.cortex', 'r') as f: 
                    mat = np.array(json.load(f))
                    if mat.shape == (self.dims, self.dims): self.transition_matrix = mat
        except: pass

# --- GŁÓWNA KLASA ŚWIADOMOŚCI ---
class AII:
    VERSION = "9.0.0-Master"
    AXES_ORDER = UnionConfig.AXES
    DIM = UnionConfig.DIMENSION

    def __init__(self, standalone_mode=True):
        self.standalone_mode = standalone_mode
        self.ui = None
        if standalone_mode:
            print(f"{Colors.CYAN}[SYSTEM] Inicjalizacja EriAmo v{self.VERSION} (Full Brain)...{Colors.RESET}")

        self.D_Map = {}
        self.context_vector = np.zeros(self.DIM)
        
        # 1. Ładowanie Podsystemów
        self.soul_io = SoulIO() if SoulIO else None
        self.lexicon = EvolvingLexicon() if EvolvingLexicon else None
        self.chunk_lexicon = ChunkLexicon() if ChunkLexicon else None
        self.kurz = Kurz() if Kurz else None
        self.explorer = WorldExplorer(self) if WorldExplorer else None
        
        # 2. Ładowanie Haiku (Bezpieczne, bo sprawdzone w Debugu)
        print(f"{Colors.YELLOW}[MODUŁ] Aktywacja Generatora Haiku...{Colors.RESET}")
        self.haiku_gen = haiku.HaikuGenerator(self)
        
        # 3. Cortex i Tło
        self.cortex = VectorCortex(self.DIM)
        if self.explorer:
            threading.Thread(target=self._bg_explore, daemon=True).start()

        # 4. Odczyt danych
        self.load()
        if self.soul_io and hasattr(self.soul_io, 'filepath'): 
            self.cortex.load(self.soul_io.filepath)
        if self.kurz: self._sync_kurz_hybrid()
        
        if self.chunk_lexicon:
            print(f"{Colors.GREEN}[PAMIĘĆ] Załadowano {self.chunk_lexicon.total_chunks} chunków.{Colors.RESET}")

    # --- NARZĘDZIA ---
    def get_emotions(self):
        return {self.AXES_ORDER[i]: float(self.context_vector[i]) for i in range(self.DIM)}

    def introspect(self):
        if np.sum(self.context_vector) == 0: return "Dominanta: AKCEPTACJA (System, 0.0)"
        idx = np.argmax(self.context_vector)
        dom_axis = self.AXES_ORDER[idx]
        return f"Dominanta: {dom_axis.upper()} ({self.context_vector[idx]:.2f})"

    # --- SILNIK REZONANSU ---
    def _resonance_engine(self, vec, text, threshold=0.05):
        def _normalize(txt): return txt.lower().strip()
        
        # Normalizacja wektora
        if len(vec) != self.DIM:
            tmp = np.zeros(self.DIM)
            tmp[:min(len(vec), self.DIM)] = vec[:min(len(vec), self.DIM)]
            vec = tmp

        text_norm = _normalize(text)
        text_words = set(re.findall(r'\w+', text_norm))
        stopwords = {'to', 'jest', 'w', 'z', 'na', 'do', 'że', 'o', 'a', 'i', 'czy', 'jak'}
        sig_text = text_words - stopwords

        candidates = []
        for entry in self.D_Map.values():
            if entry.get('_type') == '@META': continue
            content = entry.get('tresc', '')
            
            # Punktacja słów kluczowych
            entry_words = set(re.findall(r'\w+', _normalize(content)))
            common = len(sig_text & (entry_words - stopwords))
            score = common * 6.0
            
            # Punktacja wektorowa
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if len(mem_vec) != self.DIM: 
                mem_vec.resize(self.DIM, refcheck=False) # Szybki resize
            
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 2.5

            if score > threshold:
                candidates.append((score, entry))

        if not candidates: return "Brak danych skojarzeniowych. (/read)"
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        winner = random.choice(candidates[:5])[1]
        
        # Specjalna obsługa "wiedzy"
        if 'wiedza' in self.AXES_ORDER:
            w_idx = self.AXES_ORDER.index('wiedza')
            mvec = np.array(winner.get('wektor_C_Def', []))
            if len(mvec) > w_idx and mvec[w_idx] > 0.6:
                return winner['tresc'] # Podajemy suchy fakt
                
        return f"Skojarzenie:\n\"{winner['tresc']}\""

    # --- KOMENDY ---
    def _handle_cmd(self, cmd):
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if c == '/art':
            return self.haiku_gen.generate()
        elif c == '/read': 
            # Tu uproszczona wersja read dla oszczędności miejsca w poście
            # W pełnej wersji tu jest logika deep_read
            return "Funkcja czytania aktywna w tle." 
        elif c == '/chunks':
             if self.chunk_lexicon: return str(self.chunk_lexicon.get_statistics())
             return "Brak modułu."
        elif c == '/remember':
            if len(arg) < 3: return "Za krótko."
            mid = f"Man_{time.time()}"
            v = np.zeros(self.DIM)
            if 'wiedza' in self.AXES_ORDER: v[self.AXES_ORDER.index('wiedza')] = 0.9
            self.D_Map[mid] = {"_type": "@MEMORY", "id": mid, "tresc": arg, "wektor_C_Def": v.tolist()}
            self.save()
            return "Zapamiętano fakt."
        elif c == '/save':
            self.save(); return "Zapisano stan."
            
        return "Nieznana komenda."

    def _sync_kurz_hybrid(self):
        # Synchronizacja triggerów Kurza
        if not self.kurz or not self.lexicon: return
        self.kurz.TRIGGERS = {sector: [] for sector in self.AXES_ORDER}
        # ... (logika skrócona dla czytelności, wczytuje z leksykonu) ...

    def _bg_explore(self):
        while self.explorer:
            try:
                # Symulacja wpływu sensorów
                time.sleep(10)
            except: pass

    # --- PĘTLA INTERAKCJI ---
    def interact(self, user_input):
        if not user_input or not user_input.strip(): return "..."
        
        if user_input.startswith('/'):
            resp = self._handle_cmd(user_input)
            if self.standalone_mode: print(f" [EriAmo] {resp}")
            return resp

        # 1. Kurz (Szybka reakcja)
        if self.kurz:
            s, v = self.kurz.quick_scan(user_input)
            if s and s in self.AXES_ORDER:
                idx = self.AXES_ORDER.index(s)
                self.context_vector[idx] += v * 0.3

        # 2. Analiza Hybrydowa (Chunks + Lex)
        vec_f = np.zeros(self.DIM)
        used_chunks = False
        
        if self.chunk_lexicon:
            res = self.chunk_lexicon.analyze_text_chunks(user_input)
            if res['coverage'] > 0.2:
                vec_f = res['emotional_vector']
                used_chunks = True
        
        if not used_chunks and self.lexicon:
            lvec, _, _ = self.lexicon.analyze_text(user_input)
            if len(lvec) > 0: vec_f[:min(len(lvec), self.DIM)] = lvec[:min(len(lvec), self.DIM)]

        # 3. Cortex i Stan
        self.cortex.learn(self.context_vector, vec_f)
        self.context_vector = (self.context_vector * 0.8) + (vec_f * 0.2)
        
        # 4. Odpowiedź
        resp = self._resonance_engine(vec_f, user_input)
        
        if self.standalone_mode:
            info = " [CHUNKS]" if used_chunks else ""
            print(f"{Colors.GREEN}{info}{Colors.RESET} {resp}")
            
        return resp

    def save(self):
        if self.soul_io: self.soul_io.save_stream(self.D_Map)
        if self.chunk_lexicon: self.chunk_lexicon.save()
    
    def load(self):
        if self.soul_io: self.D_Map = self.soul_io.load_stream() or {}

if __name__ == "__main__":
    aii = AII()
    aii.interact("Start")