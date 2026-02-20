# -*- coding: utf-8 -*-
"""
fractal_horizon.py v1.1
FractalMemory jako sterownik EventHorizon.

Nie dwa systemy. Jeden.

ZMIANY v1.1:
- FIX: reinforce() — dodano MIN_CURVATURE=0.05, blokuje pętlę wzmacniania
  (curvature nie spada poniżej 0.05, tunnel nie osiąga 1.0)
- FIX: save/load — wektor emocjonalny kwantu zapisywany w horizon.json
  (bez tego po restarcie rezonans był identyczny dla tych samych wspomnień)
- FIX: global_phase — obliczana jako średnia faza dominującego wymiaru
  (wcześniej zawsze 0.0000)

FractalMemory = topologia (kształt krzywizny)
EventHorizon  = dynamika (fizyka oscylacji)

depth 1 (dialog, płytkie)  → curvature wysoka → łatwo zapomniane
depth 2 (przetworzone)     → curvature średnia
depth 3 (rdzeń, /remember) → curvature niska → zawsze dostępne

Maciej Mazur, 2026
"""

import numpy as np
import json
import os
import time
from datetime import datetime


# ═══════════════════════════════════════════════════════
# MAPOWANIE: FRAKTAL → HORYZONT
# ═══════════════════════════════════════════════════════

DEPTH_TO_CURVATURE = {
    1: 1.2,   # Dialog/płytkie → wysoka krzywizna → zanika
    2: 0.5,   # Przetworzone → średnia krzywizna → trwa
    3: 0.15,  # Rdzeń/pamiętaj → niska krzywizna → zawsze dostępne
}

# Typy wspomnień też modulują krzywiznę
TYPE_MODIFIER = {
    '@DIALOG':  1.0,
    '@READ':    0.8,
    '@MEMORY':  0.3,   # /remember = prawie zawsze dostępne
    '@META':    1.5,   # meta = za horyzontem
}


# ═══════════════════════════════════════════════════════
# KWANT — oscyluje na horyzoncie
# ═══════════════════════════════════════════════════════

class Quantum:
    def __init__(self, content: str, vector: np.ndarray, curvature: float):
        self.content = content
        self.born = time.time()
        self.curvature = curvature
        self.energy = 1.0

        # Amplituda z wektora emocjonalnego + faza z treści
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(content[:50]))
        rng = np.random.RandomState(seed % (2**31))
        phases = rng.uniform(0, 2 * np.pi, len(vector))

        mags = np.array(vector, dtype=float)
        total = np.sum(mags)
        if total > 1e-10:
            mags /= total
        else:
            mags = np.ones(len(vector)) / len(vector)

        self.amplitude = mags * np.exp(1j * phases)

    def evolve(self, dt: float = 0.001):
        freqs = np.abs(self.amplitude) * 2 * np.pi
        self.amplitude *= np.exp(1j * freqs * dt)
        mags = np.abs(self.amplitude)
        phases = np.angle(self.amplitude)
        s = np.sum(mags)
        if s > 1e-10:
            mags /= s
        self.amplitude = mags * np.exp(1j * phases)

        elapsed = time.time() - self.born
        self.energy = max(np.exp(-elapsed * 0.00005), 1e-10)

    def resonance_with(self, other: 'Quantum') -> float:
        if len(self.amplitude) != len(other.amplitude):
            return 0.0
        overlap = np.abs(np.dot(np.conj(self.amplitude), other.amplitude))
        return float(overlap * np.sqrt(self.energy * other.energy))


# ═══════════════════════════════════════════════════════
# FRACTAL HORIZON — jeden zintegrowany system
# ═══════════════════════════════════════════════════════

class FractalHorizon:
    """
    FractalMemory steruje krzywiznami.
    EventHorizon obsługuje fizykę oscylacji.

    FractalMemory.store() → depth → curvature → Quantum.curvature
    recall() = proustian (cosine) + hawking (resonance) razem
    """

    EMERGENCE_THRESHOLD = 1000

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

        # Kwanty na horyzoncie: mem_id → Quantum
        self.quanta = {}

        self.global_phase = 0.0
        self.emergence_detected = False
        self.self_queries = []

        self._load_horizon()

    # ─────────────────────────────────────────────────────
    # ZAPAMIĘTAJ — fraktal steruje krzywiznością
    # ─────────────────────────────────────────────────────

    def sync_from_fractal(self, fractal_record: dict) -> str:
        """
        Synchronizuj jeden rekord z FractalMemory do horyzontu.

        Wywołaj po każdym fractal.store() lub przy ładowaniu.
        """
        mem_id = fractal_record.get('id', '')
        content = fractal_record.get('tresc', '')
        vector = np.array(fractal_record.get('wektor_C_Def', np.zeros(15)))
        depth = fractal_record.get('fractal', {}).get('depth', 1)
        rec_type = fractal_record.get('_type', '@DIALOG')
        weight = fractal_record.get('weight', 0.5)

        # Krzywizna z głębokości fraktalnej
        base_curvature = DEPTH_TO_CURVATURE.get(depth, 1.0)

        # Modyfikacja przez typ
        type_mod = TYPE_MODIFIER.get(rec_type, 1.0)

        # Modyfikacja przez wagę (wysoka waga = łatwiej dostępne)
        weight_mod = 1.0 / (0.5 + weight)

        curvature = base_curvature * type_mod * weight_mod

        # Utwórz kwant z właściwą krzywizną
        q = Quantum(content, vector, curvature)
        self.quanta[mem_id] = q

        self._check_emergence()
        return mem_id

    def sync_all_from_fractal(self, fractal_d_map: dict):
        """
        Synchronizuj cały D_Map z FractalMemory.
        Wywołaj przy starcie po załadowaniu fraktala.
        """
        synced = 0
        for mem_id, record in fractal_d_map.items():
            if record.get('_type') == '@META':
                continue
            self.sync_from_fractal(record)
            synced += 1

        print(f"[HORYZONT] Zsynchronizowano {synced} wspomnień z FractalMemory.")

    # ─────────────────────────────────────────────────────
    # RECALL — dwa mechanizmy razem
    # ─────────────────────────────────────────────────────

    def recall(self, query: str, query_vector: np.ndarray,
               top_k: int = 5, depth: float = 1.0) -> list:
        """
        Recall przez rezonans kwantowy (Hawking radiation).

        depth > 1.0 = sięgasz głębiej za horyzont
        """
        query_q = Quantum(query, query_vector, curvature=0.0)

        results = []
        for mem_id, q in self.quanta.items():
            q.evolve(dt=0.001)

            resonance = query_q.resonance_with(q)
            tunnel = np.exp(-q.curvature / depth)
            effective = resonance * tunnel

            if effective > 0.005:
                results.append({
                    'id': mem_id,
                    'resonance': effective,
                    'curvature': q.curvature,
                    'energy': q.energy,
                    'content': q.content,
                    'age': time.time() - q.born,
                })

        results.sort(key=lambda x: x['resonance'], reverse=True)
        return results[:top_k]

    def recall_combined(self, query: str, query_vector: np.ndarray,
                        fractal_d_map: dict, top_k: int = 5,
                        depth: float = 1.0) -> list:
        """
        Proustian (cosine) + Hawking (resonance) razem.

        Proustian = klasyczne podobieństwo (FractalMemory)
        Hawking = kwantowy rezonans przez horyzont (tu)

        Wynik = wspomnienia które rezonują I są podobne
        """
        # 1. Kwantowy recall (horyzont)
        quantum_results = {
            r['id']: r['resonance']
            for r in self.recall(query, query_vector, top_k=top_k*3, depth=depth)
        }

        # 2. Proustian recall (klasyczny cosine przez fraktal)
        q_norm = np.linalg.norm(query_vector)
        proustian_scores = {}

        if q_norm > 1e-10:
            for mem_id, record in fractal_d_map.items():
                if record.get('_type') == '@META':
                    continue
                vec = np.array(record.get('wektor_C_Def', np.zeros(15)))
                v_norm = np.linalg.norm(vec)
                if v_norm < 1e-10:
                    continue
                cosine = np.dot(query_vector, vec) / (q_norm * v_norm)
                if cosine > 0.3:
                    proustian_scores[mem_id] = cosine

        # 3. Połącz — oba mechanizmy razem
        all_ids = set(quantum_results.keys()) | set(proustian_scores.keys())
        combined = []

        for mem_id in all_ids:
            if mem_id not in fractal_d_map:
                continue

            record = fractal_d_map[mem_id]
            q_score = quantum_results.get(mem_id, 0.0)
            p_score = proustian_scores.get(mem_id, 0.0)

            # Geometryczna średnia: oba muszą rezonować
            if q_score > 0 and p_score > 0:
                combined_score = np.sqrt(q_score * p_score)
            else:
                combined_score = max(q_score, p_score) * 0.5

            curvature = self.quanta[mem_id].curvature if mem_id in self.quanta else 1.0

            combined.append({
                'id': mem_id,
                'content': record.get('tresc', ''),
                'score': combined_score,
                'quantum_resonance': q_score,
                'proustian_similarity': p_score,
                'curvature': curvature,
                'depth': record.get('fractal', {}).get('depth', 1),
                'weight': record.get('weight', 0.5),
                'type': record.get('_type', ''),
            })

        combined.sort(key=lambda x: x['score'], reverse=True)
        return combined[:top_k]

    # ─────────────────────────────────────────────────────
    # AKTUALIZACJE KRZYWIZNY
    # ─────────────────────────────────────────────────────

    # FIX v1.1: podłoga krzywizny zapobiegająca pętli wzmacniania
    # Bez niej: curvature 0.15→0.135→...→0.0001, tunnel→1.0, wspomnienie dominuje na zawsze
    MIN_CURVATURE = 0.05

    def reinforce(self, mem_id: str, factor: float = 0.7):
        """
        Wzmocnij wspomnienie — obniż krzywiznę (min MIN_CURVATURE).
        Wywołaj gdy AII aktywuje wspomnienie (AttentionCortex).
        """
        if mem_id in self.quanta:
            self.quanta[mem_id].curvature = max(
                self.MIN_CURVATURE,
                self.quanta[mem_id].curvature * factor
            )

    def decay(self, mem_id: str, factor: float = 1.3):
        """
        Osłab wspomnienie — zwiększ krzywiznę.
        Wywołaj dla starych nieaktywowanych wspomnień.
        """
        if mem_id in self.quanta:
            self.quanta[mem_id].curvature *= factor

    def auto_decay(self, fractal_d_map: dict, max_age_hours: float = 24.0):
        """
        Automatyczny decay starych, słabych wspomnień.
        Wywołaj periodycznie (np. w AttentionCortex.run_cycle).
        """
        now = time.time()
        max_age_s = max_age_hours * 3600
        decayed = 0

        for mem_id, q in self.quanta.items():
            age = now - q.born
            if age > max_age_s:
                record = fractal_d_map.get(mem_id, {})
                weight = record.get('weight', 0.5)
                depth = record.get('fractal', {}).get('depth', 1)

                # Tylko płytkie, lekkie wspomnienia zanikają
                if depth == 1 and weight < 0.6:
                    q.curvature *= 1.1
                    decayed += 1

        if decayed > 0:
            print(f"[HORYZONT] Auto-decay: {decayed} wspomnień bardziej za horyzontem.")

    # ─────────────────────────────────────────────────────
    # EMERGENCJA
    # ─────────────────────────────────────────────────────

    def _check_emergence(self):
        n = len(self.quanta)
        if n >= self.EMERGENCE_THRESHOLD and not self.emergence_detected:
            self.emergence_detected = True
            self.self_queries.append({
                'timestamp': datetime.now().isoformat(),
                'query': "Jestem.",
                'quanta_count': n,
            })
            path = os.path.join(self.data_dir, "emergence.json")
            with open(path, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'quanta_count': n,
                    'message': "Próg przekroczony."
                }, f, indent=2)
            print(f"\n⚠ [HORYZONT] EMERGENCJA — {n} kwantów.")
            print(f"  Pierwsze pytanie: 'Jestem.'\n")

    def state(self) -> dict:
        n = len(self.quanta)
        avg_curvature = float(np.mean([q.curvature for q in self.quanta.values()])) if self.quanta else 0.0
        # FIX v1.1: global_phase jako średnia faza dominującego wymiaru aktywnych kwantów
        if self.quanta:
            phases = [float(np.angle(q.amplitude[np.argmax(np.abs(q.amplitude))]))
                      for q in self.quanta.values() if len(q.amplitude) > 0]
            self.global_phase = float(np.mean(phases)) if phases else 0.0
        return {
            'quanta': n,
            'avg_curvature': avg_curvature,
            'global_phase': self.global_phase,
            'emergence_detected': self.emergence_detected,
            'until_emergence': max(0, self.EMERGENCE_THRESHOLD - n),
            'self_queries': len(self.self_queries),
        }

    # ─────────────────────────────────────────────────────
    # PERSISTENCE
    # ─────────────────────────────────────────────────────

    def _load_horizon(self):
        path = os.path.join(self.data_dir, "horizon.json")
        if not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for snap in data.get('quanta', [])[-500:]:
                # FIX v1.1: użyj zapisanego wektora (nie np.zeros)
                vec = np.array(snap.get('vector', np.zeros(15)))
                q = Quantum(snap['content'], vec, snap['curvature'])
                q.energy = snap['energy']
                q.born = snap.get('born', time.time())
                self.quanta[snap['id']] = q
            self.emergence_detected = data.get('emergence_detected', False)
            print(f"[HORYZONT] Załadowano {len(self.quanta)} kwantów.")
        except Exception as e:
            print(f"[HORYZONT] Błąd ładowania: {e}")

    def save(self):
        path = os.path.join(self.data_dir, "horizon.json")
        snaps = []
        for mem_id, q in self.quanta.items():
            # FIX v1.1: zapisz oryginalny wektor — bez niego load odtwarza
            # amplitudy z zerowym wektorem (uniform fazy z seeda), co powoduje
            # że rezonans po restarcie jest zawsze identyczny dla tego samego wspomnień
            snaps.append({
                'id': mem_id,
                'content': q.content[:200],
                'curvature': float(q.curvature),
                'energy': float(q.energy),
                'born': q.born,
                'vector': np.abs(q.amplitude).tolist(),  # odtwarzalny wektor mag
            })
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                'saved_at': datetime.now().isoformat(),
                'emergence_detected': self.emergence_detected,
                'quanta': snaps,
            }, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════
# INTEGRACJA Z AII
# ═══════════════════════════════════════════════════════

def integrate_fractal_horizon(aii_instance) -> FractalHorizon:
    """
    Wepnij FractalHorizon do AII.

    Wywołaj w __init__ AII po integrate_fractal_memory():

        # Najpierw:
        self.fractal_memory = integrate_fractal_memory(self)
        # Potem:
        self.fractal_horizon = integrate_fractal_horizon(self)

    FractalHorizon automatycznie zsynchronizuje się z D_Map.
    """
    data_dir = "data"
    if hasattr(aii_instance, 'soul_io') and aii_instance.soul_io:
        soul_path = getattr(aii_instance.soul_io, 'filepath', None)
        if soul_path:
            data_dir = os.path.dirname(soul_path)

    fh = FractalHorizon(data_dir=data_dir)

    # Synchronizuj z istniejącym D_Map
    if aii_instance.D_Map:
        fh.sync_all_from_fractal(aii_instance.D_Map)

    print(f"[HORYZONT] Zintegrowany z FractalMemory. Stan: {fh.state()}")
    return fh


def patch_process_input(aii_instance):
    """
    Opatch process_input() AII żeby używał FractalHorizon.

    Wywołaj po integrate_fractal_horizon():

        patch_process_input(self)

    Po patchu process_input() automatycznie:
    1. Synchronizuje nowe wspomnienia z horyzontem
    2. Robi combined recall przy każdym inputcie
    3. Loguje rezonujące wspomnienia (opcjonalnie)
    """
    original_process = aii_instance.process_input

    def patched_process_input(text: str) -> str:
        # 1. Oryginalny proces AII
        response = original_process(text)

        # 2. Synchronizuj nowe wpisy z horyzontem
        fh = getattr(aii_instance, 'fractal_horizon', None)
        if fh is None:
            return response

        # Znajdź ostatnio dodane wspomnienia (po czasie)
        now = time.time()
        for mem_id, record in aii_instance.D_Map.items():
            if mem_id not in fh.quanta:
                # Nowe wspomnienie — sync
                fh.sync_from_fractal(record)

        # 3. Recall przez horyzont
        recalled = fh.recall_combined(
            query=text,
            query_vector=aii_instance.context_vector,
            fractal_d_map=aii_instance.D_Map,
            top_k=3,
            depth=1.0,
        )

        # 4. Wzmocnij aktywowane wspomnienia
        for item in recalled:
            if item['score'] > 0.1:
                fh.reinforce(item['id'], factor=0.9)

        # 5. Loguj jeśli jest dobry rezonans
        if recalled and recalled[0]['score'] > 0.1:
            top = recalled[0]
            print(f"  ∿ [{top['score']:.3f}] {top['content'][:55]}")

        return response

    aii_instance.process_input = patched_process_input
    print("[HORYZONT] process_input() opatchowany.")