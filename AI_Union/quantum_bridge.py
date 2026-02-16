# -*- coding: utf-8 -*-
"""
quantum_bridge.py v1.0.0
Most między AII (wektory realne 15D) a systemem kwantowym (amplitudy zespolone).

Łączy:
  - AII.context_vector (np.float32[15], wartości [0,1])
  - QuantumEmotionalState (complex amplitudes z fazą)
  - EmotionalInterference (macierz sprzężeń)
  - QuantumDecisionMaker (Grover-style)

Użycie w aii.py:
    from quantum_bridge import QuantumBridge
    self.quantum = QuantumBridge(self)

Autor: Maciej Mazur (GitHub: Maciej615)
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

from quantum_emotions import QuantumEmotionalState
from emotional_interference import EmotionalInterference
from decision_maker import QuantumDecisionMaker


# ═══════════════════════════════════════════════════════════════════════════════
# MAPOWANIE OSI: POLSKI ↔ ANGIELSKI
# ═══════════════════════════════════════════════════════════════════════════════

# Kolejność MUSI odpowiadać union_config.AXES (indeksy 0-14)
PL_TO_EN: Dict[str, str] = {
    'radość':      'joy',           # 0
    'smutek':      'sadness',       # 1
    'strach':      'fear',          # 2
    'gniew':       'anger',         # 3
    'miłość':      'trust',         # 4  (Plutchik: trust ≈ miłość/zaufanie)
    'wstręt':      'disgust',       # 5
    'zaskoczenie': 'surprise',      # 6
    'akceptacja':  'anticipation',  # 7  (Plutchik: anticipation ≈ akceptacja)
    'logika':      'logic',         # 8
    'wiedza':      'knowledge',     # 9
    'czas':        'time',          # 10
    'kreacja':     'creation',      # 11
    'byt':         'being',         # 12
    'przestrzeń':  'space',         # 13
    'chaos':       'chaos',         # 14
}

EN_TO_PL: Dict[str, str] = {v: k for k, v in PL_TO_EN.items()}

# Kolejność angielska (taka jak w QuantumEmotionalState.DIMENSIONS)
# vs kolejność polska (taka jak w union_config.AXES)
# -> potrzebujemy mapę indeksów

def _build_index_maps():
    """
    Buduje mapy: indeks_PL -> indeks_EN i odwrotnie.
    
    AII (PL):    [radość(0), smutek(1), strach(2), gniew(3), ...]
    Quantum (EN): [joy(0), trust(1), fear(2), surprise(3), ...]
    
    Te kolejności SĄ RÓŻNE - trzeba je mapować.
    """
    en_dims = QuantumEmotionalState.DIMENSIONS  # angielska kolejność
    
    # indeks w PL_AXES -> indeks w EN_DIMS
    pl_to_en_idx = {}
    en_to_pl_idx = {}
    
    for pl_idx, pl_name in enumerate(PL_TO_EN.keys()):
        en_name = PL_TO_EN[pl_name]
        en_idx = en_dims.index(en_name)
        pl_to_en_idx[pl_idx] = en_idx
        en_to_pl_idx[en_idx] = pl_idx
    
    return pl_to_en_idx, en_to_pl_idx

PL_TO_EN_IDX, EN_TO_PL_IDX = _build_index_maps()


# ═══════════════════════════════════════════════════════════════════════════════
# GŁÓWNA KLASA MOSTU
# ═══════════════════════════════════════════════════════════════════════════════

class QuantumBridge:
    """
    Most AII ↔ Quantum Emotions.
    
    Trzyma QuantumEmotionalState zsynchronizowany z AII.context_vector.
    Udostępnia interference i decision making bez zmiany API AII.
    """
    
    def __init__(self, aii_instance, verbose: bool = True):
        """
        Args:
            aii_instance: referencja do AII (potrzebuje .context_vector, .AXES_ORDER)
            verbose: czy drukować info o stanie kwantowym
        """
        self.aii = aii_instance
        self.verbose = verbose
        
        # Komponenty kwantowe
        self.state = QuantumEmotionalState()
        self.interference = EmotionalInterference()
        self.decider = QuantumDecisionMaker(self.state, self.interference)
        
        # Historia fazowa (interference patterns z czasem)
        self.phase_history: List[Dict[str, float]] = []
        self.max_history = 100
        
        # Synchronizuj z aktualnym stanem AII
        self.sync_from_aii()
        
        if self.verbose:
            print(f"\033[96m[QUANTUM] Most aktywny. "
                  f"Entropy: {self.state.entropy():.2f} bits\033[0m")
    
    # ─────────────────────────────────────────────────────────────
    # KONWERSJA: AII context_vector → QuantumEmotionalState
    # ─────────────────────────────────────────────────────────────
    
    # Minimalna amplituda - "kwantowe fluktuacje próżni"
    # Bez tego: zerowy context_vector = martwy stan kwantowy
    # Z tym: interference ZAWSZE ma materiał do pracy
    VACUUM_AMPLITUDE = 0.05

    def sync_from_aii(self):
        """
        Konwertuj AII.context_vector (real [0,1]) → quantum amplitudes (complex).
        
        Zasada:
        - magnitude = sqrt(wartość_realna) + VACUUM  (bo |α|² ≈ probability)
        - phase = zachowaj istniejącą fazę
        - VACUUM_AMPLITUDE zapewnia że stan nigdy nie jest zerowy
          (interference potrzebuje par emocji do pracy)
        """
        vec = self.aii.context_vector
        
        for pl_idx in range(len(vec)):
            en_idx = PL_TO_EN_IDX.get(pl_idx)
            if en_idx is None:
                continue
            
            en_name = QuantumEmotionalState.DIMENSIONS[en_idx]
            real_val = float(vec[pl_idx])
            
            # Magnitude z wartości realnej + vacuum floor
            magnitude = np.sqrt(max(0.0, real_val)) + self.VACUUM_AMPLITUDE
            
            # Zachowaj istniejącą fazę
            current_amp = self.state.amplitudes[en_name]
            current_phase = np.angle(current_amp)
            
            # Nowa amplituda = nowy magnitude + stara faza
            self.state.amplitudes[en_name] = magnitude * np.exp(1j * current_phase)
        
        self.state.normalize()
    
    def sync_to_aii(self):
        """
        Konwertuj quantum amplitudes → AII.context_vector.
        
        Zasada:
        - context_vector[i] = |α_i|² (probability)
        - Fazy NIE wracają do AII (AII nie obsługuje faz)
        """
        probs = self.state.get_probabilities()
        
        for en_name, prob in probs.items():
            pl_name = EN_TO_PL.get(en_name)
            if pl_name is None:
                continue
            
            # Znajdź indeks PL
            pl_names = list(PL_TO_EN.keys())
            pl_idx = pl_names.index(pl_name)
            
            # Ustaw w AII (clamp do [0, 1])
            self.aii.context_vector[pl_idx] = np.clip(prob, 0.0, 1.0)
    
    # ─────────────────────────────────────────────────────────────
    # GŁÓWNE OPERACJE
    # ─────────────────────────────────────────────────────────────
    
    def process_interference(self, time_step: float = 0.1) -> Dict[str, float]:
        """
        Zastosuj interference emocjonalną.
        
        Wywoływane po każdym interact() w AII:
        1. Sync z AII → quantum
        2. Apply interference (emocje wpływają na siebie)
        3. Sync quantum → AII
        
        Returns:
            Dict z metrykami: entropy, resonance, dominant
        """
        # 1. Aktualizuj stan kwantowy z AII
        self.sync_from_aii()
        
        # 2. Interference: emocje modulują się nawzajem
        self.state = self.interference.apply_interference(
            self.state, time_step=time_step
        )
        
        # 3. Oblicz rezonans
        resonance = self.interference.resonance_strength(self.state)
        
        # 4. Zapisz historię faz
        phases = {
            dim: float(np.angle(self.state.amplitudes[dim]))
            for dim in self.state.DIMENSIONS
        }
        self.phase_history.append(phases)
        if len(self.phase_history) > self.max_history:
            self.phase_history.pop(0)
        
        # 5. Sync z powrotem do AII
        self.sync_to_aii()
        
        # Metryki
        dominant = self.state.dominant_emotion()
        entropy = self.state.entropy()
        
        if self.verbose:
            dom_pl = EN_TO_PL.get(dominant[0], dominant[0])
            print(f"\033[35m[QUANTUM] {dom_pl.upper()} "
                  f"(prob={dominant[1]:.1%}) | "
                  f"Rezonans: {resonance:+.3f} | "
                  f"Entropy: {entropy:.2f} bits\033[0m")
        
        return {
            'entropy': entropy,
            'resonance': resonance,
            'dominant_en': dominant[0],
            'dominant_pl': EN_TO_PL.get(dominant[0], dominant[0]),
            'dominant_prob': dominant[1],
        }
    
    def quantum_decide(self, situation: dict) -> dict:
        """
        Kwantowe podejmowanie decyzji (Grover-style).
        
        Używane gdy AII potrzebuje zdecydować między opcjami.
        
        Args:
            situation: kontekst sytuacji (np. {'type': 'criticism'})
        
        Returns:
            dict z action, confidence, alternatives
        """
        # Sync przed decyzją
        self.sync_from_aii()
        
        # Aktualizuj decider z aktualnym stanem
        self.decider.emotional_state = self.state
        
        # Decide
        decision = self.decider.decide(situation, verify=True)
        
        return decision
    
    def measure_emotion(self) -> Tuple[str, str]:
        """
        Kwantowy pomiar - probabilistyczny kolaps.
        
        Returns:
            (en_name, pl_name) - zmierzona emocja
        """
        self.sync_from_aii()
        en_emotion = self.state.measure()
        pl_emotion = EN_TO_PL.get(en_emotion, en_emotion)
        return en_emotion, pl_emotion
    
    def get_quantum_state(self) -> Dict[str, dict]:
        """
        Pełny stan kwantowy do inspekcji / zapisu.
        
        Returns:
            Dict[emotion_pl] -> {magnitude, phase_deg, probability}
        """
        self.sync_from_aii()
        
        result = {}
        for en_name, amp in self.state.amplitudes.items():
            pl_name = EN_TO_PL.get(en_name, en_name)
            result[pl_name] = {
                'magnitude': float(abs(amp)),
                'phase_deg': float(np.degrees(np.angle(amp))),
                'probability': float(abs(amp) ** 2),
                'en_name': en_name,
            }
        
        return result
    
    def get_phase_coherence(self) -> float:
        """
        Mierzy koherencję faz w czasie.
        
        Wysoka koherencja = stabilne fazy = spójny stan emocjonalny
        Niska koherencja = chaotyczne fazy = niestabilność
        """
        if len(self.phase_history) < 2:
            return 1.0
        
        # Porównaj ostatnie 2 snapshoty faz
        prev = self.phase_history[-2]
        curr = self.phase_history[-1]
        
        diffs = []
        for dim in self.state.DIMENSIONS:
            if dim in prev and dim in curr:
                # Różnica faz (uwzględniając cykliczność)
                diff = abs(curr[dim] - prev[dim])
                diff = min(diff, 2 * np.pi - diff)
                diffs.append(diff)
        
        if not diffs:
            return 1.0
        
        # Koherencja = 1 - znormalizowana średnia zmiana faz
        mean_diff = np.mean(diffs)
        coherence = 1.0 - (mean_diff / np.pi)
        
        return max(0.0, min(1.0, coherence))
    
    # ─────────────────────────────────────────────────────────────
    # RANKING KANDYDATÓW (serce integracji z resonance engine)
    # ─────────────────────────────────────────────────────────────
    
    def rank_candidates(self, candidates: list, top_n: int = 5) -> list:
        """
        Kwantowy ranking kandydatów z D_Map.
        
        ZAMIAST random.choice(candidates[:3]) — deterministyczny wybór
        oparty na rezonansie emocjonalnym + predykcji trajektorii.
        
        Args:
            candidates: [(classical_score, mem_id, entry), ...]
            top_n: ile top kandydatów wziąć do rankingu
        
        Returns:
            Posortowana lista [(final_score, mem_id, entry), ...]
        """
        if not candidates:
            return candidates
        
        self.sync_from_aii()
        
        # Predykcja: gdzie zmierza stan emocjonalny?
        predicted_state = self._predict_trajectory()
        
        ranked = []
        max_classical = max(c[0] for c in candidates[:top_n]) if candidates else 1.0
        
        for score, mid, entry in candidates[:top_n]:
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(15)))
            
            # 1. Rezonans kwantowy: jak pamięć rezonuje z OBECNYM stanem
            q_resonance = self._memory_resonance(mem_vec)
            
            # 2. Predykcja: jak pamięć pasuje do PRZYSZŁEGO stanu
            q_prediction = self._memory_trajectory_fit(mem_vec, predicted_state)
            
            # 3. Fazowa koherencja: pamięci z podobną fazą = stabilniejsza odpowiedź
            q_phase = self._memory_phase_alignment(mem_vec)
            
            # Normalizacja classical score do [0, 1]
            classical_norm = score / max_classical if max_classical > 0 else 0
            
            # Końcowy score: classical + quantum
            # Wagi: 50% klasyczny (keywords+weight), 25% rezonans, 15% predykcja, 10% faza
            final_score = (
                classical_norm * 0.50 +
                q_resonance   * 0.25 +
                q_prediction  * 0.15 +
                q_phase       * 0.10
            )
            
            # Boost od RL weight (zachowaj wpływ +/-)
            weight = entry.get('weight', 0.5)
            final_score *= (0.5 + weight)
            
            ranked.append((final_score, mid, entry))
        
        # Dodaj resztę kandydatów (poza top_n) z oryginalnym score
        for score, mid, entry in candidates[top_n:]:
            ranked.append((score / max_classical * 0.3, mid, entry))
        
        ranked.sort(key=lambda x: x[0], reverse=True)
        
        # Verbose
        if self.verbose and len(ranked) >= 2:
            top = ranked[0]
            second = ranked[1]
            delta = top[0] - second[0]
            print(f"\033[35m[QUANTUM-RANK] "
                  f"#{1}: {top[2].get('tresc','')[:40]}... "
                  f"(q={top[0]:.3f}) | "
                  f"Δ={delta:+.3f}\033[0m")
        
        return ranked
    
    def _memory_resonance(self, mem_vec: np.ndarray) -> float:
        """
        Jak mocno pamięć rezonuje z OBECNYM stanem kwantowym?
        
        Symuluje: gdybyśmy "załadowali" tę pamięć, czy wzmocni
        konstruktywne patterny (dobrze) czy destrukcyjne (źle)?
        """
        if np.sum(np.abs(mem_vec)) < 0.01:
            return 0.5  # Neutralna pamięć
        
        # Utwórz symulowany stan z pamięci
        sim_state = QuantumEmotionalState()
        for dim in sim_state.DIMENSIONS:
            sim_state.amplitudes[dim] = self.state.amplitudes[dim]
        
        # Dodaj wpływ pamięci
        for pl_idx, val in enumerate(mem_vec):
            if val < 0.01:
                continue
            en_idx = PL_TO_EN_IDX.get(pl_idx)
            if en_idx is None:
                continue
            en_name = QuantumEmotionalState.DIMENSIONS[en_idx]
            sim_state.amplitudes[en_name] += np.sqrt(val) * 0.2
        
        sim_state.normalize()
        
        # Rezonans symulowanego stanu
        resonance = self.interference.resonance_strength(sim_state)
        
        # Normalizacja do [0, 1]
        return np.clip(0.5 + resonance, 0.0, 1.0)
    
    def _predict_trajectory(self) -> dict:
        """
        Predykcja: gdzie emocje zmierzają w następnych krokach?
        
        Używa historii faz — kierunek zmiany faz wskazuje
        "emocjonalną inercję" systemu.
        
        Returns:
            Dict[en_name] -> predicted_magnitude
        """
        predicted = {}
        probs = self.state.get_probabilities()
        
        if len(self.phase_history) < 3:
            # Za mało historii — zwróć obecny stan
            return probs
        
        # Trend z ostatnich 3 kroków
        recent = self.phase_history[-3:]
        
        for dim in self.state.DIMENSIONS:
            current_prob = probs.get(dim, 0.0)
            
            # Stabilność fazy = emocja się wzmacnia
            phases = [step.get(dim, 0.0) for step in recent]
            phase_diffs = []
            for i in range(1, len(phases)):
                diff = abs(phases[i] - phases[i-1])
                diff = min(diff, 2 * np.pi - diff)
                phase_diffs.append(diff)
            
            avg_phase_change = np.mean(phase_diffs) if phase_diffs else np.pi
            
            # Stabilna faza → emocja rośnie, niestabilna → maleje
            stability = 1.0 - (avg_phase_change / np.pi)
            predicted[dim] = current_prob * (1.0 + stability * 0.3)
        
        # Normalizacja
        total = sum(predicted.values())
        if total > 0:
            predicted = {k: v/total for k, v in predicted.items()}
        
        return predicted
    
    def _memory_trajectory_fit(self, mem_vec: np.ndarray, 
                                predicted: dict) -> float:
        """
        Jak dobrze pamięć pasuje do PREDYKOWANEGO stanu?
        
        Pamięci zgodne z trajektorią emocjonalną = wyższy score.
        To sprawia, że system "przewiduje" i wybiera odpowiedzi
        pasujące do tego, dokąd zmierza emocjonalnie.
        """
        if np.sum(np.abs(mem_vec)) < 0.01:
            return 0.5
        
        # Konwertuj mem_vec (PL indices) na EN probabilities
        mem_probs = {}
        mem_total = np.sum(np.abs(mem_vec)) + 1e-10
        
        pl_names = list(PL_TO_EN.keys())
        for pl_idx, val in enumerate(mem_vec):
            if pl_idx < len(pl_names):
                en_name = PL_TO_EN[pl_names[pl_idx]]
                mem_probs[en_name] = abs(val) / mem_total
        
        # Cosine similarity między predykowanym stanem a pamięcią
        dot = 0.0
        norm_p = 0.0
        norm_m = 0.0
        
        for dim in self.state.DIMENSIONS:
            p = predicted.get(dim, 0.0)
            m = mem_probs.get(dim, 0.0)
            dot += p * m
            norm_p += p * p
            norm_m += m * m
        
        denom = np.sqrt(norm_p * norm_m)
        if denom < 1e-10:
            return 0.5
        
        similarity = dot / denom
        return np.clip(similarity, 0.0, 1.0)
    
    def _memory_phase_alignment(self, mem_vec: np.ndarray) -> float:
        """
        Fazowa koherencja pamięci z obecnym stanem.
        
        Pamięci, których emocjonalny profil "współgra" fazowo
        z aktualnym stanem = stabilniejszy output.
        """
        if np.sum(np.abs(mem_vec)) < 0.01:
            return 0.5
        
        alignment = 0.0
        count = 0
        
        pl_names = list(PL_TO_EN.keys())
        for pl_idx, val in enumerate(mem_vec):
            if val < 0.05 or pl_idx >= len(pl_names):
                continue
            
            en_name = PL_TO_EN[pl_names[pl_idx]]
            if en_name not in self.state.amplitudes:
                continue
            
            amp = self.state.amplitudes[en_name]
            phase = np.angle(amp)
            magnitude = abs(amp)
            
            # Silna emocja + stabilna faza + pamięć ma tę emocję = alignment
            alignment += val * magnitude * np.cos(phase) ** 2
            count += 1
        
        if count == 0:
            return 0.5
        
        return np.clip(0.5 + alignment / count, 0.0, 1.0)
    
    def emotional_veto_check(self, action_vector: np.ndarray) -> Tuple[bool, str]:
        """
        Sprawdza czy akcja nie spowoduje destrukcyjnej interference.
        
        Używane przez conscience.py jako dodatkowy test:
        - Symuluje stan po akcji
        - Sprawdza czy rezonans nie jest silnie negatywny
        
        Args:
            action_vector: wektor wpływu akcji (15D, real)
        
        Returns:
            (is_safe, reason)
        """
        # Symuluj stan po akcji
        sim_state = QuantumEmotionalState()
        
        # Kopiuj amplitudy
        for dim in sim_state.DIMENSIONS:
            sim_state.amplitudes[dim] = self.state.amplitudes[dim]
        
        # Dodaj wpływ akcji
        for pl_idx, val in enumerate(action_vector):
            if val < 0.01:
                continue
            en_idx = PL_TO_EN_IDX.get(pl_idx)
            if en_idx is None:
                continue
            en_name = QuantumEmotionalState.DIMENSIONS[en_idx]
            current = sim_state.amplitudes[en_name]
            sim_state.amplitudes[en_name] = current + np.sqrt(val) * 0.3
        
        sim_state.normalize()
        
        # Sprawdź rezonans po akcji
        resonance = self.interference.resonance_strength(sim_state)
        
        if resonance < -0.5:
            return False, f"Silna destrukcyjna interference (rezonans: {resonance:.3f})"
        
        return True, f"OK (rezonans: {resonance:.3f})"
    
    # ─────────────────────────────────────────────────────────────
    # SERIALIZACJA (.soul)
    # ─────────────────────────────────────────────────────────────
    
    def to_dict(self) -> dict:
        """Serializuj stan kwantowy do dict (dla .soul file)."""
        return {
            'amplitudes': {
                dim: {
                    'magnitude': float(abs(amp)),
                    'phase': float(np.angle(amp)),
                }
                for dim, amp in self.state.amplitudes.items()
            },
            'entropy': float(self.state.entropy()),
            'coherence': float(self.get_phase_coherence()),
        }
    
    def from_dict(self, data: dict):
        """Odtwórz stan kwantowy z dict."""
        if 'amplitudes' not in data:
            return
        
        for dim, vals in data['amplitudes'].items():
            if dim in self.state.amplitudes:
                mag = vals.get('magnitude', 0.0)
                phase = vals.get('phase', 0.0)
                self.state.amplitudes[dim] = mag * np.exp(1j * phase)
        
        self.state.normalize()


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: integracja z AII (wzorowane na integrate_fractal_memory)
# ═══════════════════════════════════════════════════════════════════════════════

def integrate_quantum_bridge(aii_instance, verbose: bool = True) -> QuantumBridge:
    """
    Factory function do integracji z AII.
    
    Użycie w aii.py __init__:
        from quantum_bridge import integrate_quantum_bridge
        self.quantum = integrate_quantum_bridge(self)
    """
    bridge = QuantumBridge(aii_instance, verbose=verbose)
    return bridge


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Mock AII do testów
    class MockAII:
        AXES_ORDER = [
            'radość', 'smutek', 'strach', 'gniew',
            'miłość', 'wstręt', 'zaskoczenie', 'akceptacja',
            'logika', 'wiedza', 'czas', 'kreacja',
            'byt', 'przestrzeń', 'chaos'
        ]
        DIM = 15
        
        def __init__(self):
            self.context_vector = np.zeros(15, dtype=np.float32)
    
    print("=" * 60)
    print("TEST: QuantumBridge")
    print("=" * 60)
    
    # 1. Utwórz mock AII
    aii = MockAII()
    aii.context_vector[0] = 0.7   # radość = 0.7
    aii.context_vector[2] = 0.3   # strach = 0.3
    aii.context_vector[8] = 0.5   # logika = 0.5
    
    print(f"\nAII vector: radość={aii.context_vector[0]:.2f}, "
          f"strach={aii.context_vector[2]:.2f}, "
          f"logika={aii.context_vector[8]:.2f}")
    
    # 2. Utwórz bridge
    bridge = QuantumBridge(aii, verbose=True)
    
    # 3. Stan kwantowy
    print(f"\nStan kwantowy:")
    qs = bridge.get_quantum_state()
    for name, data in sorted(qs.items(), key=lambda x: -x[1]['probability']):
        if data['probability'] > 0.01:
            print(f"  {name:12s}: mag={data['magnitude']:.3f}, "
                  f"phase={data['phase_deg']:+6.1f}°, "
                  f"prob={data['probability']:.3f}")
    
    # 4. Interference
    print(f"\nInterference (5 kroków):")
    for i in range(5):
        metrics = bridge.process_interference(time_step=0.1)
        print(f"  t={i}: {metrics['dominant_pl'].upper()} "
              f"(entropy={metrics['entropy']:.2f}, "
              f"rezonans={metrics['resonance']:+.3f})")
    
    # 5. Pomiar
    print(f"\nPomiary kwantowe (5x):")
    for i in range(5):
        en, pl = bridge.measure_emotion()
        print(f"  Pomiar {i+1}: {pl} ({en})")
    
    # 6. Koherencja
    print(f"\nKoherencja faz: {bridge.get_phase_coherence():.3f}")
    
    # 7. Sprawdź sync z powrotem
    print(f"\nAII vector po sync:")
    print(f"  radość={aii.context_vector[0]:.3f}, "
          f"strach={aii.context_vector[2]:.3f}, "
          f"logika={aii.context_vector[8]:.3f}")
    
    # 8. Serializacja
    saved = bridge.to_dict()
    print(f"\nSerializacja: {len(saved['amplitudes'])} wymiarów, "
          f"entropy={saved['entropy']:.2f}")
    
    print("\n✅ Test zakończony.")