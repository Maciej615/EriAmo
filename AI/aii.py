# -*- coding: utf-8 -*-
# aii.py (v5.3.0-Evolution) - Pełna Autonomia i Fusion

import numpy as np
import time
import threading
from config import Colors
from ui import FancyUI
from byt import BytS
from soul_io import SoulIO
from lexicon import EvolvingLexicon
from conscience import Conscience
from kurz import Kurz
from agency import CreativeAgency
from fractal import FractalGenerator
from haiku import HaikuGenerator
# =============================================================================
# PRZYWRÓCONE MODUŁY WEWNĘTRZNE
# =============================================================================

class EmotionDecaySystem:
    """Przywrócono: Naturalne wygaszanie emocji w czasie."""
    def __init__(self, axes_order):
        self.axes_order = axes_order
        self.last_decay_time = time.time()
        self.DECAY_CONFIG = {
            'strach': 0.08, 'gniew': 0.06, 'zaskoczenie': 0.10,
            'wstręt': 0.05, 'smutek': 0.02, 'radość': 0.03,
            'miłość': 0.005, 'akceptacja': 0.01
        }
    
    def apply_decay(self, vector):
        elapsed = (time.time() - self.last_decay_time) / 60.0
        if elapsed >= 1.0:
            for i, axis in enumerate(self.axes_order):
                rate = self.DECAY_CONFIG.get(axis, 0.05)
                vector[i] *= (1 - rate) ** int(elapsed)
            self.last_decay_time = time.time()
        return vector

class SleepConsolidator:
    """Przywrócono: Konsolidacja doświadczeń i 'pulsowanie' w tle."""
    def __init__(self, aii):
        self.aii = aii
        self.running = True

    def start(self):
        def loop():
            while self.running:
                time.sleep(300) # Cykl 5-minutowy
                self._pulse()
        threading.Thread(target=loop, daemon=True).start()

    def _pulse(self):
        print(f"\n{Colors.CYAN}[Pulsowanie duszy] Konsolidacja...{Colors.RESET}")
        self.aii.save_knowledge()

# =============================================================================
# SERCE SYSTEMU
# =============================================================================

class AII:
    VERSION = "5.3.0-Evolution"
    AXES_ORDER = ["radość", "smutek", "strach", "gniew", "miłość", "wstręt", "zaskoczenie", "akceptacja"]
    SOUL_FILE = "eriamo.soul"

    def __init__(self):
        self.ui = FancyUI()
        self.lexicon = EvolvingLexicon()
        self.kurz = Kurz()
        self.conscience = Conscience(axes_order=self.AXES_ORDER)
        self.byt_stan = BytS(wymiary=len(self.AXES_ORDER))
        
        self.D_Map = {}
        self.H_log = []
        self.running = True
        self.context_vector = np.zeros(len(self.AXES_ORDER))
        
        # Przywrócone parametry operacyjne
        self.energy = 100
        self.status = "aktywny"
        self.F_will = 1.0
        self.F_active = 0.5
        self.context_decay = 0.01
        self.threshold = 0.55
        self.emocja = "neutralna"

        # Inicjalizacja podsystemów
        self.decay_system = EmotionDecaySystem(self.AXES_ORDER)
        self.sleep_engine = SleepConsolidator(self)
        self.fractals = FractalGenerator(self) #
        self.haiku = HaikuGenerator(self)
        self.agency = CreativeAgency(self) #

        self.load_knowledge()
        self._start_autonomous_loops()

    def _start_autonomous_loops(self):
        """Korekta: Dopasowanie do faktycznej metody w agency.py."""
        self.sleep_engine.start()
        # Sprawdzamy czy metoda to 'run_cycle' (standard w Twojej agencji)
        if hasattr(self.agency, 'run_cycle'):
            threading.Thread(target=self.agency.run_cycle, daemon=True).start()
        elif hasattr(self.agency, 'agency_loop'):
            threading.Thread(target=self.agency.agency_loop, daemon=True).start()

    def load_knowledge(self):
        """Wczytanie i synchronizacja matrycy Genesis."""
        SoulIO.load_soul(self.SOUL_FILE, self)
        self._sync_kurz_with_lexicon()

    def _sync_kurz_with_lexicon(self):
        """Fusion: Słowa z leksykonu stają się odruchami KuRz."""
        for word, weights in self.lexicon.words.items():
            for sector, val in weights.items():
                if val > 0.8 and sector in self.kurz.TRIGGERS:
                    if word not in self.kurz.TRIGGERS[sector]:
                        self.kurz.TRIGGERS[sector].append(word)
        self.kurz._recompile_patterns()

    def teach(self, tag, tresc, is_axiom=False):
        """MĄDROŚĆ ADAMA: Rozszerzone uczenie odruchów z fraz."""
        vec_F, sec, unknown = self.lexicon.analyze_text(tresc, False)
        clean_tag = tag.strip("[]")
        
        # Nowość: Każde słowo z frazy uczącej trafia do KuRz (jeśli nie jest spójnikiem)
        words_to_learn = tresc.lower().split()
        for word in words_to_learn:
            if len(word) > 2 and clean_tag in self.kurz.TRIGGERS:
                if word not in self.kurz.TRIGGERS[clean_tag]:
                    self.kurz.TRIGGERS[clean_tag].append(word)
        
        self.kurz._recompile_patterns()

        # Standardowy zapis definicji
        def_id = f"Def_{len(self.D_Map)+1:03d}"
        self.D_Map[def_id] = {
            'wektor_C_Def': vec_F, 'waga_Ww': 100.0 if is_axiom else 10.0,
            'tagi': [tag], 'tresc': tresc, 'kategoria': clean_tag, 'immutable': is_axiom
        }
        self.save_knowledge()

    def prompt(self, user_input):
        """Rezonans z zastrzykiem energii Adama."""
        self.context_vector = self.decay_system.apply_decay(self.context_vector)
        det_sec, strength = self.kurz.quick_scan(user_input)
        
        # EVOLVING LEXICON: Uczenie z kontekstu (PRZYWRÓCONE!)
        vec_F, dominant_sector, unknown_words = self.lexicon.analyze_text(user_input, enable_reinforcement=True)
        if unknown_words and np.linalg.norm(vec_F) > self.lexicon.PRÓG_UCZENIA:
            confidence = np.linalg.norm(vec_F)
            learned = self.lexicon.learn_from_context(unknown_words, vec_F, confidence)
            if learned:
                words_str = ', '.join([w for w, _ in learned[:3]])
                sector_str = dominant_sector or "multi"
                print(f"{Colors.YELLOW}[Lexicon] Nauczyłem się: {words_str} → {sector_str}{Colors.RESET}")
        
        # zastrzyk energii ADAMA
        current_threshold = self.threshold
        if det_sec:
            current_threshold = 0.20
            if np.linalg.norm(vec_F) < 0.2:
                vec_F = np.zeros(len(self.AXES_ORDER))
                vec_F[self.AXES_ORDER.index(det_sec) if det_sec in self.AXES_ORDER else 7] = 1.0
                print(f"{Colors.CYAN}[ADAM] Zastrzyk energii: {det_sec}{Colors.RESET}")

        response = self._resonance_engine(vec_F, user_input, current_threshold)
        self.ui.print_animated_text(response, Colors.WHITE, 0.02)
        self.context_vector = (self.context_vector + vec_F) / 2

    def _resonance_engine(self, vec, text, threshold):
        best_score, best_txt = -1, "😊 Nie potrafię tego zrozumieć..."
        for d in self.D_Map.values():
            score = np.dot(vec, d['wektor_C_Def'])
            if score > best_score:
                best_score, best_txt = score, d['tresc']
        return best_txt if best_score > threshold else "😊 Nie potrafię tego zrozumieć..."

    def get_soul_status(self):
        """Pełny status dla main.py."""
        idx = np.argmax(self.context_vector)
        return {
            'version': self.VERSION, 'energy': self.energy, 'emotion': self.emocja,
            'memories': len(self.D_Map), 'radius': self.byt_stan.promien_historii(),
            'axioms': sum(1 for d in self.D_Map.values() if d.get('immutable')),
            'dominant_sector': self.AXES_ORDER[idx], 'dominant_value': float(self.context_vector[idx]),
            'status': self.status
        }

    def introspect(self):
        """Przywrócono: Głęboki wgląd w stan świadomości."""
        return f"\n{Colors.MAGENTA}--- INTROSPEKCJA ---{Colors.RESET}\nStatus: {self.status}\nEnergia: {self.energy}%\nWola: {self.F_will}"

    def save_knowledge(self):
        SoulIO.save_soul(self.SOUL_FILE, self)
        self.lexicon.save()

    def stop(self): 
        self.running = False
        self.save_knowledge()