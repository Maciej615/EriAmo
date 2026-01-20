# -*- coding: utf-8 -*-
# explorer.py - Autonomous Filesystem Explorer dla EriAmo
"""
Moduł eksploracji świata fizycznego przez autonomiczne odkrywanie.
System SAM szuka sensorów w /sys/, /proc/ i tworzy własne parsery.
"""

import os
import re
import time
import json

# Definicja kolorów lokalnie, by nie zgubić zależności
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    FAINT = '\033[2m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class WorldExplorer:
    """
    Autonomiczny eksplorator świata fizycznego.
    Bada: /sys/class/hwmon/, /proc/, generuje kod Pythona do ich odczytu.
    """
    
    SAFE_ZONES = [
        '/sys/class/hwmon/',      
        '/proc/cpuinfo',          
        '/proc/meminfo',          
        '/sys/class/thermal/',    
        '/sys/class/power_supply/',  
    ]
    
    INTERESTING_PATTERNS = {
        'sensor': r'temp\d+_input|in\d+_input|fan\d+_input',
        'numeric': r'^\d+$',
        'cpu': r'cpu\d+',
        'memory': r'MemTotal|MemFree|MemAvailable',
        'thermal': r'thermal_zone\d+/temp',
    }
    
    def __init__(self, aii_instance=None):
        self.aii = aii_instance
        self.discoveries = []
        self.sensors = {}
        self.parsers = {}
        
        # Próba załadowania poprzedniej wiedzy
        self.load_discoveries()

    def explore_safe_zones(self):
        """Główny skan terytorium."""
        print(f"\n{Colors.CYAN}[EXPLORER] Rozpoczynam mapowanie nerwowe...{Colors.RESET}")
        discoveries_count = 0
        
        for zone in self.SAFE_ZONES:
            if not os.path.exists(zone): continue
            
            try:
                if os.path.isfile(zone):
                    if self._investigate_file(zone): discoveries_count += 1
                elif os.path.isdir(zone):
                    for root, dirs, files in os.walk(zone):
                        for fname in files:
                            filepath = os.path.join(root, fname)
                            if self._investigate_file(filepath): discoveries_count += 1
                        if root.count(os.sep) - zone.count(os.sep) > 2: break
            except Exception: continue
        
        print(f"{Colors.GREEN}[EXPLORER] Zmapowano {discoveries_count} nowych zakończeń nerwowych.{Colors.RESET}")
        self.save_discoveries() # Zapisz wiedzę
        return self.discoveries
    
    def _investigate_file(self, filepath):
        fname = os.path.basename(filepath)
        interesting_type = None
        for pattern_name, pattern in self.INTERESTING_PATTERNS.items():
            if re.search(pattern, fname):
                interesting_type = pattern_name
                break
        
        if not interesting_type: return False
        
        try:
            with open(filepath, 'r') as f: content = f.read(256).strip()
            if re.match(r'^\d+$', content):
                return self._discover_sensor(filepath, content, interesting_type)
        except: return False
        return False
    
    def _discover_sensor(self, filepath, value, sensor_type):
        sensor_id = f"sensor_{len(self.sensors)}"
        is_temp = 'temp' in filepath
        is_volt = 'in' in filepath
        is_fan = 'fan' in filepath
        
        # GENIALNE: System pisze własny kod parsera!
        parser_code = self._generate_sensor_parser(filepath, is_temp, is_volt, is_fan)
        
        discovery = {
            'id': sensor_id,
            'type': 'sensor',
            'path': filepath,
            'is_temperature': is_temp,
            'is_voltage': is_volt,
            'is_fan': is_fan,
            'parser': parser_code,
            'discovered_at': time.time()
        }
        
        self.sensors[sensor_id] = discovery
        self.discoveries.append(discovery)
        
        # Uczenie leksykonu (jeśli podłączony)
        if self.aii: self._teach_from_discovery(discovery)
        
        return True
    
    def _generate_sensor_parser(self, filepath, is_temp, is_volt, is_fan):
        conversion = "/ 1000.0" if (is_temp or is_volt) else ""
        return f"""
def read_sensor():
    try:
        with open('{filepath}', 'r') as f:
            raw = int(f.read().strip())
        return raw {conversion}
    except: return 0.0
"""
    
    def _teach_from_discovery(self, discovery):
        if hasattr(self.aii, 'lexicon'):
            if discovery['is_temperature']:
                self.aii.lexicon.learn_from_correction('gorąco', 'strach', 0.1)
            if discovery['is_fan']:
                self.aii.lexicon.learn_from_correction('wiatrak', 'radość', 0.1)

    def get_live_readings(self):
        """Uruchamia wygenerowane parsery i zwraca dane."""
        readings = {}
        for sensor_id, sensor in self.sensors.items():
            try:
                # EZEKUCJA KODU NAPISANEGO PRZEZ AI
                local_scope = {}
                exec(sensor['parser'], {}, local_scope)
                value = local_scope['read_sensor']()
                
                key = 'unknown'
                if sensor['is_temperature']: key = 'ext_temp'
                elif sensor['is_fan']: key = 'fan_rpm'
                elif sensor['is_voltage']: key = 'voltage'
                
                # Dodajemy ID żeby uniknąć nadpisania
                readings[f"{key}_{sensor_id}"] = value
            except Exception: pass
        return readings

    def save_discoveries(self, filepath='data/hardware_map.json'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {'sensors': self.sensors, 'discoveries': self.discoveries}
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_discoveries(self, filepath='data/hardware_map.json'):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.sensors = data.get('sensors', {})
                self.discoveries = data.get('discoveries', [])
            except: pass