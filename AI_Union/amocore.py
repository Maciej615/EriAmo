# amocore_v59.py
# -*- coding: utf-8 -*-
"""
System Ontologicznej Pamięci Muzyki v5.9.4 [FULL FIX]
- FIX: Przywrócono brakujące funkcje (interpret_improv_for_composition, CuriosityEngine).
- FIX: Threading RLock (zapobiega deadlockom).
- TRYB: UNBOUNDED (Historia Liniowa)
"""
import numpy as np
import threading
import time
import csv
import os
import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd

# =============================================================================
# DEFINICJA ONTOLOGICZNA: 9 WEKTORÓW DUSZY
# =============================================================================

AXES_LIST = [
    "logika",       # 0: racjonalność ↔ intuicja
    "emocje",       # 1: pobudzenie emocjonalne
    "affections",   # 2: pamięć emocjonalna
    "wiedza",       # 3: zgromadzona wiedza
    "czas",         # 4: percepcja tempa
    "kreacja",      # 5: potencjał twórczy
    "byt",          # 6: egzystencja
    "przestrzen",   # 7: percepcja przestrzeni
    "improwizacja"  # 8: swoboda vs reguły
]

EPHEMERAL_AXES = ["emocje", "czas"]
PERSISTENT_AXES = ["affections", "logika", "wiedza", "kreacja", "byt", "przestrzen", "improwizacja"]
ONTOLOGICAL_THRESHOLD = 0.98

# =============================================================================
# SYSTEM SNU (MusicMemory)
# =============================================================================
class MusicMemory:
    DATA_DIR = "data"
    H_LOG_PATH = "data/music_experience.json"
    D_MAP_PATH = "data/music_patterns.json"
    
    MUSICAL_FEATURES = [
        'repetition_density', 'leap_ratio', 'rhythmic_regularity', 'pitch_variance',
        'note_density', 'interval_avg', 'dominant_pitch_class', 'syncopation_feel',
        'pitch_range', 'second_pitch_class', 'chromatic_density', 'key_tonic', 'key_mode'
    ]
    
    def __init__(self, sleep_interval: float = 300.0):
        os.makedirs(self.DATA_DIR, exist_ok=True)
        self.H_log = []
        self.D_Map = {}
        self.sleep_interval = sleep_interval
        self.running = True
        self.is_sleeping = False
        self.last_sleep_time = time.time()
        self.sleep_count = 0
        self.experiences_since_sleep = 0
        self._load_memory()
        self._start_sleep_cycle()
        print(f"\033[96m[MEMORY] MusicMemory aktywna. Sen co {sleep_interval/60:.1f} min.\033[0m")
    
    def _load_memory(self):
        try:
            if os.path.exists(self.H_LOG_PATH):
                with open(self.H_LOG_PATH, 'r', encoding='utf-8') as f: self.H_log = json.load(f)
        except: self.H_log = []
        try:
            if os.path.exists(self.D_MAP_PATH):
                with open(self.D_MAP_PATH, 'r', encoding='utf-8') as f: self.D_Map = json.load(f)
        except: self.D_Map = {}
    
    def _save_memory(self):
        try:
            with open(self.H_LOG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.H_log[-1000:], f, indent=2, ensure_ascii=False)
            with open(self.D_MAP_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.D_Map, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"\033[91m[MEMORY] Błąd zapisu: {e}\033[0m")
    
    def _start_sleep_cycle(self):
        def cycle():
            while self.running:
                time.sleep(self.sleep_interval)
                if not self.running: break
                self._sleep()
        threading.Thread(target=cycle, daemon=True).start()
    
    def _sleep(self):
        if self.is_sleeping: return
        self.is_sleeping = True
        
        # Konsolidacja (uproszczona dla bezpieczeństwa)
        recent = self.H_log[-20:]
        for exp in recent:
            key = self._extract_pattern_key(exp)
            if key in self.D_Map:
                self.D_Map[key]['weight'] = min(self.D_Map[key]['weight'] + 1.0, 100.0)
            else:
                self.D_Map[key] = {
                    'features': exp.get('features', {}),
                    'weight': 1.0,
                    'created_at': datetime.now().isoformat()
                }
        self._save_memory()
        
        self.last_sleep_time = time.time()
        self.experiences_since_sleep = 0
        self.is_sleeping = False
        print(f"\033[92m[MEMORY] Sen zakończony. Wzorców: {len(self.D_Map)}\033[0m")
    
    def _extract_pattern_key(self, exp):
        feat = exp.get('features', {})
        parts = []
        for k in ['repetition_density', 'rhythmic_regularity']:
            val = feat.get(k, 0.5)
            cat = 'H' if val > 0.66 else ('L' if val < 0.33 else 'M')
            parts.append(f"{k[:3]}:{cat}")
        return "|".join(parts)

    def record_experience(self, features: dict, source: str = "analysis"):
        self.H_log.append({
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'source': source
        })
        self.experiences_since_sleep += 1
        if self.experiences_since_sleep > 10: self._sleep()

    def get_consolidated_style(self) -> dict:
        if not self.D_Map: return {f: 0.5 for f in self.MUSICAL_FEATURES}
        sums = {f: 0.0 for f in self.MUSICAL_FEATURES}
        total_w = 0
        for p in self.D_Map.values():
            w = p['weight']
            total_w += w
            for f, v in p.get('features', {}).items():
                if f in sums: sums[f] += v * w
        return {f: (v / total_w if total_w else 0.5) for f, v in sums.items()}
    
    def get_recent_style(self) -> dict:
        if not self.H_log: return {f: 0.5 for f in self.MUSICAL_FEATURES}
        recent = self.H_log[-5:]
        avg = {f: 0.0 for f in self.MUSICAL_FEATURES}
        for exp in recent:
            for feat, val in exp.get('features', {}).items():
                if feat in avg: avg[feat] += val / len(recent)
        return avg

    def get_blended_style(self, recent_weight: float = 0.3) -> dict:
        recent = self.get_recent_style()
        consolidated = self.get_consolidated_style()
        blended = {}
        for feat in self.MUSICAL_FEATURES:
            blended[feat] = recent_weight * recent.get(feat, 0.5) + (1 - recent_weight) * consolidated.get(feat, 0.5)
        return blended

    def shutdown(self):
        self.running = False
        self._save_memory()
        print(f"\033[93m[MEMORY] Pamięć zapisana. Dobranoc.\033[0m")

_music_memory = None
def get_music_memory() -> MusicMemory:
    global _music_memory
    if _music_memory is None: _music_memory = MusicMemory()
    return _music_memory


# =============================================================================
# ETYKA I LOGGER
# =============================================================================
ETHICS_FRAMEWORK = {
    "integrity": {"value": 1.0, "immutable": True},
    "respect": {"value": 1.0, "immutable": True},
    "authenticity": {"value": 1.0, "immutable": True},
    "harmony": {"value": 1.0, "immutable": True}
}

@dataclass
class SoulVector:
    values: np.ndarray
    timestamp: float = field(default_factory=time.time)

class SoulStateLogger:
    FILE_PATH = "data/soul_history.csv"
    HEADER = ["timestamp", "id_event", "description", "mode", "cos_alpha", "compression", "emotion_msg"] + \
             [f"S_{axis}" for axis in AXES_LIST] + [f"F_{axis}" for axis in AXES_LIST]

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.lock = threading.RLock()
        self.event_counter = 0
        self._init_file()

    def _init_file(self):
        with self.lock:
            if not os.path.exists(self.FILE_PATH):
                with open(self.FILE_PATH, 'w', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerow(self.HEADER)

    def log_state(self, core, F_vector, cos_alpha, emotion_msg, description, mode, compressed=False):
        with self.lock:
            self.event_counter += 1
            row = [datetime.now().isoformat(), self.event_counter, description, mode, 
                   f"{cos_alpha:.4f}", "YES" if compressed else "NO", emotion_msg] + \
                  core.get_vector_copy().tolist() + F_vector.tolist()
            try:
                with open(self.FILE_PATH, 'a', newline='', encoding='utf-8') as f:
                    csv.writer(f).writerow(row)
            except: pass


# =============================================================================
# RDZEŃ (EriAmoCore)
# =============================================================================
class EriAmoCore:
    AXES = AXES_LIST
    HISTORY_PATH = "data/soul_history.csv"
    
    def __init__(self):
        self.lock = threading.RLock()
        self.vector = SoulVector(np.zeros(len(self.AXES), dtype=float))
        self.last_decay_time = time.time()
        self.decay_cycle_count = 0
        self.ethics = ETHICS_FRAMEWORK.copy()
        
        if not self.load_soul_from_history():
            self.vector.values[self.AXES.index('wiedza')] = 5.0
            self.vector.values[self.AXES.index('kreacja')] = 10.0
            print("[CORE] Narodziny nowej Duszy.")

    def load_soul_from_history(self) -> bool:
        if not os.path.exists(self.HISTORY_PATH): return False
        try:
            df = pd.read_csv(self.HISTORY_PATH)
            if df.empty: return False
            last_row = df.iloc[-1]
            new_vals = []
            for axis in self.AXES:
                col = f"S_{axis}"
                val = float(last_row[col]) if col in last_row else 0.0
                new_vals.append(val)
            self.vector.values = np.array(new_vals)
            return True
        except: return False

    def get_vector_copy(self) -> np.ndarray:
        with self.lock: return self.vector.values.copy()

    def shift_axis(self, axis: str, action: str, value: float) -> bool:
        with self.lock:
            if axis not in self.AXES: return False
            i = self.AXES.index(axis)
            if action == "INCREMENT": self.vector.values[i] += value
            elif action == "SET": self.vector.values[i] = value
            elif action == "DECAY": self.vector.values[i] *= (1.0 - value)
            return True

    def compute_integrity_hash(self) -> str:
        with self.lock:
            data_str = "|".join([f"{x:.8f}" for x in self.vector.values]) + "".join(self.AXES)
            ethics_str = "|".join([f"{k}:{v['value']}" for k, v in self.ethics.items()])
            full_data = data_str + "|ETHICS|" + ethics_str
            return hashlib.sha256(full_data.encode('utf-8')).hexdigest()

    def create_memory_dump(self, filename: str = None) -> str:
        os.makedirs("data/dumps", exist_ok=True)
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"soul_dump_{timestamp}.soul"
        filepath = f"data/dumps/{filename}"
        
        with self.lock:
            dump_data = {
                "meta": {
                    "version": "5.9.4",
                    "created_at": datetime.now().isoformat(),
                    "integrity_hash": self.compute_integrity_hash(),
                },
                "soul_vector": {axis: float(self.vector.values[i]) for i, axis in enumerate(self.AXES)},
                "ethics_framework": {k: v["value"] for k, v in self.ethics.items()}
            }
            
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dump_data, f, indent=2, ensure_ascii=False)
        return filepath
        
    def apply_time_based_decay(self):
        # Placeholder dla kompatybilności
        pass


# =============================================================================
# HELPER FUNCTIONS (BRAKUJĄCE WCZEŚNIEJ!)
# =============================================================================

def interpret_improv_for_composition(improv_value: float) -> dict:
    """Interpretuje wartość osi improwizacji dla kompozytora."""
    normalized = (improv_value + 100) / 200  # -100→0, +100→1
    normalized = max(0, min(1, normalized))
    
    # FIX: Upewniono się, że słownik jest poprawnie zamknięty
    return {
        "freedom_level": normalized,
        "allow_chromatic": normalized > 0.4,
        "allow_modal_interchange": normalized > 0.5,
        "allow_unexpected_modulation": normalized > 0.6,
        "extended_chords_probability": normalized * 0.8,
        "syncopation_probability": normalized * 0.6,
        "rubato_allowed": normalized > 0.3,
        "ornamentation_density": normalized,
        "allow_large_leaps": normalized > 0.5
    }

# =============================================================================
# CURIOSITY ENGINE (TEŻ BRAKOWAŁO)
# =============================================================================

class CuriosityEngine:
    WEIGHT_KREACJA = 0.40
    WEIGHT_WIEDZA = 0.30
    WEIGHT_EMOCJE = 0.30
    WIEDZA_OPTIMUM = 50.0
    WIEDZA_SPREAD = 40.0
    
    def __init__(self):
        self.boredom_counter = {}
        self.discovery_cooldown = 0
        self.last_genres = []
        
    def compute_curiosity(self, kreacja: float, wiedza: float, emocje: float) -> dict:
        kreacja_component = self._normalize(kreacja) * 100
        wiedza_norm = self._normalize(wiedza) * 100
        wiedza_diff = abs(wiedza_norm - self.WIEDZA_OPTIMUM)
        wiedza_component = 100 * math.exp(-(wiedza_diff ** 2) / (2 * self.WIEDZA_SPREAD ** 2))
        emocje_component = min(100, abs(emocje) * 2)
        
        base_curiosity = (
            self.WEIGHT_KREACJA * kreacja_component +
            self.WEIGHT_WIEDZA * wiedza_component +
            self.WEIGHT_EMOCJE * emocje_component
        )
        
        final_curiosity = (base_curiosity - 50) * 2
        final_curiosity = max(-100, min(100, final_curiosity))
        
        return {'value': final_curiosity}
    
    def _normalize(self, value: float) -> float:
        return max(0, min(1, (value + 100) / 200))

_curiosity_engine = None
def get_curiosity_engine() -> CuriosityEngine:
    global _curiosity_engine
    if _curiosity_engine is None: _curiosity_engine = CuriosityEngine()
    return _curiosity_engine
