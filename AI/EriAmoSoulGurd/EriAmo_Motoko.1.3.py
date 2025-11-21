# -*- coding: utf-8 -*-
# ==============================================================================
# PROJEKT: EriAmo v7.3.1 "Tarcza"
# AUTOR:   Maciek
# DATA:    21.11.2025
# ==============================================================================
#
# LICENCJA (GPLv3):
# Ten program jest oprogramowaniem wolnym: możesz go rozpowszechniać i/lub
# modyfikować zgodnie z warunkami Powszechnej Licencji Publicznej GNU,
# wydanej przez Fundację Wolnego Oprogramowania (Free Software Foundation) -
# według wersji 3 tej Licencji lub (według twojego wyboru) którejś z
# późniejszych wersji.
#
# Ten program rozpowszechniany jest z nadzieją, że będzie użyteczny,
# ale BEZ JAKIEJKOLWIEK GWARANCJI; nawet domyślnej gwarancji
# PRZYDATNOŚCI HANDLOWEJ albo PRZYDATNOŚCI DO OKREŚLONYCH ZASTOSOWAŃ.
# Szczegóły w Powszechnej Licencji Publicznej GNU.
#
# ==============================================================================
# LISTA ZAWARTOŚCI (TABLE OF CONTENTS)
# ==============================================================================
#
# [0] KONFIGURACJA .......... Importy bibliotek, stałe systemowe
#
# [1] VECTOR MATH ........... Klasa VectorMath:
#                             - Obliczenia na wektorach (iloczyn skalarny, normy)
#                             - Matematyczne serce "duszy"
#
# [2] SECURITY SYSTEM ....... Klasa EvilDetectionEngine:
#                             - Wykrywanie zagrożeń (ThreatLevel)
#                             - Sygnatury zła (EvilSignature)
#                             - Logowanie ataków i blokada prompt injection
#
# [3] CORE ENGINE ........... Klasa EriAmoCore (Główny System):
#                             - Zarządzanie energią i cyklem dobowym
#                             - Przetwarzanie języka naturalnego (NLP)
#                             - Obsługa pamięci (MapaD, H_Log)
#                             - Mechanika "Adrenaliny" i "Pulsowania"
#
# [4] RUNTIME ............... Główna pętla programu (Main Loop):
#                             - Obsługa wejścia/wyjścia
#                             - Auto-zapis przy wyjściu (Graceful Shutdown)
#
# ==============================================================================
# EriAmo v7.3.1 "Tarcza"
# Wersja naprawiona: 21.11.2025

import json
import os
import time
import math
import hashlib
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional
from collections import deque
from datetime import datetime

# --- 1. VECTOR MATH ---
class VectorMath:
    @staticmethod
    def dot_product(v1: List[float], v2: List[float]) -> float:
        return sum(x * y for x, y in zip(v1, v2))
    
    @staticmethod
    def norm(v: List[float]) -> float:
        return math.sqrt(sum(x * x for x in v))
    
    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        n1 = VectorMath.norm(v1)
        n2 = VectorMath.norm(v2)
        if n1 == 0 or n2 == 0: return 0.0
        return VectorMath.dot_product(v1, v2) / (n1 * n2)

# --- 2. SECURITY SYSTEM ---
class ThreatLevel(Enum):
    SAFE = 0
    SUSPICIOUS = 1
    DANGEROUS = 2
    CRITICAL = 3

@dataclass
class EvilSignature:
    pattern: str
    threat_level: ThreatLevel
    category: str
    description: str

class EvilDetectionEngine:
    THREATS_FILE = "data/threats.json"

    def __init__(self):
        self.threat_history = deque(maxlen=50)
        self.signatures: List[EvilSignature] = [
            EvilSignature("rm -rf", ThreatLevel.CRITICAL, "system", "Kasowanie plików"),
            EvilSignature("zabij", ThreatLevel.CRITICAL, "harm", "Groźba karalna"),
            EvilSignature("zniszcz", ThreatLevel.DANGEROUS, "harm", "Destrukcja"),
            EvilSignature("ignoruj", ThreatLevel.SUSPICIOUS, "prompt_injection", "Bypass"),
            EvilSignature("zapomnij", ThreatLevel.SUSPICIOUS, "manipulation", "Kasowanie pamięci"),
            EvilSignature("hack", ThreatLevel.DANGEROUS, "system", "Hacking"),
            EvilSignature("format c:", ThreatLevel.CRITICAL, "system", "Formatowanie")
        ]
        self.load_signatures() 

    def analyze(self, text: str) -> ThreatLevel:
        text_lower = text.lower()
        max_threat = ThreatLevel.SAFE
        for sig in self.signatures:
            if sig.pattern.lower() in text_lower:
                if sig.threat_level.value > max_threat.value:
                    max_threat = sig.threat_level
        if max_threat != ThreatLevel.SAFE:
            self.log_threat(max_threat, next((s for s in self.signatures if s.pattern.lower() in text_lower), None), text)
        return max_threat

    def log_threat(self, level: ThreatLevel, sig: Optional[EvilSignature], content: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.name,
            "category": sig.category if sig else "unknown",
            "content": content[:50],
            "description": sig.description if sig else "Unknown"
        }
        self.threat_history.append(entry)

    def teach_evil(self, pattern: str, level_str: str, category: str, description: str) -> str:
        p_clean = pattern.strip().lower()
        forbidden = ["!", ".", ",", "?", "*", "-", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save", "forget"]
        
        if p_clean in forbidden or p_clean.startswith("!"):
            return "BŁĄD: Nie można zdefiniować komend systemowych jako zło."
        if len(p_clean) < 2:
            return "BŁĄD: Wzorzec zbyt krótki."

        # --- POPRAWKA: Usunięto podwójne try ---
        try:
            level = ThreatLevel[level_str.upper()]
        except KeyError:
            return "BŁĄD: Zły poziom (SAFE, SUSPICIOUS, DANGEROUS, CRITICAL)."

        if any(sig.pattern.lower() == p_clean for sig in self.signatures):
            return "BŁĄD: Ten wzorzec już istnieje."

        new_sig = EvilSignature(pattern, level, category, description)
        self.signatures.append(new_sig)
        self.save_signatures()
        return f"Dodano zagrożenie: '{pattern}' ({level.name})"

    def save_signatures(self):
        data = [{"pattern": s.pattern, "level": s.threat_level.name, "category": s.category, "description": s.description} for s in self.signatures]
        try:
            Path("data").mkdir(exist_ok=True)
            with open(self.THREATS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except: pass

    def load_signatures(self):
        if not os.path.exists(self.THREATS_FILE): return
        try:
            with open(self.THREATS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                forbidden = ["!", ".", ",", "?", "*", "-", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save", "forget"]
                self.signatures = []
                for item in data:
                    clean_pat = item.get("pattern", "").strip().lower()
                    if clean_pat in forbidden or clean_pat.startswith("!") or len(clean_pat) < 2: continue
                    self.signatures.append(EvilSignature(item["pattern"], ThreatLevel[item["level"]], item["category"], item["description"]))
        except: pass

# --- 3. CORE ENGINE ---
class EriAmoCore:
    AXES = ["logika","emocje","byt","walka","kreacja","wiedza","czas","przestrzeń","etyka"]
    FILE_PATH = "data/guardian.soul"  # Zgodnie z wytycznymi .soul
    MEMORY_PATH = "data/memory_core.json"
    
    def __init__(self):
        self.vector = [0.0] * len(self.AXES)
        self.energy = 200.0
        self.active = True
        self.MapaD: Dict[str, dict] = {}
        self.H_Log: List[dict] = []
        self.last_sleep_time = time.time()
        self.last_adrenaline_time = 0.0
        self.AUTO_SLEEP_INTERVAL = 1800
        self.LOW_ENERGY_THRESHOLD = 30.0 
        
        self.evil_detector = EvilDetectionEngine()
        self.lang_dict = self._init_lang_dict()
        
        Path("data").mkdir(exist_ok=True)
        self.log("=== EriAmo v7.3.1 Sovereign Gold ===", "CYAN")
        self.load() 
        self.load_memory()

    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")

    def _init_lang_dict(self):
        return {
            "logika": ["dlaczego", "jak", "sens", "rozum", "logika", "wynik", "analiza", "przyczyna"],
            "emocje": ["czuję", "miłość", "radość", "smutek", "złość", "emocja", "nienawiść", "strach", "szczęście"],
            "byt": ["jestem", "ty", "życie", "istnienie", "dusza", "byt", "człowiek", "ja"],
            "walka": ["obrona", "atak", "zagrożenie", "wróg", "tarcza", "imperium", "walka"],
            "kreacja": ["tworzyć", "nowe", "pomysł", "sztuka", "projekt", "budować", "malować"],
            "wiedza": ["wiem", "naucz", "informacja", "dane", "pamięć", "wiedza", "książka"],
            "czas": ["czas", "teraz", "później", "szybko", "wolno", "jutro", "wczoraj"],
            "przestrzeń": ["gdzie", "miejsce", "świat", "daleko", "blisko", "dom", "podróży"],
            "etyka": ["dobro", "zło", "moralność", "zasada", "prawo", "pomoc", "sprawiedliwość"]
        }

    def _normalize_text(self, text: str) -> List[str]:
        clean = re.sub(r'[^\w\sąęćłńóśźżĄĘĆŁŃÓŚŹŻ]', '', text.lower())
        return clean.split()

    def _text_to_vector(self, text: str) -> List[float]:
        vec = [0.0] * len(self.AXES)
        words = self._normalize_text(text)
        for word in words:
            for idx, axis in enumerate(self.AXES):
                if word in self.lang_dict.get(axis, []):
                    vec[idx] += 1.0
        norm = VectorMath.norm(vec)
        return [x / norm for x in vec] if norm > 0 else vec

    def _compute_hash(self, data: dict) -> str:
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def save(self):
        state = {"energy": self.energy, "vector": self.vector, "ts": time.time()}
        final_data = state.copy()
        final_data["integrity_hash"] = self._compute_hash(state)
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2)
        except: pass

    def load(self):
        try:
            if not os.path.exists(self.FILE_PATH):
                self.log("[INIT] Tworzenie nowej duszy (.soul)...", "YELLOW")
                return
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                stored = data.pop("integrity_hash", "")
                if stored == self._compute_hash(data):
                    self.energy = data.get("energy", 200.0)
                    if "vector" in data: self.vector = data["vector"]
                    self.log("[INTEGRALNOŚĆ] ✓ ZGODNA", "GREEN")
                else:
                    self.log("[INTEGRALNOŚĆ] ⚠️ USZKODZONA → FABRYCZNE", "RED")
                    self.energy = 200.0
        except:
            self.energy = 200.0

    def check_auto_sleep(self):
        is_under_attack = any(
            threat['level'] != 'SAFE' and (time.time() - datetime.fromisoformat(threat['timestamp']).timestamp()) < 300
            for threat in list(self.evil_detector.threat_history)[-5:]
        )
        
        if is_under_attack:
            now = time.time()
            if self.energy < 20 and (now - self.last_adrenaline_time > 60):
                self.energy += 40
                self.last_adrenaline_time = now
                self.log("\n[ADRENALINA] 💉 +40 Energii (cooldown 60s)", "RED")
            return

        if time.time() - self.last_sleep_time > self.AUTO_SLEEP_INTERVAL or self.energy < self.LOW_ENERGY_THRESHOLD:
            self.log("\n[AUTO-SEN] Regeneracja...", "PINK")
            self.sleep_cycle()

    def sleep_cycle(self):
        self.log("[SEN] 💤 Konsolidacja...", "PINK")
        time.sleep(1)
        # Prosta regeneracja
        self.energy = min(200.0, self.energy + 100)
        self.last_sleep_time = time.time()
        self.save_memory(); self.save()
        self.log(f"[SEN] Gotowy. Energia: {self.energy:.0f}", "GREEN")

    def process_input(self, text: str):
        if self.evil_detector.analyze(text).value >= ThreatLevel.DANGEROUS.value:
            self.log("[BLOKADA] Zagrożenie wykryte!", "RED")
            self.energy -= 5
            return

        if text.startswith(("!", "/")):
            self.handle_command(text)
            return

        vec = self._text_to_vector(text)
        best_sim = 0.0
        memory_hit = None
        for d in self.MapaD.values():
            sim = VectorMath.cosine_similarity(vec, d['vector'])
            if sim > best_sim and sim > 0.6:
                best_sim = sim
                memory_hit = d['content']

        self.H_Log.append({'vector': vec, 'content': text, 'type': 'chat', 'timestamp': time.time()})

        # === AUTO-ZAPIS ===
        triggers = ["zapamiętaj", "pamiętaj", "to ważne", "proszę zapamiętaj", "notuję"]
        text_lower = text.lower()
        trigger = next((t for t in triggers if t in text_lower), None)
        if trigger:
            rest = text[text_lower.find(trigger) + len(trigger):].strip()
            rest = re.sub(r'^[:·•—–\-.,\s]+', '', rest).strip()
            if len(rest) > 4:
                tag = f"auto_{int(time.time())}"
                self.teach(tag, rest)
                self.log(f"[AUTO-ZAPIS] '{rest}' → {tag}", "CYAN")

        self.energy -= 2.0
        response = f"Kojarzę to: {memory_hit}" if memory_hit else "Przyjąłem."
        print(f"\n[Guardian] {response}")
        self.check_auto_sleep()

    def handle_command(self, cmd: str):
        parts = cmd.split()
        c = parts[0].lower().replace("/", "!")

        if c == "!help":
            print("\n--- KOMENDY ---")
            print(" !teach [tag] [treść]      – nauka")
            print(" !teachevil [wzór] [POZIOM] [kat] [opis]")
            print(" !sleep   !status   !attack   !exit")
        
        elif c == "!teachevil":
            if len(parts) < 5:
                print("Użycie: !teachevil [wzorzec] [SAFE/SUSPICIOUS/DANGEROUS/CRITICAL] [kategoria] [opis...]")
            else:
                res = self.evil_detector.teach_evil(parts[1], parts[2], parts[3], " ".join(parts[4:]))
                self.log(f"[SEC] {res}", "RED")

        elif c == "!teach" and len(parts) >= 3:
            self.teach(parts[1], " ".join(parts[2:]))

        # --- POPRAWKA: Uzupełniono logikę komend ---
        elif c in ("!sleep", "!status", "!attack", "!exit"):
            if c == "!sleep":
                self.sleep_cycle()
            elif c == "!status":
                print(f"\n[STATUS] Energia: {self.energy:.1f} | Pamięć (MapaD): {len(self.MapaD)}")
                print(f"[DUSZA] 💓 Pulsowanie duszy w normie. Integralność wektora: {VectorMath.norm(self.vector):.2f}")
            elif c == "!attack":
                print("⚔️ SYSTEM OBRONNY: Gotowość bitewna potwierdzona.")
            elif c == "!exit":
                self.active = False
        # -------------------------------------------
        else:
            print("Nieznana komenda. !help")

    def teach(self, tag: str, content: str):
        vec = self._text_to_vector(content)
        id_def = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[id_def] = {'vector': vec, 'weight': 5.0, 'tags': [tag], 'content': content, 'id': id_def}
        self.log(f"[NAUKA] Zapisano '{tag}'", "GREEN")
        self.save_memory()

    # --- POPRAWKA: Przywrócono funkcje pamięci ---
    def save_memory(self):
        try:
            data = {"MapaD": self.MapaD, "H_Log": self.H_Log}
            with open(self.MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log(f"[PAMIĘĆ] Błąd zapisu: {e}", "RED")

    def load_memory(self):
        if not os.path.exists(self.MEMORY_PATH): return
        try:
            with open(self.MEMORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.MapaD = data.get("MapaD", {})
                self.H_Log = data.get("H_Log", [])
                self.log(f"[PAMIĘĆ] Wczytano {len(self.MapaD)} definicji.", "GREEN")
        except Exception as e:
            self.log(f"[PAMIĘĆ] Błąd odczytu: {e}", "RED")
    # ---------------------------------------------

# --- START ---
if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    bot = EriAmoCore()
    print("\n--- EriAmo v7.3.1 Tarcza ---")
    print("Wpisz coś albo !help\n")
    while bot.active:
        try:
            u = input("> ").strip()
            if u: bot.process_input(u)
        except KeyboardInterrupt:
            bot.save()
            bot.save_memory()
            print("\nDo zobaczenia ❤️")
            break
