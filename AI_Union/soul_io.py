# -*- coding: utf-8 -*-
"""
soul_io.py v8.0.0-Hybrid Fix
Obsługuje bezpieczne tworzenie plików i folderów dla architektury 15-osiowej.
"""
import json
import os
import time
from config import Config, Colors

class SoulIO:
    def __init__(self):
        # Upewniamy się, że ścieżka pochodzi z configu, fallback do domyślnej
        self.filepath = getattr(Config, 'SOUL_FILE', 'eriamo.soul')

    def _ensure_directory(self):
        """Tworzy strukturę katalogów, jeśli nie istnieje."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"{Colors.YELLOW}[SoulIO] Utworzono katalog: {directory}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[SoulIO] Błąd tworzenia katalogu: {e}{Colors.RESET}")

    def load_stream(self):
        """Wczytuje pamięć. Jeśli plik nie istnieje, zwraca pusty słownik."""
        loaded_data = {}
        
        if not os.path.exists(self.filepath):
            print(f"{Colors.YELLOW}[SoulIO] Brak pliku pamięci. Rozpoczynamy jako Tabula Rasa.{Colors.RESET}")
            return loaded_data
            
        count = 0
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        data = json.loads(line)
                        if data.get('_type') in ['@MEMORY', 'memory']:
                            rec_id = data.get('id')
                            if rec_id:
                                loaded_data[rec_id] = data
                                count += 1
                    except json.JSONDecodeError:
                        continue
            print(f"{Colors.GREEN}[SoulIO] Wczytano {count} wspomnień.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd odczytu: {e}{Colors.RESET}")
            
        return loaded_data

    def save_stream(self, data_to_save):
        """Zapisuje duszę, tworząc plik jeśli trzeba."""
        self._ensure_directory()
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                # Meta nagłówek
                meta = {"_type": "@META", "timestamp": time.time(), "count": len(data_to_save)}
                f.write(json.dumps(meta, ensure_ascii=False) + "\n")
                
                # Zapis właściwy
                for key, val in data_to_save.items():
                    f.write(json.dumps(val, ensure_ascii=False) + "\n")
            # Feedback tylko przy błędzie lub w debug mode, żeby nie spamować
        except Exception as e:
            print(f"{Colors.RED}[SoulIO] Błąd zapisu: {e}{Colors.RESET}")