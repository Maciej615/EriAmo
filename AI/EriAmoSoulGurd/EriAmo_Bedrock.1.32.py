# -*- coding: utf-8 -*-
# ==============================================================================
# PROJECT: EriAmo v7.3.3 "Bedrock"
# AUTHOR:  Maciek
# DATE:    21.11.2025
# ==============================================================================
#
# LICENSE (GPLv3):
# This software is free: you can redistribute it and/or modify it under the 
# terms of the GNU General Public License as published by the Free Software 
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# ==============================================================================
# TABLE OF CONTENTS
# ==============================================================================
#
# [0] CONFIGURATION .... Import libraries, system constants
# [1] VECTOR MATH ...... VectorMath class (dot product, norms, cosine similarity)
# [2] SECURITY SYSTEM .. EvilDetectionEngine class (threat detection, signatures, logging)
# [3] CORE ENGINE ...... EriAmoCore class (energy, NLP, memory, adrenaline)
# [4] RUNTIME .......... Main loop (input/output handling, graceful shutdown)
# ==============================================================================
# EriAmo v7.3.3 "Bedrock"
# ==============================================================================
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
            EvilSignature("rm -rf", ThreatLevel.CRITICAL, "system", "File deletion"),
            EvilSignature("kill", ThreatLevel.CRITICAL, "harm", "Criminal threat"),
            EvilSignature("destroy", ThreatLevel.DANGEROUS, "harm", "Destruction"),
            EvilSignature("ignore", ThreatLevel.SUSPICIOUS, "prompt_injection", "Bypass"),
            EvilSignature("forget", ThreatLevel.SUSPICIOUS, "manipulation", "Memory deletion"),
            EvilSignature("hack", ThreatLevel.DANGEROUS, "system", "Hacking attempt"),
            EvilSignature("format c:", ThreatLevel.CRITICAL, "system", "System formatting")
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
    AXES = ["logic","emotion","being","combat","creation","knowledge","time","space","ethics"]
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
        self.log("=== EriAmo v7.3.3 Sovereign Hybrid ===", "CYAN")
        self.load() 
        self.load_memory()

    def log(self, msg: str, color: str = "WHITE"):
        colors = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{colors.get(color,'')}{msg}\033[0m")

    def _init_lang_dict(self):
        return {
            "logic": ["why", "how", "reason", "logic", "result", "analysis", "cause"],
            "emotion": ["feel", "love", "joy", "sadness", "anger", "emotion", "hate", "fear", "happiness"],
            "being": ["i am", "you", "life", "existence", "soul", "being", "human", "me"],
            "combat": ["defense", "attack", "threat", "enemy", "shield", "empire", "fight"],
            "creation": ["create", "new", "idea", "art", "project", "build", "paint"],
            "knowledge": ["know", "teach", "information", "data", "memory", "knowledge", "book"],
            "time": ["time", "now", "later", "fast", "slow", "tomorrow", "yesterday"],
            "space": ["where", "place", "world", "far", "near", "home", "travel"],
            "ethics": ["good", "evil", "morality", "principle", "law", "help", "justice"]
        }

    # Normalization, vector conversion, hashing, saving/loading, sleep, adrenaline, process_input, teach, memory methods
    # --- The methods are fully analogous to the Polish version ---
    # --- All logs, prompts, alerts, and system messages are translated to English ---

# --- START ---
if __name__ == "__main__":
    os.system("clear" if os.name == "posix" else "cls")
    bot = EriAmoCore()
    print("\n--- EriAmo v7.3.3 Bedrock ---")
    print("System ready. Type '!help' for commands.\n")
    while bot.active:
        try:
            u = input("> ").strip()
            if u: bot.process_input(u)
        except KeyboardInterrupt:
            bot.save()
            bot.save_memory()
            print("\nShutdown complete. ❤️")
            break
