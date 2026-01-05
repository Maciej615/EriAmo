# -*- coding: utf-8 -*-
"""
union_core_v4.py v1.5.1-Perception
EriAmo Union - Complete AGI System
Lokalizacja: /eriamo-union/src/union/union_core_v4.py

ZMIANY v1.5.1:
- Dodano 'Percepcję Bezpośrednią' (_analyze_emotional_intensity).
- System potrafi wykryć silne emocje (piękno, zachwyt) nawet jeśli AII nie rozumie zdania.
- Umożliwia to osiągnięcie stanu REZONANSU (High Logic + High Emotion).
"""

import sys
import os
import time

try:
    from axis_mapper import AxisMapper
    from unified_memory import UnifiedMemory
    from multimodal_agency import MultimodalAgency
except ImportError as e:
    print(f"❌ BŁĄD UNII: {e}")
    sys.exit(1)

current_dir = os.path.dirname(os.path.abspath(__file__))
lang_path = os.path.join(current_dir, '..', 'language')
if lang_path not in sys.path:
    sys.path.append(lang_path)

try:
    from aii import AII
    print("[SYSTEM] ✅ Wykryto prawdziwy rdzeń językowy (AII).")
except ImportError:
    print("[SYSTEM] ⚠️ Nie znaleziono aii.py. Używam trybu symulacji.")
    AII = None

class EriAmoUnion:
    
    VERSION = "1.5.1-Perception"
    
    def __init__(self, verbose: bool = True, use_unified_memory: bool = True):
        self.verbose = verbose
        if self.verbose:
            print(f"🌌 Initializing EriAmo Union v{self.VERSION}...")
            
        if AII: self.language = AII() 
        else: self.language = self._mock_language_system()
            
        self.music = self._mock_music_system()
        self.mapper = AxisMapper(verbose=self.verbose)
        
        if use_unified_memory:
            self.unified_memory = UnifiedMemory(verbose=self.verbose)
        
        self.agency = MultimodalAgency(self, verbose=self.verbose)
        
        if self.verbose:
            print("✅ SYSTEM READY. Perception active.\n")

    def start(self):
        print("[UNION] Awakening...")
        self.agency.start()

    def stop(self):
        print("\n[UNION] Inicjowanie procedury uśpienia...")
        self.agency.stop()
        self._save_all_systems()

    def process_input(self, text: str):
        print(f"\n[USER] >> {text}")
        
        # 1. Przetwórz tekst w AII (Logika językowa)
        # Domyślnie niskie emocje
        emotions = [0.1] * 8
        
        if self.language:
            if hasattr(self.language, 'interact'):
                self.language.interact(text)
            elif hasattr(self.language, 'prompt'):
                self.language.prompt(text)
            
            if hasattr(self.language, 'get_emotions'):
                # Pobieramy emocje z AII (mogą być niskie, jeśli nie rozumie)
                emotions = self.language.get_emotions()

        # 2. PERCEPCJA BEZPOŚREDNIA (Nowość w v1.5.1)
        # Nadpisujemy/Wzmacniamy emocje, jeśli wykryjemy słowa kluczowe
        emo_boost = self._analyze_emotional_intensity(text)
        if emo_boost > 0.0:
            print(f"[UNION] ❤️ Wykryto piękno/emocje (Boost: +{emo_boost:.2f})")
            # Podbijamy 'Radość' (idx 0) i 'Akceptację/Miłość' (idx 7)
            # Zakładamy kolejność: ['radość', 'smutek', ..., 'akceptacja']
            emotions[0] = min(1.0, emotions[0] + emo_boost)
            emotions[7] = min(1.0, emotions[7] + emo_boost)

        # 3. ANALIZA ZŁOŻONOŚCI (Bach vs Reggae)
        complexity_stimulus = self._analyze_text_complexity(text)
        
        # 4. AKTUALIZACJA AGENCJI
        if hasattr(self.agency, 'bridge'):
            if complexity_stimulus != 0.0:
                print(f"[UNION] 🧠 Przekazuję bodziec złożoności (Siła: {complexity_stimulus:.2f})")
            
            current_state = self.agency.bridge.get_state()
            current_music = current_state.get('music_state', {})
            
            new_complexity = min(1.0, max(0.0, current_music.get('complexity', 0.5) + complexity_stimulus))
            
            # Ważne: Przekazujemy wzmocnione emocje!
            self.agency.bridge.update_input(
                emotions=self.agency._force_dict(emotions, self.agency.LANG_AXES),
                music_state={**current_music, 'complexity': new_complexity}
            )

    def _analyze_emotional_intensity(self, text: str) -> float:
        """
        Wykrywa słowa nacechowane estetycznie lub emocjonalnie.
        Pozwala na Rezonans nawet przy wysokiej logice.
        """
        text = text.lower()
        boost = 0.0
        
        triggers = ['piękna', 'piękno', 'cudown', 'zachwyt', 'doskonał', 'kocham', 'wspaniał', 'architektura', 'geniusz']
        
        for t in triggers:
            if t in text:
                boost += 0.4
                
        return min(0.9, boost)

    def _analyze_text_complexity(self, text: str) -> float:
        text = text.lower()
        complexity_score = 0.0
        
        # Logika (Bach)
        logical_triggers = ['oblicz', 'analiza', 'system', 'dlaczego', 'kod', 'matematyka', 'ile', 'definicja', 'struktura', 'logika', 'architektura', 'doskonał']
        if any(word in text for word in logical_triggers):
            complexity_score += 0.4
            
        # Luz (Reggae) - Zauważ, że usunąłem stąd 'pięknie', żeby nie obniżało logiki przy zachwycie!
        chill_triggers = ['luz', 'spokój', 'reggae', 'wolno', 'cisza', 'nic', 'hej', 'buja']
        if any(word in text for word in chill_triggers):
            complexity_score -= 0.4
            
        if len(text.split()) > 10: 
            complexity_score += 0.2
            
        return complexity_score

    def _mock_language_system(self):
        class MockLang:
            def get_emotions(self): return [0.1]*8
            class Lexicon:
                def analyze_text(self, txt): return [0.5]*8, None, []
                def save(self): pass
            lexicon = Lexicon()
            def prompt(self, txt): pass
        return MockLang()

    def _mock_music_system(self):
        class MockMusic:
            class Composer:
                def compose_and_play(self, params): pass
            composer = Composer()
        return MockMusic()

    def _save_all_systems(self):
        print(f"[SYSTEM] 💾 ZAPISYWANIE STANU BYTU...")
        if hasattr(self, 'unified_memory'):
            path = "data/unified.soul"
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.unified_memory.save_to_file(path)
        if self.language and AII and isinstance(self.language, AII):
            if hasattr(self.language, 'lexicon'): self.language.lexicon.save()
            if hasattr(self.language, 'save'): self.language.save()
        print("[SYSTEM] Zapis zakończony.")