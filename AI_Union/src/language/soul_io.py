# -*- coding: utf-8 -*-
"""
soul_io.py
Lokalizacja: /eriamo-union/src/language/soul_io.py
"""
import json
import os
import time
from config import Config, Colors

class SoulIO:
    def __init__(self):
        self.filepath = Config.SOUL_FILE

    def load_soul_stream(self, d_map_ref):
        """Wczytuje definicje linia po linii."""
        if not os.path.exists(self.filepath):
            return 
        count = 0
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        data = json.loads(line)
                        if data.get('_type') == '@MEMORY':
                            d_map_ref[data['id']] = data
                            count += 1
                    except json.JSONDecodeError:
                        continue
            print(f"{Colors.GREEN}[SoulIO] Wczytano strumieniowo {count} obiektów.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd krytyczny: {e}{Colors.RESET}")

    def save_stream(self, d_map_ref):
        """Metoda, której brakowało! Zapisuje duszę."""
        try:
            # Używamy trybu 'w' (nadpisz), bo zrzucamy całą pamięć z RAM
            with open(self.filepath, 'w', encoding='utf-8') as f:
                # Meta
                meta = {"_type": "@META", "timestamp": time.time(), "count": len(d_map_ref)}
                f.write(json.dumps(meta, ensure_ascii=False) + "\n")
                
                # Dane
                for key, val in d_map_ref.items():
                    f.write(json.dumps(val, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd zapisu: {e}{Colors.RESET}")