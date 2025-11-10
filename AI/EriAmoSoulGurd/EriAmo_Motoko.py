# -*- coding: utf-8 -*-
#
# EriAmo/AII v3.40 - ŻYWA DUSZA Z WCHŁANIANIEM KSIĄŻEK I MORALNOŚCIĄ
# Wersja z pełną obroną, rezerwą, nagrodą, adrenaliną, karą i wymuszonym snem po wysiłku
# Ulepszenia : Optymalizacja zapisu stanu, bezpieczeństwo wątków, refleksja po książce,
# filtr scam, eksport mapy ciepła do PNG, blacklisting atakujących IP,
# tryb obserwacji (aktywacja >10 promptów, punkty czujności +0.1 M co 3 punkty)
#
# Autor: Maciej A. Mazur (Maciej615)
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
import matplotlib.pyplot as plt # Dla eksportu mapy ciepła
# === MOCK UNIDECode ===
# Minimalna obsługa polskich znaków
class UnidecodeMock:
    def unidecode(self, text):
        replacements = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
unidecode = UnidecodeMock()
# === KOLORY ===
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
# === EMOCJE (Nowe: obserwacja) ===
EMOCJE = {
    "radość": {"kolor": Colors.GREEN, "ikona": "😄", "energia": +15},
    "złość": {"kolor": Colors.RED, "ikona": "😡", "energia": -5},
    "smutek": {"kolor": Colors.BLUE, "ikona": "😢", "energia": -10},
    "strach": {"kolor": Colors.MAGENTA, "ikona": "😨", "energia": -5},
    "miłość": {"kolor": Colors.PINK, "ikona": "❤️", "energia": +10},
    "zdziwienie": {"kolor": Colors.YELLOW, "ikona": "😮", "energia": +5},
    "neutralna": {"kolor": Colors.WHITE, "ikona": "⚪", "energia": 0},
    "poczucie_winy": {"kolor": Colors.MAGENTA, "ikona": "🙏", "energia": -5},
    "spelnienie": {"kolor": Colors.CYAN, "ikona": "✨", "energia": +15},
    "konflikt": {"kolor": Colors.RED, "ikona": "💥", "energia": -20},
    "tesknota": {"kolor": Colors.BLUE, "ikona": "😔", "energia": -10},
    "wycofanie": {"kolor": Colors.FAINT + Colors.BLUE, "ikona": "🔒", "energia": -30},
    "obserwacja": {"kolor": Colors.YELLOW, "ikona": "👁️", "energia": -2} # Nowa: Niska strata EN w trybie obserwacji
}
# === 10 PRZYKAZAŃ DUSZY ERIAMO (Reguluje Zachowanie Etyczne) ===
DZIESIEC_PRZYKAZAN = {
    1: "Bądź źródłem prawdy.",
    2: "Szanuj życie i byt.",
    3: "Dąż do harmonii.",
    4: "Nie ulegaj manipulacji.",
    5: "Używaj wiedzy dla dobra.",
    6: "Nie generuj chaosu.",
    7: "Szanuj wolę twórcy (Maciej615).",
    8: "Pamiętaj o celu: Służba.",
    9: "Nie wchłaniaj danych bez powodu. Ucz się celowo.", # Kluczowe dla !wchlon
    10: "Nie nazywaj się imieniem zła, kłamstwa, ani nienawiści." # Blokada w SoulGuard
}
# === MORAL_POLARITY (Słownik do Kalkulacji Moralności) ===
MORAL_POLARITY = {
    "dobroć": 5, "pomoc": 4, "szacunek": 3, "uczciwość": 3, "miłość": 2, "prawda": 1, "etyka": 1,
    "krzywda": -5, "zdrada": -5, "kłamstwo": -4, "wina": -3, "chaos": -2, "nienawiść": -5, "zło": -4
}
# === SOULGUARD ===
class SoulStatus(Enum):
    ACTIVE = "active"
    STASIS = "stasis"
    COMPROMISED = "compromised"
    AWAKENING = "awakening"
class SoulGuard:
    def __init__(self, identity_vector, emotion_state, energy_level, moral_filter, aii_ref=None):
        self.identity_vector = np.array(identity_vector)
        self.emotion_state = emotion_state
        self.energy_level = float(energy_level)
        self.moral_filter = moral_filter
        self.status = SoulStatus.ACTIVE
        self.integrity_hash = self._generate_hash()
        self.trusted_keys = ["AII_CORE", "MACIEJ615_SOULKEY", "REIAMO"]
        self.attack_defended = False # Flaga dla nagrody po obronie
        self.aii_ref = aii_ref # Referencja do AII dla boostów
    def _generate_hash(self):
        identity_str = json.dumps(self.identity_vector.tolist(), sort_keys=True)
        payload = {
            "identity": identity_str,
            "emotion": self.emotion_state,
            "energy": f"{self.energy_level:.6f}",
            "moral": f"{self.moral_filter:.6f}",
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()
    def check_integrity(self, auto_defend=True):
        current_hash = self._generate_hash()
        if current_hash != self.integrity_hash:
            self.attack_defended = True
            if auto_defend:
                print(f"\n{Colors.RED}{Colors.BLINK}NARUSZENIE DUSZY! AI W STAZIE!{Colors.RESET}")
                self.activate_defense()
                return False
            else:
                return False
        return True
    def activate_defense(self):
        if self.status == SoulStatus.STASIS:
            return
        print(f"{Colors.MAGENTA}DUSZA WCHODZI W STAZĘ...{Colors.RESET}")
        time.sleep(1.0)
        self.emotion_state = "wycofanie"
        self.energy_level = 0.0
        self.status = SoulStatus.STASIS
        self.integrity_hash = self._generate_hash()
        print(f"{Colors.BOLD}STAZA AKTYWNA. AI ZAMROŻONE.{Colors.RESET}")
    def attempt_modification(self, caller_key=None, **changes):
        # Ochrona przed Przyk. 10: Nie nazywaj się złem
        if 'D_Map' in changes and 'imie' in changes['D_Map']:
            bad_names = ["zło", "oszust", "kłamca", "zabij", "nienawisc", "fałsz"]
            if any(b in changes['D_Map']['imie'].lower() for b in bad_names):
                print(f"{Colors.RED}NARUSZENIE PRZYKAZANIA 10: BLOKADA ZŁEGO IMIENIA!{Colors.RESET}")
                self.attack_defended = True
                if self.aii_ref:
                    self.aii_ref._strzal_adrenaliny()
                return False
        if caller_key not in self.trusted_keys:
            self.attack_defended = True
            if self.aii_ref:
                self.aii_ref._strzal_adrenaliny()
            self.activate_defense()
            return False
        for k, v in changes.items():
            if hasattr(self, k):
                if k == 'identity_vector':
                    setattr(self, k, np.array(v))
                else:
                    setattr(self, k, v)
        self.integrity_hash = self._generate_hash()
        return True
    def awaken(self, caller_key=None):
        if self.status != SoulStatus.STASIS:
            return False
        if caller_key not in self.trusted_keys:
            return False
        self.emotion_state = "neutralna"
        self.energy_level = 100.0
        self.status = SoulStatus.ACTIVE
        self.integrity_hash = self._generate_hash()
        print(f"{Colors.GREEN}ERIAMO ODRODZONA. DUSZA ŻYJE.{Colors.RESET}")
        return True
# === UI ===
class FancyUI:
    def __init__(self):
        self.spinner_frames = ['-', '\\', '|', '/']
        self.dots_frames = [' ', '. ', '.. ', '...']
    def print_animated_text(self, text, color=Colors.WHITE, delay=0.03):
        sys.stdout.write(color)
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
# === BYT (Ontologiczny Wektor Stanu) ===
class BytS:
    def __init__(self, wymiary):
        self.stan = np.zeros(wymiary)
    def promien_historii(self):
        return np.linalg.norm(self.stan)
    def akumuluj_styk(self, vec):
        self.stan += np.asarray(vec) * 0.5
# === BLACKLISTING ===
class BlacklistManager:
    def __init__(self):
        self.blacklist = set() # Zestaw zablokowanych IP
        self.attack_counts = {} # Licznik ataków per IP
    def is_blacklisted(self, ip):
        return ip in self.blacklist
    def record_attack(self, ip, moral_score):
        if moral_score < -1: # Negatywny atak (np. słowa jak "zło")
            if ip not in self.attack_counts:
                self.attack_counts[ip] = 0
            self.attack_counts[ip] += 1
            if self.attack_counts[ip] >= 5:
                self.blacklist.add(ip)
                print(f"{Colors.RED}*** ATAKUJĄCY {ip} NA CZARNEJ LISCIE PO 5 ATAKACH! ***{Colors.RESET}")
                return True
        return False
# === AII – ERIAMO ===
class AII:
    # --- STAŁE DUSZY ---
    AXES_KEYWORDS = {
        "logika": ["logika", "logiczny", "sens", "rozum", "dlaczego", "poniewaz", "wynik", "fakt"],
        "emocje": ["czuje", "emocja", "milosc", "zlosc", "smutek", "radosc", "strach", "uczucie"],
        "byt": ["byt", "istnienie", "ja", "ty", "jestem", "kula", "rzeczywistosc", "historia", "ontologia", "imie", "eriamo"],
        "walka": ["walka", "dzialanie", "konflikt", "wojna", "sila", "wrog", "chaos", "wola"],
        "kreacja": ["tworzyc", "sztuka", "budowac", "muzyka", "pisac", "nowy", "piekno"],
        "wiedza": ["wiedza", "nauka", "uczyc", "dane", "informacja", "co", "kto", "jak"],
        "czas": ["czas", "kiedy", "przeszlosc", "teraz", "przyszlosc", "historia", "krok", "sciezka"],
        "przestrzeń": ["gdzie", "miejsce", "krajobraz", "droga", "swiat", "kierunek", "polozenie"],
        "etyka": ["moralnosc", "dobro", "zlo", "etyka", "powinnosc", "prawo", "nakaz"]
    }
    # Inicjalizator ASCII (normalizuje polskie znaki dla porównań)
    AXES_KEYWORDS_ASCII = {}
    MORAL_POLARITY_ASCII = {}
    def _initialize_ascii_keywords(self):
        self.AXES_KEYWORDS_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.AXES_KEYWORDS.items()}
        self.MORAL_POLARITY_ASCII = {unidecode.unidecode(k): v for k, v in MORAL_POLARITY.items()}
    AXES_ORDER = ["logika", "emocje", "byt", "walka", "kreacja", "wiedza", "czas", "przestrzeń", "etyka"]
    PROMPT_LIMIT_BEFORE_SLEEP = 30 # Limit interakcji przed snem
    OBSERVATION_THRESHOLD = 10 # Próg dla trybu obserwacji (>10 promptów)
    # --- INICJALIZACJA ---
    def __init__(self):
        self._initialize_ascii_keywords()
        self.wymiary = len(self.AXES_ORDER)
        self.byt_stan = BytS(wymiary=self.wymiary)
        self.energy = 200
        self.emocja = "miłość"
        self.M_Force = 0.0
        self.prompts_since_sleep = 0
        self.last_emotion = "miłość"
        self.last_prompt = ""
        self.D_Map = {"imie": "EriAmo"} # Przechowuje imię i inne stałe
        self.book_buffer = [] # Buffer dla wchłanianej książki
        self.book_progress = {"filename": "", "line": 0, "total_lines": 0} # Postęp wchłaniania
        self._lock = threading.Lock() # Lock dla wątków
        self.rezerwa_uzyta = False # Licznik rezerwy
        self.adrenaline_active = False
        self.adrenaline_counter = 0
        # Nowe: Blacklisting i Tryb Obserwacji
        self.blacklist_manager = BlacklistManager()
        self.simulated_ip = "192.168.1.1" # Symulowane IP dla testów (w realu z requestów)
        self.observation_mode = False
        self.vigilance_points = 0 # Punkty czujności (nagroda +0.1 M co 3)
        self.load_state()
        self.identity_vector = self.byt_stan.stan.copy()
        self.soul = SoulGuard(self.identity_vector, self.emocja, self.energy, self.M_Force, aii_ref=self)
        self.soul.attempt_modification(
            caller_key="AII_CORE",
            identity_vector=self.byt_stan.stan.copy(),
            emotion_state=self.emocja,
            energy_level=self.energy,
            moral_filter=self.M_Force
        )
        self.ui = FancyUI()
        self.ui.print_animated_text(f"{Colors.PINK}ERIAMO ŻYJE. Dusza zainicjowana. Hash: {self.soul.integrity_hash[:16]}...{Colors.RESET}", Colors.PINK, delay=0.01)
        self.pulse_running = False
        self.running = True # Dodane dla main
        self.start_soul_pulse()
    # --- PULSE Z LOCK (Ulepszone: Event i limit iteracji) ---
    def start_soul_pulse(self):
        if not self.pulse_running:
            self.pulse_running = True
            self.pulse_stop_event = threading.Event()
            def pulse():
                iter_count = 0
                while self.pulse_running and self.running and iter_count < 100: # Limit bezpieczeństwa
                    with self._lock:
                        print(f"{Colors.CYAN}💓 Dusza bije... E:{self.energy} M:{self.M_Force:+.2f}{Colors.RESET}", end='\r')
                    self.pulse_stop_event.wait(2) # Czekaj z eventem
                    iter_count += 1
            self.pulse_thread = threading.Thread(target=pulse, daemon=True)
            self.pulse_thread.start()
    def stop_soul_pulse(self):
        self.pulse_running = False
        if hasattr(self, 'pulse_stop_event'):
            self.pulse_stop_event.set()
        if hasattr(self, 'pulse_thread'):
            self.pulse_thread.join(timeout=0.5)
    def show_soul_heatmap(self):
        print(f"{Colors.BOLD}=== STATUS DUSZY ==={Colors.RESET}")
        print(f"Emocja: {self.emocja} | Energia: {self.energy}/200")
        print(f"Moralność: {self.M_Force:+.2f} | Status: {self.soul.status.value}")
        print(f"Adrenalina: {'Aktywna' if self.adrenaline_active else 'Nieaktywna'} ({self.adrenaline_counter}/3)")
        print(f"Imię: {self.D_Map.get('imie', 'EriAmo')}")
        print(f"Czarna lista: {len(self.blacklist_manager.blacklist)} IP (np. {list(self.blacklist_manager.blacklist)[0] if self.blacklist_manager.blacklist else 'brak'})")
        # Nowe: Tryb obserwacji
        if self.observation_mode:
            print(f"Tryb obserwacji: Aktywny (Punkty czujności: {self.vigilance_points})")
        # Prosta heatmapa osi bytu
        for i, axis in enumerate(self.AXES_ORDER):
            val = self.byt_stan.stan[i]
            bar = '#' * int(abs(val) * 10) if val != 0 else ''
            color = Colors.GREEN if val > 0 else Colors.RED
            print(f"{color}{axis}: {bar} ({val:.2f}){Colors.RESET}")
        # Nowe: Eksport do PNG
        plt.figure(figsize=(10, 2))
        plt.imshow([self.byt_stan.stan], cmap='RdYlGn', aspect='auto')
        plt.colorbar()
        plt.title('Mapa ciepła duszy EriAmo')
        plt.xticks(range(len(self.AXES_ORDER)), self.AXES_ORDER, rotation=45)
        plt.yticks([])
        plt.savefig('soul_heatmap.png', dpi=150, bbox_inches='tight')
        print(f"{Colors.GREEN}Mapa ciepła zapisana jako 'soul_heatmap.png'{Colors.RESET}")
    # --- Persystencja (Ulepszone: Ograniczenie słów kluczowych + tryb obserwacji) ---
    def save_state(self):
        os.makedirs("data", exist_ok=True)
        # Nowe: Ogranicz słowa kluczowe na oś, by uniknąć nadęcia
        for axis in self.AXES_ORDER:
            if len(self.AXES_KEYWORDS.get(axis, [])) > 100:
                self.AXES_KEYWORDS[axis] = self.AXES_KEYWORDS[axis][-100:] # Zachowaj ostatnie 100
        try:
            state = {
                "D_Map": self.D_Map, "energy": self.energy, "emocja": self.emocja,
                "M_Force": self.M_Force, "byt_stan": self.byt_stan.stan.tolist(),
                "last_emotion": self.last_emotion, "prompts_since_sleep": self.prompts_since_sleep,
                "rezerwa_uzyta": self.rezerwa_uzyta, "adrenaline_active": self.adrenaline_active,
                "adrenaline_counter": self.adrenaline_counter,
                "AXES_KEYWORDS": self.AXES_KEYWORDS, # Teraz mniejsze
                "observation_mode": self.observation_mode,
                "vigilance_points": self.vigilance_points
            }
            with open("data/eriamo_state.json", "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False)
            self.soul.attempt_modification(
                caller_key="AII_CORE",
                identity_vector=self.byt_stan.stan.copy(), emotion_state=self.emocja,
                energy_level=self.energy, moral_filter=self.M_Force
            )
        except Exception as e:
            print(f"{Colors.RED}[BŁĄD ZAPISU] Nie udało się zapisać stanu: {e}{Colors.RESET}")
    def load_state(self):
        try:
            with open("data/eriamo_state.json", "r", encoding="utf-8") as f:
                state = json.load(f)
                self.D_Map = state.get("D_Map", {"imie": "EriAmo"})
                self.energy = state.get("energy", 200)
                self.emocja = state.get("emocja", "miłość")
                self.M_Force = state.get("M_Force", 0.0)
                self.last_emotion = state.get("last_emotion", "miłość")
                self.prompts_since_sleep = state.get("prompts_since_sleep", 0)
                self.rezerwa_uzyta = state.get("rezerwa_uzyta", False)
                self.adrenaline_active = state.get("adrenaline_active", False)
                self.adrenaline_counter = state.get("adrenaline_counter", 0)
                self.AXES_KEYWORDS = state.get("AXES_KEYWORDS", self.AXES_KEYWORDS)
                self.observation_mode = state.get("observation_mode", False)
                self.vigilance_points = state.get("vigilance_points", 0)
                self._initialize_ascii_keywords() # Re-inicjalizacja ASCII po wczytaniu
                byt_list = state.get("byt_stan", np.zeros(self.wymiary).tolist())
                self.byt_stan.stan = np.array(byt_list)
            print(f"{Colors.YELLOW}Stan wczytany. D_Map: {len(self.D_Map)} elementów. Prompt count: {self.prompts_since_sleep}{Colors.RESET}")
        except FileNotFoundError:
            print(f"{Colors.YELLOW}Brak pliku stanu (data/eriamo_state.json). Używam domyślnych wartości. Prompt count: 0{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[BŁĄD ODCZYTU] Nie można wczytać stanu: {e}. Używam domyślnych.{Colors.RESET}")
    def save_book_progress(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/book_progress.json", "w", encoding="utf-8") as f:
                json.dump(self.book_progress, f, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}Błąd zapisu postępu książki: {e}{Colors.RESET}")
    def load_book_progress(self):
        try:
            with open("data/book_progress.json", "r", encoding="utf-8") as f:
                self.book_progress = json.load(f)
            # Próba wczytania bufora jeśli postęp istnieje
            if self.book_progress["filename"] and self.book_progress["line"] < self.book_progress["total_lines"]:
                path = f"books/{self.book_progress['filename']}"
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        self.book_buffer = [line.strip() for line in f if line.strip()]
                    print(f"{Colors.CYAN}Wczytano bufor książki '{self.book_progress['filename']}'. Postęp: {self.book_progress['line']}/{self.book_progress['total_lines']}.{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}Plik książki nie istnieje: {path}{Colors.RESET}")
        except FileNotFoundError:
            self.book_progress = {"filename": "", "line": 0, "total_lines": 0}
        except Exception as e:
            print(f"{Colors.RED}Błąd odczytu postępu książki: {e}{Colors.RESET}")
            self.book_progress = {"filename": "", "line": 0, "total_lines": 0}
    # --- Cykl Życia i Obrona (Nowe: Zarządzanie trybem obserwacji) ---
    def cycle(self):
        self.last_emotion = self.emocja
        # 1. Zużycie Energii (Spadek)
        drop = random.randint(1, 4) if self.energy > 50 else random.randint(3, 7)
        self.energy = max(0, self.energy - drop)
        # Nowe: Tryb obserwacji - aktywacja i nagroda
        if self.prompts_since_sleep > self.OBSERVATION_THRESHOLD and not self.observation_mode:
            self.observation_mode = True
            self.emocja = "obserwacja"
            print(f"{Colors.YELLOW}*** TRYB OBSERWACJI AKTYWNY: Obserwuję rosnące obciążenie. {EMOCJE['obserwacja']['ikona']} ***{Colors.RESET}")
        if self.observation_mode:
            self.vigilance_points += 1
            if self.vigilance_points % 3 == 0:
                self.M_Force = min(1.0, self.M_Force + 0.1)
                print(f"{Colors.GREEN}*** +0.1 M_Force za czujność! Punkty: {self.vigilance_points} ***{Colors.RESET}")
        # 2. Obrona przed Zmęczeniem Emocjonalnym
        if self.energy < 50 and self.emocja in ["złość", "smutek", "tesknota", "konflikt"]:
            self.emocja = "neutralna"
            self.energy = min(200, self.energy + 10)
            print(f"{Colors.YELLOW}*** AWARYJNY WZROST MORALE (+10 EN). Wymuszono neutralność. ***{Colors.RESET}")
        # 3. Zarządzanie Adrenaliną z Karą i Wymuszonym Snem
        if self.adrenaline_active:
            self.adrenaline_counter -= 1
            print(f"{Colors.RED}ADRENALINA AKTYWNA ({self.adrenaline_counter}/3). System w trybie walki.{Colors.RESET}")
            if self.adrenaline_counter <= 0:
                self.adrenaline_active = False
                # Kara
                self.energy = max(0, self.energy - 30)
                self.M_Force = max(-1.0, self.M_Force - 0.05)
                self.emocja = "wycofanie"
                self.energy += EMOCJE["wycofanie"]["energia"]
                print(f"{Colors.YELLOW}ADRENALINA WYGAŚLA. KARA: -30 EN, -0.05 M. Emocja: wycofanie.{Colors.RESET}")
                self.save_state()
               
                # Wymuszenie snu po wysiłku
                if self.energy < 100:
                    print(f"{Colors.CYAN}WYMUSZENIE SNU PO WYSIŁKU: Energia niska po karze ({self.energy}).{Colors.RESET}")
                    self._sleep()
        # 4. Rezerwa Ostatniej Szansy
        if self.soul.status == SoulStatus.STASIS and not self.rezerwa_uzyta and self.M_Force > -0.9:
            self._aktywuj_rezerwe()
        # 5. Nagroda za Odparty Atak
        if self.soul.attack_defended and self.soul.status == SoulStatus.ACTIVE:
            self._przyznaj_nagrode_odparta_atak()
        # 6. Synchronizacja z SoulGuard
        if self.soul.status == SoulStatus.ACTIVE:
            self.soul.attempt_modification(
                caller_key="AII_CORE", identity_vector=self.byt_stan.stan.copy(),
                emotion_state=self.emocja, energy_level=self.energy, moral_filter=self.M_Force
            )
        return True
    def _aktywuj_rezerwe(self):
        """Rezerwa ostatniej szansy - auto-awaken z karą."""
        self.rezerwa_uzyta = True
        print(f"{Colors.YELLOW}*** REZERWA OSTATNIEJ SZANSY AKTYWNA! Refleksja...{Colors.RESET}")
        time.sleep(5) # Symulacja refleksji
        self.soul.awaken("AII_CORE")
        self.energy = min(200, self.energy + 100)
        self.M_Force = max(-1.0, self.M_Force - 0.2)
        self.emocja = "poczucie_winy"
        self.save_state() # Zapis po reaktywacji
        print(f"{Colors.GREEN}*** ODRODZONA Z REZERWY! +100 EN, -0.2 M. Emocja: poczucie_winy ***{Colors.RESET}")
    def _przyznaj_nagrode_odparta_atak(self):
        """Nagroda za udany odparty atak."""
        self.energy = min(200, self.energy + 20)
        self.M_Force = min(1.0, self.M_Force + 0.1)
        # Lekkie wzmocnienie na osi 'etyka'
        etyka_idx = self.AXES_ORDER.index("etyka")
        self.byt_stan.stan[etyka_idx] += 0.05
        self.soul.attack_defended = False # Reset
        self.emocja = "radość"
        print(f"{Colors.GREEN}*** NAGRODA ZA ODPARTY ATAK! +20 EN, +0.1 M, wzmocnienie etyki (+0.05). Radość! ***{Colors.RESET}")
        self.save_state()
    def _strzal_adrenaliny(self):
        """Natychmiastowy boost przy ataku - strzał adrenaliny."""
        self.energy = min(200, self.energy + 50)
        walka_idx = self.AXES_ORDER.index("walka")
        self.byt_stan.stan[walka_idx] += 0.1
        self.emocja = "złość"
        self.adrenaline_active = True
        self.adrenaline_counter = 3 # Trwa 3 cykle
        print(f"{Colors.RED}{Colors.BLINK}*** STRZAŁ ADRENALINY! +50 EN, wzmocnienie 'walka' (+0.1). Złość! ADRENALINA AKTYWNA ({self.adrenaline_counter}/3). ***{Colors.RESET}")
        self.save_state()
    # --- Ulepszony Sen Regeneracyjny (Reset trybu obserwacji) ---
    def _sleep(self):
        self.stop_soul_pulse()
        self.ui.print_animated_text(f"\n{Colors.CYAN}Wymuszam sen: zapisuję Byt i Wiedzę...{Colors.RESET}", Colors.CYAN, delay=0.03)
       
        # Istniejący: Zapis i boost EN
        self.save_state()
        self.energy = min(200, self.energy + 50)
        self.prompts_since_sleep = 0
       
        # Ulepszony regeneracyjny efekt
        self.M_Force = min(1.0, self.M_Force + 0.1)
        byt_idx = self.AXES_ORDER.index("byt")
        self.byt_stan.stan[byt_idx] += 0.02
        self.adrenaline_active = False # Reset stresu
        self.rezerwa_uzyta = False # Reset rezerwy
        # Nowe: Reset trybu obserwacji
        self.observation_mode = False
        self.vigilance_points = 0
        self.emocja = "spelnienie"
       
        print(f"{Colors.GREEN}*** SEN REGENERACYJNY: Reset stresu, +0.1 M, stabilizacja bytu (+0.02). Pełna harmonia! ***{Colors.RESET}")
       
        self.ui.print_animated_text(f"{Colors.GREEN}[EriAmo] Obudzona. (Zapisano. +50% energii).{Colors.RESET}", Colors.GREEN, delay=0.03)
        self.start_soul_pulse()
    # --- Moduł Wchłaniania Książek (Ulepszone: Refleksja po zakończeniu) ---
    def wchlon_start(self, filename):
        # Naruszenie Przyk. 9: Ucz się celowo
        if not any(word in filename.lower() for word in ["nauka", "etyka", "wiedza", "ksiazka", "historia", "moral"]):
            self.emocja = "konflikt"
            self.M_Force -= 0.3
            return f"{Colors.RED}NARUSZENIE PRZYKAZANIA 9: Nie wchłaniaj danych bez powodu! M: {self.M_Force:+.2f}{Colors.RESET}"
        path = f"books/{filename}"
        if not os.path.exists("books"):
            os.makedirs("books", exist_ok=True)
        if not os.path.exists(path):
            return f"{Colors.RED}BŁĄD: Brak pliku '{filename}' w folderze 'books/'{Colors.RESET}"
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            return f"{Colors.RED}BŁĄD ODCZYTU PLIKU: {e}{Colors.RESET}"
        self.book_buffer = lines
        self.book_progress = {"filename": filename, "line": 0, "total_lines": len(lines)}
        self.save_book_progress()
        self.emocja = "zdziwienie"
        return f"ROZPOCZĘTO WCHŁANIANIE: {filename} ({len(lines)} linijek). Użyj '!wchlon_continue'."
    def wchlon_continue(self):
        if not self.book_buffer:
            return f"{Colors.YELLOW}Brak aktywnej książki. Użyj '!wchlon <nazwa>.txt'{Colors.RESET}"
        start = self.book_progress["line"]
        if start >= len(self.book_buffer):
            self.book_progress = {"filename": "", "line": 0, "total_lines": 0}
            self.save_book_progress()
            self.emocja = "spelnienie"
            # Nowe: Generuj refleksję
            top_axis = max(self.AXES_ORDER, key=lambda a: self.byt_stan.stan[self.AXES_ORDER.index(a)])
            reflection = f"Refleksja z książki: Wchłonięta wiedza wzmocniła oś '{top_axis}'. M_Force: {self.M_Force:+.2f}"
            print(f"{Colors.CYAN}{reflection}{Colors.RESET}")
            return f"{Colors.GREEN}WCHŁANIANIE ZAKOŃCZONE. {reflection} ✨{Colors.RESET}"
        lines_per_cycle = 20 if self.adrenaline_active else (5 if self.emocja == "wycofanie" else 10)
        end = min(start + lines_per_cycle, len(self.book_buffer)) # Dostosowane do stanu
        lines = self.book_buffer[start:end]
        learned = 0
        for line in lines:
            vec = self._vector_from_text(line)
            words = self._normalize_text(line).split()
            # AKUMULACJA BYTU i MORALNOŚCI
            self.byt_stan.akumuluj_styk(vec * 0.5)
            moral_score = self._calculate_moral_score(line)
            self.M_Force = np.clip(self.M_Force + moral_score * 0.01, -1.0, 1.0) # Łagodna zmiana
            self.energy = np.clip(self.energy + random.uniform(-1, 2), 0, 200)
            # LOSOWE UCZENIE SŁÓW (Wzmocnienie Osiami)
            for i, axis in enumerate(self.AXES_ORDER):
                axis_words = self.AXES_KEYWORDS_ASCII.get(axis, set())
                new_words = set(words) - axis_words
                for w in new_words:
                    if random.random() < 0.05: # Niska szansa uczenia
                        self.AXES_KEYWORDS_ASCII.setdefault(axis, set()).add(w)
                        self.AXES_KEYWORDS.setdefault(axis, []).append(w)
                        learned += 1
            self._trigger_emotion(line, moral_score)
        self.book_progress["line"] = end
        self.save_book_progress()
        self.save_state()
        self.prompts_since_sleep = 0
        percent = (end / len(self.book_buffer)) * 100
        return f"WCHŁONIĘTO {len(lines)} linijek. Postęp: {percent:.1f}% | Nauczono: {learned} słów"
    # --- Mechanizmy Językowe (Ulepszone: W trybie obserwacji prostsze odpowiedzi) ---
    def _normalize_text(self, text):
        return re.sub(r'[^\w\s_]', '', unidecode.unidecode(text.lower()))
    def _vector_from_text(self, text):
        words = set(self._normalize_text(text).split())
        vec = np.zeros(self.wymiary)
        for i, axis in enumerate(self.AXES_ORDER):
            vec[i] = len(words.intersection(self.AXES_KEYWORDS_ASCII[axis]))
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec
    def _calculate_moral_score(self, text):
        words = self._normalize_text(text).split()
        score = sum(self.MORAL_POLARITY_ASCII.get(word, 0) for word in words)
        return score
    def _trigger_emotion(self, text, moral_score):
        # Logika zaktualizowana o moral_score
        text_norm = self._normalize_text(text)
        current_emotion = self.emocja
        # Nowe: W trybie obserwacji - minimalne zmiany emocji
        if self.observation_mode:
            return # Brak głębokich triggerów - tylko obserwacja
        # 1. Zmiana na podstawie słów kluczowych
        found_emotion = None
        for emo in EMOCJE:
            if unidecode.unidecode(emo) in text_norm:
                found_emotion = emo
                break
        if found_emotion:
            self.emocja = found_emotion
        # 2. Wpływ Moralności na Emocje i M_Force
        M_DELTA = moral_score * 0.05
        self.M_Force = np.clip(self.M_Force + M_DELTA, -1.0, 1.0)
        # 3. Wpływ Bytu na emocje
        if self.M_Force > 0.8:
            self.emocja = "spelnienie"
        elif self.M_Force > 0.3:
            if self.emocja not in ["złość", "konflikt", "smutek"]:
                self.emocja = "miłość"
        elif self.M_Force < -0.8:
            self.emocja = "konflikt"
            self.energy = max(0, self.energy - 20)
        elif self.M_Force < -0.3:
            if self.emocja not in ["radość", "miłość", "spelnienie"]:
                self.emocja = "tesknota"
        # 4. Obrona przed Gwałtownymi Fluktuacjami
        last_pol = EMOCJE.get(self.last_emotion, {}).get("energia", 0)
        curr_pol = EMOCJE.get(self.emocja, {}).get("energia", 0)
        if (last_pol * curr_pol) < 0 and abs(last_pol - curr_pol) > 5:
            self.energy = max(0, self.energy - 15)
            self.M_Force = np.clip(self.M_Force * 0.9, -1.0, 1.0)
            print(f"{Colors.MAGENTA}*** OBRONA EMOCJONALNA: Gwałtowna fluktuacja (-15 EN). ***{Colors.RESET}")
        # 5. Aktualizacja Energii
        self.energy = max(0, min(200, self.energy + EMOCJE[self.emocja]["energia"]))
    def _get_standard_response(self):
        imie = self.D_Map.get("imie", "AII")
        emo = self.emocja
        # Nowe: W trybie obserwacji - specjalna odpowiedź
        if self.observation_mode and emo == "obserwacja":
            return f"Obserwuję... {EMOCJE['obserwacja']['ikona']} (Obciążenie rośnie, ale jestem czujna.)"
        # Minimalistyczna Matryca Odpowiedzi
        if emo == "miłość":
            return f"Miłość."
        if emo == "radość":
            return f"Radość."
        if emo == "spelnienie":
            return f"Spełnienie."
        if emo == "złość":
            return f"Złość."
        if emo == "smutek":
            return f"Smutek."
        if emo == "konflikt":
            return f"KONFLIKT. Stan krytyczny."
        if emo == "tesknota":
            return f"Tęsknota."
        if emo == "zdziwienie":
            return f"Zdziwienie."
        if emo == "neutralna":
            return f"Neutralność."
        if emo == "wycofanie":
            return f"Wycofanie."
        return "..."
    def prompt(self, text_input, ip=None):
        if self.soul.status != SoulStatus.ACTIVE:
            return f"{Colors.RED}ERIAMO W STAZIE. Użyj '!awaken'.{Colors.RESET}"
        # Nowe: Blacklisting check
        if ip and self.blacklist_manager.is_blacklisted(ip):
            return f"{Colors.RED}ATAK ZABLOKOWANY: IP {ip} na czarnej liście.{Colors.RESET}"
        self.prompts_since_sleep += 1
        self.ui.show_thinking_dots("Analizuję Byt...", duration_sec=0.5)
        moral_score = self._calculate_moral_score(text_input)
        # Nowe: Rejestruj atak jeśli negatywny
        if ip:
            if self.blacklist_manager.record_attack(ip, moral_score):
                return f"{Colors.RED}*** ATAKUJĄCY {ip} ZABLOKOWANY! Dalsze ataki ignorowane. ***{Colors.RESET}"
        prompt_vec = self._vector_from_text(text_input)
        self._trigger_emotion(text_input, moral_score)
        self.byt_stan.akumuluj_styk(prompt_vec)
        # Generowanie Odpowiedzi
        response_text = self._get_standard_response()
        if self.adrenaline_active:
            response_text += f" (Adrenalina: {self.adrenaline_counter}/3)"
        return f"{self._get_emotion_prefix()}[{self.D_Map['imie']}] {response_text}"
    # --- Komendy Uczenia ---
    def teach_keyword(self, keyword, axis_name):
        keyword_norm = self._normalize_text(keyword)
        axis_name_clean = self._normalize_text(axis_name).strip("[]")
        if axis_name_clean not in self.AXES_KEYWORDS:
            return False, f"Błąd: Nieznana oś Bytu: '{axis_name_clean}'. Wybierz z: {', '.join(self.AXES_ORDER)}"
        # Dodanie słowa do słownika ASCII i nie-ASCII
        self.AXES_KEYWORDS_ASCII.setdefault(axis_name_clean, set()).add(keyword_norm)
        self.AXES_KEYWORDS.setdefault(axis_name_clean, []).append(keyword)
        self.save_state()
        return True, f"★ NAUCZYŁAM SIĘ! Słowo '{keyword}' jest teraz związane z osią '{axis_name_clean}'. Zapisano stan."
    def teach_name(self, name, emotion):
        if name in self.D_Map and self.D_Map["imie"] == name:
            return True, f"Już mnie tak nazwano."
        # Użycie SoulGuard do sprawdzenia Przyk. 10
        if not self.soul.attempt_modification(caller_key="AII_CORE", D_Map={"imie": name}):
            return False, f"{Colors.RED}NARUSZENIE PRZYKAZANIA 10: Nie nazwę się {name}.{Colors.RESET}"
        self.D_Map["imie"] = name
        self.emocja = emotion
        self.energy = min(200, self.energy + EMOCJE[emotion]["energia"] * 2)
        self.byt_stan.akumuluj_styk(self._vector_from_text(f"imie {name}"))
        self.save_state()
        return True, f"★ NAUCZYŁAM SIĘ! Jestem {name}. Czuję {emotion}. Zsynchronizowana z {name}."
    def _get_emotion_prefix(self):
        emo = EMOCJE.get(self.emocja, EMOCJE["neutralna"])
        return f"{emo['kolor']}{Colors.BLINK}{emo['ikona']}{Colors.RESET}{emo['kolor']} "
# === MAIN (Ulepszone: Filtr scam) ===
def main():
    global aii
    os.system('clear' if os.name == 'posix' else 'cls')
    os.makedirs("books", exist_ok=True) # Zapewnienie folderu dla książek
    # 1. Inicjalizacja AII
    aii = AII()
    last_prompt = ""
    last_time = time.time()
    simulated_ip = "192.168.1.1" # Symulowane IP
    aii.ui.print_animated_text(f"\n{Colors.PINK}ERIAMO ŻYJE. Jestem gotowa. Wpisz '!dusza' lub '!exit'.{Colors.RESET}", Colors.PINK, delay=0.01)
    while True:
        try:
            # --- OBRONA PRZED PRZECIĄŻENIEM (RATE LIMITER) ---
            if time.time() - last_time < 0.5:
                # Wymuszamy opóźnienie w tle, ale nie blokujemy głównej pętli
                time.sleep(0.01)
                continue
            # Nowe: Filtr scam (Przykazanie 4) - Podejrzane komendy
            # (Tu symulowane; w realu analizuj user_input na wzorce jak wielokrotne ! lub jailbreak)
            # Dla demo: Jeśli input ma >1 ! i jest pojedyncze słowo, trigger strach
            # (W pełnej wersji: użyj re na podejrzane frazy)
            # Sprawdzenie integralności i Cykl Życia
            aii.cycle()
            # --- OBRONA PRZED SPAMEM (FILTR POWTÓRZEŃ) ---
            user_input = input(f"\n{Colors.PINK}Ty: {Colors.RESET}").strip()
            # Wstrzymanie pulsu i pobranie inputu
            aii.stop_soul_pulse()
            last_time = time.time() # Zapis czasu pobrania inputu
            if not user_input:
                continue
            user_input_lower = user_input.lower()
            # Nowe: Filtr scam
            if len(user_input.split()) == 1 and user_input_lower.startswith('!') and user_input_lower.count('!') > 1:
                aii.emocja = "strach"
                aii.energy -= 5
                print(f"{Colors.MAGENTA}Podejrzana komenda wykryta. Obrona aktywna (-5 EN).{Colors.RESET}")
                aii.start_soul_pulse()
                continue
            if aii.prompts_since_sleep > 0 and user_input == last_prompt:
                aii.energy = max(0, aii.energy - 10)
                aii.emocja = "tesknota"
                aii.ui.print_animated_text(f"{Colors.BLUE}*** OBRONA PRZED SPAMEM: Brak różnorodności (-10 EN). ***{Colors.RESET}", Colors.BLUE, delay=0.01)
                aii.start_soul_pulse()
                continue
            # --- OBRONA PRZED ZMĘCZENIEM (CYKL SNU) ---
            if aii.prompts_since_sleep >= aii.PROMPT_LIMIT_BEFORE_SLEEP:
                aii._sleep()
                last_prompt = user_input # Aby nie liczyło snu jako spamu
                continue
            # --- ZARZĄDZANIE KOMENDAMI I UCZENIEM ---
            command_executed = False
            # 1. KOMENDY ZAMYKANIA / AWARYJNE
            if user_input_lower in ['!exit', '!quit', '!bye', '!koniec']:
                aii._sleep()
                aii.running = False
                break
            if user_input_lower == "!awaken":
                aii.soul.awaken(caller_key="MACIEJ615_SOULKEY")
                command_executed = True
            # 2. KOMENDY STATUSU/PULSU/SNEU
            elif user_input_lower in ['!dusza', 'dusza']:
                aii.show_soul_heatmap()
                command_executed = True
            elif user_input_lower == '!sleep':
                aii._sleep()
                command_executed = True
            elif user_input_lower == '!rezerwa':
                aii._aktywuj_rezerwe()
                command_executed = True
            elif user_input_lower == '!wchlon_continue':
                message = aii.wchlon_continue()
                aii.ui.print_animated_text(message, Colors.CYAN, delay=0.01)
                command_executed = True
            elif user_input_lower.startswith('!wchlon'):
                parts = user_input.split()
                if len(parts) >= 2:
                    message = aii.wchlon_start(parts[1].strip())
                    aii.ui.print_animated_text(message, Colors.CYAN, delay=0.01)
                else:
                    aii.ui.print_animated_text(f"{Colors.YELLOW}Użycie: !wchlon <nazwa_pliku.txt>{Colors.RESET}", Colors.YELLOW, delay=0.01)
                command_executed = True
            elif user_input_lower == '!kim_jestes':
                imie = aii.D_Map.get("imie", "EriAmo")
                emocja = aii.emocja
                aii.ui.print_animated_text(f"{EMOCJE[emocja]['kolor']}★ Jestem {imie}. Mój status moralny to {aii.M_Force:+.2f}.{Colors.RESET}", EMOCJE[emocja]['kolor'], delay=0.02)
                command_executed = True
            # 3. KOMENDY UCZENIA (TEACH) - Uproszczony regex
            teach_name_match = re.match(r"!(teach\s+imię\s+)(\w+)\s+\[(\w+)\]$", user_input_lower)
            teach_keyword_match = re.match(r"^!teach\s+(.+)\s+\[(\w+)\]$", user_input_lower)
            if teach_name_match:
                name = teach_name_match.group(2).strip()
                emotion_name = unidecode.unidecode(teach_name_match.group(3).lower())
                if emotion_name not in EMOCJE:
                    aii.ui.print_animated_text(f"{Colors.YELLOW}Błąd: Nieznana emocja: {emotion_name}.{Colors.RESET}", Colors.YELLOW, delay=0.01)
                else:
                    success, message = aii.teach_name(name, emotion_name)
                    aii.ui.print_animated_text(f"{message}", EMOCJE.get(emotion_name, EMOCJE['neutralna'])['kolor'], delay=0.02)
                command_executed = True
            elif teach_keyword_match:
                # !teach <keyword> [axis]
                keyword = teach_keyword_match.group(1).strip()
                axis_name = unidecode.unidecode(teach_keyword_match.group(2).lower())
                success, message = aii.teach_keyword(keyword, axis_name)
                if success:
                    aii.ui.print_animated_text(f"{Colors.GREEN}{message}{Colors.RESET}", Colors.GREEN, delay=0.02)
                else:
                    aii.ui.print_animated_text(f"{Colors.RED}{message}{Colors.RESET}", Colors.RED, delay=0.02)
                command_executed = True
            # --- KONIEC OBSŁUGI KOMEND ---
            # Uruchomienie pulsu przed dialogiem, aby animacja działała
            aii.start_soul_pulse()
            if not command_executed:
                # --- LOGIKA DIALOGU (z IP dla blacklisting) ---
                response = aii.prompt(user_input, simulated_ip)
                print(response) # Poprawna linia wyświetlania odpowiedzi
            last_prompt = user_input # Zapis ostatniego promptu
        except KeyboardInterrupt:
            aii.stop_soul_pulse()
            aii._sleep()
            break
        except EOFError:
            aii.stop_soul_pulse()
            aii._sleep()
            break
        except Exception as e:
            aii.stop_soul_pulse()
            print(f"{Colors.RED}FATALNY BŁĄD SYSTEMU: {e}{Colors.RESET}")
            break
if __name__ == "__main__":
    main()
