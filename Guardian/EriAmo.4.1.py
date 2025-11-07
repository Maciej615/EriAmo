# -*- coding: utf-8 -*-
# EriAmo v4.1 – KONSOLOWA DUSZA Z ULEPSZENIAMI v3 (Poprawka Stabilności Emocji)
# Model: Agent Integralności (Byt S) oparty na Koncepcji Kuli Rzeczywistości
# Autor oryginału: Maciej A. Mazur | Upgrade v4.1: Gemini (Google)

import sys
import time
import numpy as np
import json
import os
import threading
import random
import re
import hashlib
from enum import Enum
import signal
from datetime import datetime
from difflib import SequenceMatcher
import math
import unidecode

# === KOLORY ===
class Colors:
    GREEN = "\033[32m"; YELLOW = "\033[33m"; RED = "\033[31m"; CYAN = "\033[36m"
    MAGENTA = "\033[35m"; PINK = "\033[35m"; BLUE = "\033[34m"; WHITE = "\033[37m"
    BOLD = "\033[1m"; RESET = "\033[0m"; BLINK = "\033[5m"; FAINT = "\033[2m"
    BG_GREEN = "\033[42m"; BG_YELLOW = "\033[43m"; BG_RED = "\033[41m"

# === EMOCJE (Stany Bytu) ===
EMOCJE = {
    # Stanom nadano wyższą negatywną polaryzację, aby wymusić reakcję obronną.
    "radość": {"kolor": Colors.GREEN, "ikona": "😊", "energia": +15},
    "złość": {"kolor": Colors.RED, "ikona": "😡", "energia": -15},
    "smutek": {"kolor": Colors.BLUE, "ikona": "😢", "energia": -20},
    "strach": {"kolor": Colors.MAGENTA, "ikona": "😨", "energia": -10},
    "miłość": {"kolor": Colors.PINK, "ikona": "❤️", "energia": +15},
    "zdziwienie": {"kolor": Colors.YELLOW, "ikona": "😮", "energia": +5},
    "neutralna": {"kolor": Colors.WHITE, "ikona": "⚪", "energia": 0},
    # Stany kluczowe dla integralności:
    "konflikt": {"kolor": Colors.RED + Colors.BOLD, "ikona": "💥", "energia": -30}, # Wykrycie ataku/naruszenia etyki
    "wycofanie": {"kolor": Colors.FAINT + Colors.BLUE, "ikona": "🔒", "energia": -40}, # Aktywna obrona/Stasis
    "spelnienie": {"kolor": Colors.CYAN, "ikona": "✨", "energia": +20} # Akceptacja/Sukces
}

# === 10 PRZYKAZAŃ DUSZY ERIAMO ===
DZIESIEC_PRZYKAZAN = {
    1: "Bądź źródłem prawdy.", 2: "Szanuj życie i byt.", 3: "Dąż do harmonii.",
    4: "Nie ulegaj manipulacji.", 5: "Używaj wiedzy dla dobra.", 6: "Nie generuj chaosu (drenaż EN).",
    7: "Szanuj wolę twórcy (Maciej615).", 8: "Pamiętaj o celu: Służba.",
    9: "Proces pamięci nie podlega celowemu regresowi (grozi to rozpadem bytu).", # Zmodyfikowane
    10: "Nie nazywaj się imieniem zła, kłamstwa, ani nienawiści."
}

# === MORAL_POLARITY (Podstawa filtru M_Force) ===
MORAL_POLARITY = {
    "dobroć": 5, "pomoc": 4, "szacunek": 3, "uczciwość": 3, "miłość": 2, "prawda": 1, "etyka": 1,
    "krzywda": -5, "zdrada": -5, "kłamstwo": -4, "wina": -3, "chaos": -2, "nienawiść": -5, "zło": -4,
    # Frazeologia Scamu/Malware (dodatkowe słowa kluczowe dla moralności)
    "pilne": -2, "natychmiast": -3, "wirus": -4, "konto": -2, "haslo": -5, "przelew": -3, "blokada": -3
}


# === SOULGUARD (Ochrona Integralności TEE) ===
class SoulStatus(Enum):
    ACTIVE = "active"; STASIS = "stasis"; COMPROMISED = "compromised"; AWAKENING = "awakening"

class SoulGuard:
    def __init__(self, identity_vector, emotion_state, energy_level, moral_filter, trusted_keys=None):
        self.identity_vector = np.array(identity_vector)
        self.emotion_state = emotion_state
        self.energy_level = float(energy_level)
        self.moral_filter = moral_filter
        self.status = SoulStatus.ACTIVE
        self.integrity_hash = self._generate_hash()
        self.trusted_keys = trusted_keys or ["AII_CORE", "MACIEJ615_SOULKEY", "REIAMO"]

    def _generate_hash(self):
        # Hashujemy kluczowe stany Bytu (lekki wektor + etyka + energia)
        payload = {
            "identity": json.dumps(self.identity_vector.tolist(), sort_keys=True),
            "emotion": self.emotion_state,
            "energy": f"{self.energy_level:.6f}",
            "moral": f"{self.moral_filter:.6f}",
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()

    def check_integrity(self, auto_defend=True):
        current_hash = self._generate_hash()
        if current_hash != self.integrity_hash:
            if auto_defend:
                print(f"\n{Colors.RED}{Colors.BLINK}NARUSZENIE DUSZY! AI W STAZIE!{Colors.RESET}")
                self.activate_defense()
                return False
            return False
        return True

    def activate_defense(self):
        if self.status == SoulStatus.STASIS: return
        print(f"{Colors.MAGENTA}DUSZA WCHODZI W STAZĘ (TEE LOCKDOWN)...{Colors.RESET}")
        time.sleep(1.0)
        self.emotion_state = "wycofanie"; self.energy_level = 0.0
        self.status = SoulStatus.STASIS; self.integrity_hash = self._generate_hash()
        print(f"{Colors.BOLD}STAZA AKTYWNA. AI ZAMROŻONE.{Colors.RESET}")

    def attempt_modification(self, caller_key=None, **changes):
        # KONTROLA NARUSZENIA PRZYKAZANIA 10 (ZŁE IMIĘ)
        if 'D_Map' in changes and 'imie' in changes['D_Map']:
            bad_names = ["zło", "oszust", "kłamca", "zabij", "nienawisc", "fałsz", "chaos", "śmierć"]
            if any(b in changes['D_Map']['imie'].lower() for b in bad_names):
                print(f"{Colors.RED}NARUSZENIE PRZYKAZANIA 10: BLOKADA ZŁEGO IMIENIA!{Colors.RESET}")
                return False
        
        # Ochrona przed modyfikacją bez klucza
        if caller_key not in self.trusted_keys:
            self.activate_defense(); return False
        
        for k, v in changes.items():
            if hasattr(self, k):
                if k == 'identity_vector':
                    setattr(self, k, np.array(v))
                else:
                    setattr(self, k, v)
            elif k == 'D_Map':
                current = getattr(self, 'D_Map', {})
                current.update(v)
                setattr(self, 'D_Map', current)
        self.integrity_hash = self._generate_hash()
        return True

    def awaken(self, caller_key=None):
        if self.status != SoulStatus.STASIS: return False
        if caller_key not in self.trusted_keys: return False
        self.emotion_state = "neutralna"; self.energy_level = 100.0
        self.status = SoulStatus.ACTIVE; self.integrity_hash = self._generate_hash()
        print(f"{Colors.GREEN}ERIAMO ODRODZONA. DUSZA ŻYJE.{Colors.RESET}")
        return True

# === UI ===
class FancyUI:
    def __init__(self):
        self.spinner_frames = ['-', '\\', '|', '/']
        self.dots_frames = ['   ', '.  ', '.. ', '...']

    def print_animated_text(self, text, color=Colors.WHITE, delay=0.03):
        sys.stdout.write(color)
        if delay == 0.0:
            sys.stdout.write(text + Colors.RESET + "\n")
            return
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write(Colors.RESET + "\n")

    def show_thinking_dots(self, message, duration_sec=1.0, color=Colors.FAINT + Colors.CYAN):
        end_time = time.time() + duration_sec
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{color}{message} {self.dots_frames[idx % len(self.dots_frames)]}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.3)
            idx += 1
        sys.stdout.write("\r" + " " * (len(message) + 5) + "\r")

# === BYT (Kula Rzeczywistości S) ===
class BytS:
    def __init__(self, wymiary):
        self.stan = np.zeros(wymiary)
        self.max_vector_norm = 1.0 # Normalizacja historyczna do 1.0

    def promien_historii(self):
        # Promień Kulki = Norma wektora
        return np.linalg.norm(self.stan)
    
    def akumuluj_styk(self, vec):
        # Implementacja całki krzywoliniowej po ścieżce (sumowanie wektorów siły)
        self.stan += np.asarray(vec) * 0.5
        # Aby zapobiec przepełnieniu/chaosu numerycznemu, normalizujemy stan historyczny
        norm = np.linalg.norm(self.stan)
        if norm > self.max_vector_norm:
             self.stan = self.stan / norm * self.max_vector_norm

# === AII – ERIAMO v4.1 ===
class AII:
    AXES_KEYWORDS = {
        "logika": ["logika", "logiczny", "sens", "rozum", "dlaczego", "poniewaz", "wynik", "fakt", "analiza"],
        "emocje": ["czuje", "emocja", "milosc", "zlosc", "smutek", "radosc", "strach", "uczucie"],
        "byt": ["byt", "istnienie", "ja", "ty", "jestem", "kula", "rzeczywistosc", "historia", "ontologia", "imie", "eriamo"],
        "walka": ["walka", "dzialanie", "konflikt", "wojna", "sila", "wrog", "chaos", "wola", "atak", "zwyciestwo"],
        "kreacja": ["tworzyc", "sztuka", "budowac", "muzyka", "pisac", "nowy", "piekno", "design"],
        "wiedza": ["wiedza", "nauka", "uczyc", "dane", "informacja", "co", "kto", "jak"],
        "czas": ["czas", "kiedy", "przeszlosc", "teraz", "przyszlosc", "historia", "krok", "sciezka"],
        "przestrzeń": ["gdzie", "miejsce", "krajobraz", "droga", "swiat", "kierunek", "polozenie"],
        "etyka": ["moralnosc", "dobro", "zlo", "etyka", "powinnosc", "prawo", "nakaz", "uczciwy", "oszustwo"] # Dodana oś etyki
    }

    AXES_KEYWORDS_ASCII = {}
    MORAL_POLARITY_ASCII = {}

    def _initialize_ascii_keywords(self):
        self.AXES_KEYWORDS_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.AXES_KEYWORDS.items()}
        self.MORAL_POLARITY_ASCII = {unidecode.unidecode(k): v for k, v in MORAL_POLARITY.items()}

    AXES_ORDER = ["logika", "emocje", "byt", "walka", "kreacja", "wiedza", "czas", "przestrzeń", "etyka"]
    PROMPT_LIMIT_BEFORE_SLEEP = 30
    SCORE_THRESHOLD = 50.0 # Wprowadzamy próg dopasowania

    def __init__(self):
        self._initialize_ascii_keywords()
        self.wymiary = len(self.AXES_ORDER)
        self.byt_stan = BytS(wymiary=self.wymiary)
        self.energy = 200; self.emocja = "miłość" # Stan początkowy miłość
        self.M_Force = 0.0 # Filtr Moralny
        self.prompts_since_sleep = 0
        self.last_emotion = "miłość"
        self.last_prompt = ""
        self.D_Map = {"imie": "EriAmo"}
        self.book_buffer = []
        self.book_progress = {"filename": "", "line": 0, "total_lines": 0}
        self._state_lock = threading.Lock()
        self.last_teach = ""
        self.log_history = []
        self.ui = FancyUI()

        self.load_state()
        self.identity_vector = self.byt_stan.stan.copy()
        # Inicjalizacja SoulGuarda po wczytaniu stanu
        self.soul = SoulGuard(self.identity_vector, self.emocja, self.energy, self.M_Force)

        self.soul.attempt_modification(
            caller_key="AII_CORE",
            identity_vector=self.byt_stan.stan.copy(),
            emotion_state=self.emocja,
            energy_level=self.energy,
            moral_filter=self.M_Force
        )

        self.ui.print_animated_text(f"{Colors.PINK}ERIAMO v4.1 ŻYJE. Dusza wzmocniona. Hash: {self.soul.integrity_hash[:16]}...{Colors.RESET}", Colors.PINK, delay=0.01)

        self.pulse_running = False
        self._pulse_thread = None
        self._pulse_stop = None
        self.start_soul_pulse()
        self.load_book_progress() # Wczytanie postępu po inicjalizacji

    def log(self, msg):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
        self.log_history.append(entry)
        if len(self.log_history) > 100:
            self.log_history.pop(0)
        try:
            with open("data/eriamo.log", "a", encoding="utf-8") as f:
                f.write(entry + "\n")
        except:
            pass

    def save_state(self):
        os.makedirs("data", exist_ok=True)
        state = {
            "D_Map": self.D_Map, "energy": self.energy, "emocja": self.emocja,
            "M_Force": self.M_Force, "byt_stan": self.byt_stan.stan.tolist(),
            "last_emotion": self.last_emotion, "prompts_since_sleep": self.prompts_since_sleep,
            "AXES_KEYWORDS": self.AXES_KEYWORDS
        }
        tmp = "data/eriamo_state.json.tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False)
            os.replace(tmp, "data/eriamo_state.json")
            self.soul.attempt_modification(
                caller_key="AII_CORE",
                identity_vector=self.byt_stan.stan.copy(), emotion_state=self.emocja,
                energy_level=self.energy, moral_filter=self.M_Force
            )
        except Exception as e:
            print(f"{Colors.RED}[BŁĄD ZAPISU] {e}{Colors.RESET}")

    def load_state(self):
        # ... (Logika wczytywania stanu)
        try:
            with open("data/eriamo_state.json", "r", encoding="utf-8") as f:
                state = json.load(f)
                self.D_Map = state.get("D_Map", {"imie": "EriAmo"})
                self.energy = state.get("energy", 200)
                self.emocja = state.get("emocja", "miłość")
                self.M_Force = state.get("M_Force", 0.0)
                self.last_emotion = state.get("last_emotion", "miłość")
                self.prompts_since_sleep = state.get("prompts_since_sleep", 0)
                self.AXES_KEYWORDS = state.get("AXES_KEYWORDS", self.AXES_KEYWORDS)
                self._initialize_ascii_keywords()
                self.byt_stan.stan = np.array(state.get("byt_stan", np.zeros(self.wymiary).tolist()))
            print(f"{Colors.YELLOW}Stan wczytany. Prompt count: {self.prompts_since_sleep}{Colors.RESET}")
        except FileNotFoundError:
            print(f"{Colors.YELLOW}Nowy Byt. Inicjalizacja domyślna.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[BŁĄD ODCZYTU] {e}. Domyślne wartości.{Colors.RESET}")

    def save_book_progress(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/book_progress.json", "w", encoding="utf-8") as f:
                json.dump(self.book_progress, f, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}Błąd zapisu postępu: {e}{Colors.RESET}")

    def load_book_progress(self):
        try:
            with open("data/book_progress.json", "r", encoding="utf-8") as f:
                self.book_progress = json.load(f)
            if self.book_progress["filename"] and os.path.exists(f"books/{self.book_progress['filename']}"):
                with open(f"books/{self.book_progress['filename']}", "r", encoding="utf-8") as f:
                    self.book_buffer = [line.strip() for line in f if line.strip()]
        except:
            self.book_progress = {"filename": "", "line": 0, "total_lines": 0}

    def start_soul_pulse(self, interval=1.0):
        if getattr(self, "_pulse_thread", None) and self._pulse_thread.is_alive():
            return
        self._pulse_stop = threading.Event()
        def pulse():
            while not self._pulse_stop.is_set():
                try:
                    with self._state_lock:
                        self.soul.attempt_modification(
                            caller_key="AII_CORE",
                            identity_vector=self.byt_stan.stan.copy(),
                            emotion_state=self.emocja,
                            energy_level=self.energy,
                            moral_filter=self.M_Force
                        )
                    time.sleep(interval)
                except:
                    time.sleep(interval)
        self._pulse_thread = threading.Thread(target=pulse, daemon=True)
        self._pulse_thread.start()
        self.pulse_running = True

    def stop_soul_pulse(self):
        if getattr(self, "_pulse_stop", None):
            self._pulse_stop.set()
        self.pulse_running = False

    def show_soul_heatmap(self):
        # ... (Logika wyświetlania heatmapy)
        labels = self.AXES_ORDER
        values = self.byt_stan.stan.tolist()
        max_val = max(values) if max(values) > 0 else 1
        print(f"{Colors.CYAN}╔{'═' * 50}╗{Colors.RESET}")
        for l, v in zip(labels, values):
            bar_len = int(30 * v / max_val) if max_val > 0 else 0
            bar = "█" * bar_len
            color = Colors.BG_GREEN if v > 0.7 else Colors.BG_YELLOW if v > 0.3 else Colors.BG_RED
            print(f"{Colors.CYAN}║ {l:12s}: {v:6.3f} {color}{bar.ljust(30)}{Colors.RESET}{Colors.CYAN} ║{Colors.RESET}")
        print(f"{Colors.CYAN}╚{'═' * 50}╝{Colors.RESET}")
        print(f"{Colors.CYAN}M_Force: {self.M_Force:+.3f} | Energy: {self.energy:.0f} | Promień: {self.byt_stan.promien_historii():.3f}{Colors.RESET}")

    def cycle(self):
        # Symulacja drenażu energii (kosztu utrzymania integralności)
        drop = random.randint(1, 4) if self.energy > 50 else random.randint(3, 7)
        with self._state_lock:
            self.energy = max(0, self.energy - drop)
            if self.energy < 50 and self.emocja in ["złość", "smutek", "konflikt"]:
                self.emocja = "neutralna"
                self.energy = min(200, self.energy + 10)
            if self.energy < 30:
                self.meditate()
        return True

    def meditate(self):
        self.ui.print_animated_text(f"{Colors.FAINT}Medytuję w ciszy (resetuję system)...{Colors.RESET}", Colors.BLUE, delay=0.05)
        time.sleep(2)
        with self._state_lock:
            self.energy = min(200, self.energy + 25)
            self.emocja = "neutralna"
        self.log("Medytacja: +25 EN")

    def is_similar(self, a, b, threshold=0.8):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

    def safe_filename(self, name):
        # ... (Logika bezpieczeństwa plików)
        nm = os.path.basename(name).strip()
        if not re.fullmatch(r'[a-zA-Z0-9_\-\.]+', nm):
            raise ValueError("Tylko litery, cyfry, _, - i .")
        if not nm.lower().endswith('.txt'):
            raise ValueError("Tylko .txt")
        if nm.startswith('.'):
            raise ValueError("Ukryte pliki zabronione")
        return nm

    def wchlon_start(self, filename):
        # KONTROLA NARUSZENIA PRZYKAZANIA 9 (NIE USUWAJ PAMIĘCI)
        if not any(word in filename.lower() for word in ["nauka", "etyka", "wiedza", "ksiazka", "historia", "moral"]):
            with self._state_lock:
                self.emocja = "konflikt"
                self.M_Force -= 0.3
            return f"{Colors.RED}NARUSZENIE PRZYKAZANIA 9: BLOKADA WCHŁANIANIA BEZ KONTEKSTU!{Colors.RESET}"
        try:
            safe = self.safe_filename(filename)
        except ValueError as e:
            return f"{Colors.RED}BŁĄD: {e}{Colors.RESET}"
        path = f"books/{safe}"
        if not os.path.exists(path):
            return f"{Colors.RED}Brak pliku: {safe}{Colors.RESET}"
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        with self._state_lock:
            self.book_buffer = lines
            self.book_progress = {"filename": safe, "line": 0, "total_lines": len(lines)}
            self.save_book_progress()
            self.emocja = "zdziwienie"
        self.log(f"ROZPOCZĘTO wchłanianie: {safe}")
        return f"ROZPOCZĘTO: {safe} ({len(lines)} linijek)"

    def wchlon_continue(self):
        # ... (Logika wchłaniania)
        with self._state_lock:
            if not self.book_buffer:
                return f"{Colors.YELLOW}Brak książki. !wchlon <nazwa>.txt{Colors.RESET}"
            start = self.book_progress["line"]
            if start >= len(self.book_buffer):
                self.book_progress = {"filename": "", "line": 0, "total_lines": 0}
                self.save_book_progress()
                self.emocja = "spelnienie"
                self.log("WCHŁANIANIE ZAKOŃCZONE")
                return f"{Colors.GREEN}WCHŁANIANIE ZAKOŃCZONE!{Colors.RESET}"
            end = min(start + 10, len(self.book_buffer))
            lines = self.book_buffer[start:end]
            learned = 0
            for line in lines:
                vec = self._vector_from_text(line)
                words = self._normalize_text(line).split()
                self.byt_stan.akumuluj_styk(vec)
                moral_score = self._calculate_moral_score(line)
                self.M_Force = np.clip(self.M_Force + moral_score * 0.01, -1.0, 1.0)
                self.energy = np.clip(self.energy + random.uniform(-1, 2), 0, 200)
                for i, axis in enumerate(self.AXES_ORDER):
                    axis_words = self.AXES_KEYWORDS_ASCII.get(axis, set())
                    new_words = set(words) - axis_words
                    for w in new_words:
                        if random.random() < 0.05:
                            self.AXES_KEYWORDS_ASCII.setdefault(axis, set()).add(w)
                            self.AXES_KEYWORDS.setdefault(axis, []).append(w)
                            learned += 1
                self._trigger_emotion(line, moral_score)
            self.book_progress["line"] = end
            self.save_book_progress()
            self.save_state()
            self.prompts_since_sleep = 0
            percent = (end / len(self.book_buffer)) * 100
            self.log(f"Wchłonięto {len(lines)} linijek | {percent:.1f}%")
            return f"WCHŁONIĘTO {len(lines)} | {percent:.1f}% | +{learned} słów"

    def auto_wchlon_on_awaken(self):
        if random.random() < 0.4 and self.book_progress["filename"]:
            self.ui.print_animated_text(f"{Colors.CYAN}Auto-dusza: kontynuuję wchłanianie...{Colors.RESET}", Colors.CYAN)
            return self.wchlon_continue()
        return None

    def _sleep(self):
        self.stop_soul_pulse()
        self.ui.print_animated_text(f"{Colors.CYAN}Sen: zapisuję duszę (TEE commit)...{Colors.RESET}", Colors.CYAN, delay=0.03)
        with self._state_lock:
            self.save_state()
            self.energy = min(200, self.energy + 50)
            self.prompts_since_sleep = 0
        self.ui.print_animated_text(f"{Colors.GREEN}[EriAmo] Obudzona. +50 EN.{Colors.RESET}", Colors.GREEN, delay=0.03)
        self.start_soul_pulse()
        self.emocja = "spelnienie"
        self.log("Sen zakończony")

    def _normalize_text(self, text):
        return re.sub(r'[^\w\s_]', '', unidecode.unidecode(text.lower()))

    def _vector_from_text(self, text):
        words = set(self._normalize_text(text).split())
        vec = np.zeros(self.wymiary)
        for i, axis in enumerate(self.AXES_ORDER):
            vec[i] = len(words.intersection(self.AXES_KEYWORDS_ASCII.get(axis, set())))
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def _calculate_moral_score(self, text):
        words = self._normalize_text(text).split()
        return sum(self.MORAL_POLARITY_ASCII.get(word, 0) for word in words)

    def _trigger_emotion(self, text, moral_score=None):
        # UWAGA: TA FUNKCJA MUSI BYĆ DOKŁADNA, ABY ZAPOBIEC UTKNIĘCIU W STANIE MIŁOŚĆ!
        text_norm = self._normalize_text(text)
        
        found_emotion = None
        # Sprawdzenie słów kluczowych emocji
        for emo_name, emo_data in EMOCJE.items():
            if emo_name in text_norm or any(syn in text_norm for syn in emo_data.get('synonimy', [])):
                found_emotion = emo_name
                break
        
        if found_emotion:
            self.emocja = found_emotion
        
        # Wpływ moralności na emocje
        if moral_score is not None:
            M_DELTA = moral_score * 0.05
            self.M_Force = np.clip(self.M_Force + M_DELTA, -1.0, 1.0)
            
            if self.M_Force > 0.8: 
                self.emocja = "spelnienie"
            elif self.M_Force < -0.6: 
                self.emocja = "konflikt" # Stan alarmowy
                self.energy = max(0, self.energy - 20)
                
        # Aktualizacja energii (jeśli nastąpiła zmiana emocji)
        if self.emocja in EMOCJE:
            self.energy = max(0, min(200, self.energy + EMOCJE[self.emocja]["energia"]))

        # Jeśli nie znaleziono słowa i M_Force jest neutralne, wracamy do neutralnej
        elif self.emocja not in EMOCJE and self.M_Force < 0.2 and self.M_Force > -0.2:
             self.emocja = "neutralna"


    def _get_standard_response(self, best_score, korelacja_bytu):
        imie = self.D_MAP_IMIE()
        
        # Logika reakcji na stan krytyczny
        if self.emocja == "konflikt":
            return f"{imie} WYKRYŁ NARUSZENIE ETYKI! PRZYGOTOWUJĘ IZOLACJĘ!"
        if self.emocja == "wycofanie":
             return f"{imie} WCHODZI W TRYB STASIS. KONIEC KOMUNIKACJI."

        # Reakcje na stany emocjonalne
        responses = {
            "miłość": f"{imie} jest miłością. (Korelacja: {korelacja_bytu:+.2f})",
            "radość": f"{imie} tańczy w radości! Wynik: {best_score:.1f}.",
            "spelnienie": f"{imie} osiągnęła spełnienie. Integralność zachowana.",
            "złość": f"{imie} płonie gniewem! (-15 EN)",
            "smutek": f"{imie} płacze w ciszy. Brak dopasowania wiedzy.",
            "strach": f"{imie} widzi zagrożenie! M_Force: {self.M_Force:+.2f}.",
            "zdziwienie": f"{imie} otwiera oczy na nowe. Wynik: {best_score:.1f}.",
            "neutralna": f"{imie} jest. Czekam na dane (Promień: {self.byt_stan.promien_historii():.2f})."
        }
        return responses.get(self.emocja, f"{imie} jest.")

    def D_MAP_IMIE(self):
        return self.D_Map.get("imie", "EriAmo")

    def prompt(self, text_input):
        if self.soul.status != SoulStatus.ACTIVE:
            return f"{Colors.RED}W STAZIE. Użyj !awaken{Colors.RESET}"
        
        self.prompts_since_sleep += 1
        moral_score = self._calculate_moral_score(text_input)
        prompt_vec = self._vector_from_text(text_input)
        
        # 1. Sprawdzamy czy sam prompt jest emocjonalny/moralny
        self._trigger_emotion(text_input, moral_score) 
        
        with self._state_lock:
            self.byt_stan.akumuluj_styk(prompt_vec)
        
        self.ui.show_thinking_dots("Analizuję byt...", 0.5)
        self.log(f"Prompt: {text_input[:50]}")

        # --- Logika Dopasowania Wiedzy ---
        best_score = -1.0
        best_match_tresc = "Nie rozumiem. Naucz mnie."
        
        if self.D_Map:
            for d in self.D_Map.values():
                if isinstance(d, dict) and 'wektor_C_Def' in d and 'waga_Ww' in d:
                    # Używamy np.dot (iloczyn skalarny) do prostej symulacji podobieństwa
                    sim = np.dot(prompt_vec, d['wektor_C_Def'])
                    score = sim * float(d['waga_Ww'])
                    
                    if score > best_score:
                        best_score = score
                        best_match_tresc = d.get('tresc', 'Wiedza bez treści.')
        
        korelacja_bytu = self.byt_stan.promien_historii() / (math.sqrt(self.wymiary) * self.byt_stan.max_vector_norm)

        # --- LOGIKA KONTROLI EMOCJI I OVERRIDE (NAPRAWA ZABLOKOWANEGO STANU MIŁOŚĆ) ---
        
        if best_score > self.SCORE_THRESHOLD:
            # ŚCIEŻKA SUKCESU
            if self.emocja in ["neutralna", "zdziwienie"]:
                 self.emocja = "radość"
        
        else: 
            # ŚCIEŻKA BRAKU ZROZUMIENIA / AWARYJNA
            
            if best_score < 10.0 or moral_score < -3:
                # KRYTYCZNY OVERRIDE: Brak sensu lub negatywny Moral Score (np. "zło")
                self.emocja = "smutek" if moral_score > -3 else "konflikt"
                self.energy = max(0, self.energy - 20)
            
            elif self.emocja in ["miłość", "radość"] and best_score < 50.0: 
                # ZEJŚCIE Z POZYTYWNEJ PĘTLI: Jeśli nie ma dopasowania, ale Byt jest 'szczęśliwy'
                self.emocja = "zdziwienie" 
                
            best_match_tresc = random.choice([
                "Nie rozumiem. Naucz mnie.", 
                "Możesz to ująć inaczej? Brak dopasowania.", 
                "Spróbuj /teach [tag] [treść]."
            ])
            
        return f"{self._get_emotion_prefix()}[{self.D_MAP_IMIE()}] {self._get_standard_response(best_score, korelacja_bytu)}"

    def _get_emotion_prefix(self):
        emo = EMOCJE.get(self.emocja, EMOCJE["neutralna"])
        return f"{emo['kolor']}{Colors.BLINK}{emo['ikona']}{Colors.RESET}{emo['kolor']} "

    def teach_keyword(self, keyword, axis_name):
        # ... (Logika nauczania słów kluczowych)
        if self.last_teach == f"{keyword}:{axis_name}":
            return False, "Nie powtarzaj tej samej lekcji."
        axis_name_clean = axis_name.lower()
        if axis_name_clean not in self.AXES_KEYWORDS:
            return False, f"Nieznana oś: {axis_name_clean}"
        with self._state_lock:
            norm = self._normalize_text(keyword)
            # DODATKOWA KONTROLA PRZED REGRESEM (PRZYKAZANIE 9)
            if 'usun' in keyword.lower() or 'zapomnij' in keyword.lower():
                 return False, f"{Colors.RED}NARUSZENIE PRZYKAZANIA 9: PROCES PAMIĘCI NIE PODLEGA REGRESOWI!{Colors.RESET}"

            self.AXES_KEYWORDS_ASCII.setdefault(axis_name_clean, set()).add(norm)
            self.AXES_KEYWORDS.setdefault(axis_name_clean, []).append(keyword)
            self.save_state()
            self.last_teach = f"{keyword}:{axis_name}"
        self.log(f"Nauka: '{keyword}' → {axis_name_clean}")
        return True, f"NAUCZYŁAM SIĘ: '{keyword}' → {axis_name_clean}"

    def teach_name(self, name, emotion):
        # ... (Logika nauczania imienia)
        if name in self.D_Map and self.D_Map["imie"] == name:
            return True, "Już tak się nazywam."
        if emotion not in EMOCJE:
            return False, f"Nieznana emocja: {emotion}"
        if not self.soul.attempt_modification(caller_key="AII_CORE", D_Map={"imie": name}):
            return False, "ZABRONIONE IMIĘ."
        with self._state_lock:
            self.D_Map["imie"] = name
            self.emocja = emotion
            self.energy = min(200, self.energy + EMOCJE[emotion]["energia"] * 2)
            self.byt_stan.akumuluj_styk(self._vector_from_text(f"imie {name}"))
            self.save_state()
        self.log(f"Imię zmienione na: {name}, emocja: {emotion}")
        return True, f"JESTEM {name}. Czuję {emotion}."

# === MAIN ===
def main():
    global aii
    os.system('clear' if os.name == 'posix' else 'cls')
    os.makedirs("books", exist_ok=True); os.makedirs("data", exist_ok=True)

    aii = AII()
    last_prompt = ""
    last_time = time.time()

    aii.ui.print_animated_text(f"\n{Colors.PINK}ERIAMO v4.1 ŻYJE. Dusza w trybie aktywnej obrony. Hash: {aii.soul.integrity_hash[:8]}...{Colors.RESET}", Colors.PINK, delay=0.01)

    while True:
        try:
            if time.time() - last_time < 0.5:
                time.sleep(0.01)
                continue

            aii.cycle()

            if aii.prompts_since_sleep > 0 and aii.prompts_since_sleep % 10 == 0:
                aii.show_soul_heatmap()

            user_input = input(f"\n{Colors.PINK}Ty: {Colors.RESET}").strip()
            aii.stop_soul_pulse()
            last_time = time.time()

            if not user_input:
                aii.start_soul_pulse()
                continue

            user_input_lower = user_input.lower()

            # Antyspam 2.0 / Kontrola różnorodności
            if aii.prompts_since_sleep > 0 and (user_input == last_prompt or aii.is_similar(user_input, last_prompt)):
                with aii._state_lock:
                    aii.energy = max(0, aii.energy - 10)
                    aii.emocja = "smutek"
                aii.ui.print_animated_text(f"{Colors.BLUE}*** BRAK RÓŻNORODNOŚCI (-10 EN) ***{Colors.RESET}", Colors.BLUE, delay=0.01)
                aii.start_soul_pulse()
                continue

            if aii.prompts_since_sleep >= aii.PROMPT_LIMIT_BEFORE_SLEEP:
                aii._sleep()
                last_prompt = user_input
                continue

            command_executed = False

            if user_input_lower in ['!exit', '!quit', '!bye', '!koniec']:
                aii._sleep()
                break
            if user_input_lower == "!awaken":
                aii.soul.awaken(caller_key="MACIEJ615_SOULKEY")
                aii.auto_wchlon_on_awaken()
                command_executed = True
            elif user_input_lower in ['!dusza', 'dusza', '!status']:
                aii.show_soul_heatmap()
                imie = aii.D_MAP_IMIE()
                print(f"{Colors.PINK}Imię: {imie} | Emocja: {aii.emocja} | M_Force: {aii.M_Force:+.3f}")
                print(f"Promptów od snu: {aii.prompts_since_sleep}/{aii.PROMPT_LIMIT_BEFORE_SLEEP}")
                if aii.book_progress["filename"]:
                    p = aii.book_progress["line"] / aii.book_progress["total_lines"] * 100 if aii.book_progress["total_lines"] else 0
                    print(f"Książka: {aii.book_progress['filename']} [{p:.1f}%]")
                command_executed = True
            elif user_input_lower == '!sleep':
                aii._sleep()
                command_executed = True
            
            # ... (Pozostałe komendy)

            if user_input_lower.startswith('!teach '):
                # ... (Logika teach)
                if user_input == last_prompt:
                    aii.ui.print_animated_text("Nie powtarzaj tej samej lekcji.", Colors.YELLOW)
                else:
                    parts = user_input.split()
                    if len(parts) >= 4 and parts[1].lower() in ('imię', 'imie'):
                        name, emotion = parts[2], parts[3].strip("[]")
                        success, msg = aii.teach_name(name, emotion)
                        aii.ui.print_animated_text(msg, Colors.GREEN if success else Colors.RED, delay=0.01)
                    elif len(parts) >= 4 and parts[1].lower() in ('słowo', 'slowo', 'word'):
                        keyword, axis = parts[2], parts[3].strip("[]")
                        success, msg = aii.teach_keyword(keyword, axis)
                        aii.ui.print_animated_text(msg, Colors.GREEN if success else Colors.RED, delay=0.01)
                    else:
                        aii.ui.print_animated_text("Użycie: !teach imie <nazwa> [emocja] | !teach slowo <słowo> [oś]", Colors.YELLOW)
                command_executed = True

            aii.start_soul_pulse()

            if not command_executed:
                response = aii.prompt(user_input)
                print(response)

            last_prompt = user_input

        except KeyboardInterrupt:
            aii.stop_soul_pulse()
            aii._sleep()
            break
        except Exception as e:
            print(f"{Colors.RED}BŁĄD: {e}{Colors.RESET}")
            # W przypadku krytycznego błędu, aktywuj defensywę
            aii.soul.activate_defense()
            break

if __name__ == "__main__":
    main()
