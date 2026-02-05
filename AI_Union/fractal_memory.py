# -*- coding: utf-8 -*-
"""
fractal_memory.py v1.0.3 – stabilna wersja z poprawionym proustian_recall (05.02.2026)
"""

import numpy as np
import json
import time
import hashlib
import os
import threading
import shutil
from typing import Dict, List, Optional
from collections import defaultdict
from dataclasses import dataclass, field, asdict

try:
    from union_config import UnionConfig, Colors, AXES, DIMENSION
except ImportError:
    AXES = ['radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt',
            'zaskoczenie', 'akceptacja', 'logika', 'wiedza', 'czas',
            'kreacja', 'byt', 'przestrzeń', 'chaos']
    DIMENSION = 15
    class Colors:
        CYAN = "\033[36m"
        RESET = "\033[0m"
        YELLOW = "\033[33m"
        MAGENTA = "\033[35m"
        GREEN = "\033[32m"
        RED = "\033[31m"


# ═══════════════════════════════════════════════════════════════════════════════
# STRUKTURY DANYCH
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FractalMetadata:
    depth: int = 1
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    abstraction_hash: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'FractalMetadata':
        return cls(**data) if data else cls()


@dataclass
class ResonanceMetadata:
    linked_ids: List[str] = field(default_factory=list)
    activation_count: int = 0
    last_resonance: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'ResonanceMetadata':
        return cls(**data) if data else cls()


# ═══════════════════════════════════════════════════════════════════════════════
# GŁÓWNA KLASA
# ═══════════════════════════════════════════════════════════════════════════════

class FractalMemory:
    VERSION = "1.0.3"

    def __init__(self, soul_file: str = "eriamo.soul", verbose: bool = False):
        self.soul_file = soul_file
        self.verbose = verbose

        self.D_Map: Dict[str, dict] = {}
        self._parent_index: Dict[str, str] = {}
        self._children_index: Dict[str, List[str]] = defaultdict(list)
        self._depth_index: Dict[int, set] = {1: set(), 2: set(), 3: set()}
        self._type_index: Dict[str, set] = defaultdict(set)

        self.stats = {
            'total': 0,
            'by_depth': {1: 0, 2: 0, 3: 0},
            'version': self.VERSION
        }

        self._lock = threading.RLock()

        self.load()

        if self.verbose:
            stats = self.get_statistics()
            print(f"{Colors.CYAN}[FRACTAL] v{self.VERSION} zainicjalizowana – {stats['total']} wspomnień{Colors.RESET}")

    def _clear_indices(self):
        """Resetuje wszystkie indeksy."""
        with self._lock:
            self._parent_index.clear()
            self._children_index.clear()
            self._depth_index = {1: set(), 2: set(), 3: set()}
            self._type_index.clear()
            if self.verbose:
                print(f"{Colors.YELLOW}[FRACTAL] Indeksy wyczyszczone{Colors.RESET}")

    def _index_record(self, mem_id: str, record: dict):
        """Dodaje rekord do indeksów."""
        fractal = record.get('fractal', {})
        depth = fractal.get('depth', 1)
        parent = fractal.get('parent_id')
        rec_type = record.get('_type', '@MEMORY')

        self._depth_index[depth].add(mem_id)
        self._type_index[rec_type].add(mem_id)

        if parent:
            self._parent_index[mem_id] = parent
            if mem_id not in self._children_index[parent]:
                self._children_index[parent].append(mem_id)

    def get_statistics(self) -> dict:
        """Zwraca aktualne statystyki."""
        with self._lock:
            self.stats['total'] = len(self.D_Map)
            for d in [1, 2, 3]:
                self.stats['by_depth'][d] = len(self._depth_index.get(d, set()))
            return self.stats.copy()

    def load(self) -> bool:
        if not os.path.exists(self.soul_file):
            if self.verbose:
                print(f"{Colors.YELLOW}[FRACTAL] Brak pliku {self.soul_file} – tabula rasa{Colors.RESET}")
            return False

        with self._lock:
            self.D_Map.clear()
            self._clear_indices()

            try:
                with open(self.soul_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            record = json.loads(line)
                            if record.get('_type') == '@META':
                                continue
                            mem_id = record.get('id', f"Mem_{line_num:05d}")
                            record['id'] = mem_id
                            self.D_Map[mem_id] = record
                            self._index_record(mem_id, record)
                        except json.JSONDecodeError:
                            continue

                stats = self.get_statistics()
                if self.verbose:
                    print(f"{Colors.GREEN}[FRACTAL] Wczytano {stats['total']} wspomnień{Colors.RESET}")
                return True
            except Exception as e:
                print(f"{Colors.RED}[FRACTAL] Błąd ładowania: {e}{Colors.RESET}")
                return False

    def save(self) -> bool:
        with self._lock:
            try:
                if os.path.exists(self.soul_file):
                    shutil.copy2(self.soul_file, self.soul_file + ".bak")

                temp_path = self.soul_file + ".tmp"
                with open(temp_path, 'w', encoding='utf-8') as f:
                    meta = {"_type": "@META", "version": self.VERSION, "stats": self.get_statistics()}
                    f.write(json.dumps(meta, ensure_ascii=False) + "\n")

                    for rec in self.D_Map.values():
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

                os.replace(temp_path, self.soul_file)
                if self.verbose:
                    print(f"{Colors.GREEN}[FRACTAL] Zapisano {len(self.D_Map)} wspomnień{Colors.RESET}")
                return True
            except Exception as e:
                print(f"{Colors.RED}[FRACTAL] Błąd zapisu: {e}{Colors.RESET}")
                return False

    def store(
        self,
        content: str,
        vector: np.ndarray | list,
        rec_type: str = "@DIALOG",
        weight: float = 0.5,
        auto_link: bool = True,
        auto_parent: bool = True
    ) -> str:
        """Zapisuje nowe wspomnienie."""
        if isinstance(vector, np.ndarray):
            vector = vector.tolist()

        mem_id = f"Mem_{int(time.time())}_{len(self.D_Map):04d}"

        depth = 1
        if weight >= 0.90:
            depth = 3
        elif weight >= 0.60:
            depth = 2

        record = {
            "id": mem_id,
            "tresc": content,
            "wektor_C_Def": vector,
            "_type": rec_type,
            "weight": weight,
            "time": time.time(),
            "fractal": {
                "depth": depth,
                "parent_id": None,
                "children_ids": []
            },
            "resonance": {
                "linked_ids": [],
                "activation_count": 0,
                "last_resonance": time.time()
            }
        }

        with self._lock:
            self.D_Map[mem_id] = record
            self._index_record(mem_id, record)
            self.stats['total'] = len(self.D_Map)
            self.stats['by_depth'][depth] = self.stats['by_depth'].get(depth, 0) + 1

        if self.verbose:
            print(f"[FRACTAL] Zapisano {mem_id} (depth={depth})")

        return mem_id

    def proustian_recall(self, emotion_vector: np.ndarray, threshold: float = 0.6) -> List[dict]:
        """Proustowski recall – rozszerza wektor 8D do 15D."""
        emotion_vector = np.array(emotion_vector)
        if len(emotion_vector) == 8:
            full_vec = np.zeros(DIMENSION)
            full_vec[:8] = emotion_vector  # pierwsze 8 to Plutchik
            emotion_vector = full_vec

        emo_norm = np.linalg.norm(emotion_vector)
        if emo_norm < 0.01:
            return []

        matches = []
        for mid, rec in self.D_Map.items():
            vec = np.array(rec.get('wektor_C_Def', [0] * DIMENSION))
            vec_norm = np.linalg.norm(vec)
            if vec_norm < 0.01:
                continue
            sim = np.dot(emotion_vector, vec) / (emo_norm * vec_norm)
            if sim >= threshold:
                matches.append(rec)

        matches.sort(key=lambda r: r.get('weight', 0.5), reverse=True)
        return matches[:5]


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRACJA Z AII
# ═══════════════════════════════════════════════════════════════════════════════

def integrate_fractal_memory(aii_instance, soul_file: str = "eriamo.soul"):
    fractal = FractalMemory(soul_file, verbose=True)
    aii_instance.D_Map = fractal.D_Map
    aii_instance.fractal_memory = fractal

    original_save = getattr(aii_instance, 'save', lambda: None)
    original_load = getattr(aii_instance, 'load', lambda: None)

    def new_save():
        fractal.save()
        original_save()

    def new_load():
        fractal.load()
        aii_instance.D_Map = fractal.D_Map
        original_load()

    aii_instance.save = new_save
    aii_instance.load = new_load

    stats = fractal.get_statistics()
    print(f"{Colors.GREEN}[FRACTAL] Załadowano {stats['total']} wspomnień{Colors.RESET}")
    return fractal


# ═══════════════════════════════════════════════════════════════════════════════
# TEST – teraz działa bez błędu shape
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{Colors.CYAN}TEST FractalMemory v1.0.3{Colors.RESET}")
    
    mem = FractalMemory("test.soul", verbose=True)
    
    mem.store(
        content="Test miłości",
        vector=np.array([0,0,0,0,1.0,0,0,0.5] + [0]*7),
        weight=0.8
    )
    
    mem.store(
        content="Test smutku",
        vector=np.array([0,1.0,0,0,0,0,0,0] + [0]*7),
        weight=0.4
    )
    
    print("\nStatystyki:")
    print(mem.get_statistics())
    
    print("\nProustian recall (miłość):")
    recalled = mem.proustian_recall(np.array([0,0,0,0,0.9,0,0,0]))  # 8D → automatycznie rozszerzone do 15D
    for r in recalled:
        print(f" - {r.get('tresc')} (waga: {r.get('weight')})")
    
    mem.save()
    
    print(f"\n{Colors.GREEN}Test zakończony.{Colors.RESET}")