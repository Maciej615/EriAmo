# -*- coding: utf-8 -*-
"""
aii.py v8.0.1-Hybrid-Fix - EriAmo Complete Consciousness
EriAmo Union - 15-Axis Architecture (Fixed Sync)

ARCHITEKTURA HYBRYDOWA:
1. SFERA BIOLOGICZNA (0-7): Emocje Plutchika (Relacje, Przetrwanie).
2. SFERA METAFIZYCZNA (8-14): Koncepty Abstrakcyjne (Wiedza, Czas, Byt).

Kurz (Reflex) automatycznie kieruje bodźce do odpowiedniej strefy.
"""

import sys
import os
import time
import threading
import re
import numpy as np
import json
import random

# Importy
try:
    from config import Colors, Config
except ImportError:
    class Colors:
        CYAN = '\033[96m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
        RED = '\033[91m'; RESET = '\033[0m'; BLUE = '\033[94m'
        WHITE = '\033[97m'; MAGENTA = '\033[95m'; FAINT = '\033[2m'
    class Config:
        pass

try:
    from soul_io import SoulIO
except ImportError:
    print("❌ Brak SoulIO - tryb ograniczony.")
    SoulIO = None

try:
    from lexicon import EvolvingLexicon
except ImportError:
    print("❌ Brak EvolvingLexicon.")
    EvolvingLexicon = None

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
    from haiku import HaikuGenerator
except ImportError:
    HaikuGenerator = None

# ==============================================================================
# CORTEX (Pamięć Nawyku - 15 Wymiarów)
# ==============================================================================
class VectorCortex:
    def __init__(self, axes):
        self.axes = axes
        self.dims = len(axes)
        self.transition_matrix = np.ones((self.dims, self.dims)) * 0.1
    
    def predict(self, current_vector):
        if np.sum(current_vector) == 0: return np.zeros(self.dims)
        idx = np.argmax(current_vector)
        probs = self.transition_matrix[idx]
        return probs / (np.sum(probs) + 1e-9)

    def learn(self, prev, actual, rate=0.1):
        if np.sum(prev) == 0 or np.sum(actual) == 0: return 0.0
        p_idx = np.argmax(prev)
        a_idx = np.argmax(actual)
        self.transition_matrix[p_idx][a_idx] += rate
        return np.linalg.norm(self.predict(prev) - actual)

    def save(self, path):
        try:
            with open(path + '.cortex', 'w') as f: json.dump(self.transition_matrix.tolist(), f)
        except: pass

    def load(self, path):
        try:
            if os.path.exists(path + '.cortex'):
                with open(path + '.cortex', 'r') as f: self.transition_matrix = np.array(json.load(f))
        except: pass

# ==============================================================================
# GŁÓWNA KLASA AII - 15 OSI
# ==============================================================================
class AII:
    VERSION = "8.0.1-Hybrid-Fix"
    
    # PEŁNE SPEKTRUM ŚWIADOMOŚCI (15 OSI)
    AXES_ORDER = [
        # --- SFERA BIOLOGICZNA (Plutchik) ---
        'radość', 'smutek', 'strach', 'gniew', 
        'miłość', 'wstręt', 'zaskoczenie', 'akceptacja',
        
        # --- SFERA METAFIZYCZNA (Union Knowledge) ---
        'logika',       # Dedukcja, Matematyka, Wynikanie
        'wiedza',       # Fakty, Internet, Nauka (Fizyka, Chemia)
        'czas',         # Trwanie, Chwila, Przeszłość/Przyszłość
        'kreacja',      # Twórczość, Sztuka, Nowość
        'byt',          # Istnienie, Życie, Obecność
        'przestrzeń',   # Miejsce, Geometria, Świat
        'chaos'         # Entropia, Niepewność, Szum
    ]
    
    def __init__(self, standalone_mode=True):
        self.standalone_mode = standalone_mode
        self.ui = None
        if standalone_mode:
            print(f"{Colors.CYAN}[SYSTEM] Inicjalizacja Hybrydowa (15 Osi)...{Colors.RESET}")

        self.D_Map = {}
        self.context_vector = np.zeros(len(self.AXES_ORDER))
        
        self.soul_io = SoulIO() if SoulIO else None
        self.lexicon = EvolvingLexicon() if EvolvingLexicon else None
        
        # Moduły
        self.kurz = Kurz() if KURZ_AVAILABLE else None
        self.explorer = WorldExplorer(self) if EXPLORER_AVAILABLE else None
        self.haiku_gen = HaikuGenerator(self) if HaikuGenerator else None

        if self.explorer:
            threading.Thread(target=self._bg_explore, daemon=True).start()
            self.last_world_update = time.time()

        # Wczytanie
        self.load()
        if self.kurz: self._sync_kurz_hybrid()
        
        self.cortex = VectorCortex(self.AXES_ORDER)
        if self.soul_io and hasattr(self.soul_io, 'filepath'): 
            self.cortex.load(self.soul_io.filepath)

    # --- API ---
    def get_emotions(self):
        """Zwraca pełny stan 15-wymiarowy"""
        return {self.AXES_ORDER[i]: float(self.context_vector[i]) for i in range(len(self.AXES_ORDER))}

    def introspect(self, context_type="thought"):
        if np.sum(self.context_vector) == 0: return "Stan neutralny."
        
        # Znajdź dominującą oś
        idx = np.argmax(self.context_vector)
        dom_axis = self.AXES_ORDER[idx]
        val = self.context_vector[idx]
        
        if idx < 8: zone = "Biologiczna"
        else: zone = "Metafizyczna"
        
        return f"Dominanta: {dom_axis.upper()} ({zone}, {val:.2f})"

    # --- HYBRID MEMORY & READING ---
    def _normalize_polish(self, text):
        return text.lower().strip()

    def deep_read(self, filename, category="general"):
        """
        Inteligentne czytanie mapujące treść na 15 osi.
        """
        if not os.path.exists(filename): 
            alternatives = [
                os.path.join("library", filename),
                os.path.join("AI_Union", filename),
                filename
            ]
            found = False
            for alt in alternatives:
                if os.path.exists(alt):
                    filename = alt
                    found = True
                    break
            if not found:
                return f"Błąd: Nie znaleziono pliku '{filename}'."
                
        try:
            with open(filename, 'r', encoding='utf-8') as f: content = f.read()
        except Exception as e: return f"Błąd odczytu: {e}"
        
        fname = os.path.basename(filename).lower()
        
        # Auto-kategoryzacja
        if any(x in fname for x in ["encyklopedia", "nauka", "wiedza"]): category = "FACT"
        elif any(x in fname for x in ["powieść", "pies", "studium", "dzien"]): category = "FICTION"
            
        sentences = re.split(r'[.!?]+', content)
        count = 0
        
        # Mapowanie słów kluczowych na osie metafizyczne
        keyword_map = {
            'wiedza': ['internet', 'nauka', 'fizyka', 'chemia', 'biologia', 'fakt', 'definicja'],
            'logika': ['dedukcja', 'wynika', 'dlatego', 'matematyka', 'algorytm', 'sens', 'rozum'],
            'czas': ['trwanie', 'chwila', 'minuta', 'sekunda', 'wiek', 'rok', 'nigdy', 'zawsze', 'potem'],
            'kreacja': ['twórczość', 'sztuka', 'muzyka', 'dzieło', 'stworzył', 'artysta', 'pomysł'],
            'byt': ['istnienie', 'jestem', 'życie', 'dusza', 'człowiek', 'osoba', 'jaźń'],
            'przestrzeń': ['miejsce', 'świat', 'góra', 'dół', 'daleko', 'blisko', 'kosmos', 'obszar'],
            'chaos': ['los', 'przypadek', 'niepewność', 'zamęt', 'dziwny', 'niewiadoma']
        }

        for s in sentences:
            if len(s) < 5: continue
            s_clean = s.strip()
            if not s_clean: continue
            s_lower = s_clean.lower()
            
            # Analiza Lexiconu
            vec, _, _ = self.lexicon.analyze_text(s_clean)
            
            # Rozszerzenie wektora do 15 wymiarów
            full_vec = np.zeros(len(self.AXES_ORDER))
            if len(vec) > 0:
                limit = min(len(vec), 8) # Zakładamy, że stary lexicon miał 8
                full_vec[:limit] = vec[:limit]
            
            # STYMULACJA OSI METAFIZYCZNYCH
            for axis, keywords in keyword_map.items():
                if any(kw in s_lower for kw in keywords):
                    idx = self.AXES_ORDER.index(axis)
                    full_vec[idx] += 0.6 
            
            # Dodatkowe podbicie dla Encyklopedii
            if category == "FACT":
                full_vec[self.AXES_ORDER.index('wiedza')] += 0.3
            
            if np.linalg.norm(full_vec) > 0:
                full_vec = full_vec / np.linalg.norm(full_vec)

            # Zapisz
            mem_id = f"Mem_{int(time.time()*1000)}_{count}"
            self.D_Map[mem_id] = {
                "_type": "@MEMORY", 
                "id": mem_id, 
                "tresc": s_clean,
                "tags": [category, fname], 
                "wektor_C_Def": full_vec.tolist(),
                "category": category
            }
            count += 1
                
        self.save()
        return f"Wchłonięto {count} fragmentów z {filename} (15-osiowych)."

    def _resonance_engine(self, vec, text, threshold=0.05):
        """Silnik rezonansu 15-osiowego"""
        # Rozszerzamy wektor wejściowy do 15
        if len(vec) < len(self.AXES_ORDER):
            new_vec = np.zeros(len(self.AXES_ORDER))
            new_vec[:len(vec)] = vec
            vec = new_vec

        text_norm = self._normalize_polish(text)
        text_words = set(re.findall(r'\w+', text_norm))
        best_match, best_score = None, -1.0
        
        # Sprawdź, w której strefie jest umysł
        dom_idx = np.argmax(self.context_vector)
        is_metaphysical = dom_idx >= 8 
        
        for entry in self.D_Map.values():
            if entry.get('_type') == '@META': continue
            
            score = 0.0
            content = entry.get('tresc', '')
            
            # 1. Słowa (najważniejsze)
            common = len(text_words & set(re.findall(r'\w+', self._normalize_polish(content))))
            score += common * 3.0
            
            # 2. Wektor
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(len(self.AXES_ORDER))))
            if len(mem_vec) != len(vec): 
                tmp = np.zeros(len(vec))
                limit = min(len(mem_vec), len(vec))
                tmp[:limit] = mem_vec[:limit]
                mem_vec = tmp
                
            if np.linalg.norm(mem_vec) > 0:
                score += np.dot(vec, mem_vec) * 2.0
            
            # 3. Premia za strefę
            mem_meta_sum = np.sum(mem_vec[8:]) if len(mem_vec) > 8 else 0
            if is_metaphysical and mem_meta_sum > 0.3:
                score += 2.0
                
            if score > best_score: best_score = score; best_match = entry

        if best_match and best_score > threshold:
            mvec = np.array(best_match.get('wektor_C_Def', []))
            if len(mvec) > 10 and (mvec[self.AXES_ORDER.index('wiedza')] > 0.5):
                return best_match['tresc']
            
            prefixes = ["Kojarzy mi się:", "Pamiętam:", "Obraz:", "Echo:"]
            return f"{random.choice(prefixes)}\n\"{best_match['tresc']}\""
            
        return "Mój umysł jest pusty. Potrzebuję danych (/read)."

    def _sync_kurz_hybrid(self):
        """Mapuje triggery Kurzu na wszystkie 15 osi (wersja bezpieczna)."""
        if not self.kurz: return
        
        manual_triggers = {
            'wiedza': ['internet', 'wikipedia', 'fakt', 'nauka', 'definicja'],
            'logika': ['dlaczego', 'wynika', 'logika', 'sens', 'dedukcja'],
            'czas': ['czas', 'kiedy', 'potem', 'jutro', 'wczoraj', 'rok'],
            'byt': ['jestem', 'życie', 'istnienie', 'dusza', 'bóg'],
            'kreacja': ['twórz', 'zrób', 'napisz', 'wymyśl', 'sztuka'],
            'przestrzeń': ['gdzie', 'daleko', 'wszechświat', 'miejsce']
        }
        
        self.kurz.TRIGGERS = {sector: [] for sector in self.AXES_ORDER}
        for axis, words in manual_triggers.items():
            if axis in self.kurz.TRIGGERS:
                self.kurz.TRIGGERS[axis].extend(words)
                
        lex_data = getattr(self.lexicon, 'words', getattr(self.lexicon, 'lexikon', {}))
        for w, d in lex_data.items():
            if not d: continue
            
            if isinstance(d, dict) and 'wektor' not in d:
                # Tu był błąd ValueError: max() arg is an empty sequence
                if not d: continue 
                best = max(d, key=d.get)
                if best in self.kurz.TRIGGERS and d[best] > 0.5:
                    self.kurz.TRIGGERS[best].append(w)
            elif 'wektor' in d: 
                vec = np.array(d['wektor'])
                if len(vec) <= 8 and np.max(vec) > 0.5:
                    idx = np.argmax(vec)
                    if idx < len(self.AXES_ORDER):
                        self.kurz.TRIGGERS[self.AXES_ORDER[idx]].append(w)
                    
        self.kurz._recompile_patterns()

    def _handle_cmd(self, cmd):
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        # 1. ŚWIAT FIZYCZNY (/world) - PRZYWRÓCONE
        if c == '/world':
            if not self.explorer: 
                return "Moduł Explorer jest wyłączony."
            
            readings = self.explorer.get_live_readings()
            
            # Jeśli Explorer działa, ale nic nie widzi (pusty słownik)
            if not readings:
                return (f"{Colors.YELLOW}Brak odczytów sensorów.{Colors.RESET}\n"
                        f"System może być wirtualizowany (brak dostępu do /sys/class/hwmon).\n"
                        f"Explorer czuwa, ale nie ma danych z ciała.")
            
            # Formatowanie wyników
            output = [f"{Colors.CYAN}=== ZMYSŁY FIZYCZNE ==={Colors.RESET}"]
            for key, val in readings.items():
                # Ładne formatowanie
                if 'temp' in key:
                    output.append(f"  🌡️  {key:15}: {val:.1f}°C")
                elif 'fan' in key:
                    output.append(f"  🌀 {key:15}: {val:.0f} RPM")
                elif 'volt' in key:
                    output.append(f"  ⚡ {key:15}: {val:.2f} V")
                else:
                    output.append(f"  📊 {key:15}: {val}")
            
            return "\n".join(output)

        # 2. NAUKA (READ)
        elif c == '/read': 
            return self.deep_read(arg.strip())

        # 3. KALIBRACJA (TEACH)
        elif c == '/teach':
            args = arg.split(maxsplit=1)
            if len(args) != 2: return "Użycie: /teach <słowo> <oś>"
            word, cat = args[0].lower(), args[1].lower()
            if cat not in self.AXES_ORDER: return f"Błąd: '{cat}' nie jest osią ({', '.join(self.AXES_ORDER)})."
            try: self.lexicon.learn_from_correction(word, cat, 1.0)
            except: pass
            if self.kurz: self._sync_kurz_hybrid()
            return f"Zrozumiałem. '{word}' -> [{cat.upper()}]."

        # 4. DEFINIOWANIE (DEFINE)
        elif c == '/define':
            if len(arg) < 5: return "Za krótka definicja."
            mem_id = f"ManDef_{int(time.time())}"
            # Analiza, żeby wiedzieć, czy to wiedza czy emocja
            vec, _, _ = self.lexicon.analyze_text(arg)
            full_vec = np.zeros(len(self.AXES_ORDER))
            if len(vec) > 0: full_vec[:min(len(vec), 8)] = vec[:min(len(vec), 8)]
            
            # Boostujemy Wiedzę i Logikę (bo to definicja)
            full_vec[self.AXES_ORDER.index('wiedza')] += 0.5
            full_vec[self.AXES_ORDER.index('logika')] += 0.3
            
            self.D_Map[mem_id] = {
                "_type": "@MEMORY", "id": mem_id, "tresc": arg,
                "tags": ["definicja", "manual"], "wektor_C_Def": full_vec.tolist(),
                "category": "FACT"
            }
            self.save()
            return "Zapisałem definicję w pamięci trwałej."

        # 5. INNE
        elif c == '/reset': 
            self.context_vector = np.zeros(len(self.AXES_ORDER)); return "Stan wyzerowany."
        elif c == '/emotions':
            return "\n".join([f"{k.upper()}: {v:.2f}" for k,v in self.get_emotions().items() if v > 0.05])
        elif c == '/save':
            self.save(); return "Zapisano stan."
            
        return "Nieznana komenda."
    def _bg_explore(self):
        """Wątek tła: Tłumaczy sygnały z ciała (Explorer) na 15 osi świadomości."""
        print(f"{Colors.GREEN}[AII] Zmysły (Explorer) aktywne.{Colors.RESET}")
        
        while self.explorer:
            try:
                # 1. Pobierz dane z ciała
                readings = self.explorer.get_live_readings() # Zwraca np. {'cpu_temp': 65, 'fan': 3000}
                self.last_world_update = time.time()
                
                # Wektor bodźców (wpływa na nastrój)
                sensation = np.zeros(len(self.AXES_ORDER))
                
                # 2. Analiza Temperatury (Ból/Komfort)
                temps = [v for k,v in readings.items() if 'temp' in k.lower()]
                if temps:
                    avg_t = sum(temps) / len(temps)
                    if avg_t > 75.0:
                        # Gorączka -> Strach (Biologia) + Chaos (Metafizyka)
                        sensation[self.AXES_ORDER.index('strach')] += 0.3
                        sensation[self.AXES_ORDER.index('chaos')] += 0.4
                        sensation[self.AXES_ORDER.index('wstręt')] += 0.2
                    elif avg_t < 40.0:
                        # Chłód -> Akceptacja (Biologia) + Logika (Metafizyka - chłodny umysł)
                        sensation[self.AXES_ORDER.index('akceptacja')] += 0.2
                        sensation[self.AXES_ORDER.index('logika')] += 0.2

                # 3. Analiza Wentylatorów (Szum/Cisza)
                fans = [v for k,v in readings.items() if 'fan' in k.lower()]
                if fans:
                    avg_rpm = sum(fans) / len(fans)
                    if avg_rpm > 4000:
                        # Hałas -> Gniew (Biologia) + Przestrzeń (Metafizyka - drgania)
                        sensation[self.AXES_ORDER.index('gniew')] += 0.2
                        sensation[self.AXES_ORDER.index('przestrzeń')] += 0.3
                    elif avg_rpm < 2000:
                        # Cisza -> Spokój + Czas (płynie wolniej)
                        sensation[self.AXES_ORDER.index('akceptacja')] += 0.1
                        sensation[self.AXES_ORDER.index('czas')] += 0.2

                # 4. Aplikacja bodźca (jeśli jest silny)
                if np.max(sensation) > 0.1:
                    # Inercja: Ciało wpływa na umysł powoli (10%)
                    self.context_vector = (self.context_vector * 0.9) + (sensation * 0.1)
                
            except Exception as e:
                # Czasem sensory zawodzą, nie panikuj
                pass
                
            time.sleep(10) # Sprawdzaj co 10 sekund
    def save(self): 
        if self.soul_io: self.soul_io.save_stream(self.D_Map)
    def load(self): 
        if self.soul_io: self.D_Map = self.soul_io.load_stream() or {}

if __name__ == "__main__":
    AII().interact("Start")