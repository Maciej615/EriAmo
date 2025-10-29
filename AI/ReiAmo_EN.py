#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# --- Sphere of Reality Model (S) ---
# --- ENGLISH Version ---
# Author: Maciej A. Mazur
# License: CC BY-SA 4.0
#

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
    print("Warning: 'unidecode' library not found. Normalization will be basic.")
    print("Please run: pip install unidecode")
    # Zapewnia awaryjną funkcję, jeśli unidecode nie jest zainstalowane
    class UnidecodeMock:
        def unidecode(self, text):
            return text
    unidecode = UnidecodeMock()


# --- COLORS ---
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

# --- EMOTIONS (English) ---
EMOCJE = {
    "joy":       {"kolor": Colors.GREEN,   "ikona": "😊", "energia": +10},
    "anger":     {"kolor": Colors.RED,     "ikona": "😡", "energia": -15},
    "sadness":   {"kolor": Colors.BLUE,    "ikona": "😢", "energia": -20},
    "fear":      {"kolor": Colors.MAGENTA, "ikona": "😨", "energia": -10},
    "love":      {"kolor": Colors.PINK,    "ikona": "❤️", "energia": +15},
    "surprise":  {"kolor": Colors.YELLOW,  "ikona": "😮", "energia": +5},
    "neutral":   {"kolor": Colors.WHITE,   "ikona": "⚪", "energia": 0}
}

# --- FancyUI Class (Language Agnostic) ---
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
# BytS (Sphere) Class (Language Agnostic)
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
# --- AII Integrated with BytS (ENGLISH Version) ---
# ---------------------------------------------------------------------- #
class AII:

    # --- ENGLISH AXES (Landscape P) ---
    AXES_KEYWORDS = {
        # Axis 0: Logic / Reason
        "logic": ["logic", "logical", "sense", "reason", "why", "because", "result", "fact"],
        # Axis 1: Emotion / Feeling
        "emotion": ["feel", "emotion", "love", "anger", "sadness", "joy", "fear", "feeling"],
        # Axis 2: Being / Ontology (Sphere Model)
        "being": ["being", "existence", "i", "am", "is", "sphere", "reality", "history", "ontology", "name", "reiamo"],
        # Axis 3: Action / Conflict (Will, W40k)
        "action": ["fight", "action", "conflict", "war", "force", "enemy", "chaos", "will", "do", "make"],
        # Axis 4: Creation / Art
        "creation": ["create", "art", "build", "music", "write", "new", "beauty", "design"],
        # Axis 5: Knowledge / Information
        "knowledge": ["knowledge", "science", "teach", "data", "information", "what", "who", "how"],
        # Axis 6: Time / History
        "time": ["time", "when", "past", "now", "future", "history", "step", "path", "today", "tomorrow"],
        # Axis 7: Space / Landscape
        "space": ["where", "place", "landscape", "road", "world", "direction", "location", "here", "there"]
    }
    # Normalize keywords for robust matching
    AXES_KEYWORDS_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in AXES_KEYWORDS.items()}
    AXES_ORDER = ["logic", "emotion", "being", "action", "creation", "knowledge", "time", "space"]
    
    # Ontological Compression Threshold
    ONTOLOGICAL_COMPRESSION_THRESHOLD = 0.98

    def __init__(self):
        self.D_Map = {}     
        self.H_log = []     
        self.energy = 100
        self.load = 0
        self.status = "thinking" # Translated
        self.emocja = "neutral"  # Translated
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
        
        self.load_knowledge() # Loads from the _EN.json file
        self.start_sleep_cycle()

    # ------------------------------------------------------------------ #
    # Text Normalization Utility
    # ------------------------------------------------------------------ #
    def _normalize_text(self, text):
        """Converts text to lowercase, ASCII, and removes special chars."""
        try:
            text_lower = text.lower()
            text_ascii = unidecode.unidecode(text_lower) 
            text_clean = re.sub(r'[^\w\s_]', '', text_ascii)
            return text_clean
        except Exception as e:
            print(f"{Colors.RED}Text normalization error: {e}{Colors.RESET}")
            return text.lower() 

    # ------------------------------------------------------------------ #
    # Vectorization (Language Agnostic, uses AXES_KEYWORDS_ASCII)
    # ------------------------------------------------------------------ #
    def _vector_from_text(self, text):
        """Creates a semantic vector by projecting text onto the P-Landscape axes."""
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
    # ### SEPARATE ENGLISH SAVE FILE ###
    # ------------------------------------------------------------------ #
    def save_knowledge(self):
        """Saves the entire AI state to a single, consolidated EN file."""
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
            # Save to the _EN.json file
            with open("data/AII_State_EN.json", "w", encoding="utf-8") as f:
                json.dump(master_state, f, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}[SAVE ERROR] Failed to save state: {e}{Colors.RESET}") # Translated

    # ------------------------------------------------------------------ #
    # ### SEPARATE ENGLISH LOAD FILE ###
    # ------------------------------------------------------------------ #
    def load_knowledge(self):
        """Loads the entire AI state from the single _EN.json file."""
        os.makedirs("data", exist_ok=True)
        
        try:
            # Load from the _EN.json file
            with open("data/AII_State_EN.json", encoding="utf-8") as f:
                master_state = json.load(f)
        except Exception:
            self.D_Map = {}
            self.H_log = []
            self.byt_stan = BytS(wymiary=self.wymiary)
            self.F_will = 0.5
            return 
        
        # Unpack D_Map
        try:
            data = master_state.get('D_Map_Data', {})
            self.D_Map = {k: {
                'wektor_C_Def': np.array(v['wektor_C_Def'], dtype=float),
                'waga_Ww': float(v['waga_Ww']),
                'tagi': v['tagi'],
                'tresc': v.get('tresc', 'NO CONTENT') # Translated
            } for k, v in data.items()}
        except Exception:
            self.D_Map = {}
            
        # Unpack H_log
        self.H_log = master_state.get('H_Log_Data', [])
            
        # Unpack Byt_Stan
        try:
            data = master_state.get('Byt_Stan_Data', {})
            stan_vector = np.array(data.get('stan', []), dtype=float)
            
            if stan_vector.shape == (self.wymiary,):
                self.byt_stan.stan = stan_vector
            else:
                if data: 
                    # Translated
                    print(f"{Colors.RED}[ERROR] Byt dimension in file ({stan_vector.shape}) mismatch with model ({self.wymiary,}). Resetting Byt.{Colors.RESET}")
                self.byt_stan = BytS(wymiary=self.wymiary)
                
            self.F_will = float(data.get('F_will', 0.5))
        except Exception:
            self.byt_stan = BytS(wymiary=self.wymiary)
            self.F_will = 0.5
            
    # ------------------------------------------------------------------ #
    # SLEEP CYCLE
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
        self.status = "sleeping" # Translated
        self.ui.print_animated_text(f"\n[AII] Sleep: consolidating knowledge...", Colors.CYAN + Colors.FAINT, delay=0.05) # Translated
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
        
        self.save_knowledge() # Saves the _EN.json file
        self.status = "thinking" # Translated
        self.prompts_since_sleep = 0
        self.ui.print_animated_text(f"[AII] Awake! (Consolidated {processed} weights, +15% energy)", Colors.GREEN, delay=0.02) # Translated
        print("")

    # ------------------------------------------------------------------ #
    # CYCLE
    # ------------------------------------------------------------------ #
    def cycle(self):
        self.load = int(np.random.randint(30, 70))
        if self.status != "sleeping":
            drop = int(np.random.randint(0, 4)) if self.energy > 50 else int(np.random.randint(1, 6))
            self.energy = max(0, self.energy - drop)
        if self.energy == 0 or self.prompts_since_sleep > 5:
            self.status = "tired" # Translated
        return "C", self.load, self.energy

    # ------------------------------------------------------------------ #
    # TEACHING (with Ontological Compression)
    # ------------------------------------------------------------------ #
    def teach(self, tag, tresc):
        
        # 1. Create vector for new data ($\vec{F}$)
        vec_F = self._vector_from_text(tresc)
        
        if np.linalg.norm(vec_F) == 0:
            self.ui.print_animated_text(f"[COMPRESSOR] Ignored (empty vector).", Colors.YELLOW, delay=0.01) # Translated
            return

        # 2. Calculate correlation with Byt's history
        korelacja_historyczna = self.byt_stan.oblicz_korelacje_struny(vec_F)
        
        # 3. Byt always experiences the interaction (in RAM)
        self.byt_stan.akumuluj_styk(vec_F * 1.5) 

        # 4. Compression Decision (Archiving)
        if korelacja_historyczna > self.ONTOLOGICAL_COMPRESSION_THRESHOLD:
            # --- COMPRESSION PATH ---
            # Data is semantically redundant.
            self.ui.print_animated_text(f"[COMPRESSOR] Redundant data. (Correlation: {korelacja_historyczna:+.2f}). Byt strengthened (in memory).", Colors.FAINT + Colors.CYAN, delay=0.01) # Translated
        
        else:
            # --- ARCHIVING PATH ---
            # Data is "new". Save it to the "Brain" (D_Map).
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
                'tresc': tresc # Save the ORIGINAL content
            }
            
            self.H_log.append({'h_vector': vec_F.tolist(), 'tresc': tresc, 'def_id': def_id, 'type': 'teach'})
            
            self.ui.print_animated_text(f"[ARCHIVED] New definition {def_id}. (Correlation: {korelacja_historyczna:+.2f})", Colors.GREEN + Colors.BOLD, delay=0.01) # Translated

            # 5. Save the consolidated state file
            self.save_knowledge() # Only saves to disk when new info is learned

    # ------------------------------------------------------------------ #
    # EMOTIONS (Responds to English keys)
    # ------------------------------------------------------------------ #
    def _trigger_emotion(self, text_input):
        text_input = text_input.lower()
        found_emotion = None
        for emo_name in EMOCJE.keys(): # Keys are now "joy", "anger", etc.
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
        
        if self.status == "sleeping":
            self.energy = max(0, self.energy - 5) 
            return f"{Colors.CYAN}[AII] ... (sleeping, -5 energy) ...{Colors.RESET}" # Translated
        if self.status == "tired":
            self._trigger_emotion("anger")
            return f"{self._get_emotion_prefix()}[AII] I am too tired... Must rest.{Colors.RESET}" # Translated
            
        self.prompts_since_sleep += 1
        
        # 1. Trigger emotion from prompt
        self._trigger_emotion(text_input)
        
        self.ui.show_thinking_dots("Analyzing...", duration_sec=max(0.5, len(text_input) * 0.05)) # Translated
        
        # 2. Create semantic vector from prompt
        prompt_vec = self._vector_from_text(text_input)
        
        text_input_clean = self._normalize_text(text_input)
        prompt_words = set(w.strip(".,!?;:()[]\"'") for w in text_input_clean.split())

        # 3. Calculate correlation with Byt's history
        korelacja_bytu = self.byt_stan.oblicz_korelacje_struny(prompt_vec)
        
        # 4. Byt experiences the prompt (in RAM)
        self.byt_stan.akumuluj_styk(prompt_vec)

        # 5. Search D_Map (Knowledge) for the best answer
        best_score = -1
        best_match_tresc = "I don't understand. Teach me." # Translated
        best_match_id = None
        
        if not self.D_Map:
             self._trigger_emotion("sadness") 
             best_match_tresc = "I haven't been taught anything yet." # Translated
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
                # FOUND MATCH in D_Map
                self.F_will = min(1.0, self.F_will + 0.05) 
                
                if self.emocja == "neutral":
                    if korelacja_bytu > 0.5:
                        self._trigger_emotion("joy")
                    elif korelacja_bytu < -0.5:
                         self._trigger_emotion("surprise")
            else:
                # NO MATCH in D_Map
                self.F_will = max(0.0, self.F_will - 0.05) 
                best_match_tresc = random.choice([ # Translated
                    "I don't understand. Teach me.", 
                    "Can you phrase that differently?", 
                    "I don't have a good answer for that. Surprise.",
                    "Hmm... No match. Try /teach."
                ])
                
                if self.emocja == "neutral":
                    if korelacja_bytu > 0.5:
                        self._trigger_emotion("surprise")
                    elif korelacja_bytu < -0.5:
                        self._trigger_emotion("sadness")
                    else:
                        self._trigger_emotion("surprise")

        # 6. Trigger emotion based on AI's OWN response
        self._trigger_emotion(best_match_tresc)

        # 7. Log the interaction (in memory)
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
        
        debug_info = f"{Colors.FAINT}(Byt Correlation: {korelacja_bytu:+.2f}){Colors.RESET} " # Translated
        final_response = f"{response_prefix}{debug_info}{best_match_tresc}"
        
        self.ui.print_animated_text(final_response, Colors.RESET, delay=response_delay)
        return ""

    # ------------------------------------------------------------------ #
    # STOP
    # ------------------------------------------------------------------ #
    def stop(self):
        self.ui.print_animated_text(f"\n[AII] Saving final Byt and Knowledge state...", Colors.YELLOW, delay=0.03) # Translated
        self.running = False
        self.save_knowledge() 
        self.ui.print_animated_text(f"[AII] Saved. Goodbye!", Colors.GREEN, delay=0.03) # Translated

# ---------------------------------------------------------------------- #
# MAIN LOOP (Translated)
# ---------------------------------------------------------------------- #
def main():
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass 

    ui_global = FancyUI()
    
    ui_global.print_animated_text(f"--- Booting AII (Artificial Imitation of Intelligence) ---", Colors.WHITE + Colors.BOLD, delay=0.02)
    ui_global.show_planet_scan("Initializing Sphere of Reality...", duration_sec=2.0, color=Colors.CYAN)
    
    ai_sphere = AII() 
    
    ui_global.print_animated_text(f"[AII] Ready. Energy: {ai_sphere.energy}%. Waiting for commands...", Colors.GREEN, delay=0.02)
    ui_global.print_animated_text(f"Type /teach [tag] [content], /status, /save, /exit or ask a question.", Colors.CYAN + Colors.FAINT, delay=0.01)

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
                ui_global.print_animated_text(f"[AII] State manually saved to (AII_State_EN.json).", Colors.GREEN, delay=0.01)
                continue
                
            if prompt_input.lower() == "/status":
                print(f"{Colors.YELLOW}--- AII STATUS ---")
                print(f"  Energy: {ai_sphere.energy}%")
                print(f"  Status: {ai_sphere.status} | Emotion: {ai_sphere.emocja} {EMOCJE.get(ai_sphere.emocja, {}).get('ikona', '')}")
                print(f"{Colors.CYAN}--- KNOWLEDGE (D_Map) ---")
                print(f"  Definitions (archived): {len(ai_sphere.D_Map)}")
                print(f"  Memories (archived): {len(ai_sphere.H_log)}")
                print(f"{Colors.MAGENTA}--- BEING (Sphere S) ---")
                print(f"  Will (F_will): {ai_sphere.F_will:.2f} (0=Byt, 1=Knowledge)")
                print(f"  History Radius: {ai_sphere.byt_stan.promien_historii():.4f}")
                print(f"  State Vector S(t): {ai_sphere.byt_stan.stan.round(2)}")
                print(f"{Colors.RESET}", end="")
                continue
                
            if prompt_input.lower() == "/sleep":
                 ui_global.print_animated_text(f"[AII] Forcing sleep and save cycle...", Colors.CYAN, delay=0.02)
                 ai_sphere._sleep()
                 continue

            teach_match = re.match(r"^/teach\s+(\w+)\s+(.+)", prompt_input, re.IGNORECASE)
            if teach_match:
                tag = teach_match.group(1)
                tresc = teach_match.group(2)
                ai_sphere.teach(tag, tresc)
                continue
            
            # --- Standard prompt ---
            ai_sphere.prompt(prompt_input) 

    except KeyboardInterrupt:
        ai_sphere.stop()
        sys.exit(0)
    except EOFError:
        ai_sphere.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()
