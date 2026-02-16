# -*- coding: utf-8 -*-
"""
fractal_memory.py v1.0.4 – FIXED VERSION (05.02.2026)
POPRAWKI:
- Domyślna ścieżka: data/eriamo.soul (nie eriamo.soul)
- integrate_fractal_memory: nie wywołuje original_load() (łamało referencję)
- Migracja wspomnień z AII do Fractal przy integracji
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
    VERSION = "1.0.4"

    # POPRAWKA: Domyślna ścieżka to data/eriamo.soul
    def __init__(self, soul_file: str = "data/eriamo.soul", verbose: bool = False):
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
            print(f"{Colors.CYAN}[FRACTAL] v{self.VERSION} zainicjalizowana – {stats['total']} wspomnień (plik: {self.soul_file}){Colors.RESET}")

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

        # Upewnij się że depth istnieje w indeksie
        if depth not in self._depth_index:
            self._depth_index[depth] = set()

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
                    print(f"{Colors.GREEN}[FRACTAL] Wczytano {stats['total']} wspomnień z {self.soul_file}{Colors.RESET}")
                return True
            except Exception as e:
                print(f"{Colors.RED}[FRACTAL] Błąd ładowania: {e}{Colors.RESET}")
                return False

    def save(self) -> bool:
        with self._lock:
            try:
                # Upewnij się że katalog istnieje
                directory = os.path.dirname(self.soul_file)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)

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
                    print(f"{Colors.GREEN}[FRACTAL] Zapisano {len(self.D_Map)} wspomnień do {self.soul_file}{Colors.RESET}")
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
# INTEGRACJA Z AII - POPRAWIONA WERSJA
# ═══════════════════════════════════════════════════════════════════════════════

def integrate_fractal_memory(aii_instance, soul_file: str = "data/eriamo.soul"):
    """
    Integruje FractalMemory z instancją AII.
    
    POPRAWKI v1.0.4:
    - Migracja istniejących wspomnień z AII do Fractal
    - NIE wywołuje original_load() (to łamało referencję D_Map)
    - Tylko Fractal zapisuje do .soul (unika podwójnego zapisu)
    """
    print(f"{Colors.CYAN}[FRACTAL] Integracja z plikiem: {soul_file}{Colors.RESET}")
    
    fractal = FractalMemory(soul_file, verbose=True)
    
    # Migruj istniejące wspomnienia z AII do Fractal (jeśli AII ma więcej)
    if aii_instance.D_Map:
        migrated = 0
        for mid, record in aii_instance.D_Map.items():
            if mid not in fractal.D_Map:
                fractal.D_Map[mid] = record
                fractal._index_record(mid, record)
                migrated += 1
        if migrated > 0:
            print(f"{Colors.YELLOW}[FRACTAL] Zmigrowano {migrated} wspomnień z AII{Colors.RESET}")
    
    # KRYTYCZNE: Wspólna referencja - AII używa tego samego D_Map co Fractal
    aii_instance.D_Map = fractal.D_Map
    aii_instance.fractal_memory = fractal

    def new_save():
        """Zapisuje pamięć - tylko Fractal zapisuje do .soul"""
        fractal.save()
        
        # Zapisz pozostałe komponenty (chunki, cortex)
        if aii_instance.chunk_lexicon:
            aii_instance.chunk_lexicon.save()
        if hasattr(aii_instance, 'cortex') and aii_instance.soul_io and hasattr(aii_instance.soul_io, 'filepath'):
            aii_instance.cortex.save(aii_instance.soul_io.filepath)
        
        print(f"{Colors.GREEN}[SAVE] Zapisano {len(fractal.D_Map)} wspomnień{Colors.RESET}")

    def new_load():
        """Ładuje pamięć - tylko z Fractal"""
        fractal.load()
        aii_instance.D_Map = fractal.D_Map  # Utrzymaj wspólną referencję!
        # NIE wywołujemy original_load() - to nadpisywało D_Map nowym obiektem!
        print(f"{Colors.GREEN}[LOAD] Wczytano {len(fractal.D_Map)} wspomnień{Colors.RESET}")

    aii_instance.save = new_save
    aii_instance.load = new_load

    stats = fractal.get_statistics()
    print(f"{Colors.GREEN}[FRACTAL] Zintegrowano - {stats['total']} wspomnień aktywnych{Colors.RESET}")
    return fractal


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{Colors.CYAN}TEST FractalMemory v1.0.4{Colors.RESET}")
    
    # Test z domyślną ścieżką
    mem = FractalMemory("test_fractal.soul", verbose=True)
    
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
    recalled = mem.proustian_recall(np.array([0,0,0,0,0.9,0,0,0]))
    for r in recalled:
        print(f" - {r.get('tresc')} (waga: {r.get('weight')})")
    
    mem.save()
    
    # Cleanup
    if os.path.exists("test_fractal.soul"):
        os.remove("test_fractal.soul")
    if os.path.exists("test_fractal.soul.bak"):
        os.remove("test_fractal.soul.bak")
    
    print(f"\n{Colors.GREEN}Test zakończony.{Colors.RESET}")