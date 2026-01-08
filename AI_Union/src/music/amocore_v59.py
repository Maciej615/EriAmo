# amocore_v59.py
# -*- coding: utf-8 -*-
"""
System Ontologicznej Pamięci Muzyki v5.9.3 [DEADLOCK FIX]
- FIX: Zmieniono threading.Lock na threading.RLock (zapobiega zawieszeniu przy dumpie).
- TRYB: UNBOUNDED (Historia Liniowa, Nieskończony Wzrost)
"""
import numpy as np
import threading
import time
import csv
import os
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd

# =============================================================================
# DEFINICJA ONTOLOGICZNA: 9 WEKTORÓW DUSZY
# =============================================================================

AXES_LIST = [
    "logika",       # 0: racjonalność ↔ intuicja
    "emocje",       # 1: pobudzenie emocjonalne (efemeryczne)
    "affections",   # 2: pamięć emocjonalna (trwała)
    "wiedza",       # 3: zgromadzona wiedza
    "czas",         # 4: percepcja tempa (efemeryczne)
    "kreacja",      # 5: potencjał twórczy
    "byt",          # 6: egzystencja, tożsamość
    "przestrzen",   # 7: percepcja przestrzeni dźwiękowej
    "improwizacja"  # 8: swoboda twórcza vs reguły
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
        start_time = time.time()
        
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
        self._deduplicate_patterns()
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

    def _deduplicate_patterns(self):
        pass # Placeholder dla oszczędności miejsca

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
        # Prosta średnia ważona
        sums = {f: 0.0 for f in self.MUSICAL_FEATURES}
        total_w = 0
        for p in self.D_Map.values():
            w = p['weight']
            total_w += w
            for f, v in p.get('features', {}).items():
                if f in sums: sums[f] += v * w
        return {f: (v / total_w if total_w else 0.5) for f, v in sums.items()}

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
# ETYKA I LOGGER (SoulStateLogger)
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
        self.lock = threading.RLock()  # FIX: RLock
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
# RDZEŃ (EriAmoCore) - TUTAJ BYŁ BŁĄD
# =============================================================================
class EriAmoCore:
    AXES = AXES_LIST
    HISTORY_PATH = "data/soul_history.csv"
    
    DECAY_CONFIG = {
        'emocje': {'rate': 0.05, 'floor': 0.0},
        'czas': {'rate': 0.03, 'floor': 0.0}
    }
    
    def __init__(self):
        # FIX: Używamy RLock, żeby wątek mógł wejść w locka wielokrotnie
        # (np. create_memory_dump -> compute_integrity_hash)
        self.lock = threading.RLock()
        
        self.vector = SoulVector(np.zeros(len(self.AXES), dtype=float))
        self.last_decay_time = time.time()
        self.decay_cycle_count = 0
        self.ethics = ETHICS_FRAMEWORK.copy()
        
        if not self.load_soul_from_history():
            self.vector.values[self.AXES.index('wiedza')] = 5.0
            self.vector.values[self.AXES.index('kreacja')] = 10.0
            print("[CORE] Narodziny nowej Duszy (RLock Active).")

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
        # Ta metoda wymaga locka. Jeśli wywoła ją create_memory_dump (który już ma locka),
        # zwykły Lock by się zawiesił. RLock przepuści.
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
        
        # Tu zajmujemy locka...
        with self.lock:
            dump_data = {
                "meta": {
                    "version": "5.9.3",
                    "created_at": datetime.now().isoformat(),
                    # ... a tu wywołujemy funkcję, która TEŻ chce locka!
                    "integrity_hash": self.compute_integrity_hash(), 
                    "note": "RLock fix applied."
                },
                "soul_vector": {axis: float(self.vector.values[i]) for i, axis in enumerate(self.AXES)},
                "ethics_framework": {k: v["value"] for k, v in self.ethics.items()}
            }
            
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(dump_data, f, indent=2, ensure_ascii=False)
        return filepath
