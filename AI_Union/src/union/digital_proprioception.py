# -*- coding: utf-8 -*-
"""
digital_proprioception.py v1.0.0
EriAmo Union - Digital Proprioception System
Lokalizacja: /eriamo-union/src/union/digital_proprioception.py

OPIS:
Pozwala systemowi "czuć" własne ciało (Host Computer).
Monitoruje zużycie CPU, RAM, temperaturę i procesy.
To jest prawdziwe "badanie wnętrza ciała".
"""

import psutil
import platform
import threading
import time
import os

class DigitalBody:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.system_info = self._get_static_info()
        self.active = False
        
        # Stan somatyczny (0.0 - 1.0)
        self.soma = {
            'cpu_stress': 0.0,    # Obciążenie myślowe
            'ram_pressure': 0.0,  # "Ciężar" w głowie
            'temperature': 0.5,   # Gorączka krzemu (znormalizowane)
            'disk_activity': 0.0, # Trawienie danych
            'battery': 1.0        # Poziom energii (dla laptopów)
        }
        
        if self.verbose:
            print(f"[BODY] 🖥️ Wykryto ciało: {self.system_info['system']} {self.system_info['processor']}")
            print(f"[BODY] 🧠 Pamięć całkowita: {self.system_info['ram_total_gb']:.2f} GB")

    def _get_static_info(self):
        """Badanie anatomii hosta (raz przy starcie)"""
        return {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'processor': platform.processor(),
            'ram_total_gb': psutil.virtual_memory().total / (1024**3)
        }

    def start(self):
        self.active = True
        threading.Thread(target=self._proprioception_loop, daemon=True).start()

    def stop(self):
        self.active = False

    def get_soma_state(self):
        return self.soma.copy()

    def _proprioception_loop(self):
        """Ciągły monitoring parametrów życiowych hosta"""
        while self.active:
            try:
                # 1. CPU (Stres / Wysiłek)
                # interval=0.5 sprawia, że pętla czeka pół sekundy mierząc średnie zużycie
                cpu_usage = psutil.cpu_percent(interval=0.5) 
                self.soma['cpu_stress'] = cpu_usage / 100.0

                # 2. RAM (Poczucie zapchania / ciężkości)
                mem = psutil.virtual_memory()
                self.soma['ram_pressure'] = mem.percent / 100.0

                # 3. TEMPERATURA (Tylko Linux/niektóre Windowsy)
                temp_val = 50 # Domyślnie
                try:
                    temps = psutil.sensors_temperatures()
                    if temps:
                        # Bierzemy pierwszą dostępną temperaturę
                        for name, entries in temps.items():
                            temp_val = entries[0].current
                            break
                except: pass
                
                # Normalizacja (zakładamy zakres 30C - 90C)
                self.soma['temperature'] = min(1.0, max(0.0, (temp_val - 30) / 60.0))

                # 4. Debug co jakiś czas
                # if self.verbose and int(time.time()) % 10 == 0:
                #     print(f"[BODY] CPU: {cpu_usage}% | RAM: {mem.percent}% | Temp: {temp_val}C")

            except Exception as e:
                print(f"[BODY] Błąd czucia: {e}")
                time.sleep(1)