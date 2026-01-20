# -*- coding: utf-8 -*-
"""
union_core.py v1.7.1-DictFix
EriAmo Union - Complete AGI System
Lokalizacja: /eriamo-union/src/union/union_core.py

ZMIANY v1.7.1:
- FIX: Obsługa słownika emocji (AII v6.0+) w process_input (naprawa KeyError: 0).
- FIX: Zwiększona odporność na typy danych (list vs dict) przy Boostach emocjonalnych.
"""

import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
music_path = os.path.join(current_dir, '..', 'music')
lang_path = os.path.join(current_dir, '..', 'language')

if music_path not in sys.path:
    sys.path.append(music_path)
if lang_path not in sys.path:
    sys.path.append(lang_path)

try:
    from axis_mapper import AxisMapper
    from unified_memory import UnifiedMemory
    from multimodal_agency import MultimodalAgency
except ImportError as e:
    print(f"❌ BŁĄD UNII: {e}")
    sys.exit(1)

try:
    from amocore import EriAmoCore, SoulStateLogger, get_music_memory
    from soul_composer import SoulComposerV59
    MUSIC_AVAILABLE = True
    print("[SYSTEM] 🎵 Moduł Muzyczny widoczny (SoulComposer v5.9).")
except ImportError as e:
    print(f"[SYSTEM] ⚠️ Moduł muzyczny niedostępny: {e}")
    MUSIC_AVAILABLE = False

try:
    from aii import AII
    print("[SYSTEM] ✅ Rdzeń językowy (AII) aktywny.")
except ImportError:
    print("[SYSTEM] ⚠️ Brak aii.py. Tryb symulacji języka.")
    AII = None

class EriAmoUnion:
    
    VERSION = "1.7.1-DictFix"
    
    def __init__(self, verbose: bool = True, use_unified_memory: bool = True):
        self.verbose = verbose
        if self.verbose:
            print(f"🌌 Initializing EriAmo Union v{self.VERSION}...")
            
        if AII: self.language = AII() 
        else: self.language = self._mock_language_system()
            
        self.music_core = None
        self.music_logger = None
        self.music_composer = None

        if MUSIC_AVAILABLE:
            try:
                self.music_core = EriAmoCore()
                self.music_logger = SoulStateLogger()
                self.music_composer = SoulComposerV59(self.music_core, self.music_logger)
                if self.verbose: print("[UNION] 🔌 Muzyka podłączona.")
            except Exception as e:
                print(f"[ERROR] Błąd inicjalizacji muzyki: {e}")
                self.music = self._mock_music_system()
        else:
            self.music = self._mock_music_system()

        self.mapper = AxisMapper(verbose=self.verbose)
        
        if use_unified_memory:
            self.unified_memory = UnifiedMemory(verbose=self.verbose)
        
        self.agency = MultimodalAgency(self, verbose=self.verbose)
        
        if self.verbose:
            print("✅ SYSTEM READY. Czekam na sygnał.\n")

    def start(self):
        print("[UNION] Awakening...")
        self.agency.start()

    def stop(self):
        print("\n[UNION] Inicjowanie procedury uśpienia...")
        if hasattr(self, 'agency'):
            self.agency.stop()
        
        if MUSIC_AVAILABLE:
            try:
                get_music_memory().shutdown()
            except: pass

        time.sleep(1.0)
        self._save_all_systems()

    def process_input(self, text: str):
        print(f"\n[USER] >> {text}")
        
        # 1. AKTYWACJA SKUPIENIA (Brak nudy podczas rozmowy!)
        if hasattr(self.agency, 'set_focus'):
            self.agency.set_focus(True)

        try:
            # Język
            emotions = [0.1] * 8
            if self.language:
                if hasattr(self.language, 'interact'): self.language.interact(text)
                elif hasattr(self.language, 'prompt'): self.language.prompt(text)
                
                # Pobranie emocji (może być dict lub list)
                if hasattr(self.language, 'get_emotions'): 
                    emotions = self.language.get_emotions()

            # Percepcja (Analiza sentymentu i Boost)
            emo_boost = self._analyze_emotional_intensity(text)
            if emo_boost > 0.0:
                print(f"[UNION] ❤️ Wykryto emocje (Boost: +{emo_boost:.2f})")
                
                # --- FIX v1.7.1: Obsługa obu formatów danych (Dict i List) ---
                if isinstance(emotions, dict):
                    # Wzmacniamy 'radość' i 'akceptacja' (odpowiedniki indeksów 0 i 7)
                    if 'radość' in emotions:
                        emotions['radość'] = min(1.0, emotions.get('radość', 0.0) + emo_boost)
                    if 'akceptacja' in emotions:
                        emotions['akceptacja'] = min(1.0, emotions.get('akceptacja', 0.0) + emo_boost)
                
                elif isinstance(emotions, list) and len(emotions) >= 8:
                    # Klasyczna obsługa indeksowa
                    emotions[0] = min(1.0, emotions[0] + emo_boost)
                    emotions[7] = min(1.0, emotions[7] + emo_boost)
                # -----------------------------------------------------------

            # Złożoność
            complexity_stimulus = self._analyze_text_complexity(text)
            
            # Agencja
            if hasattr(self.agency, 'bridge'):
                current_state = self.agency.bridge.get_state()
                current_music = current_state.get('music_state', {})
                new_complexity = min(1.0, max(0.0, current_music.get('complexity', 0.5) + complexity_stimulus))
                
                self.agency.bridge.update_input(
                    emotions=self.agency._force_dict(emotions, self.agency.LANG_AXES),
                    music_state={**current_music, 'complexity': new_complexity}
                )
                
        finally:
            # 2. DEZAKTYWACJA SKUPIENIA (Powrót do swobodnych myśli)
            if hasattr(self.agency, 'set_focus'):
                self.agency.set_focus(False)

    def _analyze_emotional_intensity(self, text: str) -> float:
        text = text.lower()
        boost = 0.0
        triggers = [
            'piękna', 'piękno', 'cudown', 'zachwyt', 'doskonał', 
            'kocham', 'wspaniał', 'architektura', 'geniusz',
            'ładny', 'super', 'lubię', 'fajny', 'tak', 'dzięki',
            'dobro', 'miłość', 'czuję', 'spokój', 'nadzieja'
        ]
        for t in triggers:
            if t in text: boost += 0.4
        return min(0.9, boost)

    def _analyze_text_complexity(self, text: str) -> float:
        text = text.lower()
        score = 0.0
        logical = ['oblicz', 'analiza', 'system', 'dlaczego', 'kod', 'matematyka', 'ile', 'definicja', 'struktura', 'logika']
        chill = ['luz', 'spokój', 'reggae', 'wolno', 'cisza', 'nic', 'hej', 'buja']
        if any(w in text for w in logical): score += 0.4
        if any(w in text for w in chill): score -= 0.4
        if len(text.split()) > 10: score += 0.2
        return score

    def _mock_language_system(self):
        class MockLang:
            def get_emotions(self): return [0.1]*8
            class Lexicon:
                def analyze_text(self, t): return [0.5]*8, None, []
                def save(self): pass
            lexicon = Lexicon()
            def prompt(self, t): pass
        return MockLang()

    def _mock_music_system(self):
        class MockMusic:
            class Composer:
                def compose_and_play(self, p): pass
            composer = Composer()
        return MockMusic()

    def _save_all_systems(self):
        print(f"[SYSTEM] 💾 ZAPISYWANIE STANU BYTU...")
        if hasattr(self, 'unified_memory'):
            try: self.unified_memory.save_to_file("data/unified.soul")
            except: pass
        if self.language and AII:
            try:
                if hasattr(self.language, 'lexicon'): self.language.lexicon.save()
                if hasattr(self.language, 'save'): self.language.save()
            except: pass
        if self.music_core:
            print("[SYSTEM] Zapisywanie rdzenia muzycznego...")
            try: self.music_core.create_memory_dump()
            except: pass
        print("[SYSTEM] Zapis zakończony.")