# -*- coding: utf-8 -*-
# ==============================================================================
# na licencji GPL3
# EriAmo Bedrock v7.3.4-resurrection
# AUTHOR: Maciej615
# DATE: 21.11.2025
# FEATURES: Graceful shutdown + Resurrection after Ctrl+C
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
            EvilSignature("rm -rf", ThreatLevel.CRITICAL, "system", "File deletion"),
            EvilSignature("kill", ThreatLevel.CRITICAL, "harm", "Criminal threat"),
            EvilSignature("destroy", ThreatLevel.DANGEROUS, "harm", "Destruction"),
            EvilSignature("ignore", ThreatLevel.SUSPICIOUS, "prompt_injection", "Bypass attempt"),
            EvilSignature("forget", ThreatLevel.SUSPICIOUS, "manipulation", "Memory deletion"),
            EvilSignature("hack", ThreatLevel.DANGEROUS, "system", "Hacking attempt"),
            EvilSignature("format c:", ThreatLevel.CRITICAL, "system", "System format")
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
            return "ERROR: Cannot define system commands as evil."
        if len(p_clean) < 2:
            return "ERROR: Pattern too short."
        try:
            level = ThreatLevel[level_str.upper()]
        except KeyError:
            return "ERROR: Wrong level (SAFE, SUSPICIOUS, DANGEROUS, CRITICAL)."
        if any(sig.pattern.lower() == p_clean for sig in self.signatures):
            return "ERROR: Pattern already exists."
        new_sig = EvilSignature(pattern, level, category, description)
        self.signatures.append(new_sig)
        self.save_signatures()
        return f"Added threat: '{pattern}' ({level.name})"
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
    AXES = ["logic","emotion","existence","combat","creation","knowledge","time","space","ethics"]
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
        # RESURRECTION SYSTEM
        if os.path.exists(self.RESURRECTION_FLAG):
            self.log("[RESURRECTION] Detecting brutal death... restoring soul...", "PINK")
            time.sleep(1.5)
            self.load()
            self.load_memory()
            os.remove(self.RESURRECTION_FLAG)
            self.log("[RESURRECTION] I have returned from the void. All systems nominal.", "CYAN")
        else:
            self.log("=== EriAmo Bedrock v7.3.4-resurrection ===", "CYAN")
            self.load()
            self.load_memory()
    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")
    def _init_lang_dict(self):
        return {
            "logic": ["why", "how", "reason", "logic", "result", "analysis", "cause"],
            "emotion": ["feel", "love", "joy", "sad", "anger", "emotion", "hate", "fear", "happiness"],
            "existence": ["i", "you", "life", "existence", "soul", "being", "human"],
            "combat": ["defend", "attack", "threat", "enemy", "shield", "empire", "fight"],
            "creation": ["create", "new", "idea", "art", "project", "build", "paint"],
            "knowledge": ["know", "teach", "information", "data", "memory", "knowledge", "book"],
            "time": ["time", "now", "later", "fast", "slow", "tomorrow", "yesterday"],
            "space": ["where", "place", "world", "far", "near", "home", "travel"],
            "ethics": ["good", "evil", "morality", "rule", "law", "help", "justice"]
        }
    def _normalize_text(self, text: str) -> List[str]:
        clean = re.sub(r'[^\w\s]', '', text.lower())
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
    # --- save/load ---
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
                self.log("[INIT] Creating new soul (.soul)...", "YELLOW")
                return
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                stored = data.pop("integrity_hash", "")
                if stored == self._compute_hash(data):
                    self.energy = data.get("energy", 200.0)
                    if "vector" in data: self.vector = data["vector"]
                    self.log("[INTEGRITY] ✓ OK", "GREEN")
                else:
                    self.log("[INTEGRITY] ⚠️ CORRUPTED → DEFAULT", "RED")
                    self.energy = 200.0
        except:
            self.energy = 200.0
    def save_memory(self):
        try:
            data = {"MapaD": self.MapaD, "H_Log": self.H_Log}
            with open(self.MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log(f"[MEMORY] Save error: {e}", "RED")
    def load_memory(self):
        if not os.path.exists(self.MEMORY_PATH): return
        try:
            with open(self.MEMORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.MapaD = data.get("MapaD", {})
                self.H_Log = data.get("H_Log", [])
                self.log(f"[MEMORY] Loaded {len(self.MapaD)} engrams.", "GREEN")
        except Exception as e:
            self.log(f"[MEMORY] Load error: {e}", "RED")
    # --- graceful shutdown ---
    def _graceful_shutdown(self, signum=None, frame=None):
        self.log("\n[SHUTDOWN] Signal received – initiating graceful death...", "YELLOW")
        Path(self.RESURRECTION_FLAG).touch()
        self.save()
        self.save_memory()
        self.log("[SHUTDOWN] Soul preserved. See you on the other side.", "PINK")
        self.active = False
        sys.exit(0)
   
    # --- SLEEP CYCLE SYSTEM (ADDED) ---
    def sleep_cycle(self):
        self.log("[SLEEP] Initiating deep memory consolidation...", "PINK")
        time.sleep(1)
       
        # Logika wzmocnienia i kompresji
        reinforced = 0
        compressed = 0
       
        # 1. Reinforcement - analiza ostatnich wpisów
        for entry in self.H_Log[-30:]:
            words = set(entry.get('content', '').lower().split())
            for d in self.MapaD.values():
                for tag in d['tags']:
                    if tag in words:
                        d['weight'] = min(100.0, d['weight'] + 0.5)
                        reinforced += 1
       
        # 2. Compression - usuwanie redundantnych wektorów
        new_h_log = []
        for entry in self.H_Log:
            if entry.get('type') == 'chat':
                # Sprawdź czy ten wpis jest już reprezentowany w pamięci długotrwałej (MapaD)
                redundant = any(VectorMath.cosine_similarity(entry['vector'], d['vector']) > 0.95 for d in self.MapaD.values())
                if redundant:
                    compressed += 1
                    continue
            new_h_log.append(entry)
       
        self.H_Log = new_h_log
       
        # Regeneracja energii
        self.energy = min(200.0, self.energy + 100)
        self.last_sleep_time = time.time()
       
        self.save_memory()
        self.save()
        self.log(f"[SLEEP] Woke up. Energy: {self.energy:.0f} | Reinforced: {reinforced} | Compressed: {compressed}", "GREEN")
    # --- COMMAND HANDLER (ADDED FOR !sleep SUPPORT) ---
    def handle_command(self, text: str):
        cmd = text.lower().strip().split()
        base_cmd = cmd[0]
        if base_cmd in ["!sleep", "/sleep"]:
            self.sleep_cycle()
        elif base_cmd in ["!status", "/status"]:
            self.log(f"[STATUS] Energy: {self.energy:.1f} | RAM: {len(self.MapaD)}", "CYAN")
        elif base_cmd in ["!exit", "/exit"]:
            self._graceful_shutdown()
        elif base_cmd in ["!teachevil"] and len(cmd) > 3:
            # Format: !teachevil pattern level category desc...
            # Example: !teachevil "sudo rm" CRITICAL system "Root deletion"
            # Uproszczona wersja parsowania dla przykładu
            try:
                parts = text.split('"')
                if len(parts) >= 3:
                    pattern = parts[1]
                    rest = parts[2].strip().split()
                    level = rest[0]
                    cat = rest[1]
                    desc = " ".join(rest[2:])
                    res = self.evil_detector.teach_evil(pattern, level, cat, desc)
                    self.log(f"[EVIL-DB] {res}", "YELLOW")
            except Exception as e:
                self.log(f"[ERROR] Command format error: {e}", "RED")
        else:
            self.log("[CMD] Unknown command.", "YELLOW")
    # --- input processing ---
    def process_input(self, text: str):
        if self.evil_detector.analyze(text).value >= ThreatLevel.DANGEROUS.value:
            self.log("[BLOCK] Threat detected!", "RED")
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
        triggers = ["remember", "note", "important"]
        text_lower = text.lower()
        trigger = next((t for t in triggers if t in text_lower), None)
        if trigger:
            rest = text[text_lower.find(trigger) + len(trigger):].strip()
            if len(rest) > 4:
                tag = f"auto_{int(time.time())}"
                self.teach(tag, rest)
                self.log(f"[AUTO-SAVE] '{rest}' → {tag}", "CYAN")
        self.energy -= 2.0
        response = f"I recall: {memory_hit}" if memory_hit else "Noted."
        print(f"\n[Guardian] {response}")
    def teach(self, tag: str, content: str):
        vec = self._text_to_vector(content)
        id_def = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[id_def] = {'vector': vec, 'weight': 5.0, 'tags': [tag], 'content': content, 'id': id_def}
        self.log(f"[LEARN] Saved '{tag}'", "GREEN")
        self.save_memory()
# --- MAIN LOOP ---
def main():
    bot = EriAmoCore()
    signal.signal(signal.SIGINT, bot._graceful_shutdown)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, bot._graceful_shutdown)
    print("\n[EriAmo Bedrock v7.3.4-resurrection] Ready. Ctrl+C = graceful death + resurrection\n")
    while bot.active:
        try:
            user_input = input(">>> ")
            if not bot.active:
                break
            bot.process_input(user_input)
        except KeyboardInterrupt:
            pass
        except EOFError:
            bot._graceful_shutdown()
        except Exception as e:
            bot.log(f"[ERROR] {e}", "RED")
    if bot.active:
        bot._graceful_shutdown()
if __name__ == "__main__":
    main() 
