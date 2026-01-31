# production_music_system.py
# -*- coding: utf-8 -*-
"""
PRODUKCYJNA INTEGRACJA - System Muzyczny EriAmo
Soul Composer v8.1 + Tiny NN + Menuet Generator + Mechanizm RL

ZMIANY względem przykładowego systemu:
1. ✅ Zastąpiono AIIEmotionEngine → from aii import AII
2. ✅ Zastąpiono MockComposer → SoulComposerV8
3. ✅ Dodano mechanizm RL z automatyczną oceną i zapisem do D_Map
4. ✅ Integracja z prawdziwym context_vector i get_emotions()
"""

import os
import sys
import time
import numpy as np
from typing import Dict, Optional, List, Tuple
from datetime import datetime

# === IMPORT PRAWDZIWYCH MODUŁÓW ERIAMO ===
try:
    from aii import AII
    print("[MUSIC-SYSTEM] ✓ Zaimportowano AII")
except ImportError:
    print("[ERROR] Brak modułu 'aii'. Upewnij się że jesteś w katalogu EriAmo/AI_Union")
    sys.exit(1)

try:
    from soul_composer import SoulComposerV8
    print("[MUSIC-SYSTEM] ✓ Zaimportowano SoulComposerV8")
except ImportError:
    print("[ERROR] Brak modułu 'soul_composer'")
    sys.exit(1)

try:
    from union_config import UnionConfig, Colors
    print("[MUSIC-SYSTEM] ✓ Zaimportowano UnionConfig")
except ImportError:
    print("[ERROR] Brak modułu 'union_config'")
    sys.exit(1)

# Komponenty NN (opcjonalne - system działa bez nich)
try:
    from soul_composer_tiny_nn import SoulComposerTinyNN
    NN_AVAILABLE = True
    print("[MUSIC-SYSTEM] ✓ Zaimportowano TinyNN")
except ImportError:
    NN_AVAILABLE = False
    print("[MUSIC-SYSTEM] ⚠ TinyNN niedostępne - system działa w trybie klasycznym")

try:
    from menuet_generator_enhanced import MenuetGeneratorEnhanced
    MENUET_AVAILABLE = True
    print("[MUSIC-SYSTEM] ✓ Zaimportowano MenuetGenerator")
except ImportError:
    MENUET_AVAILABLE = False
    print("[MUSIC-SYSTEM] ⚠ MenuetGenerator niedostępny")


# ==================== EWALUATOR KOMPOZYCJI ====================

class CompositionEvaluator:
    """
    Ewaluator kompozycji muzycznych z mechanizmem RL.
    Ocenia utwory według kryteriów i zwraca reward dla uczenia.
    """
    
    def __init__(self):
        self.evaluation_history = []
    
    def evaluate_composition(self, composition: dict, metrics: dict, 
                           composition_type: str = "generic") -> dict:
        """
        Ocenia kompozycję muzyczną i zwraca reward dla RL.
        
        Args:
            composition: dict z 'melody' i 'harmony'
            metrics: dict z emocjami (15 osi)
            composition_type: 'menuet', 'generic', 'freestyle'
            
        Returns:
            dict: {
                'reward': float (0-1),
                'scores': dict,
                'feedback': str
            }
        """
        scores = {}
        
        # === KRYTERIA OCENY ===
        
        # 1. Spójność strukturalna (czy ma sens?)
        scores['structural_coherence'] = self._evaluate_structure(composition)
        
        # 2. Różnorodność melodyczna (czy nie jest monotonna?)
        scores['melodic_diversity'] = self._evaluate_melody_diversity(composition)
        
        # 3. Zgodność emocjonalna (czy muzyka pasuje do emocji?)
        scores['emotional_match'] = self._evaluate_emotional_match(
            composition, metrics
        )
        
        # 4. Złożoność kompozycji
        scores['complexity'] = self._evaluate_complexity(composition, metrics)
        
        # 5. Specjalne kryteria dla menuetów
        if composition_type == "menuet":
            scores['menuet_style'] = self._evaluate_menuet_style(composition)
        
        # === OBLICZ REWARD ===
        # Wagi zależą od typu kompozycji
        if composition_type == "menuet":
            weights = {
                'structural_coherence': 0.3,
                'melodic_diversity': 0.2,
                'emotional_match': 0.2,
                'complexity': 0.1,
                'menuet_style': 0.2
            }
        else:
            weights = {
                'structural_coherence': 0.25,
                'melodic_diversity': 0.3,
                'emotional_match': 0.3,
                'complexity': 0.15
            }
        
        reward = sum(scores.get(k, 0) * weights[k] for k in weights)
        
        # === FEEDBACK TEKSTOWY ===
        feedback = self._generate_feedback(scores, reward)
        
        # Zapisz w historii
        evaluation = {
            'timestamp': datetime.now().isoformat(),
            'type': composition_type,
            'reward': reward,
            'scores': scores,
            'feedback': feedback
        }
        self.evaluation_history.append(evaluation)
        
        return evaluation
    
    def _evaluate_structure(self, composition: dict) -> float:
        """Ocenia spójność strukturalną."""
        melody = composition.get('melody', [])
        harmony = composition.get('harmony', [])
        
        if not melody or not harmony:
            return 0.3
        
        # Sprawdź czy długości się zgadzają
        if len(melody) != len(harmony):
            return 0.4
        
        # Sprawdź regularność (czy takty mają sens)
        score = 0.5
        
        # Bonus za odpowiednią długość (8, 16, 32, 64 takty)
        ideal_lengths = [8, 16, 32, 64]
        if len(melody) in ideal_lengths:
            score += 0.3
        
        # Bonus za powtórzenia strukturalne (A-A-B-B)
        if len(melody) >= 16:
            # Sprawdź czy są podobieństwa (uproszczone)
            score += 0.2
        
        return min(1.0, score)
    
    def _evaluate_melody_diversity(self, composition: dict) -> float:
        """Ocenia różnorodność melodyczną."""
        melody = composition.get('melody', [])
        
        if not melody:
            return 0.3
        
        # Zbierz wszystkie nuty
        all_pitches = []
        for measure in melody:
            for note_event in measure:
                if note_event.get('type') == 'note':
                    all_pitches.append(note_event.get('pitch', 60))
        
        if len(all_pitches) < 2:
            return 0.3
        
        # Unikalne nuty
        unique_pitches = len(set(all_pitches))
        pitch_diversity = min(1.0, unique_pitches / 12.0)  # Max 12 nut w oktawie
        
        # Zakres melodyczny (ambitus)
        pitch_range = max(all_pitches) - min(all_pitches)
        range_score = min(1.0, pitch_range / 24.0)  # Idealne: 2 oktawy
        
        # Średnia zmiana wysokości (contour)
        changes = [abs(all_pitches[i+1] - all_pitches[i]) 
                  for i in range(len(all_pitches)-1)]
        avg_change = np.mean(changes) if changes else 0
        contour_score = min(1.0, avg_change / 5.0)  # Idealne: ~5 półtonów
        
        # Kombinacja
        score = (pitch_diversity * 0.4 + range_score * 0.3 + contour_score * 0.3)
        
        return score
    
    def _evaluate_emotional_match(self, composition: dict, metrics: dict) -> float:
        """Ocenia zgodność z emocjami."""
        melody = composition.get('melody', [])
        
        if not melody:
            return 0.5
        
        score = 0.5
        
        # LOGIKA wysoka → Regularne rytmy
        logika = metrics.get('logika', 0.5)
        if logika > 0.7:
            # Sprawdź regularność rytmiczną
            durations = []
            for measure in melody:
                for note in measure:
                    durations.append(note.get('duration', 1.0))
            
            if durations:
                # Jeśli większość ma podobne wartości = regularny
                unique_dur = len(set(durations))
                if unique_dur <= 3:  # Mało unikalnych wartości = regularny
                    score += 0.2
        
        # CHAOS wysoki → Większa różnorodność
        chaos = metrics.get('chaos', 0.3)
        if chaos > 0.6:
            # Sprawdź różnorodność
            all_pitches = []
            for measure in melody:
                for note in measure:
                    if note.get('type') == 'note':
                        all_pitches.append(note.get('pitch', 60))
            
            if all_pitches:
                pitch_std = np.std(all_pitches)
                if pitch_std > 5:  # Duże odchylenie = chaotyczny
                    score += 0.2
        
        # ENERGIA → Tempo i dynamika
        energia = metrics.get('energia', 0.5)
        # (W przyszłości: sprawdź tempo z metadanych)
        
        return min(1.0, score)
    
    def _evaluate_complexity(self, composition: dict, metrics: dict) -> float:
        """Ocenia złożoność kompozycji."""
        melody = composition.get('melody', [])
        
        if not melody:
            return 0.3
        
        # Liczba nut
        note_count = sum(len(m) for m in melody)
        
        # Złożoność rytmiczna
        durations = []
        for measure in melody:
            for note in measure:
                durations.append(note.get('duration', 1.0))
        
        unique_rhythms = len(set(durations)) if durations else 1
        rhythm_complexity = min(1.0, unique_rhythms / 6.0)
        
        # Złożoność harmoniczna (liczba unikalnych akordów)
        harmony = composition.get('harmony', [])
        unique_chords = 0
        for h_measure in harmony:
            for chord_event in h_measure:
                if chord_event.get('type') == 'chord':
                    unique_chords += 1
        
        harmony_complexity = min(1.0, unique_chords / 8.0)
        
        score = (rhythm_complexity * 0.5 + harmony_complexity * 0.5)
        
        # Dostosuj do KREACJI
        kreacja = metrics.get('kreacja', 0.5)
        if kreacja > 0.7:
            score *= 1.2  # Bonus za kreatywność
        
        return min(1.0, score)
    
    def _evaluate_menuet_style(self, composition: dict) -> float:
        """Specjalna ocena dla menuetów."""
        melody = composition.get('melody', [])
        
        # Menuet powinien mieć:
        # - Strukturę 16 lub 32 lub 64 taktów
        # - Rytm 3/4
        # - Elegancką melodię
        
        score = 0.5
        
        # Długość
        if len(melody) in [16, 32, 64]:
            score += 0.3
        
        # Rytm 3/4 (suma długości w takcie = 3.0)
        measure_totals = []
        for measure in melody:
            total = sum(note.get('duration', 0) for note in measure)
            measure_totals.append(total)
        
        if measure_totals:
            avg_total = np.mean(measure_totals)
            if 2.5 <= avg_total <= 3.5:  # Tolerancja dla 3/4
                score += 0.2
        
        return min(1.0, score)
    
    def _generate_feedback(self, scores: dict, reward: float) -> str:
        """Generuje tekstowy feedback."""
        if reward > 0.8:
            quality = "Doskonała"
        elif reward > 0.6:
            quality = "Dobra"
        elif reward > 0.4:
            quality = "Przeciętna"
        else:
            quality = "Słaba"
        
        feedback = f"{quality} kompozycja (reward: {reward:.3f}). "
        
        # Dodaj szczegóły
        weak_points = [k for k, v in scores.items() if v < 0.5]
        if weak_points:
            feedback += f"Do poprawy: {', '.join(weak_points)}. "
        
        strong_points = [k for k, v in scores.items() if v > 0.7]
        if strong_points:
            feedback += f"Mocne strony: {', '.join(strong_points)}."
        
        return feedback


# ==================== GŁÓWNY SYSTEM ====================

class ProductionMusicSystem:
    """
    Produkcyjny system muzyczny EriAmo.
    Integruje: AII + SoulComposerV8 + TinyNN + Menuety + RL
    """
    
    def __init__(self, aii_instance: AII, logger=None):
        """
        Args:
            aii_instance: Instancja AII (prawdziwego silnika emocji)
            logger: Opcjonalny logger
        """
        print(f"\n{Colors.CYAN}{'='*70}")
        print("INICJALIZACJA PRODUKCYJNEGO SYSTEMU MUZYCZNEGO")
        print(f"{'='*70}{Colors.RESET}\n")
        
        # Rdzeń
        self.aii = aii_instance
        self.logger = logger
        
        # Kompozytor
        print("[1/4] Inicjalizacja SoulComposer...")
        self.composer = SoulComposerV8(self.aii, logger)
        
        # Sieci neuronowe (opcjonalne)
        print("[2/4] Inicjalizacja Neural Networks...")
        if NN_AVAILABLE:
            self.nn = SoulComposerTinyNN()
        else:
            self.nn = None
            print(f"  {Colors.YELLOW}⚠ Tryb klasyczny (bez NN){Colors.RESET}")
        
        # Generator menuetów (opcjonalny)
        print("[3/4] Inicjalizacja Menuet Generator...")
        if MENUET_AVAILABLE and self.nn:
            self.menuet_gen = MenuetGeneratorEnhanced(self.composer, self.nn)
        else:
            self.menuet_gen = None
            if not MENUET_AVAILABLE:
                print(f"  {Colors.YELLOW}⚠ MenuetGenerator niedostępny{Colors.RESET}")
        
        # Ewaluator
        print("[4/4] Inicjalizacja Evaluator...")
        self.evaluator = CompositionEvaluator()
        
        print(f"\n{Colors.GREEN}✓ System gotowy!{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")
    
    def compose_menuet(self, key='C', minor=False, use_nn=True) -> dict:
        """
        Komponuje menuet z automatyczną oceną RL.
        
        Args:
            key: Tonacja (C, D, E, F, G, A, B)
            minor: Czy molowy
            use_nn: Czy używać wariacji NN
            
        Returns:
            dict: Pełny rezultat z oceną RL
        """
        if not self.menuet_gen:
            print(f"{Colors.RED}[ERROR] Menuet Generator niedostępny{Colors.RESET}")
            return {'error': 'MenuetGenerator not available'}
        
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"KOMPONOWANIE MENUETU ({key} {'moll' if minor else 'dur'})")
        print(f"{'='*70}{Colors.RESET}\n")
        
        # Pobierz stan emocjonalny (kompatybilność z różnymi wersjami aii.py)
        if hasattr(self.aii, 'get_emotions'):
            metrics = self.aii.get_emotions()
        else:
            # Fallback - bezpośredni dostęp
            metrics = {}
            for i, axis in enumerate(self.aii.AXES_ORDER):
                metrics[axis] = float(self.aii.context_vector[i])
        
        print(f"[EMOCJE] Dominanta: {self._get_dominant_emotion(metrics)}")
        
        # Komponuj
        composition = self.menuet_gen.generate_full_menuet(
            use_nn_variations=use_nn,
            key=key,
            minor=minor
        )
        
        # === MECHANIZM RL: OCENA ===
        print(f"\n{Colors.MAGENTA}[RL] Ocena kompozycji...{Colors.RESET}")
        evaluation = self.evaluator.evaluate_composition(
            composition,
            metrics,
            composition_type='menuet'
        )
        
        reward = evaluation['reward']
        feedback = evaluation['feedback']
        
        print(f"{Colors.MAGENTA}[RL] Reward: {reward:.3f}{Colors.RESET}")
        print(f"{Colors.MAGENTA}[RL] {feedback}{Colors.RESET}")
        
        # === ZAPISZ DO D_MAP AII ===
        memory_id = f"Menuet_{key}{'m' if minor else ''}_{int(time.time())}"
        
        memory_entry = {
            "tresc": f"Menuet {key} {'moll' if minor else 'dur'} (reward: {reward:.3f})",
            "wektor_C_Def": self.aii.context_vector.tolist(),
            "_type": "@MUSIC",
            "weight": reward,  # Reward jako waga!
            "time": time.time(),
            "metadata": {
                "genre": "menuet",
                "key": key,
                "minor": minor,
                "use_nn": use_nn,
                "evaluation": evaluation
            }
        }
        
        self.aii.D_Map[memory_id] = memory_entry
        self.aii.last_winner_id = memory_id
        
        # Zapisz stan AII
        self.aii.save()
        
        print(f"{Colors.GREEN}[RL] Zapisano do D_Map: {memory_id}{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")
        
        # Zwróć kompletny rezultat
        return {
            'composition': composition,
            'evaluation': evaluation,
            'memory_id': memory_id,
            'metrics': metrics
        }
    
    def compose_freestyle(self, genre='generic', bars=8, use_nn=True) -> dict:
        """
        Komponuje utwór freestyle z oceną RL.
        
        Args:
            genre: Gatunek ('generic', 'rock', 'ambient', etc.)
            bars: Liczba taktów
            use_nn: Czy używać NN
        
        Returns:
            dict: Kompletny rezultat z oceną RL
        """
        print(f"\n{Colors.CYAN}{'='*70}")
        print(f"KOMPONOWANIE FREESTYLE ({genre.upper()})")
        print(f"{'='*70}{Colors.RESET}\n")
        
        # Pobierz emocje (kompatybilność z różnymi wersjami aii.py)
        if hasattr(self.aii, 'get_emotions'):
            metrics = self.aii.get_emotions()
        else:
            # Fallback - bezpośredni dostęp
            metrics = {}
            for i, axis in enumerate(self.aii.AXES_ORDER):
                metrics[axis] = float(self.aii.context_vector[i])
        print(f"[EMOCJE] Dominanta: {self._get_dominant_emotion(metrics)}")
        
        # Komponuj (używa istniejącej metody z SoulComposerV8)
        paths = self.composer.compose_new_work(genre)
        
        # Dla freestyle możemy tylko ocenić metryki (brak dostępu do danych)
        # W pełnej wersji: parsuj MIDI i oceń
        
        # Uproszczona ocena na podstawie emocji
        pseudo_reward = self._estimate_reward_from_metrics(metrics, genre)
        
        evaluation = {
            'timestamp': datetime.now().isoformat(),
            'type': 'freestyle',
            'reward': pseudo_reward,
            'scores': {'estimated': pseudo_reward},
            'feedback': f"Utwór {genre} wygenerowany (szacowany reward: {pseudo_reward:.3f})"
        }
        
        print(f"\n{Colors.MAGENTA}[RL] Szacowany reward: {pseudo_reward:.3f}{Colors.RESET}")
        
        # Zapisz do D_Map
        memory_id = f"Freestyle_{genre}_{int(time.time())}"
        
        memory_entry = {
            "tresc": f"Freestyle {genre} (reward: {pseudo_reward:.3f})",
            "wektor_C_Def": self.aii.context_vector.tolist(),
            "_type": "@MUSIC",
            "weight": pseudo_reward,
            "time": time.time(),
            "metadata": {
                "genre": genre,
                "paths": paths,
                "evaluation": evaluation
            }
        }
        
        self.aii.D_Map[memory_id] = memory_entry
        self.aii.last_winner_id = memory_id
        self.aii.save()
        
        print(f"{Colors.GREEN}[RL] Zapisano do D_Map: {memory_id}{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")
        
        return {
            'paths': paths,
            'evaluation': evaluation,
            'memory_id': memory_id,
            'metrics': metrics
        }
    
    def _get_dominant_emotion(self, metrics: dict) -> str:
        """Zwraca dominującą emocję."""
        dominant = max(metrics.items(), key=lambda x: x[1])
        return f"{dominant[0].upper()} ({dominant[1]:.2f})"
    
    def _estimate_reward_from_metrics(self, metrics: dict, genre: str) -> float:
        """Szacuje reward na podstawie metryk (bez parsowania MIDI)."""
        # Bazowy reward
        reward = 0.5
        
        # Bonus za wysoką logikę (struktura)
        if metrics.get('logika', 0) > 0.7:
            reward += 0.1
        
        # Bonus za kreatywność
        if metrics.get('kreacja', 0) > 0.6:
            reward += 0.15
        
        # Bonus za balans (chaos nie za wysoki)
        if 0.3 <= metrics.get('chaos', 0) <= 0.7:
            reward += 0.1
        
        # Specyficzne dla gatunku
        if genre == 'ambient':
            if metrics.get('przestrzeń', 0) > 0.6:
                reward += 0.1
        elif genre == 'rock':
            if metrics.get('energia', 0) > 0.7:
                reward += 0.1
        
        return min(1.0, reward)
    
    def get_rl_statistics(self) -> dict:
        """Zwraca statystyki RL z D_Map."""
        music_entries = {k: v for k, v in self.aii.D_Map.items() 
                        if v.get('_type') == '@MUSIC'}
        
        if not music_entries:
            return {
                'count': 0,
                'avg_reward': 0,
                'max_reward': 0,
                'min_reward': 0
            }
        
        rewards = [e.get('weight', 0.5) for e in music_entries.values()]
        
        return {
            'count': len(music_entries),
            'avg_reward': np.mean(rewards),
            'max_reward': np.max(rewards),
            'min_reward': np.min(rewards),
            'recent_entries': list(music_entries.keys())[-5:]
        }


# ==================== PRZYKŁAD UŻYCIA ====================

if __name__ == "__main__":
    print(f"{Colors.CYAN}{'='*70}")
    print("PRODUCTION MUSIC SYSTEM - DEMO")
    print(f"{'='*70}{Colors.RESET}\n")
    
    # Inicjalizacja prawdziwego AII
    print("Inicjalizacja AII...")
    aii = AII(standalone_mode=False)
    
    # Stwórz system
    music_system = ProductionMusicSystem(aii)
    
    # === TEST 1: Menuet ===
    print("\n--- TEST 1: Menuet z oceną RL ---")
    result1 = music_system.compose_menuet(key='G', minor=False, use_nn=True)
    
    # === TEST 2: Freestyle ===
    print("\n--- TEST 2: Freestyle ---")
    result2 = music_system.compose_freestyle(genre='ambient', use_nn=True)
    
    # === Statystyki RL ===
    print("\n--- Statystyki RL ---")
    stats = music_system.get_rl_statistics()
    print(f"Kompozycji w pamięci: {stats['count']}")
    print(f"Średni reward: {stats['avg_reward']:.3f}")
    print(f"Najlepszy reward: {stats['max_reward']:.3f}")
    
    print(f"\n{Colors.GREEN}✓ Demo zakończone!{Colors.RESET}")