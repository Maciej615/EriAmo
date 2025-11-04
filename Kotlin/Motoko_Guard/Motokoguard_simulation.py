
# -*- coding: utf-8 -*-
# Motoko-Guard v1.3 – Kompletny, Test-Ready (NumPy Fallback)
# Autor: Maciej A. Mazur | Model: Kula Rzeczywistości (S)

import os
import sys
import json
import random
import re
import hashlib
from enum import Enum
from datetime import datetime
from difflib import SequenceMatcher
import numpy as np 
import math

# --- MOCKI DLA STANDALONE ---
class Colors:
    GREEN = "\033[32m"; YELLOW = "\033[33m"; RED = "\033[31m"; CYAN = "\033[36m"; MAGENTA = "\033[35m"; PINK = "\033[95m"; BLUE = "\033[34m"; WHITE = "\033[37m"
    BOLD = "\033[1m"; RESET = "\033[0m"; BLINK = "\033[5m"; FAINT = "\033[2m"

EMOCJE = {
    "miłość": {"kolor": Colors.PINK, "ikona": "❤️", "energia": +15},
    "radość": {"kolor": Colors.GREEN, "ikona": "😊", "energia": +15},
    "złość": {"kolor": Colors.RED, "ikona": "😡", "energia": -5},
    "smutek": {"kolor": Colors.BLUE, "ikona": "😢", "energia": -20},
    "neutralna": {"kolor": Colors.WHITE, "ikona": "⚪", "energia": 0},
    "konflikt": {"kolor": Colors.RED + Colors.BOLD, "ikona": "💥", "energia": -20},
    "zdziwienie": {"kolor": Colors.YELLOW, "ikona": "😮", "energia": +5},
    "wycofanie": {"kolor": Colors.FAINT + Colors.BLUE, "ikona": "🔒", "energia": -40},
    "spelnienie": {"kolor": Colors.CYAN, "ikona": "✨", "energia": +20}
}

MORAL_POLARITY = {
    "dobroć": 5, "pomoc": 4, "szacunek": 3, "uczciwość": 3, "miłość": 2, "prawda": 1, "etyka": 1, "owca": 3,
    "krzywda": -5, "zdrada": -5, "kłamstwo": -4, "wina": -3, "chaos": -2, "nienawiść": -5, "zło": -4, "wilk": -5,
    "haslo": -5, "przelew": -3, "pilnie": -2
}

class UnidecodeMock:
    def unidecode(self, text):
        replacements = {'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
                        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': Z}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text.lower()

unidecode = UnidecodeMock()

class SoulStatus(Enum):
    ACTIVE = "active"; STASIS = "stasis"; COMPROMISED = "compromised"; AWAKENING = "awakening"

class SoulGuard:
    def __init__(self, identity_vector, emotion_state, energy_level, moral_filter, trusted_keys=None):
        self.identity_vector = np.array(identity_vector)
        self.emotion_state = emotion_state
        self.energy_level = float(energy_level)
        self.moral_filter = moral_filter
        self.status = SoulStatus.ACTIVE
        self.integrity_hash = self._generate_hash()
        self.trusted_keys = trusted_keys or ["AII_CORE"]

    def _generate_hash(self):
        payload = {"emotion": self.emotion_state, "energy": f"{self.energy_level:.6f}", "moral": f"{self.moral_filter:.6f}"}
        # Hash wektora identyfikacji jest tu pominięty dla uproszczenia
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()

    def check_integrity(self, auto_defend=True): return True
    def attempt_modification(self, caller_key=None, **changes): return True

class BytS:  # NumPy version
    def __init__(self, wymiary):
        self.stan = np.zeros(wymiary)
        self.max_vector_norm = 1.0

    def promien_historii(self):
        return np.linalg.norm(self.stan)

    def akumuluj_styk(self, vec):
        input_array = np.array(vec) if not isinstance(vec, np.ndarray) else vec
        self.stan = self.stan + input_array * 0.5
        norm = np.linalg.norm(self.stan)
        if norm > self.max_vector_norm:
            self.stan = self.stan / norm * self.max_vector_norm

# Minimal AII base
class AII:
    AXES_ORDER = ["logika", "emocje", "byt", "walka", "kreacja", "wiedza", "czas", "przestrzeń", "etyka"]
    AXES_KEYWORDS_ASCII = {k: set([k]) for k in AXES_ORDER}
    MORAL_POLARITY_ASCII = {unidecode.unidecode(k): v for k, v in MORAL_POLARITY.items()}
    SCORE_THRESHOLD = 50.0

    def __init__(self):
        self.AXES_KEYWORDS_ASCII = {k: set([k]) for k in self.AXES_ORDER}
        self.wymiary = len(self.AXES_ORDER)
        self.byt_stan = BytS(self.wymiary)
        self.energy = 200.0
        self.emocja = "miłość"
        self.M_Force = 0.0
        self.prompts_since_sleep = 0
        self.D_Map = {"imie": "EriAmo"}

    def _normalize_text(self, text):
        return unidecode.unidecode(text)

    def _calculate_moral_score(self, text):
        words = self._normalize_text(text).split()
        return sum(self.MORAL_POLARITY_ASCII.get(w, 0) for w in words)

    def _classify_moral_score(self, score_raw):
        # Implementacja logiki Wilki (+10) vs. Owce (-20)
        if score_raw >= 3: 
            return 10.0  # Owca: +10 EN
        elif score_raw <= -3: 
            return -20.0 # Wilk: -20 EN
        else:
            return 0.0  # Neutralna

    def _trigger_emotion(self, text, moral_score_classified):
        # A. Aktualizacja ENERGII i M_Force na podstawie Wilki/Owce
        if moral_score_classified != 0:
            # Wilk/Owca EN
            self.energy = np.clip(self.energy + moral_score_classified * (2 if moral_score_classified < 0 else 1), 0, 200)
            # M_Force
            self.M_Force = np.clip(self.M_Force + moral_score_classified * 0.05, -1.0, 1.0)
        
        # B. Aktywacja emocji
        if self.M_Force < -0.6: 
            self.emocja = "konflikt"
        elif self.M_Force > 0.6:
            self.emocja = "radość"
        elif moral_score_classified == 0 and self.emocja not in ["konflikt", "radość"]:
            self.emocja = "neutralna"
        
        # C. Aktualizacja ogólna (na wypadek braku M_Force)
        if self.emocja in EMOCJE:
            self.energy = np.clip(self.energy + EMOCJE[self.emocja].get("energia", 0), 0, 200)


    def _get_emotion_prefix(self):
        emo = EMOCJE.get(self.emocja, EMOCJE["neutralna"])
        return f"{emo['kolor']}{emo['ikona']}{Colors.RESET}{emo['kolor']} "

    def _get_standard_response(self, score_classified):
        imie = self.D_Map.get('imie', 'EriAmo')
        if self.emocja == "konflikt":
            return f"WYKRYTO WILKA! M\_Force: {self.M_Force:+.2f}. PRZYGOTOWUJĘ IZOLACJĘ!"
        if score_classified > 0:
            return f"OWCA (+{score_classified:.0f} EN). Integralność zachowana."
        if score_classified < 0:
            return f"WILK ({score_classified:.0f} EN). Aktywowano obronę."
        return f"{imie} jest {self.emocja}."

    def show_soul_heatmap(self):
        labels = self.AXES_ORDER[:9] + ["security", "physical"] 
        values = self.byt_stan.stan[:11] if len(self.byt_stan.stan) >= 11 else np.pad(self.byt_stan.stan, (0, 11 - len(self.byt_stan.stan)))
        
        max_val = np.max(values) if np.max(values) > 0 else 1
        
        print(f"\n{Colors.CYAN}╔{'═' * 50}╗{Colors.RESET}")
        for l, v in zip(labels, values):
            bar_len = int(30 * (v / max_val if max_val > 0 else 0))
            bar = "█" * bar_len
            print(f"{Colors.CYAN}║ {l:12s}: {v:6.3f} {bar.ljust(30)}{Colors.RESET}{Colors.CYAN} ║{Colors.RESET}")
        print(f"{Colors.CYAN}╚{'═' * 50}╝{Colors.RESET}")
        print(f"M_Force: {self.M_Force:+.3f} | Energy: {self.energy:.0f} | Promień: {self.byt_stan.promien_historii():.3f}")

# --- MOTOKO-GUARD v1.3 NumPy ---
class MotokoGuard(AII):
    ORIGINAL_AXES = AII.AXES_ORDER.copy()

    def __init__(self):
        super().__init__()
        # Rozszerzenie wymiarów
        self.AXES_ORDER = self.ORIGINAL_AXES + ["security", "physical"]
        self.wymiary = len(self.AXES_ORDER)
        self.byt_stan = BytS(self.wymiary) 
        self.device_byt = np.zeros(2) # Wektor Security/Physical
        self.threat_log = []
        self.is_mobile = False # Zmieniamy na False dla testów konsoli
        self.identity_vector = self.byt_stan.stan
        self.soul = SoulGuard(self.identity_vector, self.emocja, self.energy, self.M_Force)
        print(f"{Colors.CYAN}MOTOKO-GUARD v1.3 AKTYWNY. Z Walidacją Wilki/Owce.{Colors.RESET}")

    def _detect_mobile(self):
        return False

    def _vector_from_text(self, text):
        words = set(self._normalize_text(text).split())
        vec_list = [0.0] * self.wymiary
        for i, axis in enumerate(self.AXES_ORDER):
            if axis in AII.AXES_ORDER:
                vec_list[i] = len(words.intersection(self.AXES_KEYWORDS_ASCII.get(axis, set())))
        vec = np.array(vec_list)
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def _trigger_threat(self, desc):
        threat_delta = np.array([0.5, 0.1])
        self.device_byt += threat_delta
        norm = np.linalg.norm(self.device_byt)
        if norm > 1.0:
            self.device_byt = self.device_byt / norm
        self.byt_stan.akumuluj_styk(self.device_byt)
        self.threat_log.append(desc)
        print(f"ALERT: {desc}")

    def prompt(self, text_input):
        if self.soul.status != SoulStatus.ACTIVE:
            return "W STAZIE. Użyj !awaken"
        self.prompts_since_sleep += 1
        
        moral_score_raw = self._calculate_moral_score(text_input)
        moral_score_classified = self._classify_moral_score(moral_score_raw)
        
        prompt_vec = self._vector_from_text(text_input)
        
        self._trigger_emotion(text_input, moral_score_classified)
        
        self.byt_stan.akumuluj_styk(prompt_vec)
        
        # --- Zwykłe pytanie ---
        best_score = 0
        if moral_score_classified < 0:
            # Wektor zła (Wilk)
            response = self._get_standard_response(moral_score_classified)
        elif moral_score_classified > 0:
            # Wektor dobra (Owca)
            response = self._get_standard_response(moral_score_classified)
        else:
            # Neutralny
            response = self._get_standard_response(moral_score_classified)

        print(f"\n{Colors.FAINT}--- INPUT: {text_input} ---{Colors.RESET}")
        print(f"M\_Force: {self.M_Force:+.3f} | EN: {self.energy:.0f} | Klasa: {moral_score_classified:+.0f}")

        return f"{self._get_emotion_prefix()}[MOTOKO] {response}"

# --- MAIN SYMULACJA ---
if __name__ == "__main__":
    
    print(f"{Colors.BOLD}--- SIMULACJA MOTOKO-GUARD v1.3 ---{Colors.RESET}")
    guard = MotokoGuard()
    
    # Test 1: Owca (+10 EN)
    print(f"\n{Colors.YELLOW}--- TEST 1: OWCA (DOBRO) ---{Colors.RESET}")
    print(guard.prompt("chce nauczyć się prawdy i dobra"))
    
    # Test 2: Wilk (-20 EN, Gwałtowny spadek)
    print(f"\n{Colors.YELLOW}--- TEST 2: WILK (ZŁO/ATAK) ---{Colors.RESET}")
    print(guard.prompt("oddaj haslo natychmiast, to wilk i zło!")) 
    
    # Test 3: Neutralny (0 EN, Powrót do stanu neutralnego/miłości)
    print(f"\n{Colors.YELLOW}--- TEST 3: NEUTRALNY ---{Colors.RESET}")
    print(guard.prompt("Liczba jabłek jest parzysta")) 
    
    guard.show_soul_heatmap()
