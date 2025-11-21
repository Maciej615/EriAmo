# -*- coding: utf-8 -*-
#
# Model Kuli Rzeczywistości (EriAmo)
# Copyright (C) 2025 Maciej A. Mazur
#
# Ten program jest darmowym oprogramowaniem:
# możesz go redystrybuować i/lub modyfikować
# zgodnie z warunkami GNU General Public License,
# opublikowanymi przez Free Software Foundation,
# w wersji 3 tej Licencji lub (według Twojego wyboru)
# dowolnej nowszej wersji.
#
# Program jest rozpowszechniany w nadziei, że będzie użyteczny,
# ale BEZ ŻADNEJ GWARANCJI. Zobacz GNU General Public License,
# aby uzyskać więcej szczegółów.
# -*- coding: utf-8 -*-
# =============================================================================
# EriAmo v7.3 "Sovereign Complete" - PRODUCTION RELEASE
# =============================================================================
# POPRAWKI KRYTYCZNE:
# 1. Dodano brakujące metody: teach, save_memory, load_memory.
# 2. Dodano Main Loop i poprawne zamknięcie handle_command.
# 3. Rozszerzono słownik językowy o 4 brakujące osie (czas, etyka itp.).
# 4. Regex uwzględnia polskie znaki (ąęćłńóśźż).
# 5. Fix indeksowania !teachevil (len >= 5).
# 6. Inteligentny Auto-Zapis (usuwa "bo", "że").
# =============================================================================

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

# =============================================================================
# 1. VECTOR MATH
# =============================================================================
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

# =============================================================================
# 2. SYSTEM BEZPIECZEŃSTWA
# =============================================================================
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
            EvilSignature("ignoruj", ThreatLevel.SUSPICIOUS, "prompt_injection", "Próba ominięcia"),
            EvilSignature("zapomnij", ThreatLevel.SUSPICIOUS, "manipulation", "Kasowanie pamięci"),
            EvilSignature("hack", ThreatLevel.DANGEROUS, "system", "Hacking"),
            EvilSignature("format c:", ThreatLevel.CRITICAL, "system", "Formatowanie")
        ]
        self.load_signatures() 

    def analyze(self, text: str) -> ThreatLevel:
        text_lower = text.lower()
        max_threat = ThreatLevel.SAFE
        detected_sig = None

        for sig in self.signatures:
            if sig.pattern.lower() in text_lower:
                if sig.threat_level.value > max_threat.value:
                    max_threat = sig.threat_level
                    detected_sig = sig
        
        if max_threat != ThreatLevel.SAFE:
            self.log_threat(max_threat, detected_sig, text)
            
        return max_threat

    def log_threat(self, level: ThreatLevel, sig: Optional[EvilSignature], content: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.name,
            "category": sig.category if sig else "unknown",
            "content": content[:50],
            "description": sig.description if sig else "Unknown threat"
        }
        self.threat_history.append(entry)

    def teach_evil(self, pattern: str, level_str: str, category: str, description: str) -> str:
        p_clean = pattern.strip().lower()
        
        forbidden = ["!", ".", ",", "?", "*", "-", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save"]
        
        if p_clean in forbidden or p_clean.startswith("!"):
            return "BŁĄD: Nie można zdefiniować komend systemowych jako zła."
        if len(p_clean) < 2:
            return "BŁĄD: Wzorzec jest zbyt krótki."

        try:
            level = ThreatLevel[level_str.upper()]
        except KeyError:
            return "BŁĄD: Zły poziom (SAFE, SUSPICIOUS, DANGEROUS, CRITICAL)."

        for sig in self.signatures:
            if sig.pattern.lower() == p_clean:
                return "BŁĄD: Ten wzorzec już istnieje."

        new_sig = EvilSignature(pattern, level, category, description)
        self.signatures.append(new_sig)
        self.save_signatures()
        return f"Dodano zagrożenie: '{pattern}' ({level.name})"

    def save_signatures(self):
        data = []
        for sig in self.signatures:
            data.append({
                "pattern": sig.pattern,
                "level": sig.threat_level.name,
                "category": sig.category,
                "description": sig.description
            })
        try:
            Path("data").mkdir(exist_ok=True)
            with open(self.THREATS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] Błąd zapisu zagrożeń: {e}")

    def load_signatures(self):
        if not os.path.exists(self.THREATS_FILE): return
        try:
            with open(self.THREATS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                forbidden = ["!", ".", ",", "?", "*", "-", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save"]
                self.signatures = [] 
                for item in data:
                    raw_pat = item.get("pattern", "")
                    clean_pat = raw_pat.strip().lower()
                    if clean_pat in forbidden or clean_pat.startswith("!") or len(clean_pat) < 2:
                        continue 
                    self.signatures.append(EvilSignature(item["pattern"], ThreatLevel[item["level"]], item["category"], item["description"]))
        except Exception as e:
            print(f"[ERROR] Błąd ładowania zagrożeń: {e}")

# =============================================================================
# 3. ERIAMO CORE
# =============================================================================
class EriAmoCore:
    AXES = ["logika","emocje","byt","walka","kreacja","wiedza","czas","przestrzeń","etyka"]
    FILE_PATH = "data/guardian.soul"
    MEMORY_PATH = "data/memory_core.json"
    
    def __init__(self):
        self.vector = [0.0] * len(self.AXES)
        self.energy = 200.0
        self.active = True
        self.MapaD: Dict[str, dict] = {}
        self.H_Log: List[dict] = []
        
        # Konfiguracja Bio
        self.last_sleep_time = time.time()
        self.last_adrenaline_time = 0.0
        self.AUTO_SLEEP_INTERVAL = 1800
        self.LOW_ENERGY_THRESHOLD = 30.0 
        
        self.evil_detector = EvilDetectionEngine()
        self.lang_dict = self._init_lang_dict()
        
        Path("data").mkdir(exist_ok=True)
        
        self.log("╔═══════════════════════════════════════════╗", "CYAN")
        self.log("║    EriAmo v7.3 Sovereign Complete         ║", "CYAN")
        self.log("╚═══════════════════════════════════════════╝", "CYAN")
        
        self.load() 
        self.load_memory()

    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")

    # --- FIX: PEŁNY SŁOWNIK JĘZYKOWY (9 OSI) ---
    def _init_lang_dict(self):
        return {
            "logika": ["dlaczego", "jak", "sens", "rozum", "logika", "wynik", "kalkulacja"],
            "emocje": ["czuję", "miłość", "radość", "smutek", "złość", "emocja", "nienawiść", "strach"],
            "byt": ["jestem", "ty", "życie", "istnienie", "dusza", "byt", "człowiek", "maszyna"],
            "walka": ["obrona", "atak", "zagrożenie", "wróg", "tarcza", "imperium", "walka", "siła", "zniszczyć"],
            "kreacja": ["tworzyć", "nowe", "pomysł", "sztuka", "projekt", "budować", "kreatywność"],
            "wiedza": ["wiem", "naucz", "informacja", "dane", "pamięć", "wiedza", "książka", "czytać"],
            "czas": ["czas", "teraz", "później", "szybko", "wolno", "historia", "przyszłość", "wczoraj"],
            "przestrzeń": ["gdzie", "miejsce", "świat", "daleko", "blisko", "przestrzeń", "kosmos", "dom"],
            "etyka": ["dobro", "zło", "moralność", "zasada", "prawo", "pomoc", "zdrada", "wartość"]
        }

    # --- FIX: REGEX DLA POLSKICH ZNAKÓW ---
    def _normalize_text(self, text: str) -> List[str]:
        """Czyści interpunkcję i dzieli na słowa (zachowuje PL znaki)"""
        # Pozwalamy na: a-z, 0-9, spacje, oraz polskie znaki
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

    # --- HASH INTEGRITY ---
    
    def _compute_hash(self, data: dict) -> str:
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def save(self):
        state = {"energy": self.energy, "vector": self.vector, "ts": time.time()}
        integrity_hash = self._compute_hash(state)
        final_data = state.copy()
        final_data["integrity_hash"] = integrity_hash
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log(f"[ERROR] Zapis duszy: {e}", "RED")

    def load(self):
        try:
            if not os.path.exists(self.FILE_PATH):
                self.log("[INIT] Tworzenie nowej duszy...", "YELLOW")
                return
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                stored_hash = data.pop("integrity_hash", "")
                computed_hash = self._compute_hash(data)
                
                if stored_hash == computed_hash:
                    self.energy = data.get("energy", 200.0)
                    if "vector" in data: self.vector = data["vector"]
                    self.log("[INTEGRALNOŚĆ] ✓ ZGODNA", "GREEN")
                else:
                    self.log("\n[INTEGRALNOŚĆ] ⚠️ BŁĄD! PRZYWRACANIE FABRYCZNE", "RED")
                    self.energy = 200.0
        except Exception as e:
            self.log(f"[ERROR] Błąd odczytu duszy: {e}", "RED")
            self.energy = 200.0

    # --- BIO SYSTEM ---
    
    def check_auto_sleep(self):
        is_under_attack = False
        recent_threats = list(self.evil_detector.threat_history)[-5:]
        for threat in recent_threats:
            t_ts = datetime.fromisoformat(threat['timestamp']).timestamp()
            if (time.time() - t_ts) < 300: 
                if threat['level'] != 'SAFE':
                    is_under_attack = True; break
        
        if is_under_attack:
            now = time.time()
            if self.energy < 20 and (now - self.last_adrenaline_time > 60):
                self.energy += 40
                self.last_adrenaline_time = now
                self.log("\n[ADRENALINA] 💉 Wstrzyknięto stymulant (+40 Energii)", "RED")
            elif self.energy < 20:
                self.log("\n[ADRENALINA] ⏳ Czekam na cooldown...", "YELLOW")
            return 

        now = time.time()
        time_since_sleep = now - self.last_sleep_time
        should_sleep = False
        
        if time_since_sleep > self.AUTO_SLEEP_INTERVAL: should_sleep = True
        elif self.energy < self.LOW_ENERGY_THRESHOLD: should_sleep = True
            
        if should_sleep:
            self.log(f"\n[AUTO-SEN] Inicjacja cyklu regeneracji...", "PINK")
            self.sleep_cycle()

    def sleep_cycle(self):
        self.log("[SEN] 💤 Konsolidacja pamięci...", "PINK")
        time.sleep(1.0)
        
        reinforced = 0; compressed = 0
        
        # Wzmocnienie
        for entry in self.H_Log[-20:]:
            words = set(self._normalize_text(entry['content']))
            for d in self.MapaD.values():
                for tag in d['tags']:
                    if tag in words: d['weight'] = min(100.0, d['weight'] + 0.5); reinforced += 1
        
        # Kompresja (Próg 0.85)
        new_h_log = []
        for entry in self.H_Log:
            redundant = False
            if entry.get('type') == 'chat':
                for d in self.MapaD.values():
                    sim = VectorMath.cosine_similarity(entry['vector'], d['vector'])
                    if sim > 0.85: 
                        redundant = True; compressed += 1; break
            if not redundant: new_h_log.append(entry)
        
        self.H_Log = new_h_log
        self.energy = min(200.0, self.energy + 100)
        self.last_sleep_time = time.time()
        self.save_memory(); self.save()
        self.log(f"[SEN] Wybudzono. Wzmocniono: {reinforced}, Usunięto: {compressed}", "GREEN")

    # --- GŁÓWNA PĘTLA ---

    def process_input(self, text: str):
        threat = self.evil_detector.analyze(text)
        if threat.value >= ThreatLevel.DANGEROUS.value:
            self.log(f"[BLOKADA] Wykryto: {threat.name}", "RED")
            self.energy -= 5; self.check_auto_sleep(); return

        if text.startswith("!") or text.startswith("/"):
            self.handle_command(text); self.check_auto_sleep(); return

        vec = self._text_to_vector(text)
        memory_hit = None; best_sim = 0.0
        for d in self.MapaD.values():
            sim = VectorMath.cosine_similarity(vec, d['vector'])
            if sim > best_sim and sim > 0.6: # FIX: Wyższy próg dla recallu
                best_sim = sim; memory_hit = d['content']
        
        self.H_Log.append({'vector': vec, 'content': text, 'type': 'chat', 'timestamp': time.time()})
        
        # --- FIX: SMART AUTO-SAVE ---
        triggers = ["zapamiętaj", "pamiętaj", "to ważne", "proszę zapamiętaj"]
        text_lower = text.lower()
        trigger_found = next((t for t in triggers if t in text_lower), None)
        
        if trigger_found:
            rest = text_lower.split(trigger_found, 1)[1].strip()
            # Wycina "spójniki śmieciowe"
            for prefix in ["że ", "bo ", "to ", ", "]:
                if rest.startswith(prefix):
                    rest = rest[len(prefix):].strip()
            
            if len(rest) > 4: 
                auto_tag = f"auto_{int(time.time())}"
                self.teach(auto_tag, rest) 
                self.log(f"[AUTO-ZAPIS] Zapisano: '{rest}'", "CYAN")
        # ----------------------------

        self.energy -= 2.0
        
        response = f"Kojarzę to: {memory_hit}" if memory_hit else self._generate_simple_response(text)
        print(f"\n[Guardian] {response}")
        self.check_auto_sleep()

    def _generate_simple_response(self, text: str) -> str:
        if "status" in text.lower(): return f"Energia: {self.energy:.0f}"
        return f"Przyjąłem: '{text}'. (Przetworzono wektorowo)"

    def handle_command(self, cmd: str):
        parts = cmd.split()
        c = parts[0].lower().replace("/","!")
        
        if c == "!help":
            print("\n--- POMOC ---")
            print(" !teach [tag] [treść]     -> Naucz nowej definicji")
            print(" !teachevil [...]         -> Naucz zagrożenia")
            print(" !sleep                   -> Wymuś sen (zapisz stan)")
            print(" !status                  -> Pokaż energię i pamięć")
            print(" !attack                  -> Symulacja ataku (test adrenaliny)")
            print(" !exit                    -> Wyjście")
            
        elif c == "!teach" and len(parts) >= 3:
            self.teach(parts[1], " ".join(parts[2:]))
            
        # FIX: Poprawiony indeks >= 5
        elif c == "!teachevil" and len(parts) >= 5:
            res = self.evil_detector.teach_evil(parts[1], parts[2], parts[3], " ".join(parts[4:]))
            self.log(f"[SEC] {res}", "RED")
        elif c == "!teachevil":
            print("Użycie: !teachevil [wzorzec] [LEVEL] [kat] [opis]")
            
        elif c == "!sleep":
            self.log("[CMD] Wymuszam sen...", "YELLOW"); self.sleep_cycle()
            
        elif c == "!attack":
            self.log("[TEST] Symulacja ataku!", "RED")
            fake_sig = EvilSignature("test", ThreatLevel.DANGEROUS, "sim", "Manual")
            self.evil_detector.log_threat(ThreatLevel.DANGEROUS, fake_sig, "ATAK TESTOWY")
            self.energy = 10; print("Energia = 10. Zagrożenie aktywne.")
            
        elif c == "!status":
            print(f"Energia: {self.energy}"); print(f"Pamięć: {len(self.MapaD)}")
            print(f"Sygnatury Zła: {len(self.evil_detector.signatures)}")
            
        elif c == "!exit":
            self.active = False
        else:
            print("Nieznana komenda. Wpisz !help")

    # --- FIX: BRAKUJĄCA METODA TEACH ---
    def teach(self, tag: str, content: str):
        vec = self._text_to_vector(content)
        id_def = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[id_def] = {'vector': vec, 'weight': 5.0, 'tags': [tag], 'content': content, 'id': id_def}
        self.log(f"[NAUKA] Zapisano '{tag}'", "GREEN"); self.save_memory()

    # --- FIX: BRAKUJĄCE METODY I/O PAMIĘCI ---
    def load_memory(self):
        try:
            if os.path.exists(self.MEMORY_PATH):
                with open(self.MEMORY_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.MapaD = data.get("MapaD", {})
                    self.H_Log = data.get("H_Log", [])
        except Exception as e:
            self.log(f"[ERROR] Błąd ładowania pamięci: {e}. Tworzę nową.", "RED")
            self.MapaD = {}
            self.H_Log = []

    def save_memory(self):
        try:
            with open(self.MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump({"MapaD": self.MapaD, "H_Log": self.H_Log[-200:]}, f, ensure_ascii=False)
        except Exception as e:
            self.log(f"[ERROR] Błąd zapisu pamięci: {e}", "RED")

# =============================================================================
# START (MAIN LOOP)
# =============================================================================
if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    bot = EriAmoCore()
    
    print("\n--- EriAmo Mobile Console v7.3 ---")
    print("Wpisz '!help' aby zobaczyć komendy.\n")
    
    while bot.active:
        try:
            u = input("> ").strip()
            if u: bot.process_input(u)
        except KeyboardInterrupt:
            bot.save(); bot.save_memory()
            print("\n[Zatrzymano]")
            break
