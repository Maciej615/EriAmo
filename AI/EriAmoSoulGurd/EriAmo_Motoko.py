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
#
# =============================================================================
# EriAmo v6.9 "Integrity Protected" - FINAL MOBILE BUILD
# =============================================================================
# CECHY:
# 1. VectorMath: Lekki silnik matematyczny (bez Numpy).
# 2. Memory Core: Trwała pamięć (MapaD) i epizodyczna (H_Log).
# 3. Bio-Clock: Zmęczenie, Sen i Kompresja.
# 4. Combat Override: Adrenalina blokuje sen podczas ataku.
# 5. Evil Hunter (Safe): Uczenie zagrożeń z blokadą auto-sabotażu.
# 6. SoulGuard: Weryfikacja sumy kontrolnej (SHA-256) przy starcie/zamknięciu.
# =============================================================================

import json
import os
import time
import math
import hashlib  # <--- WYMAGANE DO OCHRONY INTEGRALNOŚCI
import threading
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any
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
# 2. SYSTEM BEZPIECZEŃSTWA (Evil Detection)
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
        
        # Safety Protocols
        forbidden = ["!", ".", ",", "?", "*", "-", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save"]
        
        if p_clean in forbidden or p_clean.startswith("!"):
            return "BŁĄD: Nie można zdefiniować komend systemowych jako zła (Auto-Sabotaż)."
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
                        print(f"[SEC] ⚠️ Pominięto uszkodzoną sygnaturę: '{raw_pat}'")
                        continue 
                    self.signatures.append(EvilSignature(item["pattern"], ThreatLevel[item["level"]], item["category"], item["description"]))
        except Exception as e:
            print(f"[ERROR] Błąd ładowania zagrożeń: {e}")

# =============================================================================
# 3. ERIAMO CORE (Z SoulGuard Integrity Check)
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
        
        self.last_sleep_time = time.time()
        self.AUTO_SLEEP_INTERVAL = 1800
        self.LOW_ENERGY_THRESHOLD = 30.0 
        
        self.evil_detector = EvilDetectionEngine()
        self.lang_dict = self._init_lang_dict()
        
        Path("data").mkdir(exist_ok=True)
        
        # Inicjalizacja
        self.log("╔═══════════════════════════════════════════╗", "CYAN")
        self.log("║ EriAmo v6.9 Mobile Sovereign (INTEGRITY)  ║", "CYAN")
        self.log("╚═══════════════════════════════════════════╝", "CYAN")
        
        self.load()        # <--- Tu następuje weryfikacja HASH
        self.load_memory()

    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")

    def _init_lang_dict(self):
        return {
            "logika": ["dlaczego", "jak", "sens", "rozum"],
            "emocje": ["czuję", "miłość", "radość", "smutek", "złość"],
            "byt": ["jestem", "ty", "życie", "istnienie", "dusza"],
            "walka": ["obrona", "atak", "zagrożenie", "wróg", "tarcza", "imperium"],
            "wiedza": ["wiem", "naucz", "informacja", "dane", "pamięć"]
        }

    def _text_to_vector(self, text: str) -> List[float]:
        vec = [0.0] * len(self.AXES)
        words = text.lower().split()
        for word in words:
            for idx, axis in enumerate(self.AXES):
                if word in self.lang_dict.get(axis, []):
                    vec[idx] += 1.0
        norm = VectorMath.norm(vec)
        return [x / norm for x in vec] if norm > 0 else vec

    # --- INTEGRALNOŚĆ DUSZY (HASH CHECK) ---
    
    def _compute_hash(self, data: dict) -> str:
        """Oblicza SHA-256 dla słownika danych (sortuje klucze dla powtarzalności)"""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def save(self):
        """Zapisuje stan z hashem integralności"""
        state = {
            "energy": self.energy,
            "vector": self.vector,
            "ts": time.time()
        }
        
        # Podpisz stan
        integrity_hash = self._compute_hash(state)
        
        # Zapisz stan + podpis
        final_data = state.copy()
        final_data["integrity_hash"] = integrity_hash
        
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)

    def load(self):
        """Wczytuje stan i WERYFIKUJE hash"""
        try:
            if not os.path.exists(self.FILE_PATH):
                self.log("[INIT] Tworzenie nowej duszy...", "YELLOW")
                return

            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # 1. Wyciągnij zapisany hash
                stored_hash = data.pop("integrity_hash", "")
                
                # 2. Oblicz hash dla reszty danych
                computed_hash = self._compute_hash(data)
                
                # 3. Porównaj
                if stored_hash == computed_hash:
                    self.energy = data.get("energy", 200.0)
                    if "vector" in data: self.vector = data["vector"]
                    self.log("[INTEGRALNOŚĆ] ✓ ZGODNA (Dane autoryzowane)", "GREEN")
                else:
                    self.log("\n[INTEGRALNOŚĆ] ⚠️ BŁĄD KRYTYCZNY!", "RED")
                    self.log("Wykryto manipulację plikiem duszy lub uszkodzenie danych.", "RED")
                    self.log(">>> PRZYWRACANIE USTAWIEŃ FABRYCZNYCH <<<", "YELLOW")
                    self.energy = 200.0 # Reset
                    # Nie wczytujemy wektora z uszkodzonego pliku

        except Exception as e:
            self.log(f"[ERROR] Błąd odczytu duszy: {e}", "RED")

    # --- LOGIKA SNU I ADRENALINY ---
    
    def check_auto_sleep(self):
        is_under_attack = False
        recent_threats = list(self.evil_detector.threat_history)[-5:]
        
        for threat in recent_threats:
            t_ts = datetime.fromisoformat(threat['timestamp']).timestamp()
            if (time.time() - t_ts) < 300: 
                if threat['level'] != 'SAFE':
                    is_under_attack = True
                    break
        
        if is_under_attack:
            if self.energy < 20:
                self.energy += 40
                self.log("\n[ADRENALINA] 💉 Wstrzyknięto stymulant bojowy (+40 Energii)", "RED")
            return 

        now = time.time()
        time_since_sleep = now - self.last_sleep_time
        should_sleep = False
        reason = ""
        
        if time_since_sleep > self.AUTO_SLEEP_INTERVAL:
            should_sleep = True; reason = "Cykl dobowy"
        elif self.energy < self.LOW_ENERGY_THRESHOLD:
            should_sleep = True; reason = f"Wyczerpanie ({self.energy:.0f})"
            
        if should_sleep:
            self.log(f"\n[AUTO-SEN] Teren czysty. Inicjacja: {reason}", "PINK")
            self.sleep_cycle()

    def sleep_cycle(self):
        self.log("[SEN] 💤 Konsolidacja pamięci...", "PINK")
        time.sleep(1.0)
        
        reinforced = 0
        compressed = 0
        
        for entry in self.H_Log[-20:]:
            words = set(entry['content'].lower().split())
            for d in self.MapaD.values():
                for tag in d['tags']:
                    if tag in words:
                        d['weight'] = min(100.0, d['weight'] + 0.5)
                        reinforced += 1
        
        new_h_log = []
        for entry in self.H_Log:
            redundant = False
            if entry.get('type') == 'chat':
                for d in self.MapaD.values():
                    sim = VectorMath.cosine_similarity(entry['vector'], d['vector'])
                    if sim > 0.95:
                        redundant = True
                        compressed += 1
                        break
            if not redundant:
                new_h_log.append(entry)
        
        self.H_Log = new_h_log
        self.energy = min(200.0, self.energy + 100)
        self.last_sleep_time = time.time()
        
        self.save_memory()
        self.save() # Tu też nastąpi obliczenie hasha
        self.log(f"[SEN] Wybudzono. Wzmocniono: {reinforced}, Usunięto: {compressed}", "GREEN")

    # --- GŁÓWNA PĘTLA ---

    def process_input(self, text: str):
        threat = self.evil_detector.analyze(text)
        if threat.value >= ThreatLevel.DANGEROUS.value:
            self.log(f"[BLOKADA] Wykryto: {threat.name}", "RED")
            self.energy -= 5
            self.check_auto_sleep() 
            return

        if text.startswith("!") or text.startswith("/"):
            self.handle_command(text)
            self.check_auto_sleep()
            return

        vec = self._text_to_vector(text)
        
        memory_hit = None
        best_sim = 0.0
        for d in self.MapaD.values():
            sim = VectorMath.cosine_similarity(vec, d['vector'])
            if sim > best_sim and sim > 0.5:
                best_sim = sim
                memory_hit = d['content']
        
        self.H_Log.append({
            'vector': vec, 'content': text, 'type': 'chat', 'timestamp': time.time()
        })
        
        self.energy -= 2.0
        
        response = ""
        if memory_hit:
            self.log(f"[PAMIĘĆ] (Sim: {best_sim:.2f})", "YELLOW")
            response = f"Kojarzę to: {memory_hit}"
        else:
            response = self._generate_simple_response(text)
            
        print(f"\n[Guardian] {response}")
        self.check_auto_sleep()

    def _generate_simple_response(self, text: str) -> str:
        if "status" in text.lower(): return f"Energia: {self.energy:.0f}"
        return f"Przyjąłem: '{text}'. (Przetworzono wektorowo)"

    def handle_command(self, cmd: str):
        parts = cmd.split()
        c = parts[0].lower().replace("/","!")
        
        if c == "!teach" and len(parts) >= 3:
            tag = parts[1]
            content = " ".join(parts[2:])
            self.teach(tag, content)
            
        elif c == "!teachevil":
            if len(parts) >= 4:
                res = self.evil_detector.teach_evil(parts[1], parts[2], parts[3], " ".join(parts[4:]))
                self.log(f"[SEC] {res}", "RED")
            else:
                print("Użycie: !teachevil [wzorzec] [LEVEL] [kat] [opis]")

        elif c == "!sleep":
            self.log("[CMD] Wymuszam sen...", "YELLOW")
            self.sleep_cycle()
            
        elif c == "!attack":
            self.log("[TEST] Symulacja ataku!", "RED")
            fake_sig = EvilSignature("test", ThreatLevel.DANGEROUS, "sim", "Manual")
            self.evil_detector.log_threat(ThreatLevel.DANGEROUS, fake_sig, "ATAK TESTOWY")
            self.energy = 10
            print("Energia = 10. Zagrożenie aktywne.")
            
        elif c == "!status":
            print(f"Energia: {self.energy}")
            print(f"Pamięć (MapaD): {len(self.MapaD)}")
            print(f"Sygnatury Zła: {len(self.evil_detector.signatures)}")
            
        elif c == "!exit":
            self.active = False

    def teach(self, tag: str, content: str):
        vec = self._text_to_vector(content)
        id_def = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[id_def] = {
            'vector': vec, 'weight': 5.0, 'tags': [tag], 'content': content, 'id': id_def
        }
        self.log(f"[NAUKA] Zapisano '{tag}'", "GREEN")
        self.save_memory()

    def load_memory(self):
        try:
            with open(self.MEMORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.MapaD = data.get("MapaD", {})
                self.H_Log = data.get("H_Log", [])
        except: pass

    def save_memory(self):
        with open(self.MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump({"MapaD": self.MapaD, "H_Log": self.H_Log[-200:]}, f, ensure_ascii=False)

# =============================================================================
# START
# =============================================================================
if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    bot = EriAmoCore()
    
    print("\n--- EriAmo Mobile Console ---")
    print(" !teach [tag] [treść]     - Nauka wiedzy")
    print(" !teachevil [...]         - Nauka zagrożeń")
    print(" !sleep                   - Wymuś sen (save + hash)")
    print(" !attack                  - Test Adrenaliny")
    print(" !exit                    - Wyjście\n")
    
    while bot.active:
        try:
            u = input("> ").strip()
            if u: bot.process_input(u)
        except KeyboardInterrupt:
            bot.save(); bot.save_memory()
            print("\n[Zatrzymano]")
            break
