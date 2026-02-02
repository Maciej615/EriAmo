# -*- coding: utf-8 -*-
# agency.py v2.0.0 - Autonomiczna Agencja Twórcza dla EriAmo [FULL EDITION]
"""
Moduł zarządzający autonomicznymi działaniami EriAmo
gdy system się nudzi (brak interakcji użytkownika).

NOWE w v2.0.0:
- Integracja z systemem muzycznym
- Inteligentny wybór aktywności (15 osi)
- Mechanizm nudy z automatycznym wyzwalaniem
- Rozszerzone statystyki i analiza

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
"""

import random
import time
import threading
import numpy as np
from union_config import Colors
from haiku import HaikuGenerator
from fractal import FractalGenerator

# Import systemu muzycznego (opcjonalny)
try:
    from production_music_system import ProductionMusicSystem
    MUSIC_AVAILABLE = True
except ImportError:
    MUSIC_AVAILABLE = False


class CreativeAgency:
    """
    Zarządza autonomicznymi działaniami twórczymi EriAmo.
    
    NOWE w v2.0.0:
    - Inteligentny wybór aktywności oparty na 15 osiach
    - System nudy z automatycznym wyzwalaniem
    - Integracja z muzyką (kompozycja autonomiczna)
    - Rozszerzone statystyki
    """
    
    def __init__(self, aii_instance):
        """
        Args:
            aii_instance: Referencja do głównego systemu AII
        """
        self.aii = aii_instance
        self.haiku_gen = HaikuGenerator(aii_instance)
        self.fractal_gen = FractalGenerator(aii_instance)
        
        # === SYSTEM MUZYCZNY ===
        self.music_available = False
        self.music_system = None
        
        if MUSIC_AVAILABLE:
            try:
                self.music_system = ProductionMusicSystem(
                    aii_instance=self.aii,
                    logger=None
                )
                self.music_available = True
                print(f"{Colors.GREEN}[AGENCY] ✓ System muzyczny zintegrowany{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.YELLOW}[AGENCY] ⚠ Błąd inicjalizacji muzyki: {e}{Colors.RESET}")
        
        # === MECHANIZM NUDY ===
        self.boredom_level = 0.0
        self.last_interaction_time = time.time()
        self.boredom_threshold = 0.8
        
        # === STATYSTYKI ===
        self.activities_log = []
        
        # === WĄTEK AUTONOMICZNY ===
        self.running = False
        self.autonomous_thread = None
        
        print(f"{Colors.MAGENTA}[AGENCY] Autonomia zainicjalizowana{Colors.RESET}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTELIGENTNY WYBÓR AKTYWNOŚCI (15 OSI)
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _choose_activity(self):
        """
        Wybiera aktywność na podstawie PEŁNEGO stanu 15D.
        
        LOGIKA DECYZYJNA:
        - Wysoka KREACJA + CHAOS → Fraktale (eksperymentalne)
        - Wysoka WIEDZA + LOGIKA → Haiku (struktura słów)
        - Wysoka PRZESTRZEŃ + BYT → Muzyka (ontologia dźwięku)
        - Wysoka MIŁOŚĆ/RADOŚĆ → Muzyka (wyrażenie uczuć)
        """
        emotions = self.aii.get_emotions()
        
        # Oblicz score dla każdej aktywności
        scores = {
            'haiku': self._score_haiku(emotions),
            'fractal': self._score_fractal(emotions),
        }
        
        if self.music_available:
            scores['music'] = self._score_music(emotions)
        
        # Softmax z temperaturą
        temperature = 0.8
        exp_scores = {k: np.exp(v / temperature) for k, v in scores.items()}
        total = sum(exp_scores.values())
        probs = {k: v / total for k, v in exp_scores.items()}
        
        # Wybierz według prawdopodobieństw
        choices = list(probs.keys())
        weights = list(probs.values())
        return np.random.choice(choices, p=weights)
    
    def _score_haiku(self, emotions):
        """Haiku = struktura słów, logika, wiedza"""
        return (
            emotions.get('logika', 0) * 0.4 +
            emotions.get('wiedza', 0) * 0.3 +
            emotions.get('kreacja', 0) * 0.2 +
            emotions.get('smutek', 0) * 0.1
        )
    
    def _score_fractal(self, emotions):
        """Fraktale = wizualność, chaos, eksperyment"""
        return (
            emotions.get('chaos', 0) * 0.4 +
            emotions.get('kreacja', 0) * 0.3 +
            emotions.get('przestrzeń', 0) * 0.2 +
            emotions.get('zaskoczenie', 0) * 0.1
        )
    
    def _score_music(self, emotions):
        """Muzyka = ontologia, przestrzeń, uczucia"""
        return (
            emotions.get('przestrzeń', 0) * 0.3 +
            emotions.get('byt', 0) * 0.2 +
            emotions.get('kreacja', 0) * 0.2 +
            emotions.get('miłość', 0) * 0.15 +
            emotions.get('radość', 0) * 0.15
        )
    
    def _choose_fractal_pattern(self):
        """
        Wybiera typ fraktala na podstawie emocji.
        
        Returns:
            str: 'mandala', 'triangle', 'spiral'
        """
        emotion = self.aii.introspect()
        
        pattern_map = {
            'radość': 'mandala',
            'smutek': 'spiral',
            'strach': 'triangle',
            'gniew': 'triangle',
            'miłość': 'mandala',
            'neutralna': 'mandala'
        }
        
        for key in pattern_map:
            if key.lower() in emotion.lower():
                return pattern_map[key]
        
        return 'mandala'
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MECHANIZM NUDY
    # ═══════════════════════════════════════════════════════════════════════════
    
    def start_autonomous_loop(self):
        """Uruchamia wątek autonomicznej twórczości."""
        if self.running:
            print(f"{Colors.YELLOW}[AGENCY] Autonomia już działa{Colors.RESET}")
            return
        
        self.running = True
        
        def loop():
            while self.running:
                time.sleep(10)
                self._update_boredom()
                
                if self.boredom_level > self.boredom_threshold:
                    self.start_creative_session()
                    self.boredom_level = 0.3
        
        self.autonomous_thread = threading.Thread(target=loop, daemon=True)
        self.autonomous_thread.start()
        print(f"{Colors.GREEN}[AGENCY] Autonomia aktywna!{Colors.RESET}")
    
    def stop_autonomous_loop(self):
        """Zatrzymuje wątek autonomiczny."""
        self.running = False
        if self.autonomous_thread:
            self.autonomous_thread.join(timeout=2)
        print(f"{Colors.YELLOW}[AGENCY] Autonomia zatrzymana{Colors.RESET}")
    
    def _update_boredom(self):
        """Zwiększa nudę proporcjonalnie do czasu bezczynności."""
        idle_time = time.time() - self.last_interaction_time
        
        # Nuda rośnie szybciej gdy:
        # - Długi czas bezczynności
        # - Wysoka KREACJA (potrzeba tworzenia)
        # - Niski CHAOS (potrzeba stymulacji)
        
        emotions = self.aii.get_emotions()
        kreacja_factor = 1.0 + emotions.get('kreacja', 0) * 0.5
        chaos_factor = 1.0 - emotions.get('chaos', 0) * 0.3
        
        boredom_rate = 0.01 * kreacja_factor * chaos_factor
        
        if idle_time > 30:
            self.boredom_level = min(1.0, self.boredom_level + boredom_rate)
    
    def on_user_interaction(self):
        """Wywołaj gdy użytkownik coś napisze."""
        self.last_interaction_time = time.time()
        self.boredom_level = max(0.0, self.boredom_level - 0.5)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SESJE TWÓRCZE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def start_creative_session(self):
        """
        Główna metoda - uruchamia sesję twórczą.
        ROZSZERZONA o muzykę i inteligencję.
        """
        activity = self._choose_activity()
        
        print(f"\n{Colors.CYAN}══════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.CYAN}      [AUTONOMIA] Sesja Twórcza: {activity.upper()}{Colors.RESET}")
        print(f"{Colors.CYAN}══════════════════════════════════════════════════{Colors.RESET}\n")
        
        # Diagnostyka emocjonalna
        emotions = self.aii.get_emotions()
        dominant = max(emotions.items(), key=lambda x: x[1])
        print(f"{Colors.YELLOW}Stan: {dominant[0].upper()} ({dominant[1]:.2f}){Colors.RESET}\n")
        
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
        
        elif activity == 'music':
            print(f"{Colors.MAGENTA}[WYBRANO] Komponowanie muzyki...{Colors.RESET}\n")
            time.sleep(0.3)
            self._compose_autonomous_music()
        
        print(f"{Colors.CYAN}[AUTONOMIA] Sesja zakończona. Boredom: {self.boredom_level:.2f}{Colors.RESET}\n")
        
        # Logowanie
        self.activities_log.append({
            'activity': activity,
            'emotion': dominant[0],
            'emotion_value': dominant[1],
            'timestamp': time.time()
        })
    
    def _compose_autonomous_music(self):
        """Komponuje muzykę na podstawie stanu emocjonalnego."""
        if not self.music_available:
            print(f"{Colors.YELLOW}[AGENCY] Muzyka niedostępna{Colors.RESET}")
            return
        
        emotions = self.aii.get_emotions()
        
        # Mapowanie dominującej emocji → gatunek
        genre_map = {
            'radość': 'menuet',
            'smutek': 'ambient',
            'gniew': 'rock',
            'strach': 'ambient',
            'miłość': 'menuet',
            'logika': 'menuet',
            'chaos': 'experimental',
            'kreacja': 'jazz'
        }
        
        # Znajdź dominantę
        dominant = max(emotions.items(), key=lambda x: x[1])
        genre = genre_map.get(dominant[0], 'menuet')
        
        print(f"\n{Colors.MAGENTA}[AUTONOMIA] Komponuję {genre} (dominanta: {dominant[0]})...{Colors.RESET}")
        
        try:
            if genre == 'menuet':
                is_minor = emotions.get('smutek', 0) > 0.5
                key = random.choice(['C', 'G', 'D', 'F'])
                
                result = self.music_system.compose_menuet(
                    key=key,
                    minor=is_minor,
                    use_nn=True
                )
            else:
                result = self.music_system.compose_freestyle(
                    genre=genre,
                    use_nn=True
                )
            
            # Raport
            reward = result.get('evaluation', {}).get('reward', 0.0)
            print(f"{Colors.GREEN}[SUKCES] Kompozycja ukończona (reward: {reward:.3f}){Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}[BŁĄD] {e}{Colors.RESET}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # STATYSTYKI
    # ═══════════════════════════════════════════════════════════════════════════
    
    def get_stats(self):
        """
        Zwraca podstawowe statystyki.
        
        Returns:
            dict: Statystyki
        """
        if not self.activities_log:
            return {'total': 0, 'haiku': 0, 'fractal': 0, 'music': 0}
        
        total = len(self.activities_log)
        haiku_count = sum(1 for a in self.activities_log if a['activity'] == 'haiku')
        fractal_count = sum(1 for a in self.activities_log if a['activity'] == 'fractal')
        music_count = sum(1 for a in self.activities_log if a['activity'] == 'music')
        
        return {
            'total': total,
            'haiku': haiku_count,
            'fractal': fractal_count,
            'music': music_count
        }
    
    def get_detailed_stats(self):
        """Rozszerzone statystyki z analizą."""
        if not self.activities_log:
            return {'total': 0}
        
        total = len(self.activities_log)
        
        # Liczby per aktywność
        counts = {}
        for a in self.activities_log:
            act = a['activity']
            counts[act] = counts.get(act, 0) + 1
        
        # Analiza emocjonalna
        emotion_distribution = {}
        for a in self.activities_log:
            emo = a['emotion']
            emotion_distribution[emo] = emotion_distribution.get(emo, 0) + 1
        
        # Ostatnie działania
        recent = self.activities_log[-5:]
        
        # Aktywność w czasie
        if len(self.activities_log) >= 2:
            time_diffs = [
                self.activities_log[i]['timestamp'] - self.activities_log[i-1]['timestamp']
                for i in range(1, len(self.activities_log))
            ]
            avg_interval = np.mean(time_diffs) / 60
        else:
            avg_interval = 0
        
        return {
            'total': total,
            'counts': counts,
            'emotion_distribution': emotion_distribution,
            'recent': recent,
            'avg_interval_minutes': avg_interval,
            'current_boredom': self.boredom_level
        }
    
    def print_stats_report(self):
        """Wydrukuj raport statystyk."""
        stats = self.get_detailed_stats()
        
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║  RAPORT AUTONOMICZNEJ AGENCJI         ║{Colors.RESET}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════╝{Colors.RESET}\n")
        
        print(f"Całkowita liczba sesji: {stats['total']}")
        print(f"Średni interwał: {stats.get('avg_interval_minutes', 0):.1f} min")
        print(f"Obecna nuda: {stats['current_boredom']:.2f}\n")
        
        print("Aktywności:")
        for act, count in stats.get('counts', {}).items():
            pct = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {act:10s}: {count:3d} ({pct:5.1f}%)")
        
        print("\nEmocje wyzwalające:")
        for emo, count in sorted(stats.get('emotion_distribution', {}).items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {emo:12s}: {count:3d}")
