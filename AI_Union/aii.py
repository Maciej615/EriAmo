# -*- coding: utf-8 -*-
"""
aii.py v9.6.1-Master-Torch [EVOLUTION SCALONY - FULL INTEGRATION with PyTorch]
RDZEŃ MASTER BRAIN - EriAmo Union
Autor: Maciej A. Mazur & Grok (scalenie 9.5.3 + 9.6.0 + PyTorch integration)

Zmiany względem 9.6.1-Master:
- INTEGRACJA PYTORCH: VectorCortex zastąpiony FFN z autograd i optimizerem (tylko tu, bo wysoko uzasadnione dla uczenia predykcyjnego).
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
import torch  # Dodany import dla PyTorch (dostępny w env)
import torch.nn as nn
import torch.optim as optim

try:
    from union_config import UnionConfig, Colors
except ImportError:
    print("⚠ KRYTYCZNY BŁĄD: Brak union_config.py")
    sys.exit(1)

import haiku

try:
    from chunk_lexicon import ChunkLexicon
except ImportError:
    ChunkLexicon = None
try:
    from soul_io import SoulIO
except ImportError:
    SoulIO = None
try:
    from lexicon import EvolvingLexicon
except ImportError:
    EvolvingLexicon = None
try:
    from kurz import Kurz
except ImportError:
    Kurz = None
try:
    from explorer import WorldExplorer
except ImportError:
    WorldExplorer = None


# --- KLASY POMOCNICZE ---

class VectorCortex:
    def __init__(self, axes_count):
        self.dims = axes_count
        self.hidden_dim = 32  # Ukryta warstwa dla FFN (dopasowana do dims)
        self.model = nn.Sequential(
            nn.Linear(self.dims, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.dims),
            nn.Softmax(dim=0)  # Softmax dla probabilistycznej predykcji
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)  # Optimizer zamiast ręcznej rate
        self.criterion = nn.MSELoss()  # Loss dla uczenia (MSE między pred a actual)
    
    def predict(self, current_vector):
        current_vector = np.array(current_vector)  # Kompatybilność z NumPy
        if np.sum(current_vector) == 0:
            return np.zeros(self.dims)
        tensor_in = torch.tensor(current_vector, dtype=torch.float32)
        with torch.no_grad():
            pred = self.model(tensor_in)
        return pred.numpy()  # Zwrot jako NumPy dla reszty kodu

    def learn(self, prev, actual, rate=0.01):  # Rate teraz to lr, ale zachowane dla kompatybilności
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
        
        return loss.item()  # Zwrot loss zamiast norm (lepsza metryka dla RL)
    
    def save(self, path):
        try:
            torch.save(self.model.state_dict(), path + '.cortex_torch.pt')  # Save PyTorch model
        except:
            pass

    def load(self, path):
        try:
            if os.path.exists(path + '.cortex_torch.pt'):
                self.model.load_state_dict(torch.load(path + '.cortex_torch.pt'))
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
                sys.__stdout__.write(f"\n{Colors.FAINT}[ATTENTION] Krystalizacja wzorca: {txt[:35]}...{Colors.RESET}\n")
        
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
        if intensity < 0.2:
            return
        
        candidates = []
        for entry in self.brain.D_Map.values():
            mem_vec = np.array(entry.get('wektor_C_Def', [0] * 15))
            if len(mem_vec) > idx and mem_vec[idx] > 0.4:
                candidates.append(entry)
        
        if candidates:
            echo_entry = random.choice(candidates)
            echo_entry['weight'] = min(1.0, echo_entry.get('weight', 0.5) + 0.05)
            dom_axis = self.brain.AXES_ORDER[idx]
            sys.__stdout__.write(
                f"\n{Colors.MAGENTA}[REFLEKSJA]{Colors.RESET} "
                f"Echo {dom_axis.upper()}: \"{echo_entry['tresc'][:60]}...\"\n"
            )

    def reflect_on_input(self, text, input_vec):
        if np.sum(input_vec) == 0:
            return
        resonance = np.dot(self.brain.context_vector, input_vec)
        dom_axis = self.brain.AXES_ORDER[np.argmax(self.brain.context_vector)].upper()
        if resonance > 0.4:
            sys.__stdout__.write(f"{Colors.MAGENTA}[REFLEKSJA-INPUT]{Colors.RESET} Rezonans z {dom_axis}.\n")
        elif resonance < 0.05:
            sys.__stdout__.write(f"{Colors.MAGENTA}[REFLEKSJA-INPUT]{Colors.RESET} Dysonans z {dom_axis}.\n")


# --- RDZEŃ SYSTEMU ---

class AII:
    VERSION = "9.6.1-Master-Torch"
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
        self.context_vector = np.zeros(self.DIM)
        self.last_winner_id = None
        
        self.EMOTION_DECAY = 0.96
        self.MIN_EMOTION_THRESHOLD = 0.005
        
        self.soul_io = SoulIO() if SoulIO else None
        self.lexicon = EvolvingLexicon() if EvolvingLexicon else None
        self.chunk_lexicon = ChunkLexicon() if ChunkLexicon else None
        self.kurz = Kurz() if Kurz else None
        self.explorer = WorldExplorer(self) if WorldExplorer else None
        self.haiku_gen = haiku.HaikuGenerator(self)
        self.cortex = VectorCortex(self.DIM)
        self.attention = AttentionCortex(self)

        if self.explorer:
            threading.Thread(target=self._bg_explore, daemon=True).start()

        self.load()
        if self.soul_io and hasattr(self.soul_io, 'filepath'):
            self.cortex.load(self.soul_io.filepath)
        
        added = 0
        if self.kurz:
            added = self._sync_kurz_hybrid()
            print(f"{Colors.GREEN}[KURZ] Zsynchronizowano {added} odruchów. Aktywnych: {self.kurz.get_all_triggers_count() if self.kurz else 0}.{Colors.RESET}")
        
        if self.chunk_lexicon:
            print(f"{Colors.GREEN}[PAMIĘĆ] Załadowano {self.chunk_lexicon.total_chunks} chunków.{Colors.RESET}")

    def _apply_emotion_saturation(self, impact_vec):
        self.context_vector = np.clip(self.context_vector + impact_vec, 0.0, 1.0)
        self.context_vector *= self.EMOTION_DECAY
        self.context_vector[self.context_vector < self.MIN_EMOTION_THRESHOLD] = 0

    def _sync_kurz_hybrid(self):
        if not self.kurz or not self.lexicon or not hasattr(self.lexicon, 'D_Map'):
            return 0
        added_count = 0
        for word, data in self.lexicon.D_Map.items():
            vector = np.array(data.get('wektor', np.zeros(self.DIM)))
            if np.sum(vector) > 0:
                idx = np.argmax(vector)
                sector = self.AXES_ORDER[idx]
                if self.kurz.add_trigger(sector, word):
                    added_count += 1
        if added_count > 0:
            self.kurz._recompile_patterns()
        return added_count

    def _get_initial_weight(self, text, vec):
        base = 0.5
        base += len(text.split()) / 100.0
        base += np.sum(vec) * 0.2
        return min(1.0, base)

    def _resonance_engine(self, vec, text, threshold=0.15):
        def _normalize(txt):
            return txt.lower().strip()
        
        sig_text = set(re.findall(r'\w+', _normalize(text))) - {
            'to', 'jest', 'w', 'z', 'na', 'się', 'czy', 'i', 'a', 'o', 'do'
        }
        candidates = []
        
        for mid, entry in self.D_Map.items():
            content = entry.get('tresc', '')
            entry_words = set(re.findall(r'\w+', _normalize(content)))
            score = len(sig_text & entry_words) * 6.5
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 3.0
            score *= (0.5 + entry.get('weight', 0.5))
            if score > threshold:
                candidates.append((score, mid, entry))

        if not candidates:
            return "Witaj. Co słychać?"
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        winner_score, winner_id, winner_entry = random.choice(candidates[:3])
        
        winner_entry['weight'] = min(1.0, winner_entry.get('weight', 0.5) + 0.01)
        self.last_winner_id = winner_id
        
        if winner_entry.get('_type') in ['@READ', '@MEMORY', '@FACT']:
            return winner_entry['tresc']
        
        if 'wiedza' in self.AXES_ORDER:
            w_idx = self.AXES_ORDER.index('wiedza')
            mvec = np.array(winner_entry.get('wektor_C_Def', [0]*self.DIM))
            if len(mvec) > w_idx and mvec[w_idx] > 0.6:
                return winner_entry['tresc']
        
        return f"Skojarzenie:\n\"{winner_entry['tresc']}\""

    def _handle_cmd(self, cmd):
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        if c == '/help':
            return (f"{Colors.CYAN}Dostępne komendy EriAmo:{Colors.RESET}\n"
                    "  /status      - Stan modułów, pamięć, RL\n"
                    "  /rlstats     - Statystyki wzmocnień\n"
                    "  /chunks      - Statystyki wzorców\n"
                    "  /emotions    - Wizualizacja wektora 15D\n"
                    "  /introspect  - Dominująca emocja\n"
                    "  /reflect     - Ręczne echo\n"
                    "  /read [plik] - Głębokie mapowanie pliku\n"
                    "  /remember    - Ręczne utrwalenie faktu\n"
                    "  /art         - Generowanie Haiku\n"
                    "  /save        - Ręczny zapis stanu\n"
                    "  /clear       - Czyszczenie konsoli")

        elif c == '/status':
            dp = self.explorer.get_live_readings() if self.explorer else {}
            modules = {
                "SoulIO": self.soul_io is not None,
                "Chunks": self.chunk_lexicon is not None,
                "Kurz": self.kurz is not None,
                "Explorer": self.explorer is not None,
                "Cortex": self.cortex is not None,
                "Attention": self.attention is not None
            }
            m_str = "\n".join([f"  {k:10}: {'[OK]' if v else '[OFF]'}" for k, v in modules.items()])
            temp = dp.get('temp_dev_0', 'N/A')
            avg_weight = np.mean([e.get('weight', 0.5) for e in self.D_Map.values()]) if self.D_Map else 0
            return f"{Colors.CYAN}--- STATUS EriAmo {self.VERSION} ---{Colors.RESET}\n" \
                   f"{m_str}\n" \
                   f"Pamięć: {len(self.D_Map)} (avg weight: {avg_weight:.2f})\n" \
                   f"Ostatnie RL: {self.last_winner_id}\n" \
                   f"TEMP CPU: {temp}°C"

        elif c == '/rlstats':
            weights = [e.get('weight', 0.5) for e in self.D_Map.values()]
            if weights:
                return f"RL Stats: wpisów {len(weights)}, średnia waga {np.mean(weights):.3f}, max {max(weights):.3f}, min {min(weights):.3f}"
            return "Brak danych RL."

        elif c == '/chunks':
            if self.chunk_lexicon:
                total = self.chunk_lexicon.total_chunks
                return f"{Colors.GREEN}[LEXICON]{Colors.RESET} Aktywne wzorce kognitywne: **{total}**"
            return "Moduł Chunks nieaktywny."

        elif c == '/introspect':
            if np.sum(self.context_vector) < self.MIN_EMOTION_THRESHOLD:
                return f"{Colors.FAINT}Neutralny.{Colors.RESET}"
            idx = np.argmax(self.context_vector)
            dom_axis = self.AXES_ORDER[idx]
            intensity = self.context_vector[idx]
            return f"Dominanta: {Colors.MAGENTA}{dom_axis.upper()}{Colors.RESET} ({intensity:.2f})"

        elif c == '/reflect':
            self.attention.introspective_echo()
            return f"{Colors.GREEN}Refleksja wykonana.{Colors.RESET}"

        elif c == '/emotions':
            emo = {self.AXES_ORDER[i]: round(float(self.context_vector[i]), 3) for i in range(self.DIM)}
            return "\n".join([f"  {k:12}: {Colors.YELLOW}{'█' * int(v*20)}{Colors.RESET} {v:.3f}" for k, v in emo.items()])

        elif c == '/read':
            if not arg or not os.path.exists(arg):
                return f"{Colors.RED}Błąd: Nie widzę pliku {arg or '(brak)'}.{Colors.RESET}"
            try:
                with open(arg, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                return f"{Colors.RED}Błąd odczytu: {str(e)}{Colors.RESET}"
            
            total = len(lines)
            chunks_start = self.chunk_lexicon.total_chunks if self.chunk_lexicon else 0
            print(f"{Colors.CYAN}[EXPLORER] Deep Read: {arg}{Colors.RESET}")
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                if self.chunk_lexicon:
                    self.chunk_lexicon.analyze_text_chunks(line, verbose=False)
                    self.chunk_lexicon.extract_chunks_from_text(line)

                if i % max(1, total // 20) == 0 or i == total - 1:
                    p = int((i + 1) / total * 100)
                    bar = "█" * (p // 5) + "-" * (20 - p // 5)
                    sys.stdout.write(f"\r{Colors.YELLOW}  Trawienie: [{bar}] {p}%{Colors.RESET}")
                    sys.stdout.flush()

                mid = f"Read_{int(time.time())}_{i}"
                weight = self._get_initial_weight(line, self.context_vector)
                self.D_Map[mid] = {
                    "tresc": line,
                    "wektor_C_Def": self.context_vector.tolist(),
                    "_type": "@READ",
                    "weight": weight,
                    "time": time.time()
                }
            
            self.save()
            chunks_end = self.chunk_lexicon.total_chunks if self.chunk_lexicon else 0
            return f"\n{Colors.GREEN}[SUKCES]{Colors.RESET} Nowe wzorce: +{chunks_end - chunks_start}. Plik zintegrowany."

        elif c == '/remember':
            if not arg:
                return f"{Colors.RED}Brak treści.{Colors.RESET}"
            mid = f"Man_{time.time()}"
            weight = self._get_initial_weight(arg, self.context_vector)
            self.D_Map[mid] = {
                "tresc": arg,
                "wektor_C_Def": self.context_vector.tolist(),
                "_type": "@MEMORY",
                "weight": weight,
                "time": time.time()
            }
            self.save()
            return f"{Colors.GREEN}Zapamiętano (waga {weight:.2f}).{Colors.RESET}"

        elif c == '/art':
            return self.haiku_gen.generate()

        elif c == '/save':
            self.save()
            return f"{Colors.GREEN}Stan utrwalony.{Colors.RESET}"

        elif c == '/clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Konsola wyczyszczona."

        return f"{Colors.RED}Nieznana komenda. /help.{Colors.RESET}"

    def _bg_explore(self):
        while self.explorer:
            try:
                hardware = self.explorer.get_live_readings()
                temp = hardware.get('temp_dev_0', 0)
                if temp > 75:
                    self.context_vector[14] = min(1.0, self.context_vector[14] + 0.05)
                self.attention.run_cycle()
                time.sleep(60)
            except Exception:
                time.sleep(10)

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
                if self.standalone_mode:
                    print(f"{Colors.CYAN}[RL] {status} ślad (waga: {self.D_Map[self.last_winner_id]['weight']:.2f}){Colors.RESET}")
                return f"[RL] {status}."

        if user_input.startswith('/'):
            return self._handle_cmd(user_input)

        normalized = user_input.lower().strip(string.punctuation + string.whitespace)
        if normalized in [":)", ":]", "=)", ":-)", ":>"] or "😊" in user_input or "🙂" in user_input:
            return random.choice(["😊", "🙂", "😊💫", "Uśmiech przyjęty! 😊"])

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
                if self.standalone_mode:
                    print(f"{Colors.MAGENTA}[KURZ] Odruch: {sector.upper()} ({intensity:.2f}){Colors.RESET}")

        res = self.chunk_lexicon.analyze_text_chunks(user_input, verbose=False) if self.chunk_lexicon else {'coverage':0, 'chunks_found':[], 'emotional_vector':np.zeros(self.DIM)}
        
        if res['coverage'] >= 0.7:
            resp = " ".join(res['chunks_found'])
            self._apply_emotion_saturation(res['emotional_vector'] * 0.4)
            if self.standalone_mode:
                print(f"{Colors.GREEN}[INSTYNKT]{Colors.RESET} {resp}")
            return resp

        impact = (vec_k * 0.7) + (res['emotional_vector'] * 0.3)
        if np.sum(impact) > 0:
            self._apply_emotion_saturation(impact * 0.5)
            self.cortex.learn(old_vector, self.context_vector)

        self.attention.reflect_on_input(user_input, impact)

        resp = self._resonance_engine(impact, user_input)
        if self.standalone_mode:
            print(f" [EriAmo] {resp}")
        return resp

    def save(self):
        if self.soul_io:
            self.soul_io.save_stream(self.D_Map)
        if self.chunk_lexicon:
            self.chunk_lexicon.save()
        if self.soul_io and hasattr(self.soul_io, 'filepath'):
            self.cortex.save(self.soul_io.filepath)

    def load(self):
        if self.soul_io:
            loaded = self.soul_io.load_stream()
            if loaded:
                for mid, entry in loaded.items():
                    if 'weight' not in entry:
                        entry['weight'] = 0.5
                    if 'time' not in entry:
                        entry['time'] = time.time()
                    if '_type' not in entry:
                        entry['_type'] = "@MEMORY"
                self.D_Map = loaded


if __name__ == "__main__":
    aii = AII()
