# -*- coding: utf-8 -*-
"""
multimodal_agency.py v3.2.1-MusicIntegrated-Fixed
Zarządza autonomicznymi agentami (Krytyk, Uwaga, Twórca) + MUZYKA!
+ Naprawiono _generate_haiku (patch introspect → get_emotions)
+ Dodano fallback dla menuetu (gdy MenuetGenerator niedostępny → freestyle classical)
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
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        RESET = "\033[0m"
        YELLOW = "\033[33m"
        GREEN = "\033[32m"
        RED = "\033[31m"

class MultimodalAgency:
    def __init__(self, union_core, verbose=False, **kwargs):
        """
        Inicjalizacja Agencji Autonomicznej.
        """
        self.core = union_core
        self.verbose = verbose
        self.running = False
        self.threads = []
        
        # Parametry Agencji
        self.boredom_level = 0.0
        self.attention_span = 1.0
        self.last_stimulus_time = time.time()
        
        # ========== INICJALIZACJA SYSTEMU MUZYCZNEGO ==========
        self.music_available = False
        self.music_system = None
        
        try:
            from production_music_system import ProductionMusicSystem
            self.music_system = ProductionMusicSystem(
                aii_instance=self.core.aii,
                logger=None
            )
            self.music_available = True
            if self.verbose:
                print(f"{Colors.GREEN}[AGENCY] ✓ System muzyczny zintegrowany{Colors.RESET}")
        except ImportError as e:
            if self.verbose:
                print(f"{Colors.YELLOW}[AGENCY] ⚠ System muzyczny niedostępny: {e}{Colors.RESET}")
        except Exception as e:
            if self.verbose:
                print(f"{Colors.YELLOW}[AGENCY] ⚠ Błąd inicjalizacji muzyki: {e}{Colors.RESET}")
        
        if self.verbose:
            modes = ["Haiku", "Fractals"]
            if self.music_available:
                modes.append("Music")
            print(f"{Colors.MAGENTA}[AGENCY] Autonomia aktywna: {', '.join(modes)}{Colors.RESET}")

    def start(self):
        """Uruchamia wątki autonomiczne."""
        self.running = True
        self.threads = [
            threading.Thread(target=self._boredom_loop, daemon=True, name="BoredomThread"),
            threading.Thread(target=self._creative_loop, daemon=True, name="CreativeThread")
        ]
        for t in self.threads:
            t.start()

    def stop(self):
        """Zatrzymuje agencję."""
        self.running = False

    def stimulate(self, stimulus_text):
        """Resetuje nudę gdy użytkownik coś napisze."""
        self.last_stimulus_time = time.time()
        self.boredom_level = max(0.0, self.boredom_level - 0.8)
        self.attention_span = 1.0

    def _boredom_loop(self):
        """Główna pętla nudy."""
        while self.running:
            time.sleep(5)
            
            idle_time = time.time() - self.last_stimulus_time
            
            if idle_time > 15:
                self.boredom_level = min(1.0, self.boredom_level + 0.05)
            
            if self.boredom_level > 0.8:
                if random.random() < 0.20:
                    self._trigger_spontaneous_art()
                    self.boredom_level = 0.5

    def _creative_loop(self):
        """Osobny wątek dla muzyki (działa rzadziej)."""
        while self.running:
            # Muzyka powstaje rzadziej (co 2-5 minut)
            time.sleep(random.randint(120, 300))
            
            if self.boredom_level > 0.5 and self.music_available:
                self._compose_autonomous_music()

    def _trigger_spontaneous_art(self):
        """Wybiera formę ekspresji (Haiku lub Fraktal)."""
        choice = random.choice(['haiku', 'fractal', 'fractal'])
        
        if choice == 'haiku':
            self._generate_haiku()
        elif choice == 'fractal':
            self._generate_fractal()

    # ========== AUTONOMICZNE KOMPONOWANIE ==========
    
    def _compose_autonomous_music(self):
        """
        Komponuje muzykę autonomicznie na podstawie stanu emocjonalnego.
        """
        if not self.music_available or not self.music_system:
            return
        
        print(f"\n{Colors.MAGENTA}[AGENCY] 🎵 Tworzę muzykę z nudy...{Colors.RESET}")
        
        try:
            # Pobierz stan emocjonalny
            if hasattr(self.core.aii, 'get_emotions'):
                metrics = self.core.aii.get_emotions()
            else:
                metrics = {}
                for i, axis in enumerate(self.core.aii.AXES_ORDER):
                    metrics[axis] = float(self.core.aii.context_vector[i])
            
            # Dominanta
            dominant_axis = max(metrics.items(), key=lambda x: x[1])
            dominant_name = dominant_axis[0]
            dominant_value = dominant_axis[1]
            
            print(f"{Colors.CYAN}[AGENCY] Dominanta: {dominant_name.upper()} ({dominant_value:.2f}){Colors.RESET}")
            
            # Mapowanie emocji → gatunek
            emotion_genre_map = {
                'radość': 'pop',
                'smutek': 'ambient',
                'strach': 'ambient',
                'gniew': 'heavy_metal',
                'miłość': 'menuet',
                'wstręt': 'punk',
                'zaskoczenie': 'jazz',
                'akceptacja': 'folk',
                'logika': 'menuet',
                'wiedza': 'classical',
                'czas': 'ambient',
                'kreacja': 'jazz',
                'byt': 'folk',
                'przestrzeń': 'ambient',
                'chaos': 'experimental'
            }
            
            genre = emotion_genre_map.get(dominant_name, 'menuet')
            
            # FALLBACK: jeśli menuet niedostępny → classical freestyle
            menuet_available = (hasattr(self.music_system, 'menuet_gen') and 
                              self.music_system.menuet_gen is not None)
            
            if genre == 'menuet' or dominant_name in ['logika', 'miłość']:
                if menuet_available:
                    print(f"{Colors.GREEN}[AGENCY] Komponuję menuet...{Colors.RESET}")
                    
                    keys_major = ['C', 'G', 'D', 'F']
                    keys_minor = ['A', 'D', 'E', 'B']
                    
                    is_minor = metrics.get('smutek', 0) > 0.5 or metrics.get('strach', 0) > 0.5
                    key = random.choice(keys_minor if is_minor else keys_major)
                    
                    result = self.music_system.compose_menuet(
                        key=key,
                        minor=is_minor,
                        use_nn=True
                    )
                else:
                    print(f"{Colors.YELLOW}[AGENCY] MenuetGenerator niedostępny → fallback do classical{Colors.RESET}")
                    genre = 'classical'
                    result = self.music_system.compose_freestyle(
                        genre=genre,
                        use_nn=True
                    )
            else:
                print(f"{Colors.GREEN}[AGENCY] Komponuję {genre}...{Colors.RESET}")
                result = self.music_system.compose_freestyle(
                    genre=genre,
                    use_nn=True
                )
            
            # Raport
            evaluation = result.get('evaluation', {})
            reward = evaluation.get('reward', 0.0)
            
            if reward > 0.7:
                mood = f"{Colors.GREEN}Dobra kompozycja!{Colors.RESET}"
            elif reward > 0.4:
                mood = f"{Colors.YELLOW}Przeciętna kompozycja{Colors.RESET}"
            else:
                mood = f"{Colors.RED}Słaba kompozycja{Colors.RESET}"
            
            print(f"{Colors.MAGENTA}[AGENCY] {mood} Reward: {reward:.3f}{Colors.RESET}")
            print(f"{Colors.MAGENTA}[AGENCY] Zapisano w pamięci: {result.get('memory_id', 'brak')}{Colors.RESET}\n")
            
            # Redukcja nudy
            self.boredom_level = max(0.3, self.boredom_level - 0.4)
            
        except Exception as e:
            print(f"{Colors.RED}[AGENCY] Błąd komponowania: {e}{Colors.RESET}")
            traceback.print_exc()

    # ========== HAIKU – NAPRAWIONA WERSJA ==========

    def _generate_haiku(self):
        """Wywołuje generator Haiku z rdzenia AII."""
        if hasattr(self.core, 'aii') and self.core.aii and self.core.aii.haiku_gen:
            # Patch: zastąpiono introspect() → get_emotions()
            emotions = self.core.aii.get_emotions()
            total_intensity = sum(emotions.values())
            
            if total_intensity < 0.01:
                intro = "Neutralny"
            else:
                dominant_axis = max(emotions, key=emotions.get)
                intensity = emotions[dominant_axis]
                intro = f"{dominant_axis.upper()} ({intensity:.2f})"
            
            print(f"\n{Colors.MAGENTA}[AGENCY] 📜 Nuda rodzi słowa... ({intro}){Colors.RESET}")
            
            haiku = self.core.aii.haiku_gen.generate()
            print(f"{Colors.CYAN}{haiku}{Colors.RESET}\n")
        else:
            print(f"{Colors.YELLOW}[AGENCY] Brak modułu Haiku{Colors.RESET}")

    # ========== FRAKTAL ==========

    def _generate_fractal(self):
        """Generuje ASCII Fraktal."""
        print(f"\n{Colors.MAGENTA}[AGENCY] 📐 Geometria pustki...{Colors.RESET}")
        
        size = 16
        output = []
        for y in range(size):
            line = ""
            for x in range(size * 2):
                if (x & y):
                    line += "  "
                else:
                    line += f"{Colors.CYAN}▲ {Colors.RESET}"
            output.append(line)
        
        print("\n".join(output))
        print(f"{Colors.MAGENTA}[FRACTAL PROJECTION COMPLETE]{Colors.RESET}\n")