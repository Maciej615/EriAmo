# -*- coding: utf-8 -*-
# ==============================================================================
# PROJECT: EriAmo Bedrock v7.3.3
# AUTHOR:  Maciek
# DATE:    21.11.2025
# ==============================================================================
#
# LICENSE (GPLv3):
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# ==============================================================================
# EriAmo Bedrock v7.3.3 - Full English Version

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

# --- VECTOR MATH ---
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

# --- SECURITY SYSTEM ---
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
            EvilSignature("format c:", ThreatLevel.CRITICAL, "system", "Disk format")
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
            return "ERROR: Invalid threat level (SAFE, SUSPICIOUS, DANGEROUS, CRITICAL)."

        if any(sig.pattern.lower() == p_clean for sig in self.signatures):
            return "ERROR: This pattern already exists."

        new_sig = EvilSignature(pattern, level, category, description)
        self.signatures.append(new_sig)
        self.save_signatures()
        return f"Added new threat: '{pattern}' ({level.name})"

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

# --- CORE ENGINE ---
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
        self.log("=== EriAmo Bedrock v7.3.3 Sovereign Hybrid ===", "CYAN")
        self.load() 
        self.load_memory()

    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")

    def _init_lang_dict(self):
        return {
            "logic": ["why", "how", "reason", "logic", "result", "analysis", "cause"],
            "emotion": ["feel", "love", "joy", "sad", "anger", "emotion", "hate", "fear", "happiness"],
            "existence": ["i", "you", "life", "being", "soul", "existence", "human"],
            "combat": ["defend", "attack", "threat", "enemy", "shield", "empire", "fight"],
            "creation": ["create", "new", "idea", "art", "project", "build", "paint"],
            "knowledge": ["know", "teach", "info", "data", "memory", "knowledge", "book"],
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
                    self.log("[INTEGRITY] ⚠️ CORRUPTED → RESETTING", "RED")
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
                self.log("\n[ADRENALINE] 💉 Defense Protocol: +40 Energy", "RED")
            return

        if time.time() - self.last_sleep_time > self.AUTO_SLEEP_INTERVAL or self.energy < self.LOW_ENERGY_THRESHOLD:
            self.log("\n[AUTO-SLEEP] Regeneration required...", "PINK")
            self.sleep_cycle()

    def sleep_cycle(self):
        self.log("[SLEEP] 💤 Initiating deep memory consolidation...", "PINK")
        time.sleep(1)
        
        reinforced = 0
        for entry in self.H_Log[-30:]:
            words = set(entry['content'].lower().split())
            for d in self.MapaD.values():
                for tag in d['tags']:
                    if tag in words:
                        d['weight'] = min(100.0, d['weight'] + 0.5)
                        reinforced += 1

        compressed = 0
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
        self.save()
        self.log(f"[SLEEP] Woke up. Energy: {self.energy:.0f} | Reinforced: {reinforced} | Compressed: {compressed}", "GREEN")

    def process_input(self, text: str):
        if self.evil_detector.analyze(text).value >= ThreatLevel.DANGEROUS.value:
            self.log("[BLOCK] Threat detected!", "RED")
            self.energy -= 5
            self.check_auto_sleep()
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

        triggers = ["remember", "note", "save this", "important"]
        text_lower = text.lower()
        trigger = next((t for t in triggers if t in text_lower), None)
        if trigger:
            rest = text[text_lower.find(trigger) + len(trigger):].strip()
            rest = re.sub(r'^[:·•—–\-.,\s]+', '', rest).strip()
            if len(rest) > 4:
                tag = f"auto_{int(time.time())}"
                self.teach(tag, rest)
                self.log(f"[AUTO-SAVE] '{rest}' → {tag}", "CYAN")

        self.energy -= 2.0
        response = f"I recall: {memory_hit}" if memory_hit else "Understood."
        print(f"\n[Guardian] {response}")
        self.check_auto_sleep()

    def handle_command(self, cmd: str):
        parts = cmd.split()
        c = parts[0].lower().replace("/", "!")

        if c == "!help":
            print("\n--- COMMANDS ---")
            print(" !teach [tag] [content]        – manual learning")
            print(" !teachevil [pattern] [LEVEL] [cat] [desc]")
            print(" !sleep   !status   !attack   !exit")
        
        elif c == "!teachevil":
            if len(parts) < 5:
                print("Usage: !teachevil [pattern] [SAFE/SUSPICIOUS/DANGEROUS/CRITICAL] [category] [description...]")
            else:
                res = self.evil_detector.teach_evil(parts[1], parts[2], parts[3], " ".join(parts[4:]))
                self.log(f"[SEC] {res}", "RED")

        elif c == "!teach" and len(parts) >= 3:
            self.teach(parts[1], " ".join(parts[2:]))

        elif c in ("!sleep", "!status", "!attack", "!exit"):
            if c == "!sleep":
                self.sleep_cycle()
            elif c == "!status":
                print(f"\n[STATUS] Energy: {self.energy:.1f} | Memory (MapaD): {len(self.MapaD)}")
                print(f"[SOUL] 💓 Pulse: OK. Vector integrity: {VectorMath.norm(self.vector):.2f}")
            elif c == "!attack":
                self.log("⚔️ [SIMULATION] Attack detected! Energy dropping...", "RED")
                fake_sig = EvilSignature("TEST_ATTACK", ThreatLevel.DANGEROUS, "sim", "Maneuver")
                self.evil_detector.log_threat(ThreatLevel.DANGEROUS, fake_sig, "Combat simulation")
                self.energy = 15.0
                print(f"[SYSTEM] Critical energy: {self.energy}. Awaiting defense response...")
            elif c == "!exit":
                self.active = False
        else:
            print("Unknown command. !help")

    def teach(self, tag: str, content: str):
        vec = self._text_to_vector(content)
        id_def = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[id_def] = {'vector': vec, 'weight': 5.0, 'tags': [tag], 'content': content, 'id': id_def}
        self.log(f"[LEARN] Saved '{tag}'", "GREEN")
        self.save_memory()

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
        except:
            self.MapaD = {}
            self.H_Log = []

# --- MAIN LOOP ---
def main():
    bot = EriAmoCore()
    print("\n[EriAmo Bedrock] Enter commands or type your text. !help for list of commands.\n")
    while bot.active:
        try:
            user_input = input(">>> ")
            bot.process_input(user_input)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            bot.log(f"[ERROR] {e}", "RED")

if __name__ == "__main__":
    main()
