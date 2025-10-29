#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import numpy as np
import json
import os
import threading
import hashlib 
import random
import re 
try:
    import unidecode
except ImportError:
    # Minimalna obsługa polskich znaków
    class UnidecodeMock:
        def unidecode(self, text):
            return text.replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń', 'n').replace('ó', 'o').replace('ś', 's').replace('ż', 'z').replace('ź', 'z')
    unidecode = UnidecodeMock()

# --- KOLORY ---
class Colors:
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    PINK = "\033[95m"
    BLUE = "\033[34m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    BLINK = "\033[5m"
    FAINT = "\033[2m"

# --- EMOCJE ---
EMOCJE = {
    "radość":     {"kolor": Colors.GREEN,   "ikona": "😊", "energia": +10},
    "złość":      {"kolor": Colors.RED,     "ikona": "😡", "energia": -15},
    "smutek":     {"kolor": Colors.BLUE,    "ikona": "😢", "energia": -20},
    "strach":     {"kolor": Colors.MAGENTA, "ikona": "😨", "energia": -10},
    "miłość":     {"kolor": Colors.PINK,    "ikona": "❤️", "energia": +15},
    "zdziwienie": {"kolor": Colors.YELLOW,  "ikona": "😮", "energia": +5},
    "neutralna":  {"kolor": Colors.WHITE,   "ikona": "⚪", "energia": 0}
}

# --- FancyUI Class ---
class FancyUI:
    def __init__(self):
        self.spinner_frames = ['-', '\\', '|', '/']
        self.dots_frames = ['   ', '.  ', '.. ', '...']
        self.thinking_frames = ["[_]", "[_ _]", "[_ _ _]"]
        self.planet_dots_frames = ["○ . . .", ". ○ . .", ". . ○ .", ". . . ○"]

    def print_animated_text(self, text, color=Colors.WHITE, delay=0.03):
        sys.stdout.write(color)
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(Colors.RESET + "\n")

    def show_spinner(self, message, duration_sec=1.0, final_message="", color=Colors.CYAN):
        end_time = time.time() + duration_sec
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{self.spinner_frames[idx % len(self.spinner_frames)]} {message}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1
        sys.stdout.write("\r" + " " * (len(message) + 5) + "\r")
        if final_message:
            print(f"{color}{final_message}{Colors.RESET}")
        else:
            sys.stdout.write(Colors.RESET)

    def show_thinking_dots(self, message, duration_sec=1.0, color=Colors.FAINT + Colors.CYAN):
        end_time = time.time() + duration_sec
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{message} {self.dots_frames[idx % len(self.dots_frames)]}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.3)
            idx += 1
        sys.stdout.write("\r" + " " * (len(message) + 5) + "\r")
        sys.stdout.write(Colors.RESET)

    def show_planet_scan(self, message, duration_sec=1.5, color=Colors.MAGENTA):
        end_time = time.time() + duration_sec
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{message} {self.planet_dots_frames[idx % len(self.planet_dots_frames)]}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.2)
            idx += 1
        sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
        sys.stdout.write(Colors.RESET)

# ---------------------------------------------------------------------- #
# BytS (Sphere) Class 
# ---------------------------------------------------------------------- #
class BytS:
    def __init__(self, wymiary):
        self.stan = np.zeros(wymiary)

    def promien_historii(self):
        return np.linalg.norm(self.stan)

    def oblicz_korelacje_struny(self, nowa_struna_vec):
        wektor_historii = self.stan
        wektor_bodzca = np.asarray(nowa_struna_vec)
        
        promien_historii = self.promien_historii()
        sila_bodzca = np.linalg.norm(wektor_bodzca)
        
        if promien_historii == 0 or sila_bodzca == 0:
            return 0.0 
            
        iloczyn_skalarny = np.dot(wektor_historii, wektor_bodzca)
        korelacja = iloczyn_skalarny / (promien_historii * sila_bodzca)
        
        return np.clip(korelacja, -1.0, 1.0)

    def akumuluj_styk(self, nowa_struna_vec):
        self.stan = self.stan + np.asarray(nowa_struna_vec)

# ---------------------------------------------------------------------- #
# --- AII ZINTEGROWANE Z BytS ---
# ---------------------------------------------------------------------- #
class AII:

    # Definicja "Strun" / Osi Krajobrazu P
    AXES_KEYWORDS = {
        "logika": ["logika", "logiczny", "sens", "rozum", "dlaczego", "poniewaz", "wynik", "fakt"],
        "emocje": ["czuje", "emocja", "milosc", "zlosc", "smutek", "radosc", "strach", "uczucie"],
        "byt": ["byt", "istnienie", "ja", "jestem", "kula", "rzeczywistosc", "historia", "ontologia", "imie", "reiamo"],
        "walka": ["walka", "dzialanie", "konflikt", "wojna", "sila", "wrog", "chaos", "wola"],
        "kreacja": ["tworzyc", "sztuka", "budowac", "muzyka", "pisac", "nowy", "piekno"],
        "wiedza": ["wiedza", "nauka", "uczyc", "dane", "informacja", "co", "kto", "jak"],
        "czas": ["czas", "kiedy", "przeszlosc", "teraz", "przyszlosc", "historia", "krok", "sciezka"],
        "przestrzen": ["gdzie", "miejsce", "krajobraz", "droga", "swiat", "kierunek", "polozenie"]
    }
    AXES_KEYWORDS_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in AXES_KEYWORDS.items()}
    AXES_ORDER = ["logika", "emocje", "byt", "walka", "kreacja", "wiedza", "czas", "przestrzen"]
    
    PRÓG_KOMPRESJI_ONTOLOGICZNEJ = 0.98

    def __init__(self):
        self.D_Map = {}     
        self.H_log = []     
        self.energy = 100
        self.load = 0
        self.status = "myślę"
        self.emocja = "neutralna"
        self.sleep_interval = 300
        self.running = True
        self.prompts_since_sleep = 0
        self.max_sleep_time = 2.0
        self.max_hlog = 1000
        self.F_will = 0.5   
        self.ostatnie_slowa = []
        self.ui = FancyUI()
        
        self.wymiary = len(self.AXES_ORDER) 
        self.byt_stan = BytS(wymiary=self.wymiary) 
        
        self.load_knowledge() 
        self.start_sleep_cycle()

    # ------------------------------------------------------------------ #
    # Text Normalization Utility
    # ------------------------------------------------------------------ #
    def _normalize_text(self, text):
        """Konwertuje 'cześć' -> 'czesc' i usuwa znaki specjalne."""
        try:
            text_lower = text.lower()
            text_ascii = unidecode.unidecode(text_lower) 
            text_clean = re.sub(r'[^\w\s_]', '', text_ascii)
            return text_clean
        except Exception as e:
            # Używamy print w przypadku poważnego błędu, ale kod ma już awaryjną funkcję unidecode
            return text.lower() 

    # ------------------------------------------------------------------ #
    # Vectorization
    # ------------------------------------------------------------------ #
    def _vector_from_text(self, text):
        """Tworzy wektor semantyczny przez rzutowanie tekstu na osie P-Krajobrazu."""
        text_clean = self._normalize_text(text)
        words = set(text_clean.split())
        
        if not words:
            return np.zeros(self.wymiary) 

        vec = np.zeros(self.wymiary)
        
        for i, axis_name in enumerate(self.AXES_ORDER):
            keywords = self.AXES_KEYWORDS_ASCII[axis_name]
            score = len(words.intersection(keywords))
            vec[i] = score

        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        
        return vec / norm
    
    # ------------------------------------------------------------------ #
    # SKONSOLIDOWANY ZAPIS / ODCZYT
    # ------------------------------------------------------------------ #
    def save_knowledge(self):
        os.makedirs("data", exist_ok=True)
        
        serial_dmap = {k: {
            'wektor_C_Def': v['wektor_C_Def'].tolist(),
            'waga_Ww': float(v['waga_Ww']),
            'tagi': v['tagi'],
            'tresc': v.get('tresc', '') 
        } for k, v in self.D_Map.items()}
        
        serial_hlog = self.H_log[-self.max_hlog:]
        
        serial_byt = {
            'stan': self.byt_stan.stan.tolist(),
            'F_will': self.F_will
        }

        master_state = {
            'D_Map_Data': serial_dmap,
            'H_Log_Data': serial_hlog,
            'Byt_Stan_Data': serial_byt
        }

        try:
            with open("data/AII_State.json", "w", encoding="utf-8") as f:
                json.dump(master_state, f, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}[BŁĄD ZAPISU] Nie udało się zapisać stanu: {e}{Colors.RESET}")

    def load_knowledge(self):
        os.makedirs("data", exist_ok=True)
        
        try:
            with open("data/AII_State.json", encoding="utf-8") as f:
                master_state = json.load(f)
        except Exception:
            self.D_Map = {}
            self.H_log = []
            self.byt_stan = BytS(wymiary=self.wymiary)
            self.F_will = 0.5
            return 

        try:
            data = master_state.get('D_Map_Data', {})
            self.D_Map = {k: {
                'wektor_C_Def': np.array(v['wektor_C_Def'], dtype=float),
                'waga_Ww': float(v['waga_Ww']),
                'tagi': v['tagi'],
                'tresc': v.get('tresc', 'BRAK TREŚCI') 
            } for k, v in data.items()}
        except Exception:
            self.D_Map = {}
            
        self.H_log = master_state.get('H_Log_Data', [])
            
        try:
            data = master_state.get('Byt_Stan_Data', {})
            stan_vector = np.array(data.get('stan', []), dtype=float)
            
            if stan_vector.shape == (self.wymiary,):
                self.byt_stan.stan = stan_vector
            else:
                if data: 
                    print(f"{Colors.RED}[BŁĄD] Wymiar Bytu w pliku ({stan_vector.shape}) niezgodny z modelem ({self.wymiary,}). Resetuję Byt.{Colors.RESET}")
                self.byt_stan = BytS(wymiary=self.wymiary)
                
            self.F_will = float(data.get('F_will', 0.5))
        except Exception:
            self.byt_stan = BytS(wymiary=self.wymiary)
            self.F_will = 0.5
            
    # ------------------------------------------------------------------ #
    # CYKL SNU
    # ------------------------------------------------------------------ #
    def start_sleep_cycle(self):
        def cycle():
            while self.running:
                time.sleep(self.sleep_interval)
                if not self.running:
                    break
                self._sleep()
        threading.Thread(target=cycle, daemon=True).start()

    def _sleep(self):
        self.status = "śpię"
        self.ui.print_animated_text(f"\n[AII] Sen: konsoliduję wiedzę...", Colors.CYAN + Colors.FAINT, delay=0.05)
        start = time.time()
        processed = 0
        for exp in self.H_log[-10:]: 
            if time.time() - start > self.max_sleep_time:
                break
            tag = exp.get('tresc', '')
            for d in self.D_Map.values():
                if tag in d.get('tagi', []):
                    d['waga_Ww'] = min(float(d.get('waga_Ww', 0)) + 1.0, 100.0)
                    processed += 1
                    
        self.energy = min(100, self.energy + 15)
        
        self.save_knowledge() 
        self.status = "myślę"
        self.prompts_since_sleep = 0
        self.ui.print_animated_text(f"[AII] Obudzony! (Skonsolidowano {processed} wag, +15% energii)", Colors.GREEN, delay=0.02)
        print("")

    # ------------------------------------------------------------------ #
    # CYKL PRACY
    # ------------------------------------------------------------------ #
    def cycle(self):
        self.load = int(np.random.randint(30, 70))
        if self.status != "śpię":
            drop = int(np.random.randint(0, 4)) if self.energy > 50 else int(np.random.randint(1, 6))
            self.energy = max(0, self.energy - drop)
        if self.energy == 0 or self.prompts_since_sleep > 5:
            self.status = "zmęczony"
        return "C", self.load, self.energy

    # ------------------------------------------------------------------ #
    # NAUCZANIE (Z KOMPRESJĄ LUB FORSOWANE) - ZINTEGROWANY MODUŁ
    # ------------------------------------------------------------------ #
    def teach(self, tag, tresc, force=False): # DODANO argument force=False
        
        # 1. Stwórz wektor dla nowych danych ($\vec{F}$)
        vec_F = self._vector_from_text(tresc)
        
        if np.linalg.norm(vec_F) == 0:
            self.ui.print_animated_text(f"[KOMPRESOR] Zignorowano (pusty wektor).", Colors.YELLOW, delay=0.01)
            return

        # 2. Oblicz korelację z "duszą" (historią Bytu)
        korelacja_historyczna = self.byt_stan.oblicz_korelacje_struny(vec_F)
        
        # 3. Akumuluj ten styk w Bycie (Byt ZAWSZE doświadcza W PAMIĘCI)
        self.byt_stan.akumuluj_styk(vec_F * 1.5) 

        # 4. DECYZJA O KOMPRESJI (Archiwizacji)
        # JEŚLI NIE JEST FORSOWANY ORAZ JEST REDUNDANTNY
        if not force and korelacja_historyczna > self.PRÓG_KOMPRESJI_ONTOLOGICZNEJ:
            # ŚCIEŻKA KOMPRESJI
            self.ui.print_animated_text(f"[KOMPRESOR] Dane redundantne. (Korelacja: {korelacja_historyczna:+.2f}). Wzmocniono Byt (w pamięci).", Colors.FAINT + Colors.CYAN, delay=0.01)
        
        else:
            # ŚCIEŻKA ARCHIWIZACJI LUB FORSOWANEGO ZAPISU
            
            # Wyczyść i przygotuj tagi
            def_id = f"Def_{len(self.D_Map)+1:03d}"
            tresc_clean_for_tags = self._normalize_text(tresc)
            words = [w.strip(".,!?;:()[]\"'") for w in tresc_clean_for_tags.split()]
            tag_clean = self._normalize_text(tag) 
            
            all_tags = [tag_clean] + words
            seen = []
            all_tags = [t for t in all_tags if t and (t not in seen and not seen.append(t))]
            
            self.D_Map[def_id] = {
                'wektor_C_Def': vec_F, 
                'waga_Ww': 5.0, 
                'tagi': all_tags,
                'tresc': tresc 
            }
            
            self.H_log.append({'h_vector': vec_F.tolist(), 'tresc': tresc, 'def_id': def_id, 'type': 'teach'})
            
            if force:
                 # Inny komunikat dla forsowanego zapisu
                 msg = f"[FORSOWANY ZAPIS] Nowa definicja {def_id}. (Korelacja: {korelacja_historyczna:+.2f})"
                 self.ui.print_animated_text(msg, Colors.YELLOW + Colors.BOLD, delay=0.01)
            else:
                 msg = f"[ZARCHIWIZOWANO] Nowa definicja {def_id}. (Korelacja: {korelacja_historyczna:+.2f})"
                 self.ui.print_animated_text(msg, Colors.GREEN + Colors.BOLD, delay=0.01)

            # 5. Zapisz JEDEN skonsolidowany plik stanu
            self.save_knowledge()

    # ------------------------------------------------------------------ #
    # EMOCJE
    # ------------------------------------------------------------------ #
    def _trigger_emotion(self, text_input):
        text_input = text_input.lower()
        found_emotion = None
        for emo_name in EMOCJE.keys():
            if emo_name in text_input:
                found_emotion = emo_name
                break 
        
        if found_emotion:
            self.emocja = found_emotion
            self.energy = max(0, min(100, self.energy + EMOCJE[found_emotion]["energia"]))
            
    def _get_emotion_prefix(self):
        if self.emocja in EMOCJE:
            emo = EMOCJE[self.emocja]
            return f"{emo['kolor']}{Colors.BLINK}{emo['ikona']}{Colors.RESET}{emo['kolor']} "
        return f"{Colors.WHITE}⚪ " 

    # ------------------------------------------------------------------ #
    # PROMPT / QUESTION
    # ------------------------------------------------------------------ #
    def prompt(self, text_input):
        self.cycle()
        
        if self.status == "śpię":
            self.energy = max(0, self.energy - 5) 
            return f"{Colors.CYAN}[AII] ... (śpię, -5 energii) ...{Colors.RESET}"
        if self.status == "zmęczony":
            self._trigger_emotion("złość")
            return f"{self._get_emotion_prefix()}[AII] Jestem zbyt zmęczony... Muszę odpocząć.{Colors.RESET}"
            
        self.prompts_since_sleep += 1
        
        # 1. Sprawdź, czy sam prompt wywołuje emocje
        self._trigger_emotion(text_input)
        
        self.ui.show_thinking_dots("Analizuję...", duration_sec=max(0.5, len(text_input) * 0.05))
        
        # 2. Stwórz wektor semantyczny z promptu
        prompt_vec = self._vector_from_text(text_input)
        
        text_input_clean = self._normalize_text(text_input)
        prompt_words = set(w.strip(".,!?;:()[]\"'") for w in text_input_clean.split())

        # 3. Oblicz korelację promptu z całą historią Bytu $\vec{S(t)}$
        korelacja_bytu = self.byt_stan.oblicz_korelacje_struny(prompt_vec)
        
        # 4. Byt "przeżywa" ten prompt - akumuluje go do swojej historii (W PAMIĘCI)
        self.byt_stan.akumuluj_styk(prompt_vec)

        # 5. Przeszukaj D_Map (Wiedzę) w poszukiwaniu najlepszej odpowiedzi
        best_score = -1
        best_match_tresc = "Nie rozumiem. Naucz mnie."
        best_match_id = None
        
        if not self.D_Map:
             self._trigger_emotion("smutek") 
             best_match_tresc = "Niczego mnie jeszcze nie nauczono."
        else:
            for def_id, d in self.D_Map.items():
                sim = np.dot(prompt_vec, d['wektor_C_Def']) 
                score_vec = sim * d['waga_Ww'] 
                
                tag_bonus = 0.0
                tag_match = prompt_words.intersection(d.get('tagi', [])) 
                if tag_match:
                    tag_bonus = len(tag_match) * 100.0 
                
                score = score_vec + tag_bonus
                
                if score > best_score:
                    best_score = score
                    best_match_tresc = d['tresc']
                    best_match_id = def_id

            SCORE_THRESHOLD = 50.0 
            
            if korelacja_bytu > 0.7:
                self.F_will = min(1.0, self.F_will + 0.1)
            elif korelacja_bytu < -0.7:
                self.F_will = max(0.0, self.F_will - 0.1)

            if best_score > SCORE_THRESHOLD: 
                self.F_will = min(1.0, self.F_will + 0.05) 
                
                if self.emocja == "neutralna":
                    if korelacja_bytu > 0.5:
                        self._trigger_emotion("radość")
                    elif korelacja_bytu < -0.5:
                         self._trigger_emotion("zdziwienie")
            else:
                self.F_will = max(0.0, self.F_will - 0.05) 
                best_match_tresc = random.choice([
                    "Nie rozumiem. Naucz mnie.", 
                    "Możesz to ująć inaczej?", 
                    "Nie mam na to dobrej odpowiedzi. Zdziwienie.",
                    "Hmm... Brak dopasowania. Spróbuj /teach."
                ])
                
                if self.emocja == "neutralna":
                    if korelacja_bytu > 0.5:
                        self._trigger_emotion("zdziwienie")
                    elif korelacja_bytu < -0.5:
                        self._trigger_emotion("smutek")
                    else:
                        self._trigger_emotion("zdziwienie")

        # 6. Sprawdź emocje na podstawie WŁASNEJ odpowiedzi AI
        self._trigger_emotion(best_match_tresc)

        # 7. Zapisz log (tylko w pamięci)
        self.H_log.append({
            'prompt': text_input, 
            'response': best_match_tresc, 
            'score_semantic': best_score, 
            'korelacja_bytu': korelacja_bytu, 
            'emotion': self.emocja,
            'type': 'prompt'
        })
        self.ostatnie_slowa = [text_input, best_match_tresc]
        
        # 8. Animate the response
        response_prefix = self._get_emotion_prefix()
        response_delay = random.uniform(0.01, 0.05) 
        
        debug_info = f"{Colors.FAINT}(Korelacja Bytu: {korelacja_bytu:+.2f}){Colors.RESET} "
        final_response = f"{response_prefix}{debug_info}{best_match_tresc}"
        
        self.ui.print_animated_text(final_response, Colors.RESET, delay=response_delay)
        return ""

    # ------------------------------------------------------------------ #
    # ŁADOWANIE WSADOWE (BATCH LOAD)
    # ------------------------------------------------------------------ #
    def batch_load(self, filename):
        """
        Wczytuje i przetwarza plik tekstowy (format: tag|tresc)
        używając funkcji self.teach().
        """
        self.ui.show_spinner(f"Rozpoczynam ładowanie wsadowe z '{filename}'...", 1.5, color=Colors.MAGENTA)
        count_processed = 0
        count_errors = 0
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            self.ui.print_animated_text(f"[LOADER] BŁĄD: Nie znaleziono pliku '{filename}'.", Colors.RED)
            return
        except Exception as e:
            self.ui.print_animated_text(f"[LOADER] BŁĄD podczas otwierania pliku: {e}", Colors.RED)
            return

        total_lines = len(lines)
        for i, line in enumerate(lines):
            sys.stdout.write(f"\r{Colors.FAINT}Przetwarzam linię {i+1}/{total_lines}...{Colors.RESET}")
            sys.stdout.flush()

            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if '|' not in line:
                count_errors += 1
                continue
            
            try:
                tag, tresc = line.split('|', 1)
                tag = tag.strip()
                tresc = tresc.strip()
                
                if not tag or not tresc:
                    count_errors += 1
                    continue
                
                sys.stdout.write("\r" + " " * (len(f"Przetwarzam linię {i+1}/{total_lines}...") + 5) + "\r")
                
                # Używamy TEACH z domyślnym force=False (z włączoną kompresją)
                self.teach(tag, tresc, force=False) 
                
                count_processed += 1
            except Exception:
                count_errors += 1
        
        sys.stdout.write("\r" + " " * (len(f"Przetwarzam linię {total_lines}/{total_lines}...") + 5) + "\r") 
        self.ui.print_animated_text(f"[LOADER] Ładowanie zakończone. Przetworzono: {count_processed} linii. Błędów/Pominięto: {count_errors}.", Colors.GREEN)

    # ------------------------------------------------------------------ #
    # STOP
    # ------------------------------------------------------------------ #
    def stop(self):
        self.ui.print_animated_text(f"\n[AII] Zapisuję ostateczny stan Bytu i Wiedzy...", Colors.YELLOW, delay=0.03)
        self.running = False
        self.save_knowledge() 
        self.ui.print_animated_text(f"[AII] Zapisano. Do widzenia!", Colors.GREEN, delay=0.03)

# ---------------------------------------------------------------------- #
# GŁÓWNA PĘTLA 
# ---------------------------------------------------------------------- #
def main():
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass 

    ui_global = FancyUI()
    
    ui_global.print_animated_text(f"--- Uruchamianie AII (Artificial Imitation of Intelligence) ---", Colors.WHITE + Colors.BOLD, delay=0.02)
    ui_global.show_planet_scan("Inicjalizuję Kula Rzeczywistości...", duration_sec=2.0, color=Colors.CYAN)
    
    ai_sphere = AII() 
    
    ui_global.print_animated_text(f"[AII] Gotowy. Energia: {ai_sphere.energy}%. Czekam na polecenia...", Colors.GREEN, delay=0.02)
    ui_global.print_animated_text(f"Wpisz /teach, /force_teach, /batchload, /status, /exit.", Colors.CYAN + Colors.FAINT, delay=0.01)

    try:
        while ai_sphere.running:
            prompt_input = input(f"{Colors.WHITE}{Colors.BOLD}> {Colors.RESET}")
            
            if not prompt_input:
                continue
                
            if prompt_input.lower() in ["/exit", "/quit", "/stop"]:
                ai_sphere.stop()
                break
            
            if prompt_input.lower() == "/save":
                ai_sphere.save_knowledge()
                ui_global.print_animated_text(f"[AII] Ręcznie zapisano stan do (AII_State.json).", Colors.GREEN, delay=0.01)
                continue
                
            if prompt_input.lower() == "/status":
                print(f"{Colors.YELLOW}--- STATUS AII ---")
                print(f"  Energia: {ai_sphere.energy}%")
                print(f"  Status: {ai_sphere.status} | Emocja: {ai_sphere.emocja} {EMOCJE.get(ai_sphere.emocja, {}).get('ikona', '')}")
                print(f"{Colors.CYAN}--- WIEDZA (D_Map) ---")
                print(f"  Definicje (zapisane): {len(ai_sphere.D_Map)}")
                print(f"  Wspomnienia (zapisane): {len(ai_sphere.H_log)}")
                print(f"{Colors.MAGENTA}--- BYT (Kula S) ---")
                print(f"  Wola (F_will): {ai_sphere.F_will:.2f} (0=Byt, 1=Wiedza)")
                print(f"  Promień Historii: {ai_sphere.byt_stan.promien_historii():.4f}")
                print(f"  Wektor Stanu S(t): {ai_sphere.byt_stan.stan.round(2)}")
                print(f"{Colors.RESET}", end="")
                continue
                
            if prompt_input.lower() == "/sleep":
                 ui_global.print_animated_text(f"[AII] Wymuszam cykl snu i zapisu...", Colors.CYAN, delay=0.02)
                 ai_sphere._sleep()
                 continue

            # Handler dla /batchload
            batch_match = re.match(r"^/batchload\s+(.+)", prompt_input, re.IGNORECASE)
            if batch_match:
                filename = batch_match.group(1).strip()
                ai_sphere.batch_load(filename)
                continue

            # Handler dla /force_teach
            force_teach_match = re.match(r"^/force_teach\s+(\w+)\s+(.+)", prompt_input, re.IGNORECASE)
            if force_teach_match:
                tag = force_teach_match.group(1)
                tresc = force_teach_match.group(2)
                ai_sphere.teach(tag, tresc, force=True) 
                continue

            # Oryginalny handler dla /teach (z włączoną kompresją)
            teach_match = re.match(r"^/teach\s+(\w+)\s+(.+)", prompt_input, re.IGNORECASE)
            if teach_match:
                tag = teach_match.group(1)
                tresc = teach_match.group(2)
                ai_sphere.teach(tag, tresc, force=False) 
                continue
            
            # --- Zwykłe pytanie ---
            ai_sphere.prompt(prompt_input) 

    except KeyboardInterrupt:
        ai_sphere.stop()
        sys.exit(0)
    except EOFError:
        ai_sphere.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
