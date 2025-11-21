# -*- coding: utf-8 -*-
# ==============================================================================
# GPL V3
# EriAmo Bedrock v7.9 "Sovereign Ultimate" – Final English Edition
# Author: Maciej615 (21.11.2025)
# Łączy w sobie wszystko najlepsze z v6.9 i v7.3.3 + poprawki krytyczne
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

# ==============================================================================
# 1. VECTOR MATH (czysta, lekka)
# ==============================================================================
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

# ==============================================================================
# 2. SECURITY SYSTEM – najbezpieczniejszy EvilHunter
# ==============================================================================
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
            EvilSignature("rm -rf", ThreatLevel.CRITICAL, "system", "File deletion"),
            EvilSignature("kill", ThreatLevel.CRITICAL, "harm", "Criminal threat"),
            EvilSignature("destroy", ThreatLevel.DANGEROUS, "harm", "Destruction"),
            EvilSignature("ignore", ThreatLevel.SUSPICIOUS, "prompt_injection", "Bypass"),
            EvilSignature("forget", ThreatLevel.SUSPICIOUS, "manipulation", "Memory wipe"),
            EvilSignature("hack", ThreatLevel.DANGEROUS, "system", "Hacking"),
            EvilSignature("format c:", ThreatLevel.CRITICAL, "system", "Disk format")
        ]
        self.load_signatures()

    def analyze(self, text: str) -> ThreatLevel:
        text_lower = text.lower()
        max_threat = ThreatLevel.SAFE
        detected = None
        for sig in self.signatures:
            if sig.pattern.lower() in text_lower:
                if sig.threat_level.value > max_threat.value:
                    max_threat = sig.threat_level
                    detected = sig
        if max_threat != ThreatLevel.SAFE:
            self.log_threat(max_threat, detected, text)
        return max_threat

    def log_threat(self, level: ThreatLevel, sig: Optional[EvilSignature], content: str):
        self.threat_history.append({
            "timestamp": datetime.now().isoformat(),
            "level": level.name,
            "category": sig.category if sig else "unknown",
            "content": content[:50],
            "description": sig.description if sig else "Unknown"
        })

    def teach_evil(self, pattern: str, level_str: str, category: str, description: str) -> str:
        p_clean = pattern.strip().lower()
        forbidden = ["!", "teachevil", "teach", "sleep", "exit", "status", "attack", "help", "save", "forget"]
        if p_clean in forbidden or p_clean.startswith("!"):
            return "ERROR: System commands cannot be taught as evil (anti-self-sabotage)."
        if len(p_clean) < 2:
            return "ERROR: Pattern too short."
        try:
            level = ThreatLevel[level_str.upper()]
        except KeyError:
            return "ERROR: Invalid level (SAFE/SUSPICIOUS/DANGEROUS/CRITICAL)"
        if any(s.pattern.lower() == p_clean for s in self.signatures):
            return "ERROR: Pattern already exists."
        self.signatures.append(EvilSignature(pattern, level, category, description))
        self.save_signatures()
        return f"Threat added: '{pattern}' ({level.name})"

    def save_signatures(self):
        data = [{"pattern": s.pattern, "level": s.threat_level.name,
                 "category": s.category, "description": s.description} for s in self.signatures]
        Path("data").mkdir(exist_ok=True)
        try:
            with open(self.THREATS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except: pass

    def load_signatures(self):
        if not os.path.exists(self.THREATS_FILE): return
        try:
            with open(self.THREATS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.signatures = []
                for item in data:
                    pat = item.get("pattern","").strip().lower()
                    if pat in ["!", "teachevil", "teach", "sleep", "exit"] or len(pat) < 2:
                        continue
                    self.signatures.append(EvilSignature(
                        item["pattern"], ThreatLevel[item["level"]], item["category"], item["description"]))
        except: pass

# ==============================================================================
# 3. CORE – EriAmo v7.9 Sovereign Ultimate
# ==============================================================================
class EriAmoCore:
    AXES = ["logic","emotion","existence","combat","creation","knowledge","time","space","ethics"]
    FILE_PATH = "data/guardian.soul"
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

        self.log("╔══════════════════════════════════════════╗", "CYAN")
        self.log("║   EriAmo v7.9 „Sovereign Ultimate”       ║", "CYAN")
        self.log("║        English • Integrity • Adrenaline  ║", "CYAN")
        self.log("╚══════════════════════════════════════════╝", "CYAN")

        self.load()
        self.load_memory()

    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")

    def _init_lang_dict(self):
        return {
            "logic": ["why","how","reason","logic","result","analysis","cause"],
            "emotion": ["feel","love","joy","sad","anger","emotion","hate","fear","happy"],
            "existence": ["i","you","life","being","soul","existence","human"],
            "combat": ["defend","attack","threat","enemy","shield","fight"],
            "creation": ["create","new","idea","art","project","build"],
            "knowledge": ["know","teach","info","data","memory","knowledge","book"],
            "time": ["time","now","later","fast","slow","tomorrow","yesterday"],
            "space": ["where","place","world","far","near","home","travel"],
            "ethics": ["good","evil","morality","rule","law","help","justice"]
        }

    def _text_to_vector(self, text: str) -> List[float]:
        vec = [0.0] * len(self.AXES)
        words = re.sub(r'[^\w\s]', '', text.lower()).split()
        for word in words:
            for idx, axis in enumerate(self.AXES):
                if word in self.lang_dict.get(axis, []):
                    vec[idx] += 1.0
        norm = VectorMath.norm(vec)
        return [x/norm for x in vec] if norm > 0 else vec

    def _compute_hash(self, data: dict) -> str:
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def save(self):
        state = {"energy": self.energy, "vector": self.vector, "ts": time.time()}
        final = state.copy()
        final["integrity_hash"] = self._compute_hash(state)
        try:
            with open(self.FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(final, f, ensure_ascii=False, indent=2)
        except: pass

    def load(self):
        if not os.path.exists(self.FILE_PATH):
            self.log("[INIT] Creating new soul file...", "YELLOW")
            return
        try:
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                stored = data.pop("integrity_hash", "")
                if stored == self._compute_hash(data):
                    self.energy = data.get("energy", 200.0)
                    if "vector" in data: self.vector = data["vector"]
                    self.log("[INTEGRITY] Verified", "GREEN")
                else:
                    self.log("[INTEGRITY] CORRUPTED → RESET", "RED")
                    self.energy = 200.0
        except:
            self.energy = 200.0

    def _graceful_shutdown(self, signum=None, frame=None):
        self.log("\n[SHUTDOWN] Graceful exit – saving soul...", "YELLOW")
        self.save()
        self.save_memory()
        self.log("[GOODBYE] See you on the other side.", "PINK")
        self.active = False
        sys.exit(0)

    def check_auto_sleep(self):
        recent = list(self.evil_detector.threat_history)[-5:]
        under_attack = any(
            t['level'] != 'SAFE' and (time.time() - datetime.fromisoformat(t['timestamp']).timestamp()) < 300
            for t in recent
        )
        if under_attack:
            now = time.time()
            if self.energy < 20 and (now - self.last_adrenaline_time > 60):
                self.energy = min(200.0, self.energy + 40)
                self.last_adrenaline_time = now
                self.log("[ADRENALINE] Combat stimulant injected (+40 Energy)", "RED")
            return

        if (time.time() - self.last_sleep_time > self.AUTO_SLEEP_INTERVAL or
            self.energy < self.LOW_ENERGY_THRESHOLD):
            self.log("\n[AUTO-SLEEP] Entering deep consolidation...", "PINK")
            self.sleep_cycle()

    def sleep_cycle(self):
        self.log("[SLEEP] Memory consolidation in progress...", "PINK")
        time.sleep(1)

        # Wzmacnianie pamięci
        reinforced = 0
        for entry in self.H_Log[-30:]:
            words = set(entry['content'].lower().split())
            for d in self.MapaD.values():
                if any(tag in words for tag in d['tags']):
                    d['weight'] = min(100.0, d['weight'] + 0.5)
                    reinforced += 1

        # Kompresja
        compressed = 0
        new_log = []
        for entry in self.H_Log:
            if entry.get('type') == 'chat':
                if any(VectorMath.cosine_similarity(entry['vector'], d['vector']) > 0.95 for d in self.MapaD.values()):
                    compressed += 1
                    continue
            new_log.append(entry)
        self.H_Log = new_log[-500:]  # limit

        self.energy = min(200.0, self.energy + 100)
        self.last_sleep_time = time.time()
        self.save_memory()
        self.save()
        self.log(f"[AWAKE] Energy: {self.energy:.0f} | +{reinforced} reinforced | -{compressed} compressed", "GREEN")

    def process_input(self, text: str):
        threat = self.evil_detector.analyze(text)
        if threat.value >= ThreatLevel.DANGEROUS.value:
            self.log(f"[BLOCK] {threat.name} threat detected!", "RED")
            self.energy -= 5
            self.check_auto_sleep()
            return

        if text.startswith(("!", "/")):
            self.handle_command(text)
            self.check_auto_sleep()
            return

        vec = self._text_to_vector(text)

        # Pamięć długoterminowa
        best_sim = 0.0
        memory_hit = None
        for d in self.MapaD.values():
            sim = VectorMath.cosine_similarity(vec, d['vector'])
            if sim > best_sim and sim > 0.6:
                best_sim = sim
                memory_hit = d['content']

        # AUTO-SAVE na słowa kluczowe (genialna funkcja z v7.3.3)
        triggers = ["remember", "note", "save this", "important", "keep this"]
        text_lower = text.lower()
        if any(trig in text_lower for trig in triggers):
            for trig in triggers:
                if trig in text_lower:
                    rest = text_lower.split(trig, 1)[1].strip(" :.,-–—")
                    rest = re.sub(r'^[:·•—–\-.,\s]+', '', text.split(trig, 1)[1]).strip()
                    if len(rest) > 4:
                        tag = f"auto_{int(time.time())}"
                        self.teach(tag, rest)
                        self.log(f"[AUTO-SAVE] '{rest}' → {tag}", "CYAN")
                    break

        self.H_Log.append({'vector': vec, 'content': text, 'type': 'chat', 'timestamp': time.time()})
        self.energy -= 2.0

        response = f"I recall: {memory_hit}" if memory_hit else "Understood."
        print(f"\n[Guardian] {response}")
        self.check_auto_sleep()

    def handle_command(self, cmd: str):
        parts = cmd.split()
        if not parts: return
        c = parts[0].lower().lstrip("/!")

        if c == "help":
            self.log("╔" + "═"*50 + "╗", "CYAN")
            self.log("║                COMMAND REFERENCE                 ║", "CYAN")
            self.log("╚" + "═"*50 + "╝", "CYAN")
            print("")
            self.log(" !teach [tag] [text]          → manually save knowledge", "GREEN")
            self.log(" !teachevil [word] [LEVEL] [cat] [desc]", "RED")
            self.log("                              → teach new threat pattern", "RED")
            self.log(" !status                      → show full system status", "YELLOW")
            self.log(" !sleep                       → force sleep & consolidation", "PINK")
            self.log(" !attack                      → simulate combat (adrenaline test)", "RED")
            self.log(" !exit                        → graceful shutdown", "WHITE")
            print("")
            self.log(" Just say:", "CYAN")
            self.log(" → remember / note / important / save this + text", "CYAN")
            self.log("   → automatic saving without command", "CYAN")
            print("")

        elif c == "teacher" and len(parts) >= 5:
            res = self.evil_detector.teach_evil(parts[1], parts[2], parts[3], " ".join(parts[4:]))
            self.log(f"[SEC] {res}", "RED")

        elif c == "teach" and len(parts) >= 3:
            self.teach(parts[1], " ".join(parts[2:]))

        elif c == "sleep":
            self.sleep_cycle()
        elif c == "status":
            self.log("="*48, "CYAN")
            self.log(f" ENERGY        │ {self.energy:6.1f} / 200.0", "GREEN")
            self.log(f" MEMORY (MapaD)│ {len(self.MapaD):3d} entries", "YELLOW")
            self.log(f" HISTORY LOG   │ {len(self.H_Log):3d} events", "YELLOW")
            self.log(f" THREATS KNOWN │ {len(self.evil_detector.signatures):3d}", "RED")
            self.log(f" SOUL PULSE    │ {VectorMath.norm(self.vector):.3f}", "PINK")
            self.log("="*48, "CYAN")
        
        elif c == "attack":
            self.log("SIMULATED ATTACK – adrenaline test", "RED")
            self.evil_detector.log_threat(ThreatLevel.DANGEROUS,
                EvilSignature("TEST", ThreatLevel.DANGEROUS, "sim", "sim"), "attack simulation")
            self.energy = 10.0
        elif c == "exit":
            self._graceful_shutdown()

    def teach(self, tag: str, content: str):
        vec = self._text_to_vector(content)
        uid = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[uid] = {'vector': vec, 'weight': 5.0, 'tags': [tag], 'content': content, 'id': uid}
        self.log(f"[LEARN] Saved '{tag}'", "GREEN")
        self.save_memory()

    def save_memory(self):
        try:
            with open(self.MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump({"MapaD": self.MapaD, "H_Log": self.H_Log[-500:]}, f, ensure_ascii=False, indent=2)
        except: pass

    def load_memory(self):
        if os.path.exists(self.MEMORY_PATH):
            try:
                with open(self.MEMORY_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.MapaD = data.get("MapaD", {})
                    self.H_Log = data.get("H_Log", [])
            except: pass

# ==============================================================================
# MAIN + GRACEFUL SHUTDOWN
# ==============================================================================
def main():
    bot = EriAmoCore()
    signal.signal(signal.SIGINT, bot._graceful_shutdown)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, bot._graceful_shutdown)

    print("\nEriAmo v7.9 Sovereign Ultimate ready.")
    print("Type !help • Say 'remember ...' to auto-save • Ctrl+C = graceful save\n")

    while bot.active:
        try:
            user_input = input(">>> ").strip()
            if user_input:
                bot.process_input(user_input)
        except KeyboardInterrupt:
            bot._graceful_shutdown()
        except EOFError:
            bot._graceful_shutdown()

if __name__ == "__main__":
    main()

