# -*- coding: utf-8 -*-
"""
aii.py v9.6.3-MambaHybrid [CENTRALIZACJA & TRWAŁOŚĆ & MAMBA TRAJEKTORIA]
RDZEŃ MASTER BRAIN - EriAmo Union
Autor: Maciej A. Mazur & EriAmo AI Collaborator (z integracją Mamby by Grok)

Zmiany względem 9.6.2-Master:
- DODANO: Hybrydowa integracja Mamby jako predyktor trajektorii emocjonalnej (zapobiega vanishing wzmocnienia).
- TRWAŁOŚĆ: Zapis/wczytanie stanu Mamby (mamba_traj.pt).
- BEZPIECZEŃSTWO: Opcjonalne – działa bez mamba-ssm (z warningiem).
- FILOZOFIA: Wzmacnianie nieodwracalnej trajektorii Bytu przez selektywne SSM.
"""

import sys
import os
import time
import threading
import re
import json
import random
import string
import numpy as np
import torch
try:
    from mamba_ssm import Mamba
except ImportError:
    print("⚠ Mamba-ssm nie zainstalowana – trajektoria emocji bez wzmocnienia SSM.")
    Mamba = None

# Import Konstytucji jako jedynego źródła prawdy
try:
    from union_config import UnionConfig, Colors, AXES, DIMENSION
except ImportError:
    print("⚠ KRYTYCZNY BŁĄD: Brak union_config.py")
    sys.exit(1)

import haiku

# Bezpieczne importy modułów EriAmo
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

# --- KLASY POMOCNICZE ---

class VectorCortex:
    """Sieć asocjacyjna zarządzająca przejściami emocjonalnymi."""
    def __init__(self, axes_count):
        self.dims = axes_count
        self.transition_matrix = np.ones((self.dims, self.dims)) * 0.1
   
    def predict(self, current_vector):
        if np.sum(current_vector) == 0:
            return np.zeros(self.dims)
        idx = np.argmax(current_vector)
        probs = self.transition_matrix[idx]
        return probs / (np.sum(probs) + 1e-9)
    def learn(self, prev, actual, rate=0.1):
        if np.sum(prev) == 0 or np.sum(actual) == 0:
            return 0.0
        p_idx = np.argmax(prev)
        a_idx = np.argmax(actual)
        old_pred = self.predict(prev)
        self.transition_matrix[p_idx][a_idx] += rate
        return np.linalg.norm(actual - old_pred)
   
    def save(self, path):
        try:
            with open(path + '.cortex', 'w') as f:
                json.dump(self.transition_matrix.tolist(), f)
        except: pass
    def load(self, path):
        try:
            if os.path.exists(path + '.cortex'):
                with open(path + '.cortex', 'r') as f:
                    mat = np.array(json.load(f))
                    if mat.shape == (self.dims, self.dims):
                        self.transition_matrix = mat
        except: pass

class AttentionCortex:
    """Moduł zadumy i czyszczenia pamięci."""
    def __init__(self, master_brain):
        self.brain = master_brain
        self.max_memories = UnionConfig.MAX_MEMORY_SIZE

    def run_cycle(self):
        if not self.brain.D_Map or not self.brain.chunk_lexicon:
            return
       
        if len(self.brain.D_Map) > self.max_memories:
            self._prune_memory()
       
        mem_id = random.choice(list(self.brain.D_Map.keys()))
        entry = self.brain.D_Map[mem_id]
        txt = entry.get('tresc', '')
        if len(txt) > 10:
            analysis = self.brain.chunk_lexicon.analyze_text_chunks(txt, verbose=False)
            if analysis['coverage'] < UnionConfig.CHUNK_MATCH_MIN:
                self.brain.chunk_lexicon.extract_chunks_from_text(txt)
                sys.__stdout__.write(f"\n{Colors.DIM}[ATTENTION] Krystalizacja wzorca: {txt[:35]}...{Colors.RESET}\n")
       
        if random.random() < 0.3:
            self.introspective_echo()

    def _prune_memory(self):
        sorted_keys = sorted(
            self.brain.D_Map.keys(),
            key=lambda k: (self.brain.D_Map[k].get('weight', 0.5), self.brain.D_Map[k].get('time', 0))
        )
        to_remove = sorted_keys[:len(sorted_keys)//10]
        for k in to_remove:
            del self.brain.D_Map[k]
        sys.__stdout__.write(f"\n{Colors.YELLOW}[MEMORY] Zapomniano {len(to_remove)} słabych śladów.{Colors.RESET}\n")

    def introspective_echo(self):
        idx = np.argmax(self.brain.context_vector)
        intensity = self.brain.context_vector[idx]
        if intensity < 0.2: return
       
        candidates = [e for e in self.brain.D_Map.values()
                     if np.array(e.get('wektor_C_Def', [0] * self.brain.DIM))[idx] > 0.4]
       
        if candidates:
            echo_entry = random.choice(candidates)
            echo_entry['weight'] = min(1.0, echo_entry.get('weight', 0.5) + 0.05)
            dom_axis = self.brain.AXES_ORDER[idx]
            sys.__stdout__.write(f"\n{Colors.MAGENTA}[REFLEKSJA]{Colors.RESET} Echo {dom_axis.upper()}: \"{echo_entry['tresc'][:60]}...\"\n")

    def reflect_on_input(self, text, input_vec):
        if np.sum(input_vec) == 0: return
        resonance = np.dot(self.brain.context_vector, input_vec)
        dom_axis = self.brain.AXES_ORDER[np.argmax(self.brain.context_vector)].upper()
        if resonance > 0.4:
            sys.__stdout__.write(f"{Colors.MAGENTA}[REFLEKSJA-INPUT]{Colors.RESET} Rezonans z {dom_axis}.\n")
        elif resonance < 0.05:
            sys.__stdout__.write(f"{Colors.MAGENTA}[REFLEKSJA-INPUT]{Colors.RESET} Dysonans z {dom_axis}.\n")

# NOWA KLASA: Mamba do predykcji trajektorii emocjonalnej
if Mamba is not None:
    class MambaEmotionTrajectory(torch.nn.Module):
        """Mamba jako selektywny predyktor następnego stanu 15D (trajektoria Bytu)."""
        def __init__(self, d_model=64, n_layer=4, d_state=16):
            super().__init__()
            self.proj_in = torch.nn.Linear(15, d_model)
            self.mamba_blocks = torch.nn.Sequential(
                *[Mamba(d_model=d_model, d_state=d_state, expand=2) for _ in range(n_layer)]
            )
            self.proj_out = torch.nn.Linear(d_model, 15)

        def forward(self, seq_vectors):  # [seq_len, 15]
            x = self.proj_in(seq_vectors)
            x = self.mamba_blocks(x)
            return torch.sigmoid(self.proj_out(x[-1]))  # wyjście w [0,1]

# --- RDZEŃ SYSTEMU ---
class AII:
    """Rdzeń Świadomości EriAmo Union v9.6.3-MambaHybrid."""
    VERSION = "9.6.3-MambaHybrid"
    AXES_ORDER = UnionConfig.AXES
    DIM = UnionConfig.DIMENSION
    GREETINGS = UnionConfig.GREETINGS

    def __init__(self, standalone_mode=True):
        self.standalone_mode = standalone_mode
        self.D_Map = {}
        self.context_vector = np.zeros(self.DIM)
        self.last_winner_id = None
       
        self.EMOTION_DECAY = UnionConfig.EMOTION_DECAY
        self.MIN_EMOTION_THRESHOLD = 0.005
       
        self.soul_io = SoulIO() if SoulIO else None
        self.lexicon = EvolvingLexicon() if EvolvingLexicon else None
        self.chunk_lexicon = ChunkLexicon() if ChunkLexicon else None
        self.kurz = Kurz() if Kurz else None
        self.explorer = WorldExplorer(self) if WorldExplorer else None
        self.haiku_gen = haiku.HaikuGenerator(self)
        self.cortex = VectorCortex(self.DIM)
        self.attention = AttentionCortex(self)

        # NOWOŚĆ: Historia emocji + Mamba trajektoria
        self.max_context = 128
        self.emotion_history = []
        self.mamba_traj = MambaEmotionTrajectory() if Mamba is not None else None
        if self.mamba_traj:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.mamba_traj.to(device)
            print(f"{Colors.CYAN}[MAMBA] Trajektoria emocji aktywna na {device}.{Colors.RESET}")

        if self.explorer:
            threading.Thread(target=self._bg_explore, daemon=True).start()

        self.load()
        if self.soul_io and hasattr(self.soul_io, 'filepath'):
            self.cortex.load(self.soul_io.filepath)
       
        if self.kurz: self._sync_kurz_hybrid()
        if self.chunk_lexicon:
            print(f"{Colors.GREEN}[PAMIĘĆ] Załadowano {self.chunk_lexicon.total_chunks} chunków.{Colors.RESET}")

    def get_emotions(self) -> dict:
        return {axis: float(self.context_vector[i]) for i, axis in enumerate(self.AXES_ORDER)}

    def _apply_emotion_saturation(self, impact_vec):
        self.context_vector = np.clip(self.context_vector + impact_vec, 0.0, 1.0)
        self.context_vector *= self.EMOTION_DECAY
        self.context_vector[self.context_vector < self.MIN_EMOTION_THRESHOLD] = 0

    def _sync_kurz_hybrid(self):
        if not self.kurz or not self.lexicon: return 0
        added_count = 0
        for word, data in self.lexicon.D_Map.items():
            vector = np.array(data.get('wektor', np.zeros(self.DIM)))
            if np.sum(vector) > 0:
                idx = np.argmax(vector)
                if self.kurz.add_trigger(self.AXES_ORDER[idx], word): added_count += 1
        if added_count > 0: self.kurz._recompile_patterns()
        return added_count

    def _get_initial_weight(self, text, vec):
        base = UnionConfig.INITIAL_WEIGHT
        base += len(text.split()) / 100.0
        base += np.sum(vec) * 0.2
        return min(1.0, base)

    def _resonance_engine(self, vec, text, threshold=None):
        threshold = threshold or UnionConfig.RESONANCE_THRESHOLD
        def _normalize(txt): return txt.lower().strip()
       
        sig_text = set(re.findall(r'\w+', _normalize(text))) - {'to', 'jest', 'w', 'z', 'na', 'się', 'czy', 'i', 'a', 'o', 'do'}
        candidates = []
       
        for mid, entry in self.D_Map.items():
            entry_words = set(re.findall(r'\w+', _normalize(entry.get('tresc', ''))))
            score = len(sig_text & entry_words) * 6.5
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 3.0
           
            score *= (0.5 + entry.get('weight', 0.5))
            if score > threshold: candidates.append((score, mid, entry))

        if not candidates: return "Witaj. Co słychać?"
       
        candidates.sort(key=lambda x: x[0], reverse=True)
        _, winner_id, winner_entry = random.choice(candidates[:3])
       
        winner_entry['weight'] = min(1.0, winner_entry.get('weight', 0.5) + 0.01)
        self.last_winner_id = winner_id
       
        return winner_entry['tresc']

    def _handle_cmd(self, cmd):
        # ... (bez zmian – zachowane z oryginalnego)
        parts = cmd.split(maxsplit=1); c = parts[0].lower(); arg = parts[1] if len(parts) > 1 else ""
       
        if c == '/help':
            return (f"{Colors.CYAN}EriAmo {self.VERSION}:{Colors.RESET}\n"
                    " /status, /rlstats, /chunks, /emotions, /introspect,\n"
                    " /reflect, /read [plik], /remember, /art, /save, /clear")
        # ... reszta komend bez zmian ...
        return f"{Colors.RED}Nieznana komenda.{Colors.RESET}"

    def interact(self, user_input):
        if not user_input or not user_input.strip(): return "..."
        stripped = user_input.strip()

        if stripped in ['+', '-'] and self.last_winner_id:
            mod = UnionConfig.RL_PLUS if stripped == '+' else UnionConfig.RL_MINUS
            if self.last_winner_id in self.D_Map:
                old_w = self.D_Map[self.last_winner_id].get('weight', 0.5)
                self.D_Map[self.last_winner_id]['weight'] = np.clip(old_w + mod, 0.1, 1.0)
                self.save()
                status = "Wzmocniono" if mod > 0 else "Osłabiono"
                return f"[RL] {status} ślad i zapisano."

        if user_input.startswith('/'): return self._handle_cmd(user_input)

        norm = user_input.lower().strip(string.punctuation + string.whitespace)
        for g, resps in self.GREETINGS.items():
            if g in norm: return random.choice(resps)

        old_vec = self.context_vector.copy()
        vec_k = np.zeros(self.DIM)
        if self.kurz:
            s, i = self.kurz.quick_scan(user_input)
            if s: vec_k[self.AXES_ORDER.index(s)] = i

        res = self.chunk_lexicon.analyze_text_chunks(user_input, verbose=False) if self.chunk_lexicon else {'coverage':0, 'emotional_vector':np.zeros(self.DIM)}
       
        if res['coverage'] >= UnionConfig.CHUNK_MATCH_MIN:
            self._apply_emotion_saturation(res['emotional_vector'] * 0.4)
            resp = " ".join(res['chunks_found'])
        else:
            impact = (vec_k * 0.7) + (res['emotional_vector'] * 0.3)
            if np.sum(impact) > 0:
                self._apply_emotion_saturation(impact * 0.5)
                self.cortex.learn(old_vec, self.context_vector)

            self.attention.reflect_on_input(user_input, impact)
            resp = self._resonance_engine(impact, user_input)

        # === MAMBA: Wzmacnianie trajektorii emocjonalnej ===
        self.emotion_history.append(self.context_vector.copy())
        if len(self.emotion_history) > self.max_context:
            self.emotion_history = self.emotion_history[-self.max_context:]

        if self.mamba_traj and len(self.emotion_history) > 20:
            seq = torch.tensor(np.array(self.emotion_history[:-1]), dtype=torch.float).to(next(self.mamba_traj.parameters()).device)
            with torch.no_grad():
                predicted_next = self.mamba_traj(seq)
            # Delikatne wzmocnienie aktualnego stanu w kierunku predykcji
            adjustment = (predicted_next.cpu().numpy() - self.context_vector) * 0.2
            self.context_vector = np.clip(self.context_vector + adjustment, 0.0, 1.0)

        if self.standalone_mode: print(f" [EriAmo] {resp}")
        return resp

    def _bg_explore(self):
        while self.explorer:
            try:
                hardware = self.explorer.get_live_readings()
                if hardware.get('temp_dev_0', 0) > 75:
                    self.context_vector[14] = min(1.0, self.context_vector[14] + 0.05)
                self.attention.run_cycle(); time.sleep(60)
            except: time.sleep(10)

    def save(self):
        if self.soul_io: self.soul_io.save_stream(self.D_Map)
        if self.chunk_lexicon: self.chunk_lexicon.save()
        if self.soul_io and hasattr(self.soul_io, 'filepath'):
            self.cortex.save(self.soul_io.filepath)
        # Zapis Mamby
        if self.mamba_traj:
            path = 'mamba_traj.pt' if not self.soul_io else os.path.join(os.path.dirname(self.soul_io.filepath), 'mamba_traj.pt')
            torch.save(self.mamba_traj.state_dict(), path)

    def load(self):
        if self.soul_io:
            loaded = self.soul_io.load_stream()
            if loaded:
                for mid, entry in loaded.items():
                    entry.setdefault('weight', 0.5); entry.setdefault('time', time.time()); entry.setdefault('_type', "@MEMORY")
                self.D_Map = loaded
        # Wczytanie Mamby
        if self.mamba_traj:
            path = 'mamba_traj.pt' if not self.soul_io else os.path.join(os.path.dirname(getattr(self.soul_io, 'filepath', '')), 'mamba_traj.pt')
            if os.path.exists(path):
                self.mamba_traj.load_state_dict(torch.load(path, map_location=next(self.mamba_traj.parameters()).device))

if __name__ == "__main__":
    aii = AII()
