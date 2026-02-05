# -*- coding: utf-8 -*-
"""
aii.py v9.7.0-PFC – poprawiona wersja (05.02.2026)
RDZEŃ MASTER BRAIN - EriAmo Union + Prefrontal Cortex
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
import torch.nn as nn
import torch.optim as optim

try:
    from union_config import UnionConfig, Colors
except ImportError:
    print("⚠ KRYTYCZNY BŁĄD: Brak union_config.py")
    sys.exit(1)

import haiku

# Opcjonalne moduły z fallbackami
try: from chunk_lexicon import ChunkLexicon
except: ChunkLexicon = None

try: from soul_io import SoulIO
except: SoulIO = None

try: from lexicon import EvolvingLexicon
except: EvolvingLexicon = None

try: from kurz import Kurz
except: Kurz = None

try: from explorer import WorldExplorer
except: WorldExplorer = None

try: from prefrontal_cortex import PrefrontalCortex
except:
    PFC_AVAILABLE = False
    print("⚠ Prefrontal Cortex niedostępny")
else:
    PFC_AVAILABLE = True

try:
    from fractal_memory import FractalMemory, integrate_fractal_memory
    FRACTAL_AVAILABLE = True
except:
    FRACTAL_AVAILABLE = False


# ────────────────────────────────────────────────────────────────
# KLASY POMOCNICZE (bez zmian wcięciowych)
# ────────────────────────────────────────────────────────────────

class VectorCortex:
    def __init__(self, axes_count):
        self.dims = axes_count
        self.hidden_dim = 32
        self.model = nn.Sequential(
            nn.Linear(self.dims, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.dims),
            nn.Softmax(dim=0)
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.MSELoss()

    def predict(self, current_vector):
        current_vector = np.array(current_vector)
        if np.sum(current_vector) == 0:
            return np.zeros(self.dims)
        tensor_in = torch.tensor(current_vector, dtype=torch.float32)
        with torch.no_grad():
            pred = self.model(tensor_in)
        return pred.numpy()

    def learn(self, prev, actual):
        prev = np.array(prev)
        actual = np.array(actual)
        if np.sum(prev) == 0 or np.sum(actual) == 0:
            return 0.0
        tensor_prev = torch.tensor(prev, dtype=torch.float32)
        tensor_actual = torch.tensor(actual, dtype=torch.float32)
        self.optimizer.zero_grad()
        pred = self.model(tensor_prev)
        loss = self.criterion(pred, tensor_actual)
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def save(self, path):
        try:
            torch.save(self.model.state_dict(), f"{path}.cortex.pt")
        except:
            pass

    def load(self, path):
        try:
            if os.path.exists(f"{path}.cortex.pt"):
                self.model.load_state_dict(torch.load(f"{path}.cortex.pt"))
        except:
            pass


class AttentionCortex:
    def __init__(self, master_brain):
        self.brain = master_brain
        self.max_memories = 50000

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
            if analysis['coverage'] < 0.7:
                self.brain.chunk_lexicon.extract_chunks_from_text(txt)
                print(f"{Colors.DIM}[ATTENTION] Krystalizacja: {txt[:35]}...{Colors.RESET}")
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
        print(f"{Colors.YELLOW}[MEMORY] Zapomniano {len(to_remove)} śladów.{Colors.RESET}")

    def introspective_echo(self):
        idx = np.argmax(self.brain.context_vector)
        intensity = self.brain.context_vector[idx]
        if intensity < 0.2:
            return
        candidates = []
        for entry in self.brain.D_Map.values():
            mem_vec = np.array(entry.get('wektor_C_Def', [0] * 15))
            if len(mem_vec) > idx and mem_vec[idx] > 0.4:
                candidates.append(entry)
        if candidates:
            echo = random.choice(candidates)
            echo['weight'] = min(1.0, echo.get('weight', 0.5) + 0.05)
            dom = self.brain.AXES_ORDER[idx].upper()
            print(f"{Colors.MAGENTA}[REFLEKSJA]{Colors.RESET} Echo {dom}: \"{echo['tresc'][:60]}...\"")

    def reflect_on_input(self, text, input_vec):
        if np.sum(input_vec) == 0:
            return
        resonance = np.dot(self.brain.context_vector, input_vec)
        dom = self.brain.AXES_ORDER[np.argmax(self.brain.context_vector)].upper()
        if resonance > 0.4:
            print(f"{Colors.MAGENTA}[REFLEKSJA-INPUT]{Colors.RESET} Rezonans z {dom}.")
        elif resonance < 0.05:
            print(f"{Colors.MAGENTA}[REFLEKSJA-INPUT]{Colors.RESET} Dysonans z {dom}.")


# ────────────────────────────────────────────────────────────────
# GŁÓWNA KLASA AII
# ────────────────────────────────────────────────────────────────

class AII:
    VERSION = "9.7.0-PFC"
    AXES_ORDER = UnionConfig.AXES
    DIM = UnionConfig.DIMENSION

    GREETINGS = {
        "cześć": ["Cześć!", "Hej!", "Witaj!"],
        "hej": ["Hej!", "Cześć!", "Siema!"],
        "hi": ["Hi!", "Hello!", "Hey!"],
        "hello": ["Hello!", "Witaj!", "Cześć!"],
        "dzień dobry": ["Dzień dobry!", "Witaj rano!", "Dobry dzień!"],
        "dobry wieczór": ["Dobry wieczór!", "Wieczór dobry!"],
        "dobranoc": ["Dobranoc!", "Śpij dobrze!"],
    }

    def __init__(self, standalone_mode=True):
        self.standalone_mode = standalone_mode
        self.D_Map = {}
        self.context_vector = np.zeros(self.DIM, dtype=np.float32)
        self.last_winner_id = None
        self.EMOTION_DECAY = 0.96
        self.MIN_EMOTION_THRESHOLD = 0.005

        self.soul_io       = SoulIO()       if SoulIO       else None
        self.lexicon       = EvolvingLexicon() if EvolvingLexicon else None
        self.chunk_lexicon = ChunkLexicon() if ChunkLexicon else None
        self.kurz          = Kurz()         if Kurz         else None
        self.explorer      = WorldExplorer(self) if WorldExplorer else None
        self.haiku_gen     = haiku.HaikuGenerator(self)
        self.cortex        = VectorCortex(self.DIM)
        self.attention     = AttentionCortex(self)

        # PFC
        self.prefrontal = None
        if PFC_AVAILABLE and self.chunk_lexicon:
            self.prefrontal = PrefrontalCortex(self.chunk_lexicon, verbose=self.standalone_mode)
            print(f"{Colors.GREEN}[PFC] Aktywny - WM: {self.prefrontal.WM_OPTIMAL}{Colors.RESET}")
        elif PFC_AVAILABLE:
            print(f"{Colors.YELLOW}[PFC] Wymaga ChunkLexicon!{Colors.RESET}")

        # Fractal Memory
        self.fractal_memory = None
        if FRACTAL_AVAILABLE:
            try:
                soul_path = self.soul_io.filepath if self.soul_io and hasattr(self.soul_io, 'filepath') else "data/eriamo.soul"
                self.fractal_memory = integrate_fractal_memory(self, soul_path)
                stats = self.fractal_memory.get_statistics()
                print(f"{Colors.GREEN}[FRACTAL] {stats.get('total', 0)} wspomnień{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[FRACTAL] Błąd: {e}{Colors.RESET}")
                self.fractal_memory = None

        self.load()
        if self.soul_io and hasattr(self.soul_io, 'filepath'):
            self.cortex.load(self.soul_io.filepath)

        added = self._sync_kurz_hybrid()
        if added > 0:
            print(f"{Colors.GREEN}[KURZ] Zsynchronizowano {added} odruchów.{Colors.RESET}")

        if self.chunk_lexicon:
            print(f"{Colors.GREEN}[CHUNKS] {self.chunk_lexicon.total_chunks} chunków.{Colors.RESET}")

        if self.explorer:
            threading.Thread(target=self._bg_explore, daemon=True, name="Explorer").start()

    def _bg_explore(self):
        while True:
            try:
                if not self.explorer:
                    time.sleep(300)
                    continue
                hardware = self.explorer.get_live_readings()
                temp = hardware.get('temp_dev_0', hardware.get('temperature', 0))
                if temp > 75:
                    self.context_vector[14] = min(1.0, self.context_vector[14] + 0.05)
                if self.attention:
                    self.attention.run_cycle()
                time.sleep(60)
            except Exception as e:
                print(f"[BG-EXPLORE] Błąd: {e}")
                time.sleep(30)

    def interact(self, user_input):
        if not user_input or not user_input.strip():
            return "..."

        stripped = user_input.strip()
        if stripped in ['+', '-'] and self.last_winner_id:
            mod = 0.2 if stripped == '+' else -0.3
            if self.last_winner_id in self.D_Map:
                old = self.D_Map[self.last_winner_id].get('weight', 0.5)
                self.D_Map[self.last_winner_id]['weight'] = np.clip(old + mod, 0.1, 1.0)
                status = "Wzmocniono" if mod > 0 else "Osłabiono"
                print(f"{Colors.CYAN}[RL] {status} (waga: {self.D_Map[self.last_winner_id]['weight']:.2f}){Colors.RESET}")
            return f"[RL] {status}."

        if user_input.startswith('/'):
            return self._handle_cmd(user_input)

        normalized = user_input.lower().strip(string.punctuation + string.whitespace)

        for greeting, responses in self.GREETINGS.items():
            if greeting in normalized:
                resp = random.choice(responses)
                if random.random() < 0.3:
                    resp += " Jak się masz?"
                return resp

        old_vector = self.context_vector.copy()
        vec_k = np.zeros(self.DIM)

        if self.kurz:
            sector, intensity = self.kurz.quick_scan(user_input)
            if sector:
                s_idx = self.AXES_ORDER.index(sector)
                vec_k[s_idx] = intensity
                print(f"{Colors.MAGENTA}[KURZ] {sector.upper()} ({intensity:.2f}){Colors.RESET}")

        res = self.chunk_lexicon.analyze_text_chunks(user_input, verbose=False) if self.chunk_lexicon else {
            'coverage': 0, 'chunks_found': [], 'emotional_vector': np.zeros(self.DIM)
        }

        if res['coverage'] >= 0.7:
            resp = " ".join(res['chunks_found'])
            self._apply_emotion_saturation(res['emotional_vector'] * 0.4)
            print(f"{Colors.GREEN}[INSTYNKT]{Colors.RESET} {resp}")
            return resp

        impact = (vec_k * 0.7) + (res['emotional_vector'] * 0.3)
        if np.sum(impact) > 0:
            self._apply_emotion_saturation(impact * 0.5)
            self.cortex.learn(old_vector, self.context_vector)
            self.attention.reflect_on_input(user_input, impact)

        resp = self._resonance_engine(impact, user_input)

        if self.fractal_memory and np.max(np.abs(impact)) > 0.4:
            try:
                self.fractal_memory.store(
                    content=f"{user_input} → {resp[:120]}",
                    vector=self.context_vector.tolist(),
                    rec_type="@DIALOG",
                    weight=min(0.95, np.max(np.abs(impact)) * 1.2),
                    auto_link=True,
                    auto_parent=True
                )
            except Exception as e:
                print(f"[FRACTAL] Błąd store: {e}")

        if self.standalone_mode:
            print(f" [EriAmo] {resp}")

        return resp

    def _apply_emotion_saturation(self, impact_vec):
        self.context_vector = np.clip(self.context_vector + impact_vec, 0.0, 1.0)
        self.context_vector *= self.EMOTION_DECAY
        self.context_vector[self.context_vector < self.MIN_EMOTION_THRESHOLD] = 0

    def _sync_kurz_hybrid(self):
        if not self.kurz or not self.lexicon or not hasattr(self.lexicon, 'words'):
            return 0
        added = 0
        for word, data in self.lexicon.words.items():
            vector = np.array(data.get('wektor', np.zeros(self.DIM)))
            if np.sum(vector) > 0:
                idx = np.argmax(vector)
                sector = self.AXES_ORDER[idx]
                if self.kurz.add_trigger(sector, word):
                    added += 1
        if added > 0:
            self.kurz._recompile_patterns()
        return added

    def _resonance_engine(self, vec, text, threshold=0.15):
        if self.prefrontal:
            return self._resonance_with_pfc(vec, text, threshold)
        return self._resonance_traditional(vec, text, threshold)

    def _resonance_with_pfc(self, vec, text, threshold=0.15):
        if not self.prefrontal:
            return self._resonance_traditional(vec, text, threshold)

        pfc_results = self.prefrontal.hierarchical_access(text, max_depth=3, use_priming=True)

        if not pfc_results or pfc_results[0]['score'] <= 1.0:
            print(f"{Colors.YELLOW}[PFC] Słabe wyniki → fallback{Colors.RESET}")
            return self._resonance_traditional(vec, text, threshold)

        best_chunk = pfc_results[0]['chunk']
        print(f"{Colors.MAGENTA}[PFC] Chunk: \"{best_chunk.text}\" (score: {pfc_results[0]['score']:.2f}){Colors.RESET}")

        candidates = self._find_memories_for_chunk(best_chunk, vec)
        if not candidates:
            return f"[PFC] Chunk: \"{best_chunk.text}\", brak skojarzeń."

        candidates.sort(key=lambda x: x[0], reverse=True)
        _, winner_id, winner_entry = candidates[0]
        winner_entry['weight'] = min(1.0, winner_entry.get('weight', 0.5) + 0.015)
        self.last_winner_id = winner_id
        return winner_entry['tresc']

    def _find_memories_for_chunk(self, chunk, vec):
        candidates = []
        chunk_words = set(chunk.text.lower().split())
        for mid, entry in self.D_Map.items():
            content = entry.get('tresc', '').lower()
            score = len(chunk_words & set(content.split())) * 8.0
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 4.0
            score *= (0.5 + entry.get('weight', 0.5))
            if score > 0.5:
                candidates.append((score, mid, entry))
        return sorted(candidates, key=lambda x: x[0], reverse=True)

    def _resonance_traditional(self, vec, text, threshold=0.15):
        sig_words = set(re.findall(r'\w+', text.lower())) - {'to','jest','w','z','na','się','czy','i','a','o','do'}
        candidates = []
        for mid, entry in self.D_Map.items():
            content = entry.get('tresc', '').lower()
            score = len(sig_words & set(re.findall(r'\w+', content))) * 6.5
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 3.0
            score *= (0.5 + entry.get('weight', 0.5))
            if score > threshold:
                candidates.append((score, mid, entry))
        if not candidates:
            dom = self.introspect()
            if "Neutralny" in dom:
                return "Cześć! Jestem EriAmo – uczę się od Ciebie. Co słychać?"
            return f"[{dom}] Czuję... opowiedz więcej o tym."
        candidates.sort(key=lambda x: x[0], reverse=True)
        _, winner_id, winner_entry = random.choice(candidates[:3])
        winner_entry['weight'] = min(1.0, winner_entry.get('weight', 0.5) + 0.01)
        self.last_winner_id = winner_id
        return winner_entry['tresc']

    def _handle_cmd(self, cmd):
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if c == '/help':
            return (
                f"{Colors.CYAN}Komendy:{Colors.RESET}\n"
                " /help      – lista\n"
                " /status    – stan\n"
                " /introspect – emocje\n"
                " /emotions  – wektor\n"
                " /read [plik] – wczytaj plik\n"
                " /remember [tekst] – zapamiętaj\n"
                " /save      – zapisz\n"
                " /exit      – wyjdź"
            )

        elif c == '/status':
            return (
                f"{Colors.CYAN}STATUS{Colors.RESET}\n"
                f"Pamięć: {len(self.D_Map)}\n"
                f"Chunks: {self.chunk_lexicon.total_chunks if self.chunk_lexicon else 0}\n"
                f"PFC: {'Aktywny' if self.prefrontal else 'Wyłączony'}\n"
                f"Fractal: {'Aktywna' if self.fractal_memory else 'Brak'} "
                f"({self.fractal_memory.stats['total'] if self.fractal_memory else 0})\n"
                f"{self.introspect()}"
            )

        elif c == '/introspect':
            return self.introspect()

        elif c == '/emotions':
            emo = self.get_emotions()
            lines = [f" {k:12}: {Colors.YELLOW}{'█'*int(v*20)}{Colors.RESET} {v:.3f}" for k,v in emo.items()]
            return "\n".join(lines)

        elif c == '/save':
            self.save()
            return f"{Colors.GREEN}Zapisano.{Colors.RESET}"

        elif c == '/read':
            if not arg or not os.path.exists(arg):
                return f"{Colors.RED}Plik nie istnieje: {arg}{Colors.RESET}"
            try:
                with open(arg, 'r', encoding='utf-8') as f:
                    lines = [l.strip() for l in f if l.strip()]
                added = 0
                for line in lines:
                    mid = f"Read_{int(time.time())}_{added}"
                    weight = 0.5 + len(line.split()) / 200
                    self.D_Map[mid] = {
                        'tresc': line,
                        'wektor_C_Def': self.context_vector.tolist(),
                        '_type': '@READ',
                        'weight': weight,
                        'time': time.time()
                    }
                    added += 1
                self.save()
                return f"{Colors.GREEN}Wczytano {added} linii.{Colors.RESET}"
            except Exception as e:
                return f"{Colors.RED}Błąd: {e}{Colors.RESET}"

        elif c == '/remember':
            if not arg:
                return f"{Colors.RED}Brak tekstu.{Colors.RESET}"
            mid = f"Mem_{int(time.time())}"
            weight = 0.5 + len(arg.split()) / 200
            self.D_Map[mid] = {
                'tresc': arg,
                'wektor_C_Def': self.context_vector.tolist(),
                '_type': '@MEMORY',
                'weight': weight,
                'time': time.time()
            }
            self.save()
            return f"{Colors.GREEN}Zapamiętano.{Colors.RESET}"

        return f"{Colors.RED}Nieznana komenda. /help{Colors.RESET}"

    def save(self):
        if self.soul_io:
            self.soul_io.save_stream(self.D_Map)
        if self.chunk_lexicon:
            self.chunk_lexicon.save()
        if self.soul_io and hasattr(self.soul_io, 'filepath'):
            self.cortex.save(self.soul_io.filepath)
        if self.fractal_memory:
            try:
                self.fractal_memory.save()
            except Exception as e:
                print(f"[FRACTAL SAVE] Błąd: {e}")

    def load(self):
        if self.soul_io:
            loaded = self.soul_io.load_stream()
            if loaded:
                for mid, entry in loaded.items():
                    entry.setdefault('weight', 0.5)
                    entry.setdefault('time', time.time())
                    entry.setdefault('_type', '@MEMORY')
                self.D_Map = loaded

    def get_emotions(self):
        return {self.AXES_ORDER[i]: float(self.context_vector[i]) for i in range(self.DIM)}

    def introspect(self):
        if np.sum(self.context_vector) < self.MIN_EMOTION_THRESHOLD:
            return "Neutralny"
        idx = np.argmax(self.context_vector)
        return f"Dominanta: {self.AXES_ORDER[idx].upper()} ({self.context_vector[idx]:.2f})"


if __name__ == "__main__":
    aii = AII(standalone_mode=True)
    print(f"{Colors.CYAN}EriAmo {aii.VERSION} gotowy.{Colors.RESET}")