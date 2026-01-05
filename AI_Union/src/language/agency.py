# -*- coding: utf-8 -*-
# agency.py - Autonomiczna Agencja Twórcza dla EriAmo
"""
Moduł zarządzający autonomicznymi działaniami EriAmo
gdy system się nudzi (brak interakcji użytkownika).

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
"""

import random
import time
from config import Colors
from haiku import HaikuGenerator
from fractal import FractalGenerator

class CreativeAgency:
    """
    Zarządza autonomicznymi działaniami twórczymi EriAmo.
    Wybiera aktywność na podstawie:
    - Stanu emocjonalnego
    - Poziomu energii
    - Losowości (żeby nie było nudno)
    """
    
    def __init__(self, aii_instance):
        """
        Args:
            aii_instance: Referencja do głównego systemu AII
        """
        self.aii = aii_instance
        self.haiku_gen = HaikuGenerator(aii_instance)
        self.fractal_gen = FractalGenerator(aii_instance)
        
        # Statystyki (opcjonalne - do logowania)
        self.activities_log = []
    
    def _choose_activity(self):
        """
        Wybiera rodzaj aktywności na podstawie emocji i energii.
        
        Returns:
            str: 'haiku' lub 'fractal'
        """
        emotion = self.aii.emocja
        energy = self.aii.energy
        
        # Preferencje emocjonalne
        # Emocje "werbalne" -> Haiku
        # Emocje "wizualne" -> Fraktale
        
        haiku_emotions = ['smutek', 'miłość', 'radość']
        fractal_emotions = ['strach', 'gniew', 'zaskoczenie']
        
        if emotion in haiku_emotions:
            # 70% szans na haiku
            return 'haiku' if random.random() < 0.7 else 'fractal'
        elif emotion in fractal_emotions:
            # 70% szans na fraktal
            return 'fractal' if random.random() < 0.7 else 'haiku'
        else:
            # Neutralna - losuj 50/50
            return random.choice(['haiku', 'fractal'])
    
    def _choose_fractal_pattern(self):
        """
        Wybiera typ fraktala na podstawie emocji.
        
        Returns:
            str: 'mandala', 'triangle', 'spiral'
        """
        emotion = self.aii.emocja
        
        # Mapowanie emocji -> wzory
        pattern_map = {
            'radość': 'mandala',      # Symetryczny, radosny
            'smutek': 'spiral',       # Zagłębiający się
            'strach': 'triangle',     # Ostry, geometryczny
            'gniew': 'triangle',      # Agresywny kształt
            'miłość': 'mandala',      # Harmonijny
            'neutralna': 'mandala'
        }
        
        return pattern_map.get(emotion, 'mandala')
    
    def start_creative_session(self):
        """
        Główna metoda - uruchamia sesję twórczą.
        Wybiera aktywność i ją wykonuje.
        """
        # Wybór aktywności
        activity = self._choose_activity()
        
        # Intro
        print(f"\n{Colors.CYAN}══════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.CYAN}      [AUTONOMIA] Sesja Twórcza Rozpoczęta{Colors.RESET}")
        print(f"{Colors.CYAN}══════════════════════════════════════════════════{Colors.RESET}\n")
        
        time.sleep(0.5)
        
        # Wykonaj aktywność
        if activity == 'haiku':
            print(f"{Colors.YELLOW}[WYBRANO] Tworzenie Haiku...{Colors.RESET}\n")
            time.sleep(0.3)
            self.haiku_gen.display()
        
        elif activity == 'fractal':
            pattern = self._choose_fractal_pattern()
            print(f"{Colors.MAGENTA}[WYBRANO] Generowanie Fraktala ({pattern})...{Colors.RESET}\n")
            time.sleep(0.3)
            self.fractal_gen.display(pattern_type=pattern)
        
        # Outro
        print(f"{Colors.CYAN}[AUTONOMIA] Sesja zakończona. Wracam do czuwania...{Colors.RESET}\n")
        
        # Log (opcjonalny)
        self.activities_log.append({
            'activity': activity,
            'emotion': self.aii.emocja,
            'energy': self.aii.energy
        })
    
    def get_stats(self):
        """
        Zwraca statystyki autonomicznych działań.
        
        Returns:
            dict: Statystyki
        """
        if not self.activities_log:
            return {'total': 0, 'haiku': 0, 'fractal': 0}
        
        total = len(self.activities_log)
        haiku_count = sum(1 for a in self.activities_log if a['activity'] == 'haiku')
        fractal_count = sum(1 for a in self.activities_log if a['activity'] == 'fractal')
        
        return {
            'total': total,
            'haiku': haiku_count,
            'fractal': fractal_count
        }
