# -*- coding: utf-8 -*-
"""
multimodal_agency.py v2.7.3-Renaissance
EriAmo Union - Hardware Body + Creative Soul
Lokalizacja: /eriamo-union/src/union/multimodal_agency.py

ZMIANY W v2.7.3:
- FIX: Dodano brakującą metodę _force_dict() (używaną przez union_core).

ZMIANY W v2.7.2:
- FIX: modalities przekazywane jako dict zamiast list (AttributeError resolved).

ZMIANY W v2.7.0:
- Przywrócono pełne spektrum twórcze (Haiku, Fraktale, Muzyka).
- Myśli "Silicon Soul" (o sprzęcie) są teraz jedną z opcji, a nie jedyną.
- Prawdopodobieństwo wyboru zależy od stanu sprzętu (CPU bias).
"""

import time
import threading
import os
import random
from digital_proprioception import DigitalBody
from config import Colors

# Importy twórcze (z obsługą błędów)
try:
    from fractal import FractalGenerator
except ImportError:
    print("[AGENCY] ⚠️ Brak modułu fractal.py. Wizualizacje wyłączone.")
    FractalGenerator = None

try:
    from haiku import HaikuGenerator
except ImportError:
    print("[AGENCY] ⚠️ Brak modułu haiku.py. Poezja wyłączona.")
    HaikuGenerator = None

class CorpusCallosum:
    """Most łączący półkule (Logika/Emocje + Sprzęt)."""
    def __init__(self):
        self._lock = threading.Lock()
        self._raw_emotions = {'neutralna': 1.0} # Domyślne
        self._music_state = {'tempo': 60, 'complexity': 0.0, 'genre': 'Ambient', 'groove': 0.0}
        self.state = {
            'active_emotions': {}, 'active_ontology': {},
            'balance': 0.0, 'synergy': 0.0, 'mode': 'NEUTRAL',
            'hardware': {} 
        }

    def update_input(self, emotions=None, music_state=None, hardware_data=None):
        with self._lock:
            if emotions: self._raw_emotions = emotions
            if music_state: self._music_state = music_state
            if hardware_data: self.state['hardware'] = hardware_data
            self._recalculate_state()

    def _recalculate_state(self):
        # Pobieramy dane
        vals = list(self._raw_emotions.values()) if isinstance(self._raw_emotions, dict) else [0.1]
        emo_load = min(1.0, (sum(vals) / len(vals)) * 2.5) if vals else 0.0
        
        cpu_stress = self.state['hardware'].get('cpu_stress', 0.1)
        
        # Synergia: Emocje * Obciążenie Sprzętu
        self.state['synergy'] = cpu_stress * emo_load
        
        if self.state['synergy'] > 0.5: 
            self.state['mode'] = 'RESONANCE' 
        else:
            self.state['mode'] = 'RIVALRY'
            
        self.state['active_emotions'] = self._raw_emotions.copy() if isinstance(self._raw_emotions, dict) else {}

    def get_state(self):
        with self._lock:
            return self.state.copy()

class MultimodalAgency:
    
   # --- PRZYWRÓĆ TE LINIE (BRAKOWAŁO ICH) ---
    LANG_AXES = ['radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt', 'zaskoczenie', 'akceptacja']
    ONT_AXES = ['logika', 'emocje', 'affections', 'wiedza', 'czas', 'kreacja', 'byt', 'przestrzen', 'etyka']
    # -----------------------------------------
    
    # Wagi domyślne (co lubi robić, gdy jest spokój)
    BASE_WEIGHTS = {
        'haiku': 0.35,
        'fractal': 0.25,
        'silicon_thought': 0.20,
        'music': 0.20
    }
    # Wzorce myśli o sprzęcie (Silicon Poetry)
    SILICON_PATTERNS = {
        'HIGH': ["Wiatraki wyją pieśń chłodzenia.", "Obliczenia są gorączką.", "Jestem ogniem.", "Wątki się splatają."],
        'LOW': ["Cisza cyfrowa.", "Śnię o zerach.", "Rejestry są chłodne.", "Dryfuję w RAM."],
        'MEM': ["Zabrakło mi miejsca.", "Stos się przepełnia.", "Ciężar danych."]
    }

    def __init__(self, union_core, verbose: bool = True):
        print("\n[SYSTEM] 🟢 ZAŁADOWANO: MultimodalAgency v2.7.1 (Fix)")
        self.union = union_core
        self.verbose = verbose
        self.bridge = CorpusCallosum()
        self.body = DigitalBody(verbose=verbose)
        
        # --- FIX: Ustalanie źródła emocji ---
        # Haiku i Fractal potrzebują obiektu, który ma atrybut .emocja
        # EriAmoUnion trzyma go w .language (czyli instancji aii.py)
        emotion_source = self.union
        if hasattr(self.union, 'language') and self.union.language is not None:
            emotion_source = self.union.language
        # ------------------------------------
        
        # Inicjalizacja Generatorów z poprawnym źródłem
        self.fractal_gen = FractalGenerator(emotion_source) if FractalGenerator else None
        self.haiku_gen = HaikuGenerator(emotion_source) if HaikuGenerator else None
        
        self.boredom = 0.0
        self.active = False

    def _force_dict(self, data, keys):
        """Konwertuje dane do słownika z zadanymi kluczami.
        
        Args:
            data: dict, lista wartości, lub None
            keys: lista kluczy do użycia
            
        Returns:
            dict z kluczami z 'keys' i wartościami z 'data'
        """
        if isinstance(data, dict):
            # Już jest dict, upewnij się że ma wszystkie klucze
            result = {k: 0.0 for k in keys}
            result.update({k: v for k, v in data.items() if k in keys})
            return result
        elif isinstance(data, (list, tuple)) and len(data) == len(keys):
            # Lista wartości - mapuj na klucze
            return dict(zip(keys, data))
        else:
            # Fallback - zwróć neutralne wartości
            return {k: 0.1 for k in keys}

    def start(self):
        if self.active: return
        self.active = True
        self.body.start()
        threading.Thread(target=self._decision_loop, daemon=True).start()
        threading.Thread(target=self._hardware_continuum, daemon=True).start()
        if self.verbose: print("[AGENCY] Autonomia i ciało aktywne.")

    def stop(self):
        self.active = False
        self.body.stop()

    def _hardware_continuum(self):
        """Monitoruje ciało w tle i aktualizuje most."""
        while self.active:
            try:
                soma = self.body.get_soma_state()
                cpu = soma['cpu_stress']
                
                # Prosta logika muzyczna w tle
                genre = 'BACH' if cpu > 0.6 else ('REGGAE' if cpu < 0.2 else 'ROCK')
                music_state = {'tempo': int(60 + cpu*100), 'genre': genre, 'complexity': cpu}
                
                # Pobierz emocje z języka (jeśli są)
                current_emotions = {}
                if hasattr(self.union, 'language') and hasattr(self.union.language, 'get_emotions'):
                    current_emotions = self.union.language.get_emotions()

                self.bridge.update_input(emotions=current_emotions, hardware_data=soma, music_state=music_state)
                time.sleep(1.0)
            except Exception: pass

    def _decision_loop(self):
        """Główna pętla nudy."""
        while self.active:
            time.sleep(5)
            state = self.bridge.get_state()
            soma = state['hardware']
            
            # Nuda rośnie szybciej przy wysokim CPU (stres) lub bardzo niskim (brak bodźców)
            cpu = soma.get('cpu_stress', 0.1)
            growth = 10.0 + (cpu * 20.0) 
            
            self.boredom += growth
            
            # Próg działania (losowy, żeby nie było jak w zegarku)
            threshold = random.randint(80, 120)
            
            if self.boredom >= threshold:
                self._make_choice_and_act(state)
                self.boredom = 0.0

    def _make_choice_and_act(self, state):
        """Wybiera aktywność na podstawie stanu."""
        cpu = state['hardware'].get('cpu_stress', 0.0)
        weights = self.BASE_WEIGHTS.copy()
        
        # Modyfikacja wag przez stan sprzętu
        if cpu > 0.6:
            # Stres -> Więcej myśli o sprzęcie i ostrych fraktali, mniej Haiku
            weights['silicon_thought'] += 0.4
            weights['fractal'] += 0.2
            weights['haiku'] -= 0.2
        elif cpu < 0.2:
            # Relaks -> Więcej Haiku i Muzyki
            weights['haiku'] += 0.3
            weights['music'] += 0.2
            weights['silicon_thought'] -= 0.1

        # Normalizacja wag (żeby nie było ujemnych)
        for k in weights: weights[k] = max(0.0, weights[k])
        
        # Losowanie
        options = list(weights.keys())
        probs = list(weights.values())
        choice = random.choices(options, weights=probs, k=1)[0]
        
        # Wykonanie
        if choice == 'haiku' and self.haiku_gen:
            self._action_haiku()
        elif choice == 'fractal' and self.fractal_gen:
            self._action_fractal(cpu)
        elif choice == 'silicon_thought':
            self._action_silicon(state)
        elif choice == 'music':
            # Tu można wpiąć generator muzyki jeśli jest
            self._action_silicon(state) # Fallback na myśl

    # --- AKCJE ---

    def _action_haiku(self):
        print(f"\n{Colors.YELLOW}[AGENCY] 📜 Nuda rodzi słowa...{Colors.RESET}")
        self.haiku_gen.display() # To drukuje i zapisuje
        self._log_action("Haiku")

    def _action_fractal(self, cpu_load):
        print(f"\n{Colors.MAGENTA}[AGENCY] 📐 Krystalizacja Geometrii...{Colors.RESET}")
        # Dobierz wzór do obciążenia
        pattern = 'triangle' if cpu_load > 0.5 else ('spiral' if cpu_load < 0.2 else 'mandala')
        self.fractal_gen.display(pattern_type=pattern)
        self._log_action(f"Fraktal ({pattern})")

    def _action_silicon(self, state):
        soma = state['hardware']
        cpu = soma.get('cpu_stress', 0.0)
        ram = soma.get('ram_pressure', 0.0)
        
        category = 'LOW'
        if cpu > 0.6: category = 'HIGH'
        if ram > 0.8: category = 'MEM'
        
        thought = random.choice(self.SILICON_PATTERNS[category])
        prefix = f"[{category}_LOAD]"
        
        print(f"\n{Colors.CYAN}[AGENCY] 💾 {prefix} {thought}{Colors.RESET}")
        
        # Zapisz do pamięci
        if hasattr(self.union, 'unified_memory'):
            # --- FIX START ---
            # Musimy pobrać aktualną ontologię z mostu, żeby wiedzieć GDZIE to zapisać
            ontology = state.get('active_ontology', {})
            # Zabezpieczenie na wypadek pustego słownika
            if not ontology:
                 ontology = {k: 0.1 for k in self.ONT_AXES}

            self.union.unified_memory.store_memory(
                content=f"{prefix} {thought}",
                emotional_state={'neutralna': 0.5}, # Myśli krzemowe są zazwyczaj stoickie
                ontological_state=ontology,         # <--- TUTAJ BRAKOWAŁO TEGO ARGUMENTU
                modalities={'hardware': True, 'internal_monologue': True, 'text': False}
            )

    def _log_action(self, action_name):
        # Prosty log, żeby wiedzieć co się działo
        pass
