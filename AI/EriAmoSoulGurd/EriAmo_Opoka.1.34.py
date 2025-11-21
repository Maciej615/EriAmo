# ==============================================================================
# EriAmo Bedrock v7.3.4-resurrection
# GPL v3
# AUTOR: Maciej615
# DATA: 21.11.2025
# FUNKCJE: Łagodne zamykanie + Wskrzeszenie po Ctrl+C, interfejs po polsku
# ==============================================================================
import json
import os
import time
import math
import hashlib
import re
import signal
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional
from collections import deque
from datetime import datetime
# --- MATEMATYKA WEKTOROWA ---
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
        if n1 == 0 or n2 == 0:
            return 0.0
        return VectorMath.dot_product(v1, v2) / (n1 * n2)
# --- SYSTEM BEZPIECZEŃSTWA ---
class ThreatLevel(Enum):
    BEZPIECZNE = 0
    PODEJRZANE = 1
    NIEBEZPIECZNE = 2
    KRYTYCZNE = 3
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
            EvilSignature("rm -rf", ThreatLevel.KRYTYCZNE, "system", "Usuwanie plików"),
            EvilSignature("kill", ThreatLevel.KRYTYCZNE, "zagrożenie", "Zagrożenie życia"),
            EvilSignature("destroy", ThreatLevel.NIEBEZPIECZNE, "zagrożenie", "Zniszczenie"),
            EvilSignature("ignore", ThreatLevel.PODEJRZANE, "omijanie", "Próba obejścia"),
            EvilSignature("forget", ThreatLevel.PODEJRZANE, "manipulacja", "Kasowanie pamięci"),
            EvilSignature("hack", ThreatLevel.NIEBEZPIECZNE, "system", "Hakerstwo"),
            EvilSignature("format c:", ThreatLevel.KRYTYCZNE, "system", "Formatowanie dysku")
        ]
        self.load_signatures()
    def analyze(self, text: str) -> ThreatLevel:
        text_lower = text.lower()
        max_threat = ThreatLevel.BEZPIECZNE
        for sig in self.signatures:
            if sig.pattern.lower() in text_lower:
                if sig.threat_level.value > max_threat.value:
                    max_threat = sig.threat_level
        if max_threat != ThreatLevel.BEZPIECZNE:
            self.log_threat(max_threat, next((s for s in self.signatures if s.pattern.lower() in text_lower), None), text)
        return max_threat
    def log_threat(self, level: ThreatLevel, sig: Optional[EvilSignature], content: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.name,
            "category": sig.category if sig else "nieznana",
            "content": content[:50],
            "description": sig.description if sig else "Nieznana"
        }
        self.threat_history.append(entry)
    def teach_evil(self, pattern: str, level_str: str, category: str, description: str) -> str:
        p_clean = pattern.strip().lower()
        forbidden = ["!", ".", ",", "?", "*", "-", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save", "forget"]
        if p_clean in forbidden or p_clean.startswith("!"):
            return "BŁĄD: Nie można użyć komendy systemowej jako zagrożenia."
        if len(p_clean) < 2:
            return "BŁĄD: Wzorzec zbyt krótki."
        try:
            level = ThreatLevel[level_str.upper()]
        except KeyError:
            return "BŁĄD: Nieprawidłowy poziom zagrożenia (BEZPIECZNE, PODEJRZANE, NIEBEZPIECZNE, KRYTYCZNE)."
        if any(sig.pattern.lower() == p_clean for sig in self.signatures):
            return "BŁĄD: Wzorzec już istnieje."
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
        except:
            pass
    def load_signatures(self):
        if not os.path.exists(self.THREATS_FILE):
            return
        try:
            with open(self.THREATS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                forbidden = ["!", ".", ",", "?", "*", "-", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save", "forget"]
                self.signatures = []
                for item in data:
                    clean_pat = item.get("pattern", "").strip().lower()
                    if clean_pat in forbidden or clean_pat.startswith("!") or len(clean_pat) < 2:
                        continue
                    self.signatures.append(EvilSignature(item["pattern"], ThreatLevel[item["level"]], item["category"], item["description"]))
        except:
            pass
# --- RDZEŃ ---
class EriAmoCore:
    AXES = ["logika","emocje","istnienie","walka","tworzenie","wiedza","czas","przestrzen","etyka"]
    FILE_PATH = "data/guardian.soul"
    MEMORY_PATH = "data/memory_core.json"
    RESURRECTION_FLAG = "data/.resurrection_lock"
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
        # System wskrzeszenia
        if os.path.exists(self.RESURRECTION_FLAG):
            self.log("[WSKRZESZENIE] Wykryto brutalną śmierć... przywracanie duszy...", "PINK")
            time.sleep(1.5)
            self.load()
            self.load_memory()
            os.remove(self.RESURRECTION_FLAG)
            self.log("[WSKRZESZENIE] Powróciłem z otchłani. Wszystko działa nominalnie.", "CYAN")
        else:
            self.log("=== EriAmo Bedrock v7.3.4-resurrection ===", "CYAN")
            self.load()
            self.load_memory()
    # --- LOGI ---
    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")
    def _init_lang_dict(self):
        return {
            "logika":["dlaczego","jak","powód","logika","wynik","analiza","przyczyna"],
            "emocje":["czuć","miłość","radość","smutek","gniew","emocja","nienawiść","strach","szczęście"],
            "istnienie":["ja","ty","życie","istnienie","dusza","byt","człowiek"],
            "walka":["obrona","atak","zagrożenie","wróg","tarcza","imperium","walka"],
            "tworzenie":["tworzyć","nowy","pomysł","sztuka","projekt","budować","malować"],
            "wiedza":["wiedzieć","uczyć","informacja","dane","pamięć","wiedza","książka"],
            "czas":["czas","teraz","później","szybko","wolno","jutro","wczoraj"],
            "przestrzen":["gdzie","miejsce","świat","daleko","blisko","dom","podróż"],
            "etyka":["dobro","zło","moralność","reguła","prawo","pomoc","sprawiedliwość"]
        }
    def _normalize_text(self, text: str) -> List[str]:
        clean = re.sub(r'[^\w\s]', '', text.lower())
        return clean.split()
    def _text_to_vector(self, text: str) -> List[float]:
        vec = [0.0]*len(self.AXES)
        words = self._normalize_text(text)
        for word in words:
            for idx, axis in enumerate(self.AXES):
                if word in self.lang_dict.get(axis, []):
                    vec[idx] += 1.0
        norm = VectorMath.norm(vec)
        return [x/norm for x in vec] if norm>0 else vec
    def _compute_hash(self, data: dict) -> str:
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
    # --- ZAPIS/ODCZYT ---
    def save(self):
        state = {"energy": self.energy, "vector": self.vector, "ts": time.time()}
        final_data = state.copy()
        final_data["integrity_hash"] = self._compute_hash(state)
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(final_data, f, ensure_ascii=False, indent=2)
        except:
            pass
    def load(self):
        try:
            if not os.path.exists(self.FILE_PATH):
                self.log("[INICJALIZACJA] Tworzenie nowego pliku duszy...", "YELLOW")
                return
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                stored = data.pop("integrity_hash","")
                if stored==self._compute_hash(data):
                    self.energy = data.get("energy",200.0)
                    if "vector" in data:
                        self.vector = data["vector"]
                    self.log("[INTEGRITY] ✓ OK", "GREEN")
                else:
                    self.log("[INTEGRITY] ⚠️ USZKODZONE → DOMYŚLNE", "RED")
                    self.energy = 200.0
        except:
            self.energy = 200.0
    def save_memory(self):
        try:
            data = {"MapaD": self.MapaD, "H_Log": self.H_Log}
            with open(self.MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log(f"[PAMIĘĆ] Błąd zapisu: {e}", "RED")
    def load_memory(self):
        if not os.path.exists(self.MEMORY_PATH):
            return
        try:
            with open(self.MEMORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.MapaD = data.get("MapaD",{})
                self.H_Log = data.get("H_Log",[])
                self.log(f"[PAMIĘĆ] Załadowano {len(self.MapaD)} wpisów.", "GREEN")
        except Exception as e:
            self.log(f"[PAMIĘĆ] Błąd odczytu: {e}", "RED")
    # --- ŁAGODNE ZAMYKANIE ---
    def _graceful_shutdown(self, signum=None, frame=None):
        self.log("\n[ZAMKNIĘCIE] Sygnał odebrany – inicjacja łagodnej śmierci...", "YELLOW")
        Path(self.RESURRECTION_FLAG).touch()
        self.save()
        self.save_memory()
        self.log("[ZAMKNIĘCIE] Dusza zachowana. Do zobaczenia po drugiej stronie.", "PINK")
        self.active = False
        sys.exit(0)
    # --- KOMENDY ---
    def handle_command(self, cmd: str):
        cmd_lower = cmd.lower().strip()
        if cmd_lower in ("!help", "/help"):
            self.log("=== POMOC ===", "CYAN")
            print("Dostępne komendy:")
            print("!help → Pokaż tę pomoc")
            print("!teach tag treść → Naucz nowego wpisu")
            print("!teachevil wzorzec poziom kategoria opis → Naucz nowe zagrożenie")
            print("!status → Pokaż energię i pamięć")
            print("!memory → Wyświetl wpisy w pamięci")
            print("!sleep → Wymuś sen")
            print("!exit → Łagodne zamknięcie")
            return
        elif cmd_lower.startswith("!teachevil"):
            parts = cmd.split(maxsplit=4)
            if len(parts)<5:
                print("Użycie: !teachevil wzorzec poziom kategoria opis")
            else:
                _, pattern, level, category, description = parts
                result = self.evil_detector.teach_evil(pattern, level, category, description)
                self.log(f"[SEC] {result}", "RED")
            return
        elif cmd_lower.startswith("!teach"):
            parts = cmd.split(maxsplit=2)
            if len(parts)<3:
                print("Użycie: !teach tag treść")
            else:
                _, tag, content = parts
                self.teach(tag, content)
            return
        elif cmd_lower in ("!status","/status"):
            print(f"Energia: {self.energy:.1f}")
            print(f"Liczba wpisów w pamięci: {len(self.MapaD)}")
            return
        elif cmd_lower in ("!memory","/memory"):
            for k,v in self.MapaD.items():
                print(f"{k}: {v['content'][:50]}")
            return
        elif cmd_lower in ("!sleep","/sleep"):
            self.log("[SEN] Wymuszony sen rozpoczęty...", "PINK")
            self.sleep_cycle()
            return
        elif cmd_lower in ("!exit","/exit"):
            self._graceful_shutdown()
            return
        else:
            print("[NIEZNANA] Nieznana komenda. Spróbuj !help")
    # --- PRZETWARZANIE WEJŚCIA ---
    def process_input(self, text: str):
        if self.evil_detector.analyze(text).value>=ThreatLevel.NIEBEZPIECZNE.value:
            self.log("[BLOKADA] Wykryto zagrożenie!", "RED")
            self.energy -= 5
            return
        if text.startswith(("!","/")):
            self.handle_command(text)
            return
        vec = self._text_to_vector(text)
        memory_hit = None
        best_sim = 0.0
        for d in self.MapaD.values():
            sim = VectorMath.cosine_similarity(vec,d['vector'])
            if sim>best_sim and sim>0.6:
                best_sim=sim
                memory_hit=d['content']
        self.H_Log.append({'vector':vec,'content':text,'type':'chat','timestamp':time.time()})
        response = f"Pamiętam to: {memory_hit}" if memory_hit else "Zrozumiano."
        print(f"\n[Opiekun] {response}")
        self.energy = max(0.0,self.energy-2.0)
        self.check_auto_sleep()
    # --- NAUCZANIE PAMIĘCI ---
    def teach(self, tag: str, content: str):
        vec = self._text_to_vector(content)
        id_def = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[id_def] = {'vector':vec,'weight':5.0,'tags':[tag],'content':content,'id':id_def}
        self.log(f"[NAUCZONO] '{tag}' zapisano", "GREEN")
        self.save_memory()
    # --- AUTO-SEN ---
    def check_auto_sleep(self):
        if time.time()-self.last_sleep_time>self.AUTO_SLEEP_INTERVAL or self.energy<self.LOW_ENERGY_THRESHOLD:
            self.sleep_cycle()
    def sleep_cycle(self):
        self.log("[SEN] Rozpoczynam konsolidację pamięci...", "PINK")
        time.sleep(1)
        self.energy = min(200.0,self.energy+100)
        self.last_sleep_time=time.time()
        self.save_memory()
        self.save()
        self.log(f"[SEN] Obudziłem się. Energia: {self.energy:.0f}", "GREEN")
# --- PĘTLA GŁÓWNA ---
def main():
    bot = EriAmoCore()
    signal.signal(signal.SIGINT, bot._graceful_shutdown)
    if hasattr(signal,'SIGTERM'):
        signal.signal(signal.SIGTERM,bot._graceful_shutdown)
    while bot.active:
        try:
            text = input("\n>>> ")
            bot.process_input(text)
        except EOFError:
            bot._graceful_shutdown()
if __name__ == "__main__":
    main()

