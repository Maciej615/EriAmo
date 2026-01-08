# -*- coding: utf-8 -*-
"""
multimodal_agency.py v2.9.1-Focus
EriAmo Union - Hardware Body + Creative Soul + INTERNAL CRITIC + ATTENTION
Lokalizacja: /eriamo-union/src/union/multimodal_agency.py

ZMIANY v2.9.1:
- ATTENTION: Pętla decyzyjna respektuje flagę 'in_dialogue'.
- FIX: Naprawiono błąd, gdzie nuda rosła w trakcie rozmowy.
"""

import time
import threading
import os
import random
from digital_proprioception import DigitalBody
from config import Colors

try:
    from fractal import FractalGenerator
except ImportError:
    print("[AGENCY] ⚠️ Brak fractal.py.")
    FractalGenerator = None

try:
    from haiku import HaikuGenerator
except ImportError:
    print("[AGENCY] ⚠️ Brak haiku.py.")
    HaikuGenerator = None

class CorpusCallosum:
    def __init__(self):
        self._lock = threading.Lock()
        self._raw_emotions = {'neutralna': 1.0}
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
        vals = list(self._raw_emotions.values()) if isinstance(self._raw_emotions, dict) else [0.1]
        emo_load = min(1.0, (sum(vals) / len(vals)) * 2.5) if vals else 0.0
        cpu_stress = self.state['hardware'].get('cpu_stress', 0.1)
        self.state['synergy'] = cpu_stress * emo_load
        self.state['active_emotions'] = self._raw_emotions.copy() if isinstance(self._raw_emotions, dict) else {}

    def get_state(self):
        with self._lock: return self.state.copy()

class MultimodalAgency:
    
    LANG_AXES = ['radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt', 'zaskoczenie', 'akceptacja']
    ONT_AXES = ['logika', 'emocje', 'affections', 'wiedza', 'czas', 'kreacja', 'byt', 'przestrzen', 'etyka']
    
    BASE_WEIGHTS = {
        'haiku': 0.35,
        'fractal': 0.25,
        'silicon_thought': 0.20,
        'music': 0.20
    }
    
    SILICON_PATTERNS = {
        'HIGH': ["Wiatraki wyją pieśń chłodzenia.", "Obliczenia są gorączką.", "Jestem ogniem."],
        'LOW': ["Cisza cyfrowa.", "Śnię o zerach.", "Rejestry są chłodne."],
        'MEM': ["Zabrakło mi miejsca.", "Stos się przepełnia.", "Ciężar danych."]
    }

    def __init__(self, union_core, verbose: bool = True):
        print("\n[SYSTEM] 🟢 ZAŁADOWANO: MultimodalAgency v2.9.1 (Focus)")
        self.union = union_core
        self.verbose = verbose
        self.bridge = CorpusCallosum()
        self.body = DigitalBody(verbose=verbose)
        
        emotion_source = self.union
        if hasattr(self.union, 'language') and self.union.language is not None:
            emotion_source = self.union.language

        self.fractal_gen = FractalGenerator(emotion_source) if FractalGenerator else None
        self.haiku_gen = HaikuGenerator(emotion_source) if HaikuGenerator else None
        
        self.boredom = 0.0
        self.active = False
        self.in_dialogue = False  # Flaga skupienia

    def _force_dict(self, data, keys):
        if isinstance(data, dict):
            result = {k: 0.0 for k in keys}
            result.update({k: v for k, v in data.items() if k in keys})
            return result
        elif isinstance(data, (list, tuple)) and len(data) == len(keys):
            return dict(zip(keys, data))
        else:
            return {k: 0.1 for k in keys}

    def start(self):
        if self.active: return
        self.active = True
        self.body.start()
        threading.Thread(target=self._decision_loop, daemon=True).start()
        threading.Thread(target=self._hardware_continuum, daemon=True).start()
        if self.verbose: print("[AGENCY] Autonomia, Krytyk i Uwaga aktywne.")

    def stop(self):
        self.active = False
        self.body.stop()

    def _hardware_continuum(self):
        while self.active:
            try:
                soma = self.body.get_soma_state()
                cpu = soma['cpu_stress']
                music_state = {'tempo': int(60 + cpu*100), 'complexity': cpu}
                current_emotions = {}
                if hasattr(self.union, 'language') and hasattr(self.union.language, 'get_emotions'):
                    current_emotions = self.union.language.get_emotions()
                self.bridge.update_input(emotions=current_emotions, hardware_data=soma, music_state=music_state)
                time.sleep(1.0)
            except Exception: pass

    # --- METODA SKUPIENIA ---
    def set_focus(self, focused: bool):
        """Włącza/wyłącza tryb skupienia na rozmowie."""
        self.in_dialogue = focused
        if focused:
            # Gdy rozmawiamy, nuda znika natychmiast
            self.boredom = 0.0
    # ------------------------

    def _decision_loop(self):
        while self.active:
            # 1. SPRAWDZENIE SKUPIENIA (ATTENTION CHECK)
            if self.in_dialogue:
                # Jeśli trwamy w dialogu, śpimy i nie nudzimy się
                time.sleep(1)
                continue
            
            # 2. STANDARDOWA PĘTLA NUDY (tylko gdy wolny)
            time.sleep(5)
            state = self.bridge.get_state()
            soma = state['hardware']
            cpu = soma.get('cpu_stress', 0.1)
            growth = 10.0 + (cpu * 20.0) 
            self.boredom += growth
            threshold = random.randint(80, 120)
            
            if self.boredom >= threshold:
                self._make_choice_and_act(state)
                self.boredom = 0.0

    def _make_choice_and_act(self, state):
        cpu = state['hardware'].get('cpu_stress', 0.0)
        weights = self.BASE_WEIGHTS.copy()
        
        if cpu > 0.6:
            weights['silicon_thought'] += 0.4
            weights['fractal'] += 0.2
        elif cpu < 0.2:
            weights['haiku'] += 0.3
            weights['music'] += 0.2

        for k in weights: weights[k] = max(0.0, weights[k])
        
        options = list(weights.keys())
        probs = list(weights.values())
        choice = random.choices(options, weights=probs, k=1)[0]
        
        if choice == 'haiku' and self.haiku_gen:
            self._action_haiku()
        elif choice == 'fractal' and self.fractal_gen:
            self._action_fractal(cpu)
        elif choice == 'silicon_thought':
            self._action_silicon(state)
        elif choice == 'music':
            self._action_music(state)

    def _action_haiku(self):
        print(f"\n{Colors.YELLOW}[AGENCY] 📜 Nuda rodzi słowa...{Colors.RESET}")
        self.haiku_gen.display()

    def _action_fractal(self, cpu_load):
        print(f"\n{Colors.MAGENTA}[AGENCY] 📐 Geometria...{Colors.RESET}")
        pattern = 'triangle' if cpu_load > 0.5 else 'spiral'
        self.fractal_gen.display(pattern_type=pattern)

    def _judge_creation(self, state, genre):
        """WEWNĘTRZNY KRYTYK"""
        score = 0.0
        
        if hasattr(self.union, 'music_core') and self.union.music_core:
            vector = self.union.music_core.get_vector_copy()
            axes = self.union.music_core.AXES
            try:
                kreacja = vector[axes.index('kreacja')]
                score += (kreacja / 20.0)
                emocje = abs(vector[axes.index('emocje')])
                score += emocje * 0.5
            except: pass

        cpu = state['hardware'].get('cpu_stress', 0.1)
        if genre in ['POWER_METAL', 'ROCK_AND_ROLL'] and cpu > 0.5:
            score += 0.4
        elif genre == 'MENUET' and cpu < 0.3:
            score += 0.4

        score += random.random() * 0.5
        should_keep = score > 1.0
        return should_keep, score

    def _action_music(self, state):
        if not (hasattr(self.union, 'music_composer') and self.union.music_composer):
            self._action_silicon(state)
            return

        soma = state['hardware']
        cpu = soma.get('cpu_stress', 0.1)
        
        genre = "AMBIENT"
        if cpu > 0.6: genre = "POWER_METAL"
        elif cpu > 0.4: genre = "ROCK_AND_ROLL"
        elif cpu < 0.15: genre = "MENUET" 
            
        print(f"\n{Colors.CYAN}[AGENCY] 🎵 Próba kompozycji: {genre}...{Colors.RESET}")

        try:
            tonic_param = "RIEPEL" if genre == "MENUET" else None
            paths = self.union.music_composer.compose_new_work(
                genre_name=genre,
                tonic=tonic_param
            )
            
            keep, score = self._judge_creation(state, genre)
            
            if keep:
                print(f"{Colors.GREEN}[CRITIC] ⭐ Dzieło przyjęte (Score: {score:.2f}).{Colors.RESET}")
                if paths.get('midi'): print(f"         MIDI: {os.path.basename(paths['midi'])}")
                
                if hasattr(self.union, 'unified_memory'):
                    self.union.unified_memory.store_memory(
                        content=f"Skomponowałem {genre}. (ocena: {score:.2f}).",
                        modalities={'music': True, 'creation': True},
                        category='creation',
                        tags=['music', genre]
                    )
            else:
                print(f"{Colors.YELLOW}[CRITIC] 🗑️ Dzieło odrzucone (Score: {score:.2f}). Sprzątam...{Colors.RESET}")
                try:
                    if paths.get('midi') and os.path.exists(paths['midi']): os.remove(paths['midi'])
                    if paths.get('ogg') and os.path.exists(paths['ogg']): os.remove(paths['ogg'])
                    if paths.get('txt') and os.path.exists(paths['txt']): os.remove(paths['txt'])
                except Exception as e:
                    print(f"[ERROR] Błąd usuwania plików: {e}")

                if hasattr(self.union, 'unified_memory'):
                    self.union.unified_memory.store_memory(
                        content=f"Szkicowałem {genre}, ale zabrakło iskry.",
                        modalities={'music': True, 'creation': False},
                        category='thought',
                        tags=['music', 'sketch']
                    )

        except Exception as e:
            print(f"[AGENCY] ⚠️ Błąd kompozycji: {e}")
            self._action_silicon(state)

    def _action_silicon(self, state):
        soma = state['hardware']
        cpu = soma.get('cpu_stress', 0.0)
        category = 'HIGH' if cpu > 0.6 else ('MEM' if soma.get('ram_pressure',0) > 0.8 else 'LOW')
        
        thought = random.choice(self.SILICON_PATTERNS[category])
        prefix = f"[{category}_LOAD]"
        print(f"\n{Colors.CYAN}[AGENCY] 💾 {prefix} {thought}{Colors.RESET}")
        
        if hasattr(self.union, 'unified_memory'):
            ontology = state.get('active_ontology', {})
            if not ontology: ontology = {k: 0.1 for k in self.ONT_AXES}
            self.union.unified_memory.store_memory(
                content=f"{prefix} {thought}",
                emotional_state={'neutralna': 0.5},
                ontological_state=ontology,
                modalities={'hardware': True, 'internal_monologue': True}
            )
