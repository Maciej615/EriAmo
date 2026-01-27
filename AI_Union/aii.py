# -*- coding: utf-8 -*-
"""
aii.py v9.3.1-Master
RDZEŃ MASTER BRAIN - EriAmo Union
Autor: Maciej A. Mazur

ZMIANY v9.3.1:
- ✅ FIXED: _sync_kurz_hybrid teraz faktycznie ładuje słowa z lexicon.soul do KuRz.
- ✅ FIXED: Poprawiona logika aktualizacji wektora (silniejszy wpływ emocji).
- ✅ ZACHOWANO: Chunks, Resonance Engine, VectorCortex.
"""

import sys
import os
import time
import threading
import re
import numpy as np
import json
import random

try:
    from union_config import UnionConfig, Colors
except ImportError:
    print("⚠ KRYTYCZNY BŁĄD: Brak union_config.py")
    sys.exit(1)

import haiku 

try: from chunk_lexicon import ChunkLexicon
except ImportError: ChunkLexicon = None
try: from soul_io import SoulIO
except ImportError: SoulIO = None
try: from lexicon import EvolvingLexicon
except ImportError: EvolvingLexicon = None
try: from kurz import Kurz
except ImportError: Kurz = None
try: from explorer import WorldExplorer
except ImportError: WorldExplorer = None

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

class AII:
    VERSION = "9.3.1-Master"
    AXES_ORDER = UnionConfig.AXES
    DIM = UnionConfig.DIMENSION

    def __init__(self, standalone_mode=True):
        self.standalone_mode = standalone_mode
        self.D_Map = {}
        self.context_vector = np.zeros(self.DIM)
        
        # PARAMETRY EMOCJI
        self.EMOTION_DECAY = 0.95  # Wolniejsze wygasanie dla stabilności
        self.MIN_EMOTION_THRESHOLD = 0.005
        
        self.soul_io = SoulIO() if SoulIO else None
        self.lexicon = EvolvingLexicon() if EvolvingLexicon else None
        self.chunk_lexicon = ChunkLexicon() if ChunkLexicon else None
        self.kurz = Kurz() if Kurz else None
        self.explorer = WorldExplorer(self) if WorldExplorer else None
        self.haiku_gen = haiku.HaikuGenerator(self)
        self.cortex = VectorCortex(self.DIM)

        if self.explorer:
            threading.Thread(target=self._bg_explore, daemon=True).start()

        self.load()
        if self.soul_io and hasattr(self.soul_io, 'filepath'): 
            self.cortex.load(self.soul_io.filepath)
        
        # ✅ KLUCZOWA SYNCHRONIZACJA
        if self.kurz:
            self._sync_kurz_hybrid()
            print(f"{Colors.GREEN}[KURZ] Aktywowano {self.kurz.get_all_triggers_count()} odruchów.{Colors.RESET}")
        
        if self.chunk_lexicon:
            print(f"{Colors.GREEN}[PAMIĘĆ] Załadowano {self.chunk_lexicon.total_chunks} chunków.{Colors.RESET}")

    def get_emotions(self):
        return {self.AXES_ORDER[i]: round(float(self.context_vector[i]), 3) for i in range(self.DIM)}

    def introspect(self):
        if np.sum(self.context_vector) < self.MIN_EMOTION_THRESHOLD: 
            return f"{Colors.FAINT}Dominanta: NEUTRALNY (brak emocji){Colors.RESET}"
        idx = np.argmax(self.context_vector)
        dom_axis = self.AXES_ORDER[idx]
        intensity = self.context_vector[idx]
        return f"Dominanta: {Colors.MAGENTA}{dom_axis.upper()}{Colors.RESET} ({intensity:.2f})"

    def _apply_emotion_decay(self):
        self.context_vector *= self.EMOTION_DECAY
        self.context_vector[self.context_vector < self.MIN_EMOTION_THRESHOLD] = 0

    def _sync_kurz_hybrid(self):
        """Pobiera definicje emocji z lexicon.soul i wstrzykuje do KuRz."""
        if not self.kurz or not self.lexicon or not hasattr(self.lexicon, 'D_Map'): return
        
        added_count = 0
        for word, data in self.lexicon.D_Map.items():
            vector = np.array(data.get('wektor', np.zeros(self.DIM)))
            if np.sum(vector) > 0:
                # Znajdź oś o najwyższej wartości
                idx = np.argmax(vector)
                sector = self.AXES_ORDER[idx]
                # Dodaj do triggerów Kurz
                if self.kurz.add_trigger(sector, word):
                    added_count += 1
        
        if added_count > 0:
            self.kurz._recompile_patterns()

    def _resonance_engine(self, vec, text, threshold=0.05):
        def _normalize(txt): return txt.lower().strip()
        sig_text = set(re.findall(r'\w+', _normalize(text))) - {'to', 'jest', 'w', 'z', 'na', 'czy'}

        candidates = []
        for entry in self.D_Map.values():
            content = entry.get('tresc', '')
            entry_words = set(re.findall(r'\w+', _normalize(content)))
            score = len(sig_text & entry_words) * 6.0
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 2.5
            if score > threshold:
                candidates.append((score, entry))

        if not candidates: return "Brak danych skojarzeniowych. (/read)"
        candidates.sort(key=lambda x: x[0], reverse=True)
        winner = random.choice(candidates[:3])[1]
        
        if 'wiedza' in self.AXES_ORDER:
            w_idx = self.AXES_ORDER.index('wiedza')
            mvec = np.array(winner.get('wektor_C_Def', []))
            if len(mvec) > w_idx and mvec[w_idx] > 0.6:
                return winner['tresc']
        return f"Skojarzenie:\n\"{winner['tresc']}\""

    def _handle_cmd(self, cmd):
        parts = cmd.split(maxsplit=1)
        c, arg = parts[0].lower(), parts[1] if len(parts) > 1 else ""
        
        if c == '/art': return self.haiku_gen.generate()
        elif c == '/introspect': return self.introspect()
        elif c == '/emotions': 
            emo = self.get_emotions()
            return "\n".join([f"  {k:12}: {'█' * int(v*20)} {v:.3f}" for k, v in emo.items()])
        elif c == '/read':
            if not os.path.exists(arg): return f"Błąd: Nie widzę pliku {arg}"
            with open(arg, 'r', encoding='utf-8') as f: lines = f.readlines()
            total = len(lines)
            print(f"{Colors.CYAN}[EXPLORER] Deep Read: {arg}{Colors.RESET}")
            for i, line in enumerate(lines):
                line = line.strip()
                if not line: continue
                # Logika chunkowania
                max_len = 200
                text_chunks = [line[k:k+max_len] for k in range(0, len(line), max_len)]
                parent_id = f"Read_{int(time.time())}_{i}"
                for idx, chunk_text in enumerate(text_chunks):
                    if self.chunk_lexicon:
                        self.chunk_lexicon.analyze_text_chunks(chunk_text, verbose=False)
                        self.chunk_lexicon.extract_chunks_from_text(chunk_text)
                    mid = f"{parent_id}_ch{idx}"
                    self.D_Map[mid] = {
                        "tresc": chunk_text, 
                        "wektor_C_Def": self.context_vector.tolist(),
                        "chunk": {"idx": idx, "total": len(text_chunks), "parent": parent_id}
                    }
                # Pasek postępu
                if i % (max(1, total // 20)) == 0 or i == total - 1:
                    p = int((i + 1) / total * 100)
                    sys.stdout.write(f"\r{Colors.YELLOW}  Postęp: [{'█'*(p//5)}{'-'*(20-p//5)}] {p}%{Colors.RESET}")
                    sys.stdout.flush()
            self.save()
            return f"\n{Colors.GREEN}[SUKCES] Wiedza zintegrowana.{Colors.RESET}"
        elif c == '/remember':
            mid = f"Man_{time.time()}"
            self.D_Map[mid] = {"tresc": arg, "wektor_C_Def": self.context_vector.tolist()}
            self.save(); return "Zapamiętano."
        elif c == '/save': self.save(); return "Zapisano stan."
        return "Nieznana komenda."

    def _bg_explore(self):
        while self.explorer:
            try: time.sleep(10)
            except: pass

    def interact(self, user_input):
        if not user_input or not user_input.strip(): return "..."
        if user_input.startswith('/'): return self._handle_cmd(user_input)

        # 1. Decay
        self._apply_emotion_decay()

        # 2. Skan KuRz (Odruchy)
        vec_k = np.zeros(self.DIM)
        if self.kurz:
            sector, intensity = self.kurz.quick_scan(user_input)
            if sector:
                s_idx = self.AXES_ORDER.index(sector)
                vec_k[s_idx] = intensity
                print(f"{Colors.MAGENTA}[KURZ] Odruch: {sector.upper()} ({intensity:.2f}){Colors.RESET}")

        # 3. Analiza Chunków
        vec_f = np.zeros(self.DIM)
        if self.chunk_lexicon:
            res = self.chunk_lexicon.analyze_text_chunks(user_input, verbose=True)
            if res['coverage'] == 1.0:
                resp = " ".join(res['chunks_found'])
                if self.standalone_mode: print(f" [EriAmo] {resp}")
                return resp
            vec_f = res['emotional_vector']

        # 4. Sumowanie wpływu i aktualizacja
        # Łączymy odruch Kurz z analizą semantyczną Chunków
        combined_impact = (vec_k * 0.7) + (vec_f * 0.3)
        if np.sum(combined_impact) > 0:
            self.context_vector = (self.context_vector * 0.5) + (combined_impact * 0.5)
        
        # 5. Ucz cortex i generuj odpowiedź
        self.cortex.learn(self.context_vector, combined_impact)
        resp = self._resonance_engine(combined_impact, user_input)
        
        if self.standalone_mode: print(f" [EriAmo] {resp}")
        return resp

    def save(self):
        if self.soul_io: self.soul_io.save_stream(self.D_Map)
        if self.chunk_lexicon: self.chunk_lexicon.save()
        if self.soul_io and hasattr(self.soul_io, 'filepath'): self.cortex.save(self.soul_io.filepath)

    def load(self):
        if self.soul_io: self.D_Map = self.soul_io.load_stream() or {}

if __name__ == "__main__":
    aii = AII()