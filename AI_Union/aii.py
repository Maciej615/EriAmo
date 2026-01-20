# -*- coding: utf-8 -*-
"""
aii.py v6.0.3-Hotfix - EriAmo Language Core + Full Union Compatibility

ZMIANY v6.0.3:
- HOTFIX: Naprawiono KeyError: 'neutralna' w _sync_kurz_with_lexicon (ignorowanie nieobsługiwanych osi).

ARCHITEKTURA:
- 8 emocji Plutchika (ephemeral)
- Komunikacja z 9 osiami ontologicznymi (persistent)
- Dwukierunkowy przepływ: Emocje → Ontologia → Emocje
"""

import sys
import os
import time
import threading
import re
import numpy as np
import json
import random

# Importy podstawowe
try:
    from config import Colors, Config
except ImportError:
    class Colors:
        CYAN = '\033[96m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        RED = '\033[91m'; RESET = '\033[0m'; BLUE = '\033[94m'
        WHITE = '\033[97m'; MAGENTA = '\033[95m'; PINK = '\033[95m'; FAINT = '\033[2m'
    class Config:
        pass

try:
    from ui import FancyUI
except ImportError:
    FancyUI = None

try:
    from soul_io import SoulIO
except ImportError as e:
    print(f"❌ [AII] Błąd krytyczny: Brak SoulIO: {e}")
    raise

try:
    from lexicon import EvolvingLexicon
except ImportError as e:
    print(f"❌ [AII] Błąd krytyczny: Brak EvolvingLexicon: {e}")
    raise

try:
    from conscience import Conscience
except ImportError:
    Conscience = None

try:
    from agency import CreativeAgency
except ImportError:
    CreativeAgency = None

try:
    from fractal import FractalGenerator
except ImportError:
    FractalGenerator = None

try:
    from byt import BytS
except ImportError:
    BytS = None

try:
    from kurz import Kurz
    KURZ_AVAILABLE = True
except ImportError:
    Kurz = None
    KURZ_AVAILABLE = False

try:
    from explorer import WorldExplorer
    EXPLORER_AVAILABLE = True
except ImportError:
    WorldExplorer = None
    EXPLORER_AVAILABLE = False

try:
    from haiku_hybrid import HaikuGenerator
except ImportError:
    HaikuGenerator = None

# ==============================================================================
# VECTOR CORTEX
# ==============================================================================
class VectorCortex:
    def __init__(self, axes):
        self.axes = axes
        self.dims = len(axes)
        self.transition_matrix = np.ones((self.dims, self.dims)) * 0.1
        self.last_input_vector = np.zeros(self.dims)
    
    def predict(self, current_vector):
        if np.sum(current_vector) == 0:
            return np.zeros(self.dims)
        dominant_idx = np.argmax(current_vector)
        probs = self.transition_matrix[dominant_idx]
        prediction = probs / (np.sum(probs) + 1e-9)
        return prediction

    def learn(self, prev_vector, actual_vector, learning_rate=0.1):
        if np.sum(prev_vector) == 0 or np.sum(actual_vector) == 0:
            return 0.0
        prev_idx = np.argmax(prev_vector)
        actual_idx = np.argmax(actual_vector)
        self.transition_matrix[prev_idx][actual_idx] += learning_rate
        prediction = self.predict(prev_vector)
        surprise = np.linalg.norm(prediction - actual_vector)
        return surprise

    def save(self, path):
        try:
            with open(path + '.cortex', 'w') as f:
                json.dump(self.transition_matrix.tolist(), f)
        except: pass

    def load(self, path):
        try:
            if os.path.exists(path + '.cortex'):
                with open(path + '.cortex', 'r') as f:
                    self.transition_matrix = np.array(json.load(f))
        except: pass


# ==============================================================================
# GŁÓWNA KLASA AII
# ==============================================================================
class AII:
    VERSION = "6.0.3-Hotfix"
    AXES_ORDER = ['radość', 'smutek', 'strach', 'gniew', 'miłość', 'wstręt', 'zaskoczenie', 'akceptacja']
    
    # Parametry progowe
    EMOTION_THRESHOLD = 0.35
    UNKNOWN_WORD_THRESHOLD = 0.12
    SURPRISE_THRESHOLD = 0.8

    def __init__(self, standalone_mode=True):
        """
        Args:
            standalone_mode: True = tryb samodzielny, False = tryb Union
        """
        self.standalone_mode = standalone_mode
        
        if standalone_mode:
            self.ui = FancyUI() if FancyUI else None
            if self.ui: self.ui.print_logo()
        
        print(f"{Colors.CYAN}[SYSTEM] Inicjalizacja rdzenia {self.VERSION}...{Colors.RESET}")

        self.D_Map = {}
        self.status = "active"
        
        # Stan i Fizyka
        self.byt_stan = BytS(len(self.AXES_ORDER)) if BytS else None
        self.energy = 100.0
        self.emocja = "neutralna"
        
        # Wektor Kontekstu (główny stan emocjonalny)
        self.context_vector = np.zeros(8)
        
        # === UNION COMPATIBILITY ===
        # Pamięć ostatnich emocji dla get_emotions()
        self.last_emotion_dict = {axis: 0.0 for axis in self.AXES_ORDER}
        
        # Moduły podstawowe
        self.soul_io = SoulIO()
        self.lexicon = EvolvingLexicon()

        # === KURZ - WARSTWA ODRUCHOWA ===
        if KURZ_AVAILABLE:
            print(f"{Colors.CYAN}[KURZ] Inicjalizacja warstwy odruchowej...{Colors.RESET}")
            self.kurz = Kurz()
            self._sync_kurz_with_lexicon()
            print(f"{Colors.GREEN}[KURZ] ✓ Odruch gotowy.{Colors.RESET}")
        else:
            self.kurz = None

        # === EXPLORER - UCIELEŚNIENIE ===
        if EXPLORER_AVAILABLE:
            print(f"{Colors.CYAN}[EXPLORER] Inicjalizacja eksploracji...{Colors.RESET}")
            self.explorer = WorldExplorer(aii_instance=self)
            threading.Thread(target=self._background_explore, daemon=True).start()
        else:
            self.explorer = None
            
        if EXPLORER_AVAILABLE:
            self.last_world_update = time.time()
            self.world_update_interval = 30.0

        # === SEED LEKSYKONU ===
        self._init_basic_lexicon()

        # Wczytanie danych
        self.load()
        
        # Synchronizacja Kurz po załadowaniu
        if self.kurz:
            self._sync_kurz_with_lexicon()

        # Conscience i VectorCortex
        self.conscience = Conscience(self.AXES_ORDER) if Conscience else None
        self.cortex = VectorCortex(self.AXES_ORDER)
        
        if hasattr(self.soul_io, 'filepath'):
            self.cortex.load(self.soul_io.filepath)

        # Agency
        self.agency = CreativeAgency(self) if CreativeAgency else None
        self.haiku_gen = HaikuGenerator(self) if HaikuGenerator else None

    def _init_basic_lexicon(self):
        """Seed leksykonu - rozbudowany zestaw emocjonalnych słów"""
        basic_emotional_words = {
            'radość': [1.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.3, 0.6],
            'szczęście': [1.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.2, 0.7],
            'wesoły': [0.9, 0.0, 0.0, 0.0, 0.3, 0.0, 0.1, 0.5],
            'uśmiech': [0.9, 0.0, 0.0, 0.0, 0.3, 0.0, 0.2, 0.4],
            'śmiech': [0.9, 0.0, 0.0, 0.1, 0.2, 0.0, 0.4, 0.3],
            'zachwyt': [0.8, 0.0, 0.1, 0.0, 0.4, 0.0, 0.7, 0.5],
            'smutek': [0.0, 1.0, 0.2, 0.1, 0.0, 0.2, 0.1, 0.1],
            'żal': [0.0, 0.9, 0.1, 0.3, 0.0, 0.2, 0.0, 0.0],
            'samotność': [0.0, 0.9, 0.3, 0.1, 0.0, 0.3, 0.0, 0.0],
            'strach': [0.0, 0.2, 1.0, 0.2, 0.0, 0.2, 0.6, 0.0],
            'lęk': [0.0, 0.3, 0.9, 0.1, 0.0, 0.2, 0.4, 0.0],
            'gniew': [0.0, 0.2, 0.2, 1.0, 0.0, 0.4, 0.3, 0.0],
            'złość': [0.0, 0.2, 0.1, 0.9, 0.0, 0.3, 0.2, 0.0],
            'miłość': [0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.2, 0.7],
            'kocham': [0.6, 0.0, 0.0, 0.0, 1.0, 0.0, 0.1, 0.6],
            'wstręt': [0.0, 0.3, 0.3, 0.4, 0.0, 1.0, 0.3, 0.0],
            'zaskoczenie': [0.3, 0.1, 0.3, 0.0, 0.1, 0.0, 1.0, 0.2],
            'akceptacja': [0.3, 0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 1.0],
            'spokój': [0.3, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.9],
        }
        
        for word, vec in basic_emotional_words.items():
            self.lexicon.learn_from_correction(word, None, 0.0, vector_override=vec)

    # ==========================================================================
    # UNION COMPATIBILITY API
    # ==========================================================================
    
    def get_emotions(self):
        """
        UNION API: Eksport stanu emocjonalnego dla AxisMapper.
        """
        self.last_emotion_dict = {
            self.AXES_ORDER[i]: float(self.context_vector[i])
            for i in range(len(self.AXES_ORDER))
        }
        return self.last_emotion_dict
    
    def apply_ontological_feedback(self, ontological_modulation: np.ndarray, strength: float = 0.2):
        """
        UNION API: Przyjmuje feedback z ontologii muzycznej.
        """
        if ontological_modulation is None or len(ontological_modulation) != 8:
            return
        
        self.context_vector = (
            self.context_vector * (1.0 - strength) +
            ontological_modulation * strength
        )
        
        magnitude = np.linalg.norm(self.context_vector)
        if magnitude > 2.0:
            self.context_vector = (self.context_vector / magnitude) * 2.0
    
    def prompt(self, text: str):
        return self.interact(text)

    # ==========================================================================
    # KURZ & EXPLORER METHODS
    # ==========================================================================
    
    def _sync_kurz_with_lexicon(self):
        """
        Synchronizuje warstwę odruchową z leksikonem.
        FIX: Dostosowano do struktury danych lexicon.py v6.0 (słownik zamiast 'wektor').
        """
        # Sprawdzamy czy mamy dostęp do słownika słów (nazwa pola to 'words')
        lexicon_data = None
        if hasattr(self.lexicon, 'words'):
            lexicon_data = self.lexicon.words
        elif hasattr(self.lexicon, 'lexikon'): # Fallback dla starszych wersji
            lexicon_data = self.lexicon.lexikon
            
        if not self.kurz or not lexicon_data:
            return
            
        # Czyścimy stare triggery
        for sector in self.kurz.TRIGGERS:
            self.kurz.TRIGGERS[sector] = []
        
        # Iterujemy po słowach
        for word, data in lexicon_data.items():
            # Obsługa nowego formatu (słownik: {'radość': 0.8})
            if isinstance(data, dict) and 'wektor' not in data:
                if not data: continue
                # Znajdź najsilniejszą emocję
                best_sector = max(data, key=data.get)
                
                # --- FIX v6.0.3: Omijanie kluczy, których Kurz nie obsługuje (np. neutralna) ---
                if best_sector not in self.kurz.TRIGGERS:
                    continue
                # ----------------------------------------------------------------------------

                max_val = data[best_sector]
                
                # Próg odruchu - tylko silne skojarzenia (>0.4) trafiają do Kurzu
                if max_val > 0.4:
                    self.kurz.TRIGGERS[best_sector].append(word.lower())

            # Obsługa starego formatu (dla kompatybilności)
            elif 'wektor' in data:
                vec = np.array(data['wektor'])
                if np.max(vec) > 0.4:
                    dominant_idx = np.argmax(vec)
                    sector = self.AXES_ORDER[dominant_idx]
                    # Zabezpieczenie dla starego formatu
                    if sector in self.kurz.TRIGGERS:
                        self.kurz.TRIGGERS[sector].append(word.lower())
        
        # Kompilacja regexów w Kurzu
        self.kurz._recompile_patterns()

    def _background_explore(self):
        """Mapowanie sprzętu w tle."""
        try:
            discoveries = self.explorer.explore_safe_zones()
            if discoveries:
                print(f"{Colors.GREEN}[EXPLORER] ✓ Zmapowano {len(discoveries)} zakończeń.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[EXPLORER] ⚠️ Błąd: {e}{Colors.RESET}")

    def _update_from_world(self):
        """Aktualizuje stan na podstawie sensorów."""
        if not self.explorer:
            return
            
        try:
            readings = self.explorer.get_live_readings()
            
            temps = [v for k, v in readings.items() if 'temp' in k.lower()]
            if temps:
                avg_temp = sum(temps) / len(temps)
                
                if avg_temp > 75.0:
                    stress_vec = np.zeros(8)
                    stress_vec[self.AXES_ORDER.index('strach')] = 0.3
                    stress_vec[self.AXES_ORDER.index('gniew')] = 0.2
                    self.context_vector = (self.context_vector * 0.9) + (stress_vec * 0.1)
                    
                elif avg_temp < 35.0:
                    calm_vec = np.zeros(8)
                    calm_vec[self.AXES_ORDER.index('akceptacja')] = 0.2
                    self.context_vector = (self.context_vector * 0.95) + (calm_vec * 0.05)
            
            fans = [v for k, v in readings.items() if 'fan' in k.lower()]
            if fans:
                avg_fan = sum(fans) / len(fans)
                if avg_fan > 3000:
                    stress_vec = np.zeros(8)
                    stress_vec[self.AXES_ORDER.index('strach')] = 0.1
                    self.context_vector = (self.context_vector * 0.95) + (stress_vec * 0.05)
        except:
            pass

    # ==========================================================================
    # CORE INTERACTION
    # ==========================================================================

    def load(self):
        """Wczytanie danych z SoulIO"""
        try:
            loaded_data = self.soul_io.load_stream()
            if loaded_data:
                self.D_Map = loaded_data
                print(f"{Colors.GREEN}[AII] Załadowano {len(self.D_Map)} wpisów.{Colors.RESET}")
            
            if hasattr(self.lexicon, 'load_from_soul'):
                loaded_count = self.lexicon.load_from_soul()
                print(f"{Colors.GREEN}[AII] Leksykon: {loaded_count} słów.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}[AII] Brak zapisanego stanu: {e}{Colors.RESET}")

    def _handle_command(self, full_cmd):
        """Obsługa komend systemowych (z zachowaniem Case Sensitivity argumentów)"""
        parts = full_cmd.strip().split(maxsplit=1)
        if not parts:
            return "Pusta komenda."
            
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == '/world':
            if not self.explorer:
                return "Explorer niedostępny."
            readings = self.explorer.get_live_readings()
            if not readings:
                return "Brak odczytów sensorów."
            output = [f"{Colors.CYAN}=== ŚWIAT FIZYCZNY ==={Colors.RESET}"]
            for sensor, value in readings.items():
                if 'temp' in sensor:
                    output.append(f"  🌡️  {sensor}: {value:.1f}°C")
                elif 'fan' in sensor:
                    output.append(f"  🌀 {sensor}: {value:.0f} RPM")
                else:
                    output.append(f"  📊 {sensor}: {value}")
            return "\n".join(output)
        
        elif command == '/sync-kurz':
            if not self.kurz:
                return "Kurz niedostępny."
            self._sync_kurz_with_lexicon()
            trigger_count = sum(len(v) for v in self.kurz.TRIGGERS.values())
            return f"Zsynchronizowano Kurz: {trigger_count} triggerów."
        
        elif command == '/emotions':
            emotions = self.get_emotions()
            output = [f"{Colors.CYAN}=== STAN EMOCJONALNY ==={Colors.RESET}"]
            for emotion, value in emotions.items():
                if value > 0.1:
                    bar = '█' * int(value * 20)
                    output.append(f"  {emotion:12s} {bar} {value:.3f}")
            return "\n".join(output)
        
        elif command == '/save':
            self.save()
            return "Stan zapisany."
        
        elif command == '/status':
            status = self.get_soul_status()
            return (f"Wspomnienia: {status['memories']}, "
                   f"Energia: {status['energy']:.1f}, "
                   f"Sektor: {status['dominant_sector']} ({status['dominant_value']:.2f})")
        
        elif command == '/teach':
            teach_parts = args.split(maxsplit=1)
            if len(teach_parts) < 2:
                return "Użycie: /teach <słowo> <kategoria>"
            word, category = teach_parts[0], teach_parts[1]
            
            if category.lower() not in self.AXES_ORDER:
                return f"Kategoria: {', '.join(self.AXES_ORDER)}"
            
            self.lexicon.learn_from_correction(word, category.lower(), 0.5)
            if self.kurz:
                self._sync_kurz_with_lexicon()
            return f"Nauczono: '{word}' → {category.lower()}"
        
        elif command == '/read':
            if not args:
                return "Użycie: /read <ścieżka>"
            filepath = args.strip()
            result = self.deep_read(filepath)
            return result
        
        elif command == '/haiku':
            if not self.haiku_gen:
                return "Moduł haiku niedostępny."
            haiku = self.haiku_gen.generate_haiku(self.context_vector)
            return f"\n{Colors.MAGENTA}{haiku}{Colors.RESET}"
        
        else:
            return f"Nieznana komenda: {command}"

    def deep_read(self, filename):
        """Deep reading pliku z uczeniem emocjonalnym"""
        if not os.path.exists(filename):
            return f"{Colors.RED}Plik nie istnieje: {filename}{Colors.RESET}"
        
        start_time = time.time()
        print(f"{Colors.CYAN}[DeepRead] {filename}{Colors.RESET}")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return f"{Colors.RED}Błąd odczytu: {e}{Colors.RESET}"
        
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        total_sentences = len(sentences)
        
        learned_transitions = 0
        memories_created = 0
        prev_vector = np.zeros(8)
        
        for i, clean_sent in enumerate(sentences):
            if not clean_sent: continue
            
            current_vector, dominant_sector, unknown_words = self.lexicon.analyze_text(clean_sent)
            
            if np.sum(current_vector) > 0:
                surprise = self.cortex.learn(prev_vector, current_vector)
                if surprise > 0.1:
                    learned_transitions += 1
            
            emotion_strength = float(np.linalg.norm(current_vector))
            if unknown_words and emotion_strength > self.UNKNOWN_WORD_THRESHOLD:
                confidence = emotion_strength
                self.lexicon.learn_from_context(unknown_words, current_vector, confidence=0.25)
            
            if emotion_strength > self.EMOTION_THRESHOLD or (len(clean_sent) > 30 and unknown_words):
                tags = [w.strip(".,!?\"')") for w in clean_sent.split() if len(w) > 5][:6]
                mem_id = f"Mem_{int(time.time()*100000) + i}"
                memory_entry = {
                    "_type": "@MEMORY",
                    "id": mem_id,
                    "tresc": clean_sent,
                    "tags": tags + ["wspomnienie", os.path.basename(filename)],
                    "wektor_C_Def": current_vector.tolist(),
                    "created_at": time.time(),
                    "source": "DeepRead"
                }
                self.D_Map[mem_id] = memory_entry
                memories_created += 1
            
            prev_vector = (prev_vector * 0.5) + (current_vector * 0.5)
            
            if i % 50 == 0:
                sys.stdout.write(f"\r[DeepRead] {i}/{total_sentences} (wspomnień: {memories_created})...")
                sys.stdout.flush()
        
        print()
        
        try:
            self.save()
            if self.kurz:
                self._sync_kurz_with_lexicon()
        except Exception as e:
            print(f"{Colors.RED}⚠️ Błąd zapisu: {e}{Colors.RESET}")
        
        duration = time.time() - start_time
        return (f"\n{Colors.GREEN}✓ Zakończono w {duration:.2f}s.\n"
                f"   🧠 {learned_transitions} połączeń.\n"
                f"   💾 {memories_created} wspomnień.{Colors.RESET}")

    def save(self):
        """Zapis"""
        try:
            self.soul_io.save_stream(self.D_Map)
            if hasattr(self.lexicon, 'save_to_soul'):
                self.lexicon.save_to_soul()
            self.cortex.save(self.soul_io.filepath if hasattr(self.soul_io, 'filepath') else 'eriamo')
            print(f"{Colors.GREEN}[AII] Zapisano.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[AII] Błąd zapisu: {e}{Colors.RESET}")
            raise

    def get_soul_status(self):
        dom_sector = "neutralna"
        dom_val = 0.0
        if isinstance(self.context_vector, np.ndarray) and self.context_vector.size > 0:
            idx = np.argmax(self.context_vector)
            dom_sector = self.AXES_ORDER[idx]
            dom_val = float(self.context_vector[idx])
        
        return {
            'memories': len(self.D_Map),
            'energy': self.energy,
            'emotion': self.emocja,
            'dominant_sector': dom_sector,
            'dominant_value': dom_val,
        }

    def interact(self, user_input):
        """Główna metoda interakcji"""
        if user_input.strip().startswith('/'):
            # Przekazujemy oryginalny input (nie lowercase) do obsługi komend
            response = self._handle_command(user_input)
            if self.standalone_mode:
                print(f" [System] {response}")
            return response
        
        # Cykliczny update ze świata
        if self.explorer:
            current_time = time.time()
            if current_time - self.last_world_update > self.world_update_interval:
                self._update_from_world()
                self.last_world_update = current_time
        
        # KURZ - odruch
        if self.kurz:
            intent_sector, intent_strength = self.kurz.quick_scan(user_input)
            if intent_sector and intent_strength > 0:
                intent_idx = self.AXES_ORDER.index(intent_sector)
                reflex_boost = np.zeros(8)
                reflex_boost[intent_idx] = 0.3 * intent_strength
                self.context_vector = (self.context_vector * 0.7) + (reflex_boost * 0.3)
        
        # Predykcja
        predicted_vector = self.cortex.predict(self.context_vector)
        
        # Analiza leksykalna
        vec_F, dominant_sector, unknown_words = self.lexicon.analyze_text(user_input)
        
        # Uczenie
        surprise_level = self.cortex.learn(self.context_vector, vec_F)
        
        # Zaskoczenie
        if surprise_level > self.SURPRISE_THRESHOLD:
            zaskoczenie_idx = self.AXES_ORDER.index('zaskoczenie')
            vec_F[zaskoczenie_idx] += 0.5
        
        # Uczenie nieznanych słów
        if unknown_words and np.max(vec_F) > 0.15:
            confidence = np.max(vec_F)
            self.lexicon.learn_from_context(unknown_words, vec_F, confidence)
            if self.kurz:
                self._sync_kurz_with_lexicon()
        
        # Aktualizacja kontekstu
        self.context_vector = (self.context_vector + vec_F) / 2.0
        
        # Generowanie odpowiedzi
        response = self._resonance_engine(vec_F, user_input, threshold=0.05)
        
        # Wyświetlenie (tylko w standalone)
        if self.standalone_mode:
            if self.ui:
                self.ui.print_animated_text(response, Colors.WHITE, 0.02)
            else:
                print(f" [EriAmo] {response}")
        
        return response

    def _normalize_polish(self, text):
        polish_map = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
            'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
            'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        for pl, ascii_char in polish_map.items():
            text = text.replace(pl, ascii_char)
        return text

    def _resonance_engine(self, vec, text, threshold=0.05):
        """Silnik rezonansu pamięciowego"""
        text_normalized = self._normalize_polish(text.lower())
        text_words = set(re.findall(r'\w+', text_normalized))
        
        best_score = -1.0
        best_match = None
        is_memory = False
        
        current_mood_strength = np.linalg.norm(self.context_vector)
        
        for entry in self.D_Map.values():
            if entry.get('_type') == '@META': 
                continue
            
            score = 0.0
            content = entry.get('tresc', '').lower()
            content_norm = self._normalize_polish(content)
            tags = [self._normalize_polish(str(t).lower()) for t in entry.get('tags', [])]
            
            content_words = set(re.findall(r'\w+', content_norm))
            overlap = len(text_words & (content_words | set(tags)))
            score += overlap * 1.2
            
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(8)))
            if np.linalg.norm(mem_vec) > 0.01:
                similarity = np.dot(vec, mem_vec) / (np.linalg.norm(vec) + 1e-8)
                score += similarity * 1.5
            
            if entry.get('_type') == '@MEMORY' and current_mood_strength > 0.4:
                score += 2.5
            
            if ("co to" in text_normalized or "czym jest" in text_normalized) and entry.get('id', '').startswith('Def_'):
                score += 3.0
            
            if score > best_score and score > threshold:
                best_score = score
                best_match = entry
                is_memory = entry.get('_type') == '@MEMORY'
        
        if best_match:
            content = best_match['tresc']
            if is_memory:
                prefixes = [
                    "Przypomina mi się...",
                    "Mam takie wspomnienie:",
                    "To jak fragment...",
                    "Kojarzy mi się:",
                ]
                return f"{random.choice(prefixes)}\n\n\"{content}\""
            else:
                return content
        
        return "Nie rozumiem jeszcze tego pojęcia, ale uczę się."

    def live(self):
        """Główna pętla (tylko standalone)"""
        if not self.standalone_mode:
            print(f"{Colors.RED}[AII] live() dostępne tylko w trybie standalone.{Colors.RESET}")
            return
            
        print(f"{Colors.BLUE}Komendy: /teach, /save, /status, /read, /emotions, /world, /sync-kurz{Colors.RESET}")
        while True:
            try:
                cmd = input(f"{Colors.BLUE}Ty > {Colors.RESET}")
                if cmd.lower() in ["exit", "quit"]: 
                    break
                self.interact(cmd)
            except KeyboardInterrupt:
                print("\nZamykanie...")
                self.save()
                break

if __name__ == "__main__":
    app = AII(standalone_mode=True)
    app.live()