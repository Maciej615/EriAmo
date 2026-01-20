# -*- coding: utf-8 -*-
"""
soul_io.py v6.0.1-Union Fix
Lokalizacja: /eriamo-union/src/language/soul_io.py
"""
import json
import os
import time
from config import Config, Colors

class SoulIO:
    def __init__(self):
        self.filepath = Config.SOUL_FILE

    def load_stream(self):
        """
        Wczytuje definicje i ZWRACA słownik (dla AII v6.0.0).
        Nie wymaga argumentu d_map_ref.
        """
        loaded_data = {} # Tworzymy nowy, lokalny słownik
        
        if not os.path.exists(self.filepath):
            return loaded_data
            
        count = 0
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        data = json.loads(line)
                        # Sprawdzamy typ rekordu (kompatybilność wsteczna i nowa)
                        if data.get('_type') in ['@MEMORY', 'memory']:
                            # Używamy ID jako klucza
                            rec_id = data.get('id')
                            if rec_id:
                                loaded_data[rec_id] = data
                                count += 1
                    except json.JSONDecodeError:
                        continue
            print(f"{Colors.GREEN}[SoulIO] Wczytano strumieniowo {count} obiektów.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd odczytu: {e}{Colors.RESET}")
            
        return loaded_data

    def save_stream(self, data_to_save):
        """Metoda zapisuje duszę (nadal przyjmuje dane jako argument)."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                # Meta nagłówek
                meta = {"_type": "@META", "timestamp": time.time(), "count": len(data_to_save)}
                f.write(json.dumps(meta, ensure_ascii=False) + "\n")
                
                # Zapis właściwy
                for key, val in data_to_save.items():
                    f.write(json.dumps(val, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd zapisu: {e}{Colors.RESET}")