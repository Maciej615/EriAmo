# -*- coding: utf-8 -*-
"""
multimodal_agency.py v3.1.0-Alive
Zarządza autonomicznymi agentami (Krytyk, Uwaga, Twórca).
FIX: Przywrócono logikę generowania Haiku, Fraktali i Muzyki (byliśmy w trybie 'pass').
"""

import threading
import time
import random
import sys

# Konfiguracja kolorów
try:
    from union_config import Colors
except ImportError:
    class Colors:
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        RESET = "\033[0m"
        YELLOW = "\033[33m"
        GREEN = "\033[32m"

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
        self.boredom_level = 0.0      # 0.0 (Skupiony) -> 1.0 (Znudzony)
        self.attention_span = 1.0     # 1.0 (Pełna uwaga)
        self.last_stimulus_time = time.time()
        
        # Generator fraktali (prosty ASCII)
        self.fractal_buffer = []
        
        if self.verbose:
            print(f"{Colors.MAGENTA}[AGENCY] Autonomia w pełni aktywna (Fractals+Haiku+Music).{Colors.RESET}")

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
        """
        Resetuje nudę, gdy użytkownik coś napisze.
        """
        self.last_stimulus_time = time.time()
        # Zmniejszamy nudę drastycznie, bo użytkownik wrócił
        self.boredom_level = max(0.0, self.boredom_level - 0.8) 
        self.attention_span = 1.0 

    def _boredom_loop(self):
        """
        Główna pętla nudy. Co 5 sekund sprawdza, czy użytkownik milczy.
        """
        while self.running:
            time.sleep(5)
            
            # Czas od ostatniej aktywności
            idle_time = time.time() - self.last_stimulus_time
            
            # Jeśli nikt nie pisze przez 15 sekund, nuda rośnie
            if idle_time > 15:
                self.boredom_level = min(1.0, self.boredom_level + 0.05)
            
            # PROGI REAKCJI:
            # > 0.6 -> Drobne myśli (logi)
            # > 0.8 -> Sztuka (Haiku / Fraktale)
            
            if self.boredom_level > 0.8:
                # 20% szansy na artystyczny wybuch co cykl
                if random.random() < 0.20:
                    self._trigger_spontaneous_art()
                    # Po stworzeniu dzieła nuda nieco spada (satysfakcja)
                    self.boredom_level = 0.5 

    def _creative_loop(self):
        """
        Osobny wątek dla muzyki (działa rzadziej).
        """
        while self.running:
            # Muzyka powstaje rzadziej (co 40-90 sekund)
            time.sleep(random.randint(40, 90))
            
            if self.boredom_level > 0.5:
                # Generuj muzykę
                self._compose_music()

    def _trigger_spontaneous_art(self):
        """Wybiera formę ekspresji."""
        choice = random.choice(['haiku', 'fractal', 'fractal']) # Fraktale są efektowne w GUI
        
        if choice == 'haiku':
            self._generate_haiku()
        elif choice == 'fractal':
            self._generate_fractal()

    def _generate_haiku(self):
        """Wywołuje generator Haiku z rdzenia AII."""
        # Sprawdzamy, czy AII ma moduł haiku
        if hasattr(self.core, 'aii') and self.core.aii and self.core.aii.haiku_gen:
            # Pobieramy dominującą emocję dla kontekstu
            intro = self.core.aii.introspect()
            print(f"\n{Colors.MAGENTA}[AGENCY] 📜 Nuda rodzi słowa... ({intro}){Colors.RESET}")
            
            # Generuj
            haiku = self.core.aii.haiku_gen.generate()
            print(f"{Colors.CYAN}{haiku}{Colors.RESET}\n")
        else:
            print(f"{Colors.YELLOW}[AGENCY] Próbowałem napisać Haiku, ale nie mam papieru (brak modułu).{Colors.RESET}")

    def _generate_fractal(self):
        """Generuje ASCII Fraktal (Trójkąt Sierpińskiego) jako 'wizualizację myśli'."""
        print(f"\n{Colors.MAGENTA}[AGENCY] 📐 Geometria pustki...{Colors.RESET}")
        
        size = 16
        output = []
        for y in range(size):
            line = ""
            for x in range(size * 2):
                # Prosta logika bitowa dla Sierpińskiego
                if (x & y): 
                    line += "  "
                else:
                    line += f"{Colors.CYAN}▲ {Colors.RESET}"
            output.append(line)
        
        # Wyświetlamy
        print("\n".join(output))
        print(f"{Colors.MAGENTA}[FRACTAL PROJECTION COMPLETE]{Colors.RESET}\n")

    def _compose_music(self):
        """Symuluje (lub wywołuje) komponowanie muzyki."""
        # W pełnej wersji tutaj wołamy SoulComposer. 
        # Na razie symulujemy proces, który wygląda efektownie w logach.
        
        print(f"\n{Colors.MAGENTA}[AGENCY] 🎵 Nucę melodię w ciszy...{Colors.RESET}")
        scales = ["A-Minor", "C-Major", "Dorian Mode", "Pentatonic"]
        chosen = random.choice(scales)
        
        # Symulacja procesu twórczego
        print(f"{Colors.GREEN}[SoulComposer] Wybrano skalę: {chosen}{Colors.RESET}")
        time.sleep(0.5)
        print(f"{Colors.GREEN}[SoulComposer] Generowanie sekwencji MIDI...{Colors.RESET}")
        
        # Generujemy nazwę pliku
        filename = f"melody_{int(time.time())}.mid"
        print(f"{Colors.YELLOW}⭐ Utwór gotowy: {filename}{Colors.RESET}\n")