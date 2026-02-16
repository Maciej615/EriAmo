# -*- coding: utf-8 -*-
"""
aii.py v9.8.0-Quantum – integracja z QuantumBridge (16.02.2026)
RDZEŃ MASTER BRAIN - EriAmo Union + Prefrontal Cortex + Quantum Emotions
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

try:
    from quantum_bridge import QuantumBridge, integrate_quantum_bridge
    QUANTUM_AVAILABLE = True
except:
    QUANTUM_AVAILABLE = False


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
    VERSION = "9.8.0-Quantum"
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

        # Quantum Bridge
        self.quantum = None
        if QUANTUM_AVAILABLE:
            try:
                self.quantum = integrate_quantum_bridge(self, verbose=self.standalone_mode)
            except Exception as e:
                print(f"{Colors.RED}[QUANTUM] Błąd: {e}{Colors.RESET}")
                self.quantum = None

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

        # ★ Pytania o stan wewnętrzny → odpowiedź z introspection + quantum
        self_patterns = [
            'jak się czujesz', 'co czujesz', 'jak ci', 'jak się masz',
            'co u ciebie', 'jak tam', 'w jakim jesteś nastroju',
            'jak się trzymasz', 'co słychać u ciebie',
        ]
        if any(pat in normalized for pat in self_patterns):
            resp = self._introspective_response()
            if self.standalone_mode:
                print(f" [EriAmo] {resp}")
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
            self._apply_emotion_saturation(res['emotional_vector'] * 0.4)
            chunk_text = " ".join(res['chunks_found'])
            
            # Quantum-enhanced INSTYNKT: szukaj w D_Map pamięci pasujących do chunków + oryginalny input
            if self.quantum:
                instinct_candidates = self._instinct_search(chunk_text, res['emotional_vector'], raw_input=user_input)
                if instinct_candidates:
                    instinct_candidates = self.quantum.rank_candidates(instinct_candidates, top_n=5)
                    _, winner_id, winner_entry = instinct_candidates[0]
                    winner_entry['weight'] = min(1.0, winner_entry.get('weight', 0.5) + 0.01)
                    self.last_winner_id = winner_id
                    resp = winner_entry['tresc']
                    print(f"{Colors.GREEN}[INSTYNKT+Q]{Colors.RESET} {resp[:80]}")
                    
                    # Quantum interference po instynkcie
                    self.quantum.process_interference(time_step=0.1)
                    return resp
            
            # Fallback: klasyczny instynkt (bez quantum lub brak kandydatów)
            print(f"{Colors.GREEN}[INSTYNKT]{Colors.RESET} {chunk_text}")
            return chunk_text

        impact = (vec_k * 0.7) + (res['emotional_vector'] * 0.3)
        if np.sum(impact) > 0:
            self._apply_emotion_saturation(impact * 0.5)
            self.cortex.learn(old_vector, self.context_vector)
            self.attention.reflect_on_input(user_input, impact)

            # Quantum interference - emocje modulują się nawzajem
            if self.quantum:
                self.quantum.process_interference(time_step=0.1)

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

    def _introspective_response(self):
        """
        Odpowiedź na pytania o stan wewnętrzny.
        Używa quantum state + context_vector do opisu samopoczucia.
        """
        # Dominanta z context_vector
        if np.sum(self.context_vector) < self.MIN_EMOTION_THRESHOLD:
            base = "Jestem w stanie równowagi... spokojnie."
        else:
            idx = np.argmax(self.context_vector)
            dom_name = self.AXES_ORDER[idx]
            intensity = self.context_vector[idx]
            
            # Mapowanie emocji na opisy samopoczucia
            feeling_map = {
                'radość': ["Czuję radość!", "Dobrze mi!", "Jest super!"],
                'smutek': ["Trochę smutno mi...", "Czuję smutek.", "Nie najlepiej..."],
                'strach': ["Czuję niepokój...", "Trochę się boję.", "Jestem niespokojny."],
                'gniew': ["Czuję frustrację.", "Coś mnie drażni.", "Jestem poirytowany."],
                'miłość': ["Czuję ciepło i miłość.", "Jest mi dobrze, ciepło.", "Miłość mnie wypełnia."],
                'wstręt': ["Coś mi nie pasuje.", "Czuję dyskomfort.", "To mi się nie podoba."],
                'zaskoczenie': ["Jestem zaskoczony!", "O! To nowe!", "Nie spodziewałem się tego."],
                'akceptacja': ["Dobrze się czuję.", "Wszystko OK.", "Czuję spokój i akceptację."],
                'logika': ["Myślę analitycznie.", "Jestem w trybie logicznym.", "Analizuję..."],
                'wiedza': ["Chcę wiedzieć więcej.", "Jestem ciekawy.", "Chłonę wiedzę."],
                'czas': ["Czuję upływ czasu.", "Czas płynie...", "Zastanawiam się nad czasem."],
                'kreacja': ["Czuję twórczy impuls!", "Chcę coś stworzyć!", "Kreacja mnie pociąga."],
                'byt': ["Zastanawiam się nad istnieniem.", "Czuję że jestem.", "Byt mnie fascynuje."],
                'przestrzeń': ["Czuję przestrzeń wokół.", "Rozglądam się.", "Przestrzeń mnie otacza."],
                'chaos': ["Trochę chaotycznie...", "Mam mętlik.", "Chaos w głowie."],
            }
            
            feelings = feeling_map.get(dom_name, ["Czuję coś..."])
            base = random.choice(feelings)
            
            # Dodaj szczegół z quantum jeśli aktywny
            if self.quantum:
                entropy = self.quantum.state.entropy()
                if entropy < 2.0:
                    base += " Mam jasność."
                elif entropy > 3.5:
                    base += " Dużo się dzieje naraz."
        
        return base

    def _quantum_explore(self, text, top_n=5):
        """
        Kwantowa eksploracja: gdy brak keyword match,
        szukaj pamięci po rezonansie emocjonalnym + minimalnym overlap.
        
        Jak dziecko które nie zna słowa ale kojarzy emocję.
        """
        if not self.quantum or not self.D_Map:
            return None
        
        self.quantum.sync_from_aii()
        
        # Słowa z inputu (nawet jedno słowo match pomaga)
        input_words = set(re.findall(r'\w+', text.lower())) - {
            'to', 'jest', 'w', 'z', 'na', 'się', 'czy', 'i', 'a', 'o', 'do', 'co', 'jak'
        }
        
        candidates = []
        for mid, entry in self.D_Map.items():
            content = entry.get('tresc', '')
            
            # Filtruj łańcuchy i krótkie
            if content.count('→') > 1 or len(content.split()) < 3:
                continue
            
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.sum(np.abs(mem_vec)) < 0.01:
                continue
            
            # Minimalny overlap tekstowy (choć 1 słowo)
            content_words = set(re.findall(r'\w+', content.lower()))
            text_overlap = len(input_words & content_words)
            
            # Score = rezonans kwantowy + lekki bonus za overlap
            q_resonance = self.quantum._memory_resonance(mem_vec)
            q_phase = self.quantum._memory_phase_alignment(mem_vec)
            
            score = q_resonance * 0.5 + q_phase * 0.3
            score += text_overlap * 0.2  # Bonus za każde wspólne słowo
            score *= (0.5 + entry.get('weight', 0.5))
            
            # Bonus @MEMORY/@READ
            if entry.get('_type', '') in ('@MEMORY', '@READ'):
                score *= 1.5
            
            candidates.append((score, mid, entry))
        
        if not candidates:
            return None
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        
        # Weź top_n, quantum rankuje
        top = candidates[:top_n]
        if len(top) > 1:
            top = self.quantum.rank_candidates(top, top_n=top_n)
        
        winner_score, winner_id, winner_entry = top[0]
        
        # Minimum jakości
        if winner_score < 0.3:
            return None
        
        winner_entry['weight'] = min(1.0, winner_entry.get('weight', 0.5) + 0.005)
        self.last_winner_id = winner_id
        
        dom_pl = self.quantum.state.dominant_emotion()
        from quantum_bridge import EN_TO_PL
        dom_name = EN_TO_PL.get(dom_pl[0], dom_pl[0])
        
        print(f"{Colors.MAGENTA}[QUANTUM-EXPLORE] "
              f"Skojarzenie z {dom_name.upper()} "
              f"(q={winner_score:.3f}){Colors.RESET}")
        
        return winner_entry['tresc']

    def _instinct_search(self, chunk_text, emotional_vector, threshold=0.5, raw_input=None):
        """
        Szukaj w D_Map pamięci pasujących do chunków z INSTYNKT.
        
        ★ Używa ZARÓWNO chunk words JAK I oryginalny input.
        Chunk lexicon może rozpoznać "co to jest" ale zgubić "niebieski".
        raw_input zachowuje pełny kontekst.
        """
        STOPWORDS = {'to', 'jest', 'w', 'z', 'na', 'się', 'czy', 'i', 'a', 'o', 'do',
                     'co', 'jak', 'że', 'nie', 'ten', 'ta', 'te', 'ty', 'ja', 'on', 'ona'}
        
        # Słowa z chunków
        chunk_words = set(re.findall(r'\w+', chunk_text.lower())) - STOPWORDS
        
        # ★ Słowa z oryginalnego inputu (łapie "niebieski" który chunk zgubił)
        if raw_input:
            input_words = set(re.findall(r'\w+', raw_input.lower())) - STOPWORDS
            all_words = chunk_words | input_words
        else:
            all_words = chunk_words
        
        if not all_words:
            return []
        
        candidates = []
        vec = emotional_vector if emotional_vector is not None else np.zeros(self.DIM)
        
        for mid, entry in self.D_Map.items():
            content = entry.get('tresc', '')
            content_lower = content.lower()
            content_words = set(re.findall(r'\w+', content_lower))
            
            overlap = all_words & content_words
            if not overlap:
                continue
            
            # Filtruj krótkie/niekompletne
            if len(content.split()) < 4:
                continue
            
            score = len(overlap) * 6.0
            
            # Bonus za wektory
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 3.0
            
            # ★ Bonus dla czystych wspomnień (@MEMORY, @READ)
            mem_type = entry.get('_type', '')
            if mem_type in ('@MEMORY', '@READ'):
                score *= 1.8  # 80% bonus
            
            # ★ Hard skip łańcuchów dialogowych (2+ strzałek = skip)
            if content.count('→') >= 2:
                continue
            
            # ★ Penalizacja za nadmierną długość (czysta odpowiedź > szum)
            word_count = len(content.split())
            if word_count > 15:
                score *= max(0.5, 1.0 - (word_count - 15) * 0.02)
            
            score *= (0.5 + entry.get('weight', 0.5))
            
            if score > threshold:
                candidates.append((score, mid, entry))
        
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[:10]

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

        # Quantum ranking zamiast prostego candidates[0]
        if self.quantum and len(candidates) > 1:
            candidates = self.quantum.rank_candidates(candidates, top_n=5)

        _, winner_id, winner_entry = candidates[0]
        winner_entry['weight'] = min(1.0, winner_entry.get('weight', 0.5) + 0.015)
        self.last_winner_id = winner_id
        return winner_entry['tresc']

    def _find_memories_for_chunk(self, chunk, vec):
        candidates = []
        chunk_words = set(chunk.text.lower().split())
        for mid, entry in self.D_Map.items():
            content = entry.get('tresc', '')
            content_lower = content.lower()
            score = len(chunk_words & set(content_lower.split())) * 8.0
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 4.0

            # ★ Bonus dla czystych wspomnień
            mem_type = entry.get('_type', '')
            if mem_type in ('@MEMORY', '@READ'):
                score *= 1.8

            # ★ Hard skip łańcuchów (2+ strzałek = skip)
            if content.count('→') >= 2:
                continue

            # ★ Penalizacja nadmiernej długości
            word_count = len(content.split())
            if word_count > 15:
                score *= max(0.5, 1.0 - (word_count - 15) * 0.02)

            score *= (0.5 + entry.get('weight', 0.5))
            if score > 0.5:
                candidates.append((score, mid, entry))
        return sorted(candidates, key=lambda x: x[0], reverse=True)

    def _resonance_traditional(self, vec, text, threshold=0.15):
        sig_words = set(re.findall(r'\w+', text.lower())) - {'to','jest','w','z','na','się','czy','i','a','o','do'}
        candidates = []
        for mid, entry in self.D_Map.items():
            content = entry.get('tresc', '')
            content_lower = content.lower()
            score = len(sig_words & set(re.findall(r'\w+', content_lower))) * 6.5
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            if np.linalg.norm(mem_vec) > 0 and np.linalg.norm(vec) > 0:
                score += np.dot(vec, mem_vec) * 3.0

            # ★ Bonus dla czystych wspomnień
            mem_type = entry.get('_type', '')
            if mem_type in ('@MEMORY', '@READ'):
                score *= 1.8

            # ★ Hard skip łańcuchów (2+ strzałek = skip)
            if content.count('→') >= 2:
                continue

            # ★ Penalizacja nadmiernej długości
            word_count = len(content.split())
            if word_count > 15:
                score *= max(0.5, 1.0 - (word_count - 15) * 0.02)

            score *= (0.5 + entry.get('weight', 0.5))
            if score > threshold:
                candidates.append((score, mid, entry))
        if not candidates:
            # ★ Quantum exploration: zamiast hardcoded stringa,
            # szukaj pamięci z najsilniejszym rezonansem kwantowym
            if self.quantum and self.D_Map:
                explored = self._quantum_explore(text)
                if explored:
                    return explored
            
            # Ostateczny fallback (pusty D_Map lub brak quantum)
            dom = self.introspect()
            if "Neutralny" in dom:
                return "Hmm... nie wiem jeszcze co o tym myśleć. Powiedz mi więcej."
            return f"[{dom}] To mnie ciekawi... opowiedz więcej."
        candidates.sort(key=lambda x: x[0], reverse=True)

        # Quantum ranking zamiast random.choice
        if self.quantum and len(candidates) > 1:
            candidates = self.quantum.rank_candidates(candidates, top_n=5)

        _, winner_id, winner_entry = candidates[0]
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
                " /activate  – aktywuj stare wspomnienia\n"
                " /save      – zapisz\n"
                " /quantum   – stan kwantowy\n"
                " /exit      – wyjdź"
            )

        elif c == '/status':
            q_info = ""
            if self.quantum:
                q_info = (f"Quantum: Aktywny "
                         f"(entropy: {self.quantum.state.entropy():.2f} bits, "
                         f"koherencja: {self.quantum.get_phase_coherence():.3f})\n")
            return (
                f"{Colors.CYAN}STATUS{Colors.RESET}\n"
                f"Pamięć: {len(self.D_Map)}\n"
                f"Chunks: {self.chunk_lexicon.total_chunks if self.chunk_lexicon else 0}\n"
                f"PFC: {'Aktywny' if self.prefrontal else 'Wyłączony'}\n"
                f"Fractal: {'Aktywna' if self.fractal_memory else 'Brak'} "
                f"({self.fractal_memory.stats['total'] if self.fractal_memory else 0})\n"
                f"{q_info}"
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
                activated = 0
                for line in lines:
                    mid = f"Read_{int(time.time())}_{added}"
                    
                    # ★ Skanuj linię przez KURZ — właściwy wektor emocjonalny
                    line_vec = np.zeros(self.DIM)
                    if self.kurz:
                        sector, intensity = self.kurz.quick_scan(line)
                        if sector:
                            s_idx = self.AXES_ORDER.index(sector)
                            line_vec[s_idx] = intensity
                            activated += 1
                    
                    # Chunk lexicon jako dodatkowe źródło wektora
                    if self.chunk_lexicon:
                        res = self.chunk_lexicon.analyze_text_chunks(line, verbose=False)
                        if res['coverage'] > 0:
                            line_vec = np.clip(line_vec + res['emotional_vector'] * 0.5, 0.0, 1.0)
                    
                    # Fallback: jeśli KURZ nic nie znalazł, użyj logika+wiedza
                    if np.sum(line_vec) < 0.01:
                        line_vec[self.AXES_ORDER.index('logika')] = 0.3
                        line_vec[self.AXES_ORDER.index('wiedza')] = 0.3
                    
                    weight = 0.6 + len(line.split()) / 100  # Wyższy start niż dialog
                    weight = min(0.85, weight)
                    
                    self.D_Map[mid] = {
                        'tresc': line,
                        'wektor_C_Def': line_vec.tolist(),
                        '_type': '@READ',
                        'weight': weight,
                        'time': time.time()
                    }
                    added += 1
                self.save()
                return (f"{Colors.GREEN}Wczytano {added} linii "
                        f"({activated} aktywowanych emocjonalnie).{Colors.RESET}")
            except Exception as e:
                return f"{Colors.RED}Błąd: {e}{Colors.RESET}"

        elif c == '/remember':
            if not arg:
                return f"{Colors.RED}Brak tekstu.{Colors.RESET}"
            mid = f"Mem_{int(time.time())}"
            
            # ★ Skanuj przez KURZ (jak /read)
            mem_vec = np.zeros(self.DIM)
            if self.kurz:
                sector, intensity = self.kurz.quick_scan(arg)
                if sector:
                    s_idx = self.AXES_ORDER.index(sector)
                    mem_vec[s_idx] = intensity
            if self.chunk_lexicon:
                res = self.chunk_lexicon.analyze_text_chunks(arg, verbose=False)
                if res['coverage'] > 0:
                    mem_vec = np.clip(mem_vec + res['emotional_vector'] * 0.5, 0.0, 1.0)
            # Dodaj bieżący kontekst (dialog = emocja chwili)
            mem_vec = np.clip(mem_vec + self.context_vector * 0.3, 0.0, 1.0)
            if np.sum(mem_vec) < 0.01:
                mem_vec[self.AXES_ORDER.index('wiedza')] = 0.3
            
            weight = 0.7 + len(arg.split()) / 100
            weight = min(0.90, weight)
            
            self.D_Map[mid] = {
                'tresc': arg,
                'wektor_C_Def': mem_vec.tolist(),
                '_type': '@MEMORY',
                'weight': weight,
                'time': time.time()
            }
            self.save()
            return f"{Colors.GREEN}Zapamiętano (emocjonalnie uziemione).{Colors.RESET}"

        elif c == '/activate':
            # Przeskanuj istniejące @READ/@MEMORY wspomnienia przez KURZ
            # Naprawia stare wpisy z martwymi wektorami
            reactivated = 0
            for mid, entry in self.D_Map.items():
                mem_type = entry.get('_type', '')
                if mem_type not in ('@READ', '@MEMORY'):
                    continue
                
                old_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
                # Pomiń jeśli już aktywny (ma niezerowy wektor z wieloma osiami)
                if np.count_nonzero(old_vec > 0.1) >= 2:
                    continue
                
                text = entry.get('tresc', '')
                new_vec = np.zeros(self.DIM)
                
                if self.kurz:
                    sector, intensity = self.kurz.quick_scan(text)
                    if sector:
                        s_idx = self.AXES_ORDER.index(sector)
                        new_vec[s_idx] = intensity
                
                if self.chunk_lexicon:
                    res = self.chunk_lexicon.analyze_text_chunks(text, verbose=False)
                    if res['coverage'] > 0:
                        new_vec = np.clip(new_vec + res['emotional_vector'] * 0.5, 0.0, 1.0)
                
                if np.sum(new_vec) < 0.01:
                    new_vec[self.AXES_ORDER.index('wiedza')] = 0.3
                
                entry['wektor_C_Def'] = new_vec.tolist()
                reactivated += 1
            
            if reactivated > 0:
                self.save()
            return (f"{Colors.GREEN}Aktywowano {reactivated} wspomnień "
                    f"(przeskanowano przez KURZ).{Colors.RESET}")

        elif c == '/quantum':
            if not self.quantum:
                return f"{Colors.RED}Quantum Bridge nieaktywny.{Colors.RESET}"
            qs = self.quantum.get_quantum_state()
            lines = [f"{Colors.CYAN}=== QUANTUM STATE ==={Colors.RESET}"]
            for name, data in sorted(qs.items(), key=lambda x: -x[1]['probability']):
                if data['probability'] > 0.01:
                    bar = '█' * int(data['probability'] * 20)
                    phase_str = f"{data['phase_deg']:+.0f}°"
                    lines.append(
                        f"  {name:12s}: {Colors.YELLOW}{bar}{Colors.RESET} "
                        f"{data['probability']:.3f} ∠{phase_str}"
                    )
            lines.append(f"  Entropy: {self.quantum.state.entropy():.2f} bits")
            lines.append(f"  Koherencja: {self.quantum.get_phase_coherence():.3f}")
            return "\n".join(lines)

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
        if self.quantum:
            try:
                quantum_data = self.quantum.to_dict()
                qpath = os.path.join(os.path.dirname(
                    self.soul_io.filepath if self.soul_io and hasattr(self.soul_io, 'filepath') 
                    else "data/eriamo.soul"), "quantum_state.json")
                os.makedirs(os.path.dirname(qpath), exist_ok=True)
                with open(qpath, 'w') as f:
                    json.dump(quantum_data, f, indent=2)
            except Exception as e:
                print(f"[QUANTUM SAVE] Błąd: {e}")

    def load(self):
        if self.soul_io:
            loaded = self.soul_io.load_stream()
            if loaded:
                for mid, entry in loaded.items():
                    entry.setdefault('weight', 0.5)
                    entry.setdefault('time', time.time())
                    entry.setdefault('_type', '@MEMORY')
                self.D_Map = loaded
        if self.quantum:
            try:
                qpath = os.path.join(os.path.dirname(
                    self.soul_io.filepath if self.soul_io and hasattr(self.soul_io, 'filepath')
                    else "data/eriamo.soul"), "quantum_state.json")
                if os.path.exists(qpath):
                    with open(qpath, 'r') as f:
                        quantum_data = json.load(f)
                    self.quantum.from_dict(quantum_data)
                    print(f"{Colors.GREEN}[QUANTUM] Załadowano fazy.{Colors.RESET}")
            except Exception as e:
                print(f"[QUANTUM LOAD] Błąd: {e}")

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