# -*- coding: utf-8 -*-
"""
aii.py v5.7.1 - EriAmo Core (API Fix)
Lokalizacja: /eriamo-union/src/language/aii.py

Zmiany v5.7.1:
- FIX KRYTYCZNY: Naprawiono wywołanie analyze_text() - używa nowej sygnatury API.
- Dodano automatyczne uczenie nieznanych słów z kontekstu emocjonalnego.
- System teraz rozumie input i uczy się nowych słów!

Zmiany v5.7.0:
- Dodano obliczanie 'dominant_sector' i 'dominant_value' w get_soul_status.
- Naprawiono obsługę statusu dla zaawansowanych skryptów Genesis.
"""

import sys
import os
import time
import threading
import numpy as np

try:
    from config import Colors, Config
    from ui import FancyUI
    from byt import BytS
    from soul_io import SoulIO
    from lexicon import EvolvingLexicon
    from conscience import Conscience
    from kurz import Kurz
    from agency import CreativeAgency
    from fractal import FractalGenerator
    from haiku import HaikuGenerator
except ImportError as e:
    print(f"❌ [AII] Błąd importu: {e}")
    sys.exit(1)

class AII:
    VERSION = "5.7.1-APIFix"
    AXES_ORDER = ['radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt', 'zaskoczenie', 'akceptacja']

    def __init__(self):
        self.ui = FancyUI()
        self.ui.print_logo()
        print(f"{Colors.CYAN}[SYSTEM] Inicjalizacja rdzenia {self.VERSION}...{Colors.RESET}")

        self.D_Map = {} 
        self.status = "active"
        
        # Fizyka Bytu
        self.byt_stan = BytS(len(self.AXES_ORDER))
        
        self.energy = 100.0
        self.emocja = "neutralna"
        
        # Wektor Kontekstu (8 osi)
        self.context_vector = np.zeros(8)
        
        # Moduły
        self.soul_io = SoulIO()
        self.lexicon = EvolvingLexicon()
        self.conscience = Conscience(self.AXES_ORDER)
        self.kurz = Kurz()
        self.agency = CreativeAgency(self)
        self.fractal = FractalGenerator(self)
        
        try:
            self.haiku = HaikuGenerator(self)
        except:
            self.haiku = HaikuGenerator()

        # START
        self._load_memory()
        self.lock = threading.Lock()

    def _load_memory(self):
        print(f"{Colors.CYAN}[SoulIO] Sprawdzanie integralności duszy...{Colors.RESET}")
        try:
            self.soul_io.load_soul_stream(self.D_Map)
        except: pass

        # --- DETEKCJA PUSTKI I START FUSION ---
        if not self.D_Map:
            print(f"\n{Colors.YELLOW}╔════════════════════════════════════════════╗{Colors.RESET}")
            print(f"{Colors.YELLOW}║  WYKRYTO PUSTKĘ. URUCHAMIAM FUSION.        ║{Colors.RESET}")
            print(f"{Colors.YELLOW}╚════════════════════════════════════════════╝{Colors.RESET}\n")
            
            try:
                import genesisfusion
                genesisfusion.run_fusion(self)
            except ImportError:
                print(f"{Colors.RED}❌ Brak genesisfusion.py w src/language!{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}❌ Błąd FUSION: {e}{Colors.RESET}")
                import traceback
                traceback.print_exc()
        else:
            print(f"{Colors.GREEN}[SoulIO] Wiedza załadowana: {len(self.D_Map)} definicji.{Colors.RESET}")

    def teach(self, content, tags=None, immutable=False, is_axiom=False):
        """Dodaje wiedzę. Obsługuje parametry z Genesis."""
        if tags is None: tags = []
        if is_axiom: immutable = True
        if isinstance(tags, str): tags = [tags]

        def_id = f"Def_{len(self.D_Map) + 1:05d}"
        
        vec = np.zeros(8)
        for t in tags:
            clean_t = t.replace("[", "").replace("]", "").lower()
            if clean_t in self.AXES_ORDER:
                idx = self.AXES_ORDER.index(clean_t)
                vec[idx] = 1.0

        definition = {
            "_type": "@MEMORY",
            "id": def_id,
            "tresc": content,
            "tags": tags,
            "immutable": immutable,
            "wektor_C_Def": vec.tolist(),
            "created_at": time.time()
        }
        
        self.D_Map[def_id] = definition
        return def_id

    def save_knowledge(self):
        """Alias dla skryptów Genesis."""
        self.save()

    def get_soul_status(self):
        """
        Zwraca pełny raport o stanie duszy (Naprawia KeyError: dominant_sector).
        """
        axioms_count = sum(1 for d in self.D_Map.values() if d.get('immutable'))
        
        radius = 0.0
        if hasattr(self.byt_stan, 'promien_historii'):
            radius = self.byt_stan.promien_historii()
        elif hasattr(self.byt_stan, 'promien'):
            radius = self.byt_stan.promien

        # --- OBLICZANIE SEKTORA DOMINUJĄCEGO ---
        dom_sector = "neutralna"
        dom_val = 0.0
        if isinstance(self.context_vector, np.ndarray):
            idx = np.argmax(self.context_vector)
            dom_sector = self.AXES_ORDER[idx]
            dom_val = float(self.context_vector[idx])
        # ---------------------------------------

        return {
            'memories': len(self.D_Map),
            'radius': radius,
            'axioms': axioms_count,
            'energy': self.energy,
            'emotion': self.emocja,
            'status': self.status,
            'dominant_sector': dom_sector, # <--- TEGO BRAKOWAŁO
            'dominant_value': dom_val,
            'lexicon': {'total': 0}
        }

    def save(self):
        try:
            self.soul_io.save_stream(self.D_Map)
            if hasattr(self.lexicon, 'save_to_soul'):
                self.lexicon.save_to_soul()
            elif hasattr(self.lexicon, 'save'):
                self.lexicon.save()
            print(f"{Colors.GREEN}[AII] Zapisano stan świadomości.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[AII] Błąd zapisu: {e}{Colors.RESET}")

    def get_emotions(self):
        if isinstance(self.context_vector, np.ndarray):
            return self.context_vector.tolist()
        return self.context_vector if isinstance(self.context_vector, list) else [0.0]*8

    def interact(self, user_input):
        if not hasattr(self.lexicon, 'learn_from_correction'):
             self.lexicon.learn_from_correction = lambda w, e, v: None

        # Nowa sygnatura: (vector, dominant_sector, unknown_words)
        vec_F, dominant_sector, unknown_words = self.lexicon.analyze_text(user_input)
        
        # Uczenie nieznanych słów z kontekstu emocjonalnego
        if unknown_words and np.max(vec_F) > 0.15:
            confidence = np.max(vec_F)
            learned = self.lexicon.learn_from_context(unknown_words, vec_F, confidence)
            if learned:
                print(f"{Colors.GREEN}[Lexicon] Nauczyłem się {len(learned)} nowych słów!{Colors.RESET}")
        
        self.context_vector = (self.context_vector + vec_F) / 2.0
        
        response = self._resonance_engine(vec_F, user_input, threshold=0.05)
        
        if hasattr(self, 'ui'):
            self.ui.print_animated_text(response, Colors.WHITE, 0.02)
        else:
            print(f" [EriAmo] {response}")
        return response

    def _resonance_engine(self, vec, text, threshold):
        best_score = -1.0
        best_txt = "😊 Nie potrafię tego zrozumieć..."
        is_zero_vector = np.all(vec == 0)
        
        for d in self.D_Map.values():
            score = 0.0
            if not is_zero_vector:
                def_vec = d.get('wektor_C_Def')
                if def_vec is not None:
                    try: score = np.dot(vec, def_vec)
                    except: pass
            # Match tags (TRIGGERY - wysoki priorytet!)
            if 'tags' in d and isinstance(d['tags'], list):
                for tag in d['tags']:
                    if isinstance(tag, str) and tag.lower() in text.lower():
                        score += 2.0  # Mocny bonus za tag match
                        break
            
            # Match treść (niższy priorytet)
            if text.lower() in d['tresc'].lower():
                score += 0.5
            if score > best_score:
                best_score = score
                best_txt = d['tresc']
        
        if best_score > threshold:
            return best_txt
        else:
            axioms = [d['tresc'] for d in self.D_Map.values() if d.get('immutable')]
            if axioms and np.random.random() < 0.3:
                return np.random.choice(axioms)
            return "😊 Nie potrafię tego zrozumieć..."

    def live(self):
        while True:
            cmd = input(f"{Colors.BLUE}Ty > {Colors.RESET}")
            if cmd == "exit": break
            self.interact(cmd)

if __name__ == "__main__":
    app = AII()
    app.live()
