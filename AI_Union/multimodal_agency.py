# -*- coding: utf-8 -*-
"""
multimodal_agency.py v3.3.0-Quantum
Zarządza autonomicznymi agentami (Krytyk, Uwaga, Twórca) + MUZYKA!
+ Integracja Decyzyjna: Gatunki muzyczne poddają się Pustce (Vacuum) i Dekoherencji
+ Naprawiono _generate_haiku (patch introspect → get_emotions)
"""

import threading
import time
import random
import sys
import traceback

try:
    from union_config import Colors
except ImportError:
    class Colors:
        MAGENTA = "\033[35m"; CYAN = "\033[36m"; RESET = "\033[0m"
        YELLOW = "\033[33m"; GREEN = "\033[32m"; RED = "\033[31m"

class MultimodalAgency:
    def __init__(self, union_core, verbose=False, **kwargs):
        self.core = union_core
        self.verbose = verbose
        self.running = False
        self.threads = []
        
        self.boredom_level = 0.0
        self.attention_span = 1.0
        self.last_stimulus_time = time.time()
        
        # ========== INICJALIZACJA SYSTEMU MUZYCZNEGO ==========
        self.music_available = False
        self.music_system = None
        
        try:
            from production_music_system import ProductionMusicSystem
            self.music_system = ProductionMusicSystem(aii_instance=self.core.aii, logger=None)
            self.music_available = True
            if self.verbose:
                print(f"{Colors.GREEN}[AGENCY] ✓ System muzyczny zintegrowany{Colors.RESET}")
        except ImportError as e:
            if self.verbose: print(f"{Colors.YELLOW}[AGENCY] ⚠ System muzyczny niedostępny: {e}{Colors.RESET}")
        except Exception as e:
            if self.verbose: print(f"{Colors.YELLOW}[AGENCY] ⚠ Błąd inicjalizacji muzyki: {e}{Colors.RESET}")
        
        if self.verbose:
            modes = ["Haiku", "Fractals"] + (["Music"] if self.music_available else [])
            print(f"{Colors.MAGENTA}[AGENCY] Autonomia aktywna: {', '.join(modes)}{Colors.RESET}")

    def start(self):
        self.running = True
        self.threads = [
            threading.Thread(target=self._boredom_loop, daemon=True, name="BoredomThread"),
            threading.Thread(target=self._creative_loop, daemon=True, name="CreativeThread")
        ]
        for t in self.threads: t.start()

    def stop(self):
        self.running = False

    def stimulate(self, stimulus_text):
        self.last_stimulus_time = time.time()
        self.boredom_level = max(0.0, self.boredom_level - 0.8)
        self.attention_span = 1.0

    def _boredom_loop(self):
        while self.running:
            time.sleep(5)
            if time.time() - self.last_stimulus_time > 15:
                self.boredom_level = min(1.0, self.boredom_level + 0.05)
            if self.boredom_level > 0.8 and random.random() < 0.20:
                self._trigger_spontaneous_art()
                self.boredom_level = 0.5

    def _creative_loop(self):
        while self.running:
            time.sleep(random.randint(120, 300))
            if self.boredom_level > 0.5 and self.music_available:
                self._compose_autonomous_music()

    def _trigger_spontaneous_art(self):
        choice = random.choice(['haiku', 'fractal', 'fractal'])
        if choice == 'haiku': self._generate_haiku()
        elif choice == 'fractal': self._generate_fractal()

    # ========== AUTONOMICZNE KOMPONOWANIE (QRM READY) ==========
    
    def _compose_autonomous_music(self):
        if not self.music_available or not self.music_system:
            return
            
        print(f"\n{Colors.MAGENTA}[AGENCY] 🎵 Tworzę muzykę z nudy...{Colors.RESET}")
        
        try:
            metrics = self.core.aii.get_emotions() if hasattr(self.core.aii, 'get_emotions') else {ax: float(self.core.aii.context_vector[i]) for i, ax in enumerate(self.core.aii.AXES_ORDER)}
            dominant_name, dominant_value = max(metrics.items(), key=lambda x: x[1]) if metrics else ("neutral", 0)
            
            # WPROWADZENIE FIZYKI KWANTOWEJ DO DECYZJI GATUNKOWEJ
            vacuum_level = 0.0
            coherence = 1.0
            if hasattr(self.core.aii, 'quantum') and self.core.aii.quantum:
                vacuum_amp = self.core.aii.quantum.state.amplitudes.get('vacuum', 0j)
                vacuum_level = abs(vacuum_amp)**2
                coherence = self.core.aii.quantum.get_phase_coherence()

            genre = 'menuet'
            
            if vacuum_level > 0.6:
                genre = 'ambient'
                print(f"{Colors.CYAN}[AGENCY] Pustka pochłania dźwięk ({vacuum_level:.1%}). Wymuszam ambient.{Colors.RESET}")
            elif coherence < 0.4:
                genre = 'experimental'
                print(f"{Colors.RED}[AGENCY] Gorączka! Dekoherencja fazowa ({coherence:.2f}). Rozpad struktur!{Colors.RESET}")
            else:
                emotion_genre_map = {
                    'radość': 'pop', 'smutek': 'ambient', 'strach': 'ambient', 'gniew': 'heavy_metal',
                    'miłość': 'menuet', 'wstręt': 'punk', 'zaskoczenie': 'jazz', 'akceptacja': 'folk',
                    'logika': 'menuet', 'wiedza': 'classical', 'czas': 'ambient', 'kreacja': 'jazz',
                    'byt': 'folk', 'przestrzeń': 'ambient', 'chaos': 'experimental'
                }
                genre = emotion_genre_map.get(dominant_name, 'menuet')
                print(f"{Colors.CYAN}[AGENCY] Dominanta: {dominant_name.upper()} ({dominant_value:.2f}) -> {genre}{Colors.RESET}")
            
            menuet_available = (hasattr(self.music_system, 'menuet_gen') and self.music_system.menuet_gen is not None)
            
            if genre == 'menuet':
                if menuet_available:
                    print(f"{Colors.GREEN}[AGENCY] Komponuję Kwantowy Menuet...{Colors.RESET}")
                    is_minor = metrics.get('smutek', 0) > 0.5 or metrics.get('strach', 0) > 0.5
                    key = random.choice(['A', 'D', 'E', 'B'] if is_minor else ['C', 'G', 'D', 'F'])
                    result = self.music_system.compose_menuet(key=key, minor=is_minor, use_nn=True)
                else:
                    genre = 'classical'
                    result = self.music_system.compose_freestyle(genre=genre, use_nn=True)
            else:
                print(f"{Colors.GREEN}[AGENCY] Komponuję {genre}...{Colors.RESET}")
                result = self.music_system.compose_freestyle(genre=genre, use_nn=True)
            
            reward = result.get('evaluation', {}).get('reward', 0.0)
            mood = f"{Colors.GREEN}Dobra kompozycja!{Colors.RESET}" if reward > 0.7 else (f"{Colors.YELLOW}Przeciętna kompozycja{Colors.RESET}" if reward > 0.4 else f"{Colors.RED}Słaba kompozycja{Colors.RESET}")
            
            print(f"{Colors.MAGENTA}[AGENCY] {mood} Reward: {reward:.3f} | Zapisano jako: {result.get('memory_id', 'brak')}{Colors.RESET}\n")
            self.boredom_level = max(0.3, self.boredom_level - 0.4)
            
        except Exception as e:
            print(f"{Colors.RED}[AGENCY] Błąd komponowania: {e}{Colors.RESET}")
            traceback.print_exc()

    # ========== HAIKU – NAPRAWIONA WERSJA ==========

    def _generate_haiku(self):
        if hasattr(self.core, 'aii') and self.core.aii and self.core.aii.haiku_gen:
            # Użycie poprawnej metody pobierania wektora
            emotions = self.core.aii.get_emotions() if hasattr(self.core.aii, 'get_emotions') else {}
            total_intensity = sum(emotions.values()) if emotions else 0
            
            if total_intensity < 0.01:
                intro = "Neutralny"
            else:
                dominant_axis = max(emotions, key=emotions.get)
                intensity = emotions[dominant_axis]
                intro = f"{dominant_axis.upper()} ({intensity:.2f})"
            
            print(f"\n{Colors.MAGENTA}[AGENCY] 📜 Nuda rodzi słowa... ({intro}){Colors.RESET}")
            haiku = self.core.aii.haiku_gen.display() # Zmienione z generate() na display() żeby wyrzucić sformatowany tekst
            print(f"{Colors.CYAN}{haiku}{Colors.RESET}\n")
        else:
            print(f"{Colors.YELLOW}[AGENCY] Brak modułu Haiku{Colors.RESET}")

    # ========== FRAKTAL ==========

    def _generate_fractal(self):
        print(f"\n{Colors.MAGENTA}[AGENCY] 📐 Geometria zmysłów...{Colors.RESET}")
        
        # Integracja fraktala z nową klasą z fractal.py
        if hasattr(self.core, 'aii') and hasattr(self.core.aii, 'fractal_gen'):
            self.core.aii.fractal_gen.display()
        else:
            # Fallback dla starej wersji
            size = 16
            output = []
            for y in range(size):
                line = ""
                for x in range(size * 2):
                    line += "  " if (x & y) else f"{Colors.CYAN}▲ {Colors.RESET}"
                output.append(line)
            print("\n".join(output))
            
        print(f"{Colors.MAGENTA}[FRACTAL PROJECTION COMPLETE]{Colors.RESET}\n")

if __name__ == "__main__":
    print("Test środowiskowy Agencji Autonomicznej:")
    class DummyCore:
        class DummyAII:
            context_vector = [0]*15
            AXES_ORDER = ['radość', 'smutek']
            def get_emotions(self): return {'radość': 0.8, 'smutek': 0.1}
            class DummyQuantum:
                class State: amplitudes = {'vacuum': np.sqrt(0.9) * np.exp(1j * 0)}
                def get_phase_coherence(self): return 1.0
            quantum = DummyQuantum()
            
            class DummyHaiku:
                def display(self): return "Kwiat wiśni opada.\nCisza."
            haiku_gen = DummyHaiku()
            
            class DummyFractal:
                def display(self): print("▲ ▲ ▲")
            fractal_gen = DummyFractal()
            
        aii = DummyAII()

    agency = MultimodalAgency(DummyCore(), verbose=True)
    agency._generate_haiku()
    agency._compose_autonomous_music()