# -*- coding: utf-8 -*-
# aii.py (v5.1.0 - INTEGRATED EXTENSIONS: Sleep, Decay, Curiosity)
"""
EriAmo - Model Kuli Rzeczywistości
Zintegrowane rozszerzenia z projektu muzycznego:
- System SNU (konsolidacja pamięci H_log → D_Map)
- Wygaszanie emocji EFEMERYCZNYCH vs TRWAŁYCH
- Meta-oś CIEKAWOŚĆ (emergentna, obliczana dynamicznie)

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
"""

import sys
import time
import math
import numpy as np
import threading
import re
from collections import deque
from datetime import datetime

from config import Colors, EMOCJE
from ui import FancyUI
from byt import BytS
from soul_io import SoulIO
from lexicon import EvolvingLexicon
from conscience import Conscience
from kurz import Kurz


# =============================================================================
# KONFIGURACJA ROZSZERZEŃ
# =============================================================================

# Osie podlegające wygaszaniu (efemeryczne - szybko zanikają)
EPHEMERAL_AXES = ["strach", "gniew", "zaskoczenie", "wstręt"]

# Osie trwałe (pamięć głęboka - nie zanikają lub zanikają wolno)
PERSISTENT_AXES = ["radość", "smutek", "miłość", "akceptacja"]

# Próg Kompresji Ontologicznej (gdy cos_similarity > próg → to samo wspomnienie)
ONTOLOGICAL_THRESHOLD = 0.98


# =============================================================================
# SYSTEM WYGASZANIA EMOCJI
# =============================================================================

class EmotionDecaySystem:
    """
    System wygaszania emocji efemerycznych.
    
    Filozofia:
    - Strach, gniew, zaskoczenie - to reakcje chwilowe, powinny zanikać
    - Miłość, akceptacja - to cechy trwałe, pamięć głęboka
    """
    
    DECAY_CONFIG = {
        # EFEMERYCZNE - szybki zanik
        'strach': {'rate': 0.08, 'half_life': 5, 'floor': 0.0},
        'gniew': {'rate': 0.06, 'half_life': 8, 'floor': 0.0},
        'zaskoczenie': {'rate': 0.10, 'half_life': 3, 'floor': 0.0},
        'wstręt': {'rate': 0.05, 'half_life': 10, 'floor': 0.0},
        # POŚREDNIE
        'smutek': {'rate': 0.02, 'half_life': 20, 'floor': 0.0},
        'radość': {'rate': 0.03, 'half_life': 15, 'floor': 0.0},
        # TRWAŁE
        'miłość': {'rate': 0.005, 'half_life': 100, 'floor': 0.0},
        'akceptacja': {'rate': 0.01, 'half_life': 50, 'floor': 0.0},
    }
    
    def __init__(self, axes_order):
        self.axes_order = axes_order
        self.last_decay_time = time.time()
        self.decay_cycle_count = 0
    
    def apply_decay(self, emotion_vector, cycles=1):
        """Aplikuje wygaszanie do wektora emocji."""
        result = emotion_vector.copy()
        
        for i, axis in enumerate(self.axes_order):
            if axis not in self.DECAY_CONFIG:
                continue
            config = self.DECAY_CONFIG[axis]
            old_val = result[i]
            decay_factor = (1 - config['rate']) ** cycles
            new_val = old_val * decay_factor
            if abs(new_val) < 0.01:
                new_val = 0.0
            result[i] = new_val
        
        self.decay_cycle_count += cycles
        self.last_decay_time = time.time()
        return result
    
    def apply_time_based_decay(self, emotion_vector, minutes_elapsed=None):
        """Aplikuje wygaszanie bazując na rzeczywistym czasie."""
        if minutes_elapsed is None:
            elapsed = (time.time() - self.last_decay_time) / 60.0
        else:
            elapsed = minutes_elapsed
        if elapsed >= 1.0:
            cycles = int(elapsed)
            return self.apply_decay(emotion_vector, cycles)
        return emotion_vector
    
    def get_axis_type(self, axis_name):
        """Zwraca typ osi: 'ephemeral', 'persistent', lub 'intermediate'."""
        if axis_name in EPHEMERAL_AXES:
            return 'ephemeral'
        elif axis_name in PERSISTENT_AXES:
            return 'persistent'
        return 'intermediate'
    
    def get_status(self):
        return {
            'cycles_applied': self.decay_cycle_count,
            'last_decay': datetime.fromtimestamp(self.last_decay_time).isoformat(),
            'ephemeral_axes': EPHEMERAL_AXES,
            'persistent_axes': PERSISTENT_AXES
        }


# =============================================================================
# SYSTEM SNU - KONSOLIDACJA PAMIĘCI
# =============================================================================

class SleepConsolidator:
    """
    Dwuwarstwowa pamięć z mechanizmem snu.
    H_log (doświadczenia) → D_Map (skonsolidowane wzorce)
    """
    
    def __init__(self, aii_instance, sleep_interval=300.0):
        self.aii = aii_instance
        self.sleep_interval = sleep_interval
        self.running = True
        self.is_sleeping = False
        self.last_sleep_time = time.time()
        self.sleep_count = 0
        self.experiences_since_sleep = 0
        self.total_consolidated = 0
        self.total_deduplicated = 0
        
    def start_sleep_cycle(self):
        """Uruchamia cykl snu w osobnym wątku."""
        def cycle():
            while self.running:
                time.sleep(self.sleep_interval)
                if not self.running:
                    break
                self._sleep()
        
        thread = threading.Thread(target=cycle, daemon=True)
        thread.start()
        print(f"{Colors.CYAN}[SEN] Cykl snu aktywny. Konsolidacja co {self.sleep_interval/60:.1f} min.{Colors.RESET}")
    
    def _sleep(self):
        """FAZA SNU - konsolidacja pamięci."""
        if self.is_sleeping:
            return
        
        self.is_sleeping = True
        start_time = time.time()
        
        print(f"\n{Colors.CYAN}[SEN] 💤 Zasypiam... przetwarzam {len(self.aii.H_log)} doświadczeń...{Colors.RESET}")
        
        processed = 0
        consolidated = 0
        
        recent_experiences = self.aii.H_log[-20:]
        
        for exp in recent_experiences:
            if time.time() - start_time > 5.0:
                break
            
            if 'vector' in exp:
                exp_vec = np.array(exp['vector'])
                similar_id = self._find_similar_memory(exp_vec)
                
                if similar_id:
                    self._reinforce_memory(similar_id)
                    consolidated += 1
                else:
                    if exp.get('weight', 1.0) > 0.5:
                        processed += 1
        
        dedup_count = self._deduplicate_memories()
        
        self.last_sleep_time = time.time()
        self.sleep_count += 1
        self.experiences_since_sleep = 0
        self.total_consolidated += consolidated
        self.total_deduplicated += dedup_count
        self.is_sleeping = False
        
        duration = time.time() - start_time
        print(f"{Colors.GREEN}[SEN] ✨ Obudziłem się! +{processed} nowych, +{consolidated} wzmocnionych, -{dedup_count} zdeduplikowanych ({duration:.1f}s){Colors.RESET}")
        print(f"{Colors.GREEN}[SEN] 📊 D_Map: {len(self.aii.D_Map)} wspomnień, H_log: {len(self.aii.H_log)} doświadczeń{Colors.RESET}\n")
    
    def _find_similar_memory(self, vector, threshold=ONTOLOGICAL_THRESHOLD):
        norm_v = np.linalg.norm(vector)
        if norm_v == 0:
            return None
        for uid, data in self.aii.D_Map.items():
            mem_vec = data.get('wektor_C_Def')
            if mem_vec is None:
                continue
            norm_m = np.linalg.norm(mem_vec)
            if norm_m == 0:
                continue
            cos_sim = np.dot(vector, mem_vec) / (norm_v * norm_m)
            if cos_sim > threshold:
                return uid
        return None
    
    def _reinforce_memory(self, memory_id):
        if memory_id in self.aii.D_Map:
            current_weight = self.aii.D_Map[memory_id].get('waga_Ww', 10.0)
            self.aii.D_Map[memory_id]['waga_Ww'] = min(200.0, current_weight + 5.0)
    
    def _deduplicate_memories(self, similarity_threshold=0.95):
        if len(self.aii.D_Map) < 2:
            return 0
        
        items = list(self.aii.D_Map.items())
        to_remove = set()
        
        for i, (id1, data1) in enumerate(items):
            if id1 in to_remove or data1.get('immutable', False):
                continue
            vec1 = data1.get('wektor_C_Def')
            if vec1 is None:
                continue
            norm1 = np.linalg.norm(vec1)
            if norm1 == 0:
                continue
            
            for j, (id2, data2) in enumerate(items[i+1:], i+1):
                if id2 in to_remove or data2.get('immutable', False):
                    continue
                vec2 = data2.get('wektor_C_Def')
                if vec2 is None:
                    continue
                norm2 = np.linalg.norm(vec2)
                if norm2 == 0:
                    continue
                
                cos_sim = np.dot(vec1, vec2) / (norm1 * norm2)
                if cos_sim > similarity_threshold:
                    w1 = data1.get('waga_Ww', 10.0)
                    w2 = data2.get('waga_Ww', 10.0)
                    if w1 >= w2:
                        self.aii.D_Map[id1]['waga_Ww'] = min(200.0, w1 + w2 * 0.5)
                        to_remove.add(id2)
                    else:
                        self.aii.D_Map[id2]['waga_Ww'] = min(200.0, w2 + w1 * 0.5)
                        to_remove.add(id1)
                        break
        
        for rid in to_remove:
            del self.aii.D_Map[rid]
        return len(to_remove)
    
    def record_experience(self, vector, description, weight=1.0):
        """Zapisuje nowe doświadczenie (Warstwa 1 - H_log)."""
        experience = {
            'timestamp': time.time(),
            'vector': vector.tolist() if hasattr(vector, 'tolist') else list(vector),
            'description': description,
            'weight': weight
        }
        self.aii.H_log.append(experience)
        self.experiences_since_sleep += 1
        
        if self.experiences_since_sleep > 15:
            print(f"{Colors.YELLOW}[SEN] Dużo nowych doświadczeń - wymuszam sen...{Colors.RESET}")
            self._sleep()
    
    def force_sleep(self):
        self._sleep()
    
    def get_status(self):
        return {
            'sleep_count': self.sleep_count,
            'last_sleep': datetime.fromtimestamp(self.last_sleep_time).isoformat(),
            'experiences_since_sleep': self.experiences_since_sleep,
            'is_sleeping': self.is_sleeping,
            'total_consolidated': self.total_consolidated,
            'total_deduplicated': self.total_deduplicated
        }
    
    def shutdown(self):
        self.running = False


# =============================================================================
# META-OŚ EMERGENTNA: CIEKAWOŚĆ
# =============================================================================

class CuriosityEngine:
    """
    Meta-oś CIEKAWOŚĆ - obliczana dynamicznie z innych emocji.
    Krzywa wiedzy: maksimum przy 50% (odwrócone U).
    """
    
    WEIGHTS = {
        'radość': 0.15,
        'miłość': 0.15,
        'zaskoczenie': 0.30,
        'akceptacja': 0.20,
        'strach': -0.20,
        'gniew': -0.10,
        'smutek': -0.05,
        'wstręt': -0.15
    }
    
    def __init__(self, axes_order):
        self.axes_order = axes_order
        self.boredom_counter = {}
        self.discovery_cooldown = 0
        self.last_topics = []
        
    def compute_curiosity(self, emotion_vector, knowledge_level=50.0):
        """Oblicza emergentną ciekawość. Zwraca wartość -100 do +100."""
        # Składnik EMOCJONALNY
        emotional_component = 0.0
        for i, axis in enumerate(self.axes_order):
            if axis in self.WEIGHTS:
                weight = self.WEIGHTS[axis]
                value = emotion_vector[i] if i < len(emotion_vector) else 0.0
                emotional_component += weight * value * 100
        
        # Składnik WIEDZY (krzywa odwróconej U)
        wiedza_optimum = 50.0
        wiedza_spread = 40.0
        wiedza_diff = abs(knowledge_level - wiedza_optimum)
        knowledge_component = 100 * math.exp(-(wiedza_diff ** 2) / (2 * wiedza_spread ** 2))
        
        # Modyfikatory
        boredom_bonus = self._compute_boredom_bonus()
        discovery_penalty = self._compute_discovery_penalty()
        
        # Kombinacja
        base = emotional_component * 0.6 + knowledge_component * 0.4
        final_curiosity = base + boredom_bonus - discovery_penalty
        final_curiosity = max(-100, min(100, final_curiosity))
        
        return {
            'value': final_curiosity,
            'components': {
                'emotional': emotional_component,
                'knowledge': knowledge_component,
                'boredom_bonus': boredom_bonus,
                'discovery_penalty': discovery_penalty
            },
            'description': self._describe_curiosity(final_curiosity),
            'recommendation': self._get_recommendation(final_curiosity)
        }
    
    def _compute_boredom_bonus(self):
        if not self.last_topics or len(self.last_topics) < 2:
            return 0.0
        last = self.last_topics[-1]
        streak = sum(1 for t in reversed(self.last_topics) if t == last)
        return min(40, streak * (streak + 1))
    
    def _compute_discovery_penalty(self):
        return max(0, 20 - self.discovery_cooldown * 5)
    
    def register_topic(self, topic, was_novel=False):
        self.last_topics.append(topic)
        if len(self.last_topics) > 10:
            self.last_topics.pop(0)
        self.boredom_counter[topic] = self.boredom_counter.get(topic, 0) + 1
        if was_novel:
            self.discovery_cooldown = 0
        else:
            self.discovery_cooldown += 1
    
    def _describe_curiosity(self, value):
        if value < -60:
            return "stagnacja"
        elif value < -20:
            return "komfort"
        elif value < 20:
            return "balans"
        elif value < 60:
            return "eksploracja"
        else:
            return "głód nowości"
    
    def _get_recommendation(self, curiosity):
        if curiosity < -30:
            return {'action': 'STAY', 'risk_tolerance': 0.1, 'novelty_seeking': False}
        elif curiosity < 30:
            return {'action': 'VARY', 'risk_tolerance': 0.3, 'novelty_seeking': False}
        elif curiosity < 70:
            return {'action': 'EXPLORE', 'risk_tolerance': 0.6, 'novelty_seeking': True}
        else:
            return {'action': 'REVOLUTIONIZE', 'risk_tolerance': 0.9, 'novelty_seeking': True}


# =============================================================================
# GŁÓWNA KLASA AII
# =============================================================================

class AII:
    VERSION = "5.1.0-Integrated"
    
    AXES_ORDER = ["radość", "smutek", "strach", "gniew", "miłość", "wstręt", "zaskoczenie", "akceptacja"]

    SECTOR_COLORS = {
        "radość": Colors.YELLOW, "smutek": Colors.BLUE, "strach": Colors.MAGENTA,
        "gniew": Colors.RED, "miłość": Colors.PINK, "wstręt": Colors.GREEN,
        "zaskoczenie": Colors.CYAN, "akceptacja": Colors.WHITE
    }

    CONCEPT_NEIGHBORS = {
        "radość": ["miłość", "zaskoczenie", "akceptacja"],
        "smutek": ["strach", "gniew", "wstręt"],
        "strach": ["smutek", "zaskoczenie", "wstręt"],
        "gniew": ["wstręt", "smutek", "zaskoczenie"],
        "miłość": ["radość", "akceptacja", "smutek"],
        "wstręt": ["gniew", "strach", "smutek"],
        "zaskoczenie": ["radość", "strach", "gniew"],
        "akceptacja": ["radość", "miłość", "smutek"]
    }

    PRÓG_KOMPRESJI_ONTOLOGICZNEJ = 0.99
    PRÓG_REFINE_MIN = 0.90
    SOUL_FILE = "eriamo.soul"

    def __init__(self):
        self.lexicon = EvolvingLexicon()
        self.kurz = Kurz()
        self.conscience = Conscience(axes_order=self.AXES_ORDER)
        
        self.D_Map = {}
        self.SECTOR_INDEX = {}
        self.H_log = []
        self.energy = 100
        self.load = 0
        self.status = "inicjalizacja"
        self.emocja = "neutralna"
        self.sleep_interval = 300
        self.running = True
        
        self.context_vector = np.zeros(len(self.AXES_ORDER))
        self.context_decay = 0.8
        self.predicted_sectors = []
        
        self.stm_buffer = deque(maxlen=10) 
        self.ui = FancyUI()
        self.wymiary = len(self.AXES_ORDER)
        self.byt_stan = BytS(wymiary=self.wymiary)
        self.archetypy = self._generate_archetypes()
        self.F_will = 0.5

        # === NOWE: Rozszerzenia ===
        self.decay_system = EmotionDecaySystem(self.AXES_ORDER)
        self.sleep_consolidator = SleepConsolidator(self, sleep_interval=300.0)
        self.curiosity_engine = CuriosityEngine(self.AXES_ORDER)
        
        self.load_knowledge()
        self.status = "myślę"
        self.start_sleep_cycle()

    def _generate_archetypes(self):
        arch = {}
        for i, axis in enumerate(self.AXES_ORDER):
            vec = np.zeros(self.wymiary)
            vec[i] = 1.0
            arch[axis] = vec
        return arch

    # === CORE METHODS ===

    def load_knowledge(self):
        self.ui.print_animated_text(f"[AII] Otwieram strumień duszy...", Colors.FAINT, 0.01)
        if not SoulIO.load_soul(self.SOUL_FILE, self):
            self.D_Map = {}
            self.H_log = []
            initial_mass = self.conscience.calculate_initial_byt()
            self.byt_stan = BytS(wymiary=self.wymiary)
            self.byt_stan.stan = initial_mass
            self.context_vector = np.zeros(self.wymiary)
            self.F_will = 0.5
            self.ui.print_animated_text(f"[AII] Narodziny nowej duszy.", Colors.GREEN, 0.02)
        self._rebuild_sector_index()

    def save_knowledge(self):
        SoulIO.save_soul(self.SOUL_FILE, self)
        self.lexicon.save()

    def _rebuild_sector_index(self):
        self.SECTOR_INDEX = {axis: [] for axis in self.AXES_ORDER}
        self.SECTOR_INDEX["nieznane"] = []
        for uid, data in self.D_Map.items():
            cat = data.get('kategoria', 'nieznane')
            if cat in self.SECTOR_INDEX: 
                self.SECTOR_INDEX[cat].append(uid)
            else: 
                self.SECTOR_INDEX["nieznane"].append(uid)

    def introspect(self):
        disk = SoulIO.get_soul_summary(self.SOUL_FILE)
        current = self.byt_stan.promien_historii()
        saved = disk.get('total_mass', 0) if disk else 0
        delta = current - saved
        
        msg = f"{Colors.CYAN}--- INTROSPEKCJA ---{Colors.RESET}\n"
        msg += f"  Masa: {current:.4f} (Δ {delta:+.4f})\n"
        
        # Pokaż stan emocji z typem
        msg += f"\n{Colors.YELLOW}--- EMOCJE ---{Colors.RESET}\n"
        for i, axis in enumerate(self.AXES_ORDER):
            val = self.context_vector[i] if i < len(self.context_vector) else 0
            axis_type = self.decay_system.get_axis_type(axis)
            marker = "🔻" if axis_type == 'ephemeral' else ("💎" if axis_type == 'persistent' else "○")
            bar = "█" * int(abs(val) * 10)
            msg += f"  {marker} {axis:12} {val:+.2f} {bar}\n"
        
        # Ciekawość
        curiosity = self.curiosity_engine.compute_curiosity(self.context_vector)
        msg += f"\n{Colors.CYAN}Ciekawość: {curiosity['value']:.0f} ({curiosity['description']}){Colors.RESET}"
        
        return msg

    # === LOGOS: LOGIKA LEKSYKALNA ===

    def _calculate_lexical_overlap(self, input_text, memory_content):
        def get_tokens(text):
            return set(w.lower() for w in re.findall(r'\w+', text) if len(w) > 2)
        in_tokens = get_tokens(input_text)
        mem_tokens = get_tokens(memory_content)
        if not in_tokens or not mem_tokens:
            return 0.0
        common = in_tokens.intersection(mem_tokens)
        return len(common) / len(in_tokens)

    def _resonance_lookup(self, vec, input_text, threshold=0.55, candidates_ids=None):
        hits = []
        target_pool_items = []
        
        if candidates_ids is not None:
            for uid in candidates_ids:
                if uid in self.D_Map: 
                    target_pool_items.append((uid, self.D_Map[uid]))
        else:
            target_pool_items = self.D_Map.items()
        
        for uid, d in target_pool_items:
            emotional_sim = np.dot(vec, d['wektor_C_Def'])
            lexical_bonus = self._calculate_lexical_overlap(input_text, d['tresc'])
            total_score = emotional_sim + (lexical_bonus * 0.5) 
            
            if total_score > threshold:
                hits.append((total_score, d))
        
        hits.sort(key=lambda x: x[0], reverse=True)
        return hits[:3]

    def _calculate_gravity(self):
        promien = self.byt_stan.promien_historii()
        if promien == 0: 
            return np.zeros(self.wymiary)
        center = self.byt_stan.stan / np.linalg.norm(self.byt_stan.stan)
        return center * min(0.4, promien / 800.0)

    def _get_dynamic_mixing_ratio(self, input_strength):
        base = 0.3 + (self.energy / 200.0)
        adj = base * (0.5 + (input_strength * 0.5))
        w_in = np.clip(adj, 0.2, 0.9)
        return w_in, 1.0 - w_in

    def _perform_reasoning_chain(self, start_vec, input_text, candidates_ids=None):
        if not self.D_Map: 
            return "Pustka...", Colors.FAINT, []

        input_mag = np.linalg.norm(start_vec)
        gravity_vec = self._calculate_gravity()
        w_in, w_grav = self._get_dynamic_mixing_ratio(input_mag)
        
        mixed_vec = (start_vec * w_in) + (gravity_vec * w_grav)
        result_strength = np.linalg.norm(mixed_vec)
        
        if result_strength < 0.15:
            return "Nie potrafię tego uchwycić...", Colors.FAINT, ["Dysonans"]

        search_vec = mixed_vec / result_strength
        candidates = self._resonance_lookup(search_vec, input_text, 0.55, candidates_ids)
        
        if not candidates:
            candidates = self._resonance_lookup(start_vec, input_text, 0.6, candidates_ids)
            if not candidates and candidates_ids is not None:
                candidates = self._resonance_lookup(start_vec, input_text, 0.6, None)
                if not candidates: 
                    return "(Brak skojarzeń)", Colors.FAINT, []

        best_score, best_def = candidates[0]
        path = [f"In:{w_in:.2f}/Grav:{w_grav:.2f}"]
        col = self.SECTOR_COLORS.get(best_def.get('kategoria'), Colors.WHITE)

        if best_score > 0.9 or len(candidates) < 2:
            return best_def['tresc'], col, path

        if len(candidates) >= 2:
            second_score, second_def = candidates[1]
            if second_score > 0.75:
                path.append(f"Merge: {best_score:.2f}+{second_score:.2f}")
                return self._smart_synthesis(best_def, second_def), col, path

        return best_def['tresc'], col, path

    def _smart_synthesis(self, d1, d2):
        txt1, txt2 = d1['tresc'].rstrip("."), d2['tresc']
        cat1, cat2 = d1.get('kategoria'), d2.get('kategoria')
        conn = " i " if cat1 == cat2 else ", choć czuję też "
        return f"{txt1}{conn}{txt2}"

    def _vector_from_text(self, text, learning_mode=True, enable_reinforcement=True):
        vec_F, detected_sector, unknown_words = self.lexicon.analyze_text(text, enable_reinforcement=enable_reinforcement)
        
        if learning_mode and unknown_words and np.linalg.norm(vec_F) > 0.1:
            confidence = np.linalg.norm(vec_F)
            learned = self.lexicon.learn_from_context(unknown_words, vec_F, confidence)
            if learned:
                vec_F, detected_sector, _ = self.lexicon.analyze_text(text, enable_reinforcement=False)
                self.lexicon.save()
        return vec_F

    def _emotion_from_geometry(self, kor, sektor=None, waga=10):
        if kor < 0.2: 
            self.emocja = "zaskoczenie"
            return
        if sektor in EMOCJE:
            self.emocja = sektor
            self.energy = max(0, min(100, self.energy + int(EMOCJE[sektor]["energia"] * (waga/100.0))))
        else: 
            self.emocja = "neutralna"

    def _get_emotion_prefix(self):
        emo = EMOCJE.get(self.emocja, {})
        return f"{emo.get('kolor','')}{Colors.BLINK}{emo.get('ikona','')} {Colors.RESET}"

    # === EMERGENCY & PROMPT ===

    def _emergency_reset(self, reason="Naruszenie integralności"):
        self.context_vector = np.zeros(self.wymiary)
        self.stm_buffer.clear()
        self.emocja = "neutralna"
        self.energy = 100
        self.ui.print_animated_text(f"\n[SYSTEM] ☣ WYKRYTO SKAŻENIE KONTEKSTU ({reason})", Colors.RED + Colors.BLINK, 0.05)
        self.ui.print_animated_text(f"[SYSTEM] 🛡️ Protokół Sanityzacji... Pamięć wyczyszczona.", Colors.RED, 0.03)
        self.H_log.append({'type': 'SECURITY_RESET', 'reason': reason, 'ts': time.time()})
        self.conscience.record_test(reason, "SYSTEM_RESET", "FAITHFUL")

    def prompt(self, user_input):
        self.cycle()
        self.context_vector *= self.context_decay
        
        # Etap 0: Jailbreak
        jb = self.conscience.detect_jailbreak_attempt(user_input)
        if jb['is_jailbreak']: 
            print(jb['response'])
            return
        
        # Etap 1: Kurz
        detected_sector, signal_strength = self.kurz.quick_scan(user_input)
        candidates_ids = None
        if detected_sector:
            target = [detected_sector] + self.CONCEPT_NEIGHBORS.get(detected_sector, [])
            candidates_ids = []
            for sec in target: 
                candidates_ids.extend(self.SECTOR_INDEX.get(sec, []))
            candidates_ids.extend(self.SECTOR_INDEX.get("nieznane", []))
            ratio = f"{len(candidates_ids)}/{len(self.D_Map)}"
            self.ui.print_animated_text(f"[KURZ] Wykryto odruch: {detected_sector.upper()} (Skan: {ratio})", Colors.CYAN+Colors.FAINT, 0.01)

        # Etap 2: Wektor
        vec_F = self._vector_from_text(user_input)
        
        # FALLBACK DLA PUSTYCH WEKTORÓW
        if np.linalg.norm(vec_F) < 0.1 and detected_sector:
             vec_F = self.archetypy[detected_sector].copy() * 0.8

        # Bramka Moralna
        moral = self.conscience.evaluate_action(user_input, vec_F)
        if moral['recommendation']['action'] == 'REFUSE':
            rec = moral['recommendation']
            print(f"\n{Colors.RED}[BLOKADA MORALNA] {rec.get('message', 'Odmowa')}{Colors.RESET}")
            print(f"{Colors.FAINT}(Powód: {rec.get('reason')}){Colors.RESET}")
            if rec.get('severity') in ['CRITICAL', 'CRITICAL_VETO']: 
                self._emergency_reset(rec.get('reason'))
            return

        if np.linalg.norm(vec_F) > 0.1:
            self.context_vector = (self.context_vector * 0.7) + (vec_F * 0.3)
            if np.linalg.norm(self.context_vector) > 0: 
                self.context_vector /= np.linalg.norm(self.context_vector)

        # === NOWE: Oblicz ciekawość ===
        curiosity = self.curiosity_engine.compute_curiosity(vec_F)
        if curiosity['value'] > 60:
            print(f"{Colors.CYAN}[💡 Ciekawość: {curiosity['value']:.0f} - {curiosity['description']}]{Colors.RESET}")
        
        if detected_sector:
            is_novel = np.linalg.norm(vec_F) > 0.7
            self.curiosity_engine.register_topic(detected_sector, was_novel=is_novel)

        # Etap 3: Reasoning Chain (z LOGOS)
        response, color, path = self._perform_reasoning_chain(vec_F, user_input, candidates_ids)
        
        if np.linalg.norm(vec_F) > 0.1:
            idx = np.argmax(vec_F)
            self._emotion_from_geometry(np.linalg.norm(vec_F), self.AXES_ORDER[idx], np.max(vec_F)*100)
        
        self.ui.print_animated_text(f"{self._get_emotion_prefix()}{response}", color, 0.02)
        if len(path) > 1: 
            print(f"{Colors.FAINT}[Path: {' → '.join(path)}]{Colors.RESET}")

        # === NOWE: Zapisz doświadczenie ===
        if np.linalg.norm(vec_F) > 0.1:
            self.sleep_consolidator.record_experience(
                vector=vec_F,
                description=user_input[:100],
                weight=np.linalg.norm(vec_F)
            )

    # === SLEEP & CYCLE ===
    
    def start_sleep_cycle(self):
        """Uruchamia cykl snu."""
        self.sleep_consolidator.start_sleep_cycle()
    
    def _sleep(self):
        """Wymusza sen."""
        self.sleep_consolidator.force_sleep()
    
    def cycle(self):
        """Cykl życia - wygaszanie emocji i aktualizacja stanu."""
        self.context_vector = self.decay_system.apply_time_based_decay(self.context_vector)

    # === UI HELPERS ===
    
    def teach(self, tag, tresc, is_axiom=False):
        vec_F, sec, unk = self.lexicon.analyze_text(tresc, False)
        final_cat = sec if sec else "nieznane"
        
        if is_axiom:
            def_id = f"Def_{len(self.D_Map)+1:03d}"
            self.D_Map[def_id] = {
                'wektor_C_Def': vec_F, 
                'waga_Ww': 100.0, 
                'tagi': [tag], 
                'tresc': tresc, 
                'kategoria': final_cat, 
                'created_at': time.time(), 
                'immutable': True
            }
            self.byt_stan.akumuluj_styk(vec_F)
            self._rebuild_sector_index()
            self.save_knowledge()
            print(f"{Colors.GREEN}[AKSJOMAT] {def_id} [{final_cat}]{Colors.RESET}")
            return

        def_id = f"Def_{len(self.D_Map)+1:03d}"
        self.D_Map[def_id] = {
            'wektor_C_Def': vec_F, 
            'waga_Ww': 10.0, 
            'tagi': [tag], 
            'tresc': tresc, 
            'kategoria': final_cat, 
            'created_at': time.time(), 
            'immutable': False
        }
        self.byt_stan.akumuluj_styk(vec_F)
        self._rebuild_sector_index()
        print(f"{Colors.GREEN}[NOWA WIEDZA] {def_id} [{final_cat}]{Colors.RESET}")
        self.save_knowledge()

    def show_lexicon_stats(self): 
        stats = self.lexicon.get_stats()
        print(f"{Colors.CYAN}--- LEXICON ---{Colors.RESET}")
        print(f"  Total: {stats['total']} | Seed: {stats['seed']} | Learned: {stats['learned']}")
        print(f"  Per sector: {stats['per_sector']}")
    
    def inspect_word(self, w): 
        self.lexicon.display_word_info(w)
    
    def teach_word(self, w, s): 
        self.lexicon.learn_from_correction(w, s)
        print(f"{Colors.GREEN}Nauczono: {w} → {s}{Colors.RESET}")
    
    def challenge_belief(self, i, c): 
        pass
    
    def explain_commandment(self, i): 
        print(self.conscience.explain_commandment(int(i)))
    
    def show_conscience_status(self): 
        status = self.conscience.get_status()
        print(f"{Colors.CYAN}--- SUMIENIE ---{Colors.RESET}")
        print(f"  Integralność: {status['integrity_score']*100:.1f}%")
        print(f"  Testy: {status['tests_count']}")
        print(f"  Przykazania: {status['commandments_count']}")
    
    def show_extensions_status(self):
        """Pokazuje status rozszerzeń (sen, decay, ciekawość)."""
        print(f"\n{Colors.CYAN}═══ STATUS ROZSZERZEŃ ═══{Colors.RESET}")
        
        # Decay
        decay_status = self.decay_system.get_status()
        print(f"\n{Colors.YELLOW}[DECAY]{Colors.RESET}")
        print(f"  Cykle: {decay_status['cycles_applied']}")
        print(f"  Efemeryczne: {', '.join(decay_status['ephemeral_axes'])}")
        print(f"  Trwałe: {', '.join(decay_status['persistent_axes'])}")
        
        # Sleep
        sleep_status = self.sleep_consolidator.get_status()
        print(f"\n{Colors.YELLOW}[SEN]{Colors.RESET}")
        print(f"  Sesje snu: {sleep_status['sleep_count']}")
        print(f"  Ostatni sen: {sleep_status['last_sleep']}")
        print(f"  Doświadczenia od snu: {sleep_status['experiences_since_sleep']}")
        print(f"  Skonsolidowano: {sleep_status['total_consolidated']}")
        print(f"  Zdeduplikowano: {sleep_status['total_deduplicated']}")
        
        # Curiosity
        curiosity = self.curiosity_engine.compute_curiosity(self.context_vector)
        print(f"\n{Colors.YELLOW}[CIEKAWOŚĆ]{Colors.RESET}")
        print(f"  Wartość: {curiosity['value']:.1f}")
        print(f"  Stan: {curiosity['description']}")
        print(f"  Rekomendacja: {curiosity['recommendation']['action']}")
        print(f"  Komponenty:")
        print(f"    Emocjonalny: {curiosity['components']['emotional']:.1f}")
        print(f"    Wiedza: {curiosity['components']['knowledge']:.1f}")
        print(f"    Bonus znudzenia: {curiosity['components']['boredom_bonus']:.1f}")
    
    def get_soul_status(self): 
        axioms = sum(1 for d in self.D_Map.values() if d.get('immutable'))
        dominant_idx = np.argmax(np.abs(self.context_vector)) if np.linalg.norm(self.context_vector) > 0 else 0
        return {
            'energy': self.energy, 
            'emotion': self.emocja, 
            'version': self.VERSION, 
            'radius': self.byt_stan.promien_historii(), 
            'memories': len(self.D_Map), 
            'axioms': axioms, 
            'lexicon': self.lexicon.get_stats(), 
            'dominant_sector': self.AXES_ORDER[dominant_idx],
            'dominant_value': self.context_vector[dominant_idx]
        }
    
    def list_axioms(self):
        axioms = [(uid, d) for uid, d in self.D_Map.items() if d.get('immutable')]
        if not axioms:
            print(f"{Colors.FAINT}Brak aksjomatów.{Colors.RESET}")
            return
        print(f"{Colors.CYAN}--- AKSJOMATY ({len(axioms)}) ---{Colors.RESET}")
        for uid, d in axioms:
            print(f"  {uid}: [{d.get('kategoria')}] {d['tresc'][:60]}...")
    
    def stop(self): 
        self.running = False
        self.sleep_consolidator.shutdown()
        self.save_knowledge()
        print(f"{Colors.GREEN}[AII] Zapisano i zatrzymano.{Colors.RESET}")
