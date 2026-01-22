# -*- coding: utf-8 -*-
"""
aii.py v8.1.0-Stabilized - EriAmo Complete Consciousness
EriAmo Union - Architektura oparta na Single Source of Truth (union_config.py).

Ten moduł jest MÓZGIEM systemu. Integruje:
- Biologię (Emocje Plutchika)
- Metafizykę (Logika, Czas, Przestrzeń - dla Muzyki)
- Zmysły (Explorer)
- Odruchy (Kurz)
"""

import sys
import os
import time
import threading
import re
import numpy as np
import json
import random

# --- IMPORT JEDNEGO ŹRÓDŁA PRAWDY ---
try:
    from union_config import UnionConfig, Colors
except ImportError:
    print("❌ Błąd krytyczny: Brak pliku 'union_config.py'. System nie może wystartować.")
    sys.exit(1)

# Importy modułów pomocniczych
try: from soul_io import SoulIO
except ImportError: SoulIO = None

try: from lexicon import EvolvingLexicon
except ImportError: EvolvingLexicon = None

try: from kurz import Kurz
except ImportError: Kurz = None

try: from explorer import WorldExplorer
except ImportError: WorldExplorer = None

try: from haiku import HaikuGenerator
except ImportError: HaikuGenerator = None


# ==============================================================================
# CORTEX (Pamięć Nawyku Wektorowego)
# ==============================================================================
class VectorCortex:
    def __init__(self, axes_count):
        self.dims = axes_count
        # Macierz przejść n x n (Dynamiczny rozmiar z Configu)
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
                with open(path + '.cortex', 'r') as f: 
                    mat = np.array(json.load(f))
                    # Walidacja wymiarów (Krytyczne dla stabilności!)
                    if mat.shape == (self.dims, self.dims):
                        self.transition_matrix = mat
                    else:
                        print(f"{Colors.RED}[Cortex] Niezgodność wymiarów macierzy (Plik vs Config). Reset.{Colors.RESET}")
        except: pass


# ==============================================================================
# GŁÓWNA KLASA AII
# ==============================================================================
class AII:
    VERSION = "8.1.0-Stabilized"
    
    # Pobieramy definicje z Configu
    AXES_ORDER = UnionConfig.AXES
    DIM = UnionConfig.DIMENSION

    def __init__(self, standalone_mode=True):
        self.standalone_mode = standalone_mode
        self.ui = None
        if standalone_mode:
            print(f"{Colors.CYAN}[SYSTEM] Inicjalizacja Stabilna ({self.DIM} Osi)...{Colors.RESET}")

        self.D_Map = {}
        # Wektor Kontekstu o poprawnym rozmiarze
        self.context_vector = np.zeros(self.DIM)
        
        # Inicjalizacja Podsystemów
        self.soul_io = SoulIO() if SoulIO else None
        self.lexicon = EvolvingLexicon() if EvolvingLexicon else None
        self.kurz = Kurz() if Kurz else None
        self.explorer = WorldExplorer(self) if WorldExplorer else None
        self.haiku_gen = HaikuGenerator(self) if HaikuGenerator else None

        # Uruchomienie zmysłów w tle
        if self.explorer:
            threading.Thread(target=self._bg_explore, daemon=True).start()
            self.last_world_update = time.time()

        # Wczytanie pamięci
        self.load()
        
        # Synchronizacja odruchów
        if self.kurz: self._sync_kurz_hybrid()
        
        # Inicjalizacja Cortexu
        self.cortex = VectorCortex(self.DIM)
        if self.soul_io and hasattr(self.soul_io, 'filepath'): 
            self.cortex.load(self.soul_io.filepath)

    # --- API (Dostęp dla innych modułów) ---
    def get_emotions(self):
        """Zwraca słownik {oś: wartość} dla wszystkich wymiarów."""
        return {self.AXES_ORDER[i]: float(self.context_vector[i]) for i in range(self.DIM)}

    def introspect(self):
        """Opisuje stan wewnętrzny słowami."""
        if np.sum(self.context_vector) == 0: return "Stan neutralny."
        idx = np.argmax(self.context_vector)
        dom_axis = self.AXES_ORDER[idx]
        val = self.context_vector[idx]
        
        # Dynamiczne określenie strefy (Bio vs Meta)
        zone = "Biologiczna" if idx < UnionConfig.BIO_DIM else "Metafizyczna"
        return f"Dominanta: {dom_axis.upper()} ({zone}, {val:.2f})"

    # --- CZYTANIE I PAMIĘĆ ---
    def _normalize_polish(self, text):
        return text.lower().strip()

    def deep_read(self, filename, category="general"):
        """Inteligentne czytanie plików (Auto-Tagowanie Fact/Fiction)."""
        if not os.path.exists(filename):
            # Szukanie w podkatalogach
            alternatives = [os.path.join("library", filename), os.path.join("AI_Union", filename), filename]
            for alt in alternatives:
                if os.path.exists(alt):
                    filename = alt; break
            else:
                return f"Błąd: Nie znaleziono pliku '{filename}'."

        try:
            with open(filename, 'r', encoding='utf-8') as f: content = f.read()
        except Exception as e: return f"Błąd odczytu: {e}"
        
        fname = os.path.basename(filename).lower()
        
        # Automatyczne rozpoznawanie kategorii
        if any(x in fname for x in ["encyklopedia", "nauka", "wiedza"]): category = "FACT"
        elif any(x in fname for x in ["powieść", "pies", "studium", "dzien"]): category = "FICTION"
            
        sentences = re.split(r'[.!?]+', content)
        count = 0
        
        # Mapa słów kluczowych do osi metafizycznych
        keyword_map = {
            'wiedza': ['internet', 'nauka', 'fizyka', 'fakt', 'definicja'],
            'logika': ['dedukcja', 'wynika', 'matematyka', 'sens', 'dlatego'],
            'czas': ['czas', 'kiedy', 'potem', 'rok', 'chwila'],
            'byt': ['jestem', 'życie', 'istnienie', 'dusza', 'człowiek'],
            'przestrzeń': ['świat', 'miejsce', 'kosmos', 'daleko'],
            'chaos': ['los', 'przypadek', 'niepewność', 'zamęt']
        }

        for s in sentences:
            s_clean = s.strip()
            if len(s_clean) < 5: continue
            
            # Analiza leksykalna
            vec, _, _ = self.lexicon.analyze_text(s_clean)
            
            # Skalowanie wektora do DIM
            full_vec = np.zeros(self.DIM)
            if len(vec) > 0:
                limit = min(len(vec), self.DIM)
                full_vec[:limit] = vec[:limit]
            
            # Boostowanie słowami kluczowymi
            s_lower = s_clean.lower()
            for axis, keywords in keyword_map.items():
                if any(kw in s_lower for kw in keywords):
                    if axis in self.AXES_ORDER:
                        idx = self.AXES_ORDER.index(axis)
                        full_vec[idx] += 0.6 
            
            # Boost dla faktów
            if category == "FACT" and 'wiedza' in self.AXES_ORDER:
                full_vec[self.AXES_ORDER.index('wiedza')] += 0.3
            
            # Normalizacja
            if np.linalg.norm(full_vec) > 0:
                full_vec = full_vec / np.linalg.norm(full_vec)

            # Zapis do pamięci
            mem_id = f"Mem_{int(time.time()*1000)}_{count}"
            self.D_Map[mem_id] = {
                "_type": "@MEMORY", "id": mem_id, "tresc": s_clean,
                "tags": [category, fname], "wektor_C_Def": full_vec.tolist(),
                "category": category
            }
            count += 1
                
        self.save()
        return f"Wchłonięto {count} fragmentów z {fname}."

    def _resonance_engine(self, vec, text, threshold=0.05):
        """Silnik skojarzeniowy (zwraca odpowiedź tekstową)."""
        # Upewniamy się, że wektor zapytania ma dobry wymiar
        if len(vec) != self.DIM:
            new_vec = np.zeros(self.DIM)
            limit = min(len(vec), self.DIM)
            new_vec[:limit] = vec[:limit]
            vec = new_vec

        text_norm = self._normalize_polish(text)
        text_words = set(re.findall(r'\w+', text_norm))
        best_match, best_score = None, -1.0
        
        # Stan systemu
        dom_idx = np.argmax(self.context_vector)
        is_metaphysical = dom_idx >= UnionConfig.BIO_DIM
        
        for entry in self.D_Map.values():
            if entry.get('_type') == '@META': continue
            content = entry.get('tresc', '')
            score = 0.0
            
            # 1. Wspólne słowa
            common = len(text_words & set(re.findall(r'\w+', self._normalize_polish(content))))
            score += common * 3.0
            
            # 2. Podobieństwo wektorowe
            mem_vec = np.array(entry.get('wektor_C_Def', np.zeros(self.DIM)))
            # Bezpieczne wyrównanie wymiarów
            if len(mem_vec) != self.DIM:
                tmp = np.zeros(self.DIM)
                tmp[:min(len(mem_vec), self.DIM)] = mem_vec[:min(len(mem_vec), self.DIM)]
                mem_vec = tmp
                
            if np.linalg.norm(mem_vec) > 0:
                score += np.dot(vec, mem_vec) * 2.0
            
            # 3. Kontekst strefy (Bio vs Meta)
            mem_meta_sum = np.sum(mem_vec[UnionConfig.BIO_DIM:])
            if is_metaphysical and mem_meta_sum > 0.3:
                score += 2.0 # Preferuj mądre odpowiedzi w trybie naukowym
                
            if score > best_score: best_score = score; best_match = entry

        # Generowanie odpowiedzi
        if best_match and best_score > threshold:
            mvec = np.array(best_match.get('wektor_C_Def', []))
            
            # Jeśli to czysta wiedza (Fakt), podaj bez ozdobników
            if 'wiedza' in self.AXES_ORDER:
                wiedza_idx = self.AXES_ORDER.index('wiedza')
                # Sprawdź czy indeks mieści się w wektorze (na wypadek starych danych)
                if len(mvec) > wiedza_idx and mvec[wiedza_idx] > 0.5:
                    return best_match['tresc']
            
            prefixes = ["Kojarzy mi się:", "Pamiętam:", "Obraz:", "Echo:"]
            return f"{random.choice(prefixes)}\n\"{best_match['tresc']}\""
            
        return "Mój umysł jest pusty. Potrzebuję danych (/read)."

    # --- SYNCHRONIZACJA ODRUCHÓW ---
    def _sync_kurz_hybrid(self):
        """Bezpieczna synchronizacja Kurzu z Leksykonem."""
        if not self.kurz: return
        self.kurz.TRIGGERS = {sector: [] for sector in self.AXES_ORDER}
        
        # Manualne triggery (skrót)
        manual = {'wiedza': ['internet', 'nauka'], 'logika': ['dlaczego', 'sens']}
        for k, v in manual.items(): 
            if k in self.kurz.TRIGGERS: self.kurz.TRIGGERS[k].extend(v)

        # Synchronizacja z leksykonu
        lex_data = getattr(self.lexicon, 'words', getattr(self.lexicon, 'lexikon', {}))
        for w, d in lex_data.items():
            if not d: continue
            if isinstance(d, dict) and 'wektor' not in d:
                # Zabezpieczenie przed pustym słownikiem
                if not d: continue
                best = max(d, key=d.get)
                if best in self.kurz.TRIGGERS and d[best] > 0.5:
                    self.kurz.TRIGGERS[best].append(w)
            elif 'wektor' in d:
                vec = np.array(d['wektor'])
                if len(vec) <= self.DIM and np.max(vec) > 0.5:
                    idx = np.argmax(vec)
                    if idx < self.DIM:
                        self.kurz.TRIGGERS[self.AXES_ORDER[idx]].append(w)
        self.kurz._recompile_patterns()

    # --- OBSŁUGA KOMEND ---
    def _handle_cmd(self, cmd):
        parts = cmd.split(maxsplit=1)
        c = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""
        
        # 1. Zmysły (/world)
        if c == '/world':
            if not self.explorer: return "Explorer wyłączony."
            readings = self.explorer.get_live_readings()
            if not readings:
                return f"{Colors.YELLOW}Brak odczytów (wirtualizacja/brak dostępu).{Colors.RESET}"
            out = [f"{Colors.CYAN}=== ZMYSŁY ==={Colors.RESET}"]
            for k, v in readings.items(): out.append(f"  {k}: {v}")
            return "\n".join(out)
            
        # 2. Cyfrowa Świadomość (/scan)
        elif c == '/scan':
            if not self.explorer: return "Explorer wyłączony."
            files = self.explorer.explore_project_files(root_path="..")
            count = 0
            for f in files:
                mem_id = f"SysFile_{int(time.time())}_{count}"
                # Wektor pliku: Wiedza + Przestrzeń
                vec = np.zeros(self.DIM)
                if 'wiedza' in self.AXES_ORDER: vec[self.AXES_ORDER.index('wiedza')] = 0.5
                if 'przestrzeń' in self.AXES_ORDER: vec[self.AXES_ORDER.index('przestrzeń')] = 0.5
                
                self.D_Map[mem_id] = {
                    "_type": "@MEMORY", "id": mem_id, 
                    "tresc": f"Wiem o pliku {f['name']} w {f['path']}.",
                    "tags": ["system", "plik"], "wektor_C_Def": vec.tolist(),
                    "category": "FACT"
                }
                count += 1
            self.save()
            return f"Zmapowano {count} plików w projekcie."

        # 3. Nauka (/read, /teach, /define)
        elif c == '/read': return self.deep_read(arg.strip())
        elif c == '/teach':
            args = arg.split(maxsplit=1)
            if len(args) != 2: return "Użycie: /teach <słowo> <oś>"
            w, cat = args[0].lower(), args[1].lower()
            if cat not in self.AXES_ORDER: return f"Nieznana oś: {cat}"
            self.lexicon.learn_from_correction(w, cat, 1.0)
            if self.kurz: self._sync_kurz_hybrid()
            return f"Zrozumiałem: {w} -> {cat}"
        elif c == '/define':
            if len(arg) < 5: return "Za krótka definicja."
            mem_id = f"ManDef_{int(time.time())}"
            vec = np.zeros(self.DIM)
            if 'wiedza' in self.AXES_ORDER: vec[self.AXES_ORDER.index('wiedza')] = 0.8
            self.D_Map[mem_id] = {
                "_type": "@MEMORY", "id": mem_id, "tresc": arg,
                "tags": ["manual", "definicja"], "wektor_C_Def": vec.tolist(),
                "category": "FACT"
            }
            self.save()
            return "Zapisałem definicję."
            
        # 4. Inne
        elif c == '/reset': 
             self.context_vector = np.zeros(self.DIM); return "Reset."
        elif c == '/emotions':
            return "\n".join([f"{k.upper()}: {v:.2f}" for k,v in self.get_emotions().items() if v > 0.05])
        elif c == '/save':
            self.save(); return "Zapisano."
            
        return "Nieznana komenda."

    # --- PĘTLA GŁÓWNA ---
    def interact(self, user_input):
        if not user_input or user_input.strip() == "": return "..."
        if user_input.strip().startswith('/'): return self._handle_cmd(user_input)
        
        # 1. Odruch (Kurz)
        if self.kurz:
            s, v = self.kurz.quick_scan(user_input)
            if s and s in self.AXES_ORDER:
                idx = self.AXES_ORDER.index(s)
                r = np.zeros(self.DIM)
                r[idx] = v * 0.4
                self.context_vector = (self.context_vector * 0.7) + (r * 0.3)

        # 2. Analiza głęboka (Lexicon)
        vec_f = np.zeros(self.DIM)
        lex_vec, _, _ = self.lexicon.analyze_text(user_input)
        if len(lex_vec) > 0:
            limit = min(len(lex_vec), self.DIM)
            vec_f[:limit] = lex_vec[:limit]
            
        # 3. Cortex i Inercja
        self.cortex.learn(self.context_vector, vec_f)
        self.context_vector = (self.context_vector * 0.85) + (vec_f * 0.15)
        
        # 4. Rezonans (Odpowiedź)
        response = self._resonance_engine(vec_f, user_input)
        
        if self.standalone_mode:
            if self.ui: self.ui.print_animated_text(response, Colors.WHITE)
            else: print(f" [EriAmo] {response}")
            
        return response
    
    # --- ZMYSŁY W TLE ---
    def _bg_explore(self):
        """Tłumaczy fizykę (temp, fan) na metafizykę (chaos, logika)."""
        while self.explorer:
            try:
                readings = self.explorer.get_live_readings()
                sensation = np.zeros(self.DIM)
                
                # Temp -> Chaos/Strach
                temps = [v for k,v in readings.items() if 'temp' in k]
                if temps:
                    avg = sum(temps)/len(temps)
                    if avg > 75.0 and 'chaos' in self.AXES_ORDER:
                        sensation[self.AXES_ORDER.index('chaos')] += 0.3
                        
                # Fan -> Przestrzeń/Gniew
                fans = [v for k,v in readings.items() if 'fan' in k]
                if fans:
                    avg = sum(fans)/len(fans)
                    if avg > 4000 and 'przestrzeń' in self.AXES_ORDER:
                        sensation[self.AXES_ORDER.index('przestrzeń')] += 0.3
                        
                if np.max(sensation) > 0.1:
                    self.context_vector = (self.context_vector * 0.9) + (sensation * 0.1)
            except: pass
            time.sleep(10)

    def save(self): 
        if self.soul_io: self.soul_io.save_stream(self.D_Map)
    def load(self): 
        if self.soul_io: self.D_Map = self.soul_io.load_stream() or {}

if __name__ == "__main__":
    AII().interact("Start")