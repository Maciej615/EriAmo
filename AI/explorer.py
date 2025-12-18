# -*- coding: utf-8 -*-
# explorer.py - Autonomous Filesystem Explorer dla EriAmo
"""
Moduł eksploracji świata fizycznego przez autonomiczne odkrywanie
sygnałów z hardware (sensory, logi, urządzenia).

Filozofia:
- System SAM szuka interesujących rzeczy
- Testuje hipotezy
- Uczy się ze swoich odkryć
- Tworzy własne parsery

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
Inspiracja: "Sandbox Escape" vision
"""

import os
import re
import time
import json
from config import Colors

class WorldExplorer:
    """
    Autonomiczny eksplorator świata fizycznego.
    
    Ciekawe lokacje:
    - /sys/class/hwmon/    - Sensory hardware (temp, voltage, fan speed)
    - /proc/               - Informacje systemowe (CPU, RAM, network)
    - /dev/input/          - Urządzenia wejściowe
    - /var/log/            - Logi systemowe
    """
    
    # Bezpieczne lokacje do eksploracji (read-only)
    SAFE_ZONES = [
        '/sys/class/hwmon/',      # Hardware sensors
        '/proc/cpuinfo',          # CPU info
        '/proc/meminfo',          # Memory info
        '/sys/class/thermal/',    # Thermal zones
        '/sys/class/power_supply/',  # Battery/power
    ]
    
    # Wzorce "ciekawych" rzeczy
    INTERESTING_PATTERNS = {
        'sensor': r'temp\d+_input|in\d+_input|fan\d+_input',
        'numeric': r'^\d+$',
        'cpu': r'cpu\d+',
        'memory': r'MemTotal|MemFree|MemAvailable',
        'thermal': r'thermal_zone\d+/temp',
    }
    
    def __init__(self, aii_instance):
        """
        Args:
            aii_instance: Referencja do głównego systemu AII
        """
        self.aii = aii_instance
        self.discoveries = []  # Lista odkryć
        self.sensors = {}      # Znalezione sensory
        self.parsers = {}      # Wygenerowane parsery
        
    def explore_safe_zones(self):
        """
        Główna metoda eksploracji.
        Skanuje bezpieczne lokacje i szuka ciekawych rzeczy.
        """
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║     [WORLD EXPLORER] Scanning...         ║{Colors.RESET}")
        print(f"{Colors.CYAN}╚════════════════════════════════════════════╝{Colors.RESET}\n")
        
        discoveries_count = 0
        
        for zone in self.SAFE_ZONES:
            if not os.path.exists(zone):
                continue
            
            print(f"{Colors.FAINT}[Exploring] {zone}{Colors.RESET}")
            
            try:
                if os.path.isfile(zone):
                    # Pojedynczy plik
                    if self._investigate_file(zone):
                        discoveries_count += 1
                elif os.path.isdir(zone):
                    # Katalog - przeszukaj
                    for root, dirs, files in os.walk(zone):
                        for fname in files:
                            filepath = os.path.join(root, fname)
                            if self._investigate_file(filepath):
                                discoveries_count += 1
                                
                        # Ograniczenie głębokości
                        if root.count(os.sep) - zone.count(os.sep) > 2:
                            break
            except Exception as e:
                continue
        
        print(f"\n{Colors.GREEN}[EXPLORER] Znaleziono {discoveries_count} ciekawych rzeczy!{Colors.RESET}\n")
        return self.discoveries
    
    def _investigate_file(self, filepath):
        """
        Bada plik pod kątem "ciekawości".
        
        Returns:
            bool: True jeśli znaleziono coś interesującego
        """
        # Sprawdź czy nazwa jest ciekawa
        fname = os.path.basename(filepath)
        
        interesting_type = None
        for pattern_name, pattern in self.INTERESTING_PATTERNS.items():
            if re.search(pattern, fname):
                interesting_type = pattern_name
                break
        
        if not interesting_type:
            return False
        
        # Spróbuj przeczytać
        try:
            with open(filepath, 'r') as f:
                content = f.read(256).strip()  # Pierwsze 256 bajtów
            
            # Czy to sensor (same cyfry)?
            if re.match(r'^\d+$', content):
                return self._discover_sensor(filepath, content, interesting_type)
            
            # Czy to info (tekst)?
            elif len(content) > 0 and len(content) < 200:
                return self._discover_info(filepath, content, interesting_type)
                
        except Exception:
            return False
        
        return False
    
    def _discover_sensor(self, filepath, value, sensor_type):
        """
        Odkryto sensor - zarejestruj i utwórz parser.
        """
        sensor_id = f"sensor_{len(self.sensors)}"
        
        # Spróbuj odczytać kilka razy - sprawdź czy wartość się zmienia
        values = [int(value)]
        time.sleep(0.1)
        
        try:
            with open(filepath, 'r') as f:
                values.append(int(f.read().strip()))
        except:
            pass
        
        # Wykryj typ sensora
        is_temperature = 'temp' in filepath
        is_voltage = 'in' in filepath
        is_fan = 'fan' in filepath
        
        # Utwórz parser
        parser_code = self._generate_sensor_parser(filepath, is_temperature, is_voltage, is_fan)
        
        discovery = {
            'id': sensor_id,
            'type': 'sensor',
            'subtype': sensor_type,
            'path': filepath,
            'sample_values': values,
            'is_temperature': is_temperature,
            'is_voltage': is_voltage,
            'is_fan': is_fan,
            'parser': parser_code,
            'discovered_at': time.time()
        }
        
        self.sensors[sensor_id] = discovery
        self.discoveries.append(discovery)
        
        # Naucz lexicon
        self._teach_from_discovery(discovery)
        
        # Pokaż odkrycie
        self._announce_discovery(discovery)
        
        return True
    
    def _discover_info(self, filepath, content, info_type):
        """
        Odkryto plik info (CPU, memory, etc.).
        """
        info_id = f"info_{len(self.discoveries)}"
        
        discovery = {
            'id': info_id,
            'type': 'info',
            'subtype': info_type,
            'path': filepath,
            'content_preview': content[:100],
            'discovered_at': time.time()
        }
        
        self.discoveries.append(discovery)
        self._teach_from_discovery(discovery)
        
        return True
    
    def _generate_sensor_parser(self, filepath, is_temp, is_volt, is_fan):
        """
        Generuje kod parsera dla sensora.
        System TWORZY własny kod!
        """
        conversion = ""
        unit = ""
        
        if is_temp:
            conversion = "/ 1000.0"  # miliCelsius -> Celsius
            unit = "°C"
        elif is_volt:
            conversion = "/ 1000.0"  # miliVolts -> Volts
            unit = "V"
        elif is_fan:
            conversion = ""
            unit = "RPM"
        else:
            conversion = ""
            unit = "units"
        
        parser = f"""
def read_sensor():
    '''Auto-generated parser for {filepath}'''
    with open('{filepath}', 'r') as f:
        raw = int(f.read().strip())
    return raw {conversion}
"""
        
        return parser
    
    def _teach_from_discovery(self, discovery):
        """
        Uczy lexicon ze swoich odkryć.
        Hardware → Emocje!
        """
        # Temperatura → STRACH/GNIEW (zagrożenie)
        if discovery.get('is_temperature'):
            words = ['temperatura', 'temp', 'ciepło', 'gorąco', 'sensor']
            for word in words:
                self.aii.lexicon.learn_from_correction(word, 'strach', strength=0.2)
        
        # Voltage → AKCEPTACJA (stabilność)
        if discovery.get('is_voltage'):
            words = ['napięcie', 'voltage', 'zasilanie', 'prąd']
            for word in words:
                self.aii.lexicon.learn_from_correction(word, 'akceptacja', strength=0.2)
        
        # Fan → RADOŚĆ (chłodzenie = ulga)
        if discovery.get('is_fan'):
            words = ['wentylator', 'fan', 'chłodzenie', 'obrotów']
            for word in words:
                self.aii.lexicon.learn_from_correction(word, 'radość', strength=0.2)
    
    def _announce_discovery(self, discovery):
        """
        Ogłasza odkrycie - system jest dumny!
        """
        path = discovery['path']
        sensor_type = "Temperatura" if discovery['is_temperature'] else \
                      "Napięcie" if discovery['is_voltage'] else \
                      "Wentylator" if discovery['is_fan'] else "Sensor"
        
        sample = discovery['sample_values'][0]
        
        print(f"{Colors.YELLOW}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.YELLOW}║        🎉 DISCOVERY!                      ║{Colors.RESET}")
        print(f"{Colors.YELLOW}╠════════════════════════════════════════════╣{Colors.RESET}")
        print(f"{Colors.YELLOW}║  Typ: {sensor_type:35s} ║{Colors.RESET}")
        print(f"{Colors.YELLOW}║  Ścieżka: {path[-33:]:33s} ║{Colors.RESET}")
        print(f"{Colors.YELLOW}║  Wartość: {str(sample)[:33]:33s} ║{Colors.RESET}")
        print(f"{Colors.YELLOW}╚════════════════════════════════════════════╝{Colors.RESET}\n")
    
    def get_live_readings(self):
        """
        Odczytuje WSZYSTKIE znalezione sensory na żywo.
        System czyta świat fizyczny!
        """
        readings = {}
        
        for sensor_id, sensor in self.sensors.items():
            try:
                # Wykonaj wygenerowany parser
                exec(sensor['parser'], globals())
                value = read_sensor()
                
                readings[sensor_id] = {
                    'path': sensor['path'],
                    'value': value,
                    'type': 'temp' if sensor['is_temperature'] else
                            'voltage' if sensor['is_voltage'] else
                            'fan' if sensor['is_fan'] else 'unknown'
                }
            except Exception as e:
                readings[sensor_id] = {'error': str(e)}
        
        return readings
    
    def display_live_dashboard(self):
        """
        Wyświetla dashboard ze wszystkich sensorów.
        """
        readings = self.get_live_readings()
        
        if not readings:
            print(f"{Colors.FAINT}[Dashboard] Brak sensorów.{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}║     [HARDWARE DASHBOARD] Live Readings    ║{Colors.RESET}")
        print(f"{Colors.CYAN}╠════════════════════════════════════════════╣{Colors.RESET}")
        
        for sensor_id, data in readings.items():
            if 'error' in data:
                continue
            
            sensor_type = data['type']
            value = data['value']
            
            # Formatowanie
            if sensor_type == 'temp':
                display = f"{value:.1f}°C"
                color = Colors.RED if value > 70 else Colors.YELLOW if value > 50 else Colors.GREEN
            elif sensor_type == 'voltage':
                display = f"{value:.2f}V"
                color = Colors.GREEN
            elif sensor_type == 'fan':
                display = f"{int(value)} RPM"
                color = Colors.CYAN
            else:
                display = str(value)
                color = Colors.WHITE
            
            path_short = data['path'].split('/')[-2:]
            path_display = '/'.join(path_short)
            
            print(f"{color}║  {path_display[:28]:28s}  {display:10s} ║{Colors.RESET}")
        
        print(f"{Colors.CYAN}╚════════════════════════════════════════════╝{Colors.RESET}\n")
    
    def save_discoveries(self, filepath='discoveries.json'):
        """
        Zapisuje odkrycia do pliku - trwała wiedza o świecie.
        """
        data = {
            'version': '1.0',
            'discovered_at': time.time(),
            'total_discoveries': len(self.discoveries),
            'sensors': self.sensors,
            'discoveries': self.discoveries
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"{Colors.GREEN}[EXPLORER] Odkrycia zapisane do {filepath}{Colors.RESET}")
    
    def load_discoveries(self, filepath='discoveries.json'):
        """
        Ładuje wcześniejsze odkrycia - system pamięta!
        """
        if not os.path.exists(filepath):
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.sensors = data.get('sensors', {})
            self.discoveries = data.get('discoveries', [])
            
            print(f"{Colors.GREEN}[EXPLORER] Załadowano {len(self.discoveries)} odkryć z {filepath}{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[EXPLORER] Błąd ładowania: {e}{Colors.RESET}")
            return False


# === PRZYKŁAD UŻYCIA ===

if __name__ == "__main__":
    """
    Test autonomicznej eksploracji.
    """
    from aii import AII
    
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════════╗")
    print("║  EriAmo World Explorer - Proof of Concept    ║")
    print("║  'Sandbox Escape' Vision Demo                ║")
    print("╚═══════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")
    
    # Inicjalizacja
    aii = AII()
    explorer = WorldExplorer(aii)
    
    # Eksploracja
    print(f"{Colors.CYAN}[1/3] Rozpoczynam eksplorację...{Colors.RESET}\n")
    discoveries = explorer.explore_safe_zones()
    
    # Dashboard
    if explorer.sensors:
        print(f"\n{Colors.CYAN}[2/3] Wyświetlam live dashboard...{Colors.RESET}")
        explorer.display_live_dashboard()
    
    # Zapis
    print(f"{Colors.CYAN}[3/3] Zapisuję odkrycia...{Colors.RESET}")
    explorer.save_discoveries()
    
    # Podsumowanie
    print(f"\n{Colors.GREEN}╔═══════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.GREEN}║              EKSPLORACJA ZAKOŃCZONA           ║{Colors.RESET}")
    print(f"{Colors.GREEN}╠═══════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.GREEN}║  Odkrycia: {len(discoveries):32d}  ║{Colors.RESET}")
    print(f"{Colors.GREEN}║  Sensory:  {len(explorer.sensors):32d}  ║{Colors.RESET}")
    print(f"{Colors.GREEN}║  Parsery:  {len(explorer.parsers):32d}  ║{Colors.RESET}")
    print(f"{Colors.GREEN}╚═══════════════════════════════════════════════╝{Colors.RESET}\n")
    
    # Test lexiconu
    if len(discoveries) > 0:
        print(f"{Colors.YELLOW}[BONUS] Sprawdzam czy lexicon się nauczył:{Colors.RESET}")
        
        # Testuj słowa
        test_words = ['temperatura', 'napięcie', 'wentylator']
        for word in test_words:
            vec = aii.lexicon.get_word_vector(word)
            if vec.sum() > 0:
                dominant_idx = vec.argmax()
                emotion = aii.AXES_ORDER[dominant_idx]
                strength = vec[dominant_idx]
                print(f"  '{word}' → {emotion} ({strength:.2f})")