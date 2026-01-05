# -*- coding: utf-8 -*-
"""
genesisfusion.py v2.2 - Hardcoded Path
Łączy moduły Genesis, używając sztywnej ścieżki do plików.
"""

import os
import sys
from config import Colors

def run_fusion(aii_instance):
    print(f"{Colors.BOLD}{Colors.CYAN}--- PROCES FUSION: Integracja Wiedzy (Hardcoded Path) ---{Colors.RESET}")
    
    # 1. SZTYWNA ŚCIEŻKA (Bez zgadywania)
    base_dir = "/home/maciej/EriAmo_Union/src/language"
    
    # 2. Lista modułów w kolejności logicznej
    genesis_files = [
        "genesissk.py",   # Składnia
        "genesisdef.py",  # Definicje faktów
        "genesiskit.py",  # Gramatyka emocji
        "genesispyt.py",  # Pytania
        "genesis.py"      # Asocjacje podstawowe
    ]
    
    # 3. Kontekst współdzielony (Przekazujemy Twój działający mózg jako 'ai')
    context = {
        'ai': aii_instance,      # <--- To jest ten jedyny, prawdziwy mózg
        'AII': type(aii_instance), 
        'Colors': Colors,
        'print': print
    }

    total = len(genesis_files)
    
    # Sprawdzenie czy katalog w ogóle istnieje
    if not os.path.exists(base_dir):
        print(f"{Colors.RED}[FUSION] BŁĄD KRYTYCZNY: Katalog nie istnieje: {base_dir}{Colors.RESET}")
        return

    for i, gf_name in enumerate(genesis_files):
        # Pełna ścieżka do pliku
        gf_path = os.path.join(base_dir, gf_name)
        
        if os.path.exists(gf_path):
            print(f"{Colors.CYAN}[FUSION {i+1}/{total}] Operacja na: {gf_name}...{Colors.RESET}")
            try:
                with open(gf_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    
                # --- CHIRURGIA KODU (Wyciananie 'ai = AII()') ---
                safe_code = []
                for line in lines:
                    # Blokujemy tworzenie nowych instancji, żeby użyć tej z kontekstu
                    if "ai = AII()" in line:
                        safe_code.append(f"# {line.strip()}  <-- Zablokowane przez Fusion\n")
                    elif "from aii import AII" in line:
                        safe_code.append(f"# {line.strip()}  <-- Zablokowane przez Fusion\n")
                    else:
                        safe_code.append(line)
                
                final_code = "".join(safe_code)
                
                # Wykonujemy zmodyfikowany kod
                exec(final_code, context)
                
            except Exception as e:
                print(f"{Colors.RED}[FUSION] ⚠️ Błąd w module {gf_name}: {e}{Colors.RESET}")
                import traceback
                traceback.print_exc()
        else:
            print(f"{Colors.YELLOW}[FUSION] Brak pliku: {gf_name}{Colors.RESET}")
            print(f"Szukano dokładnie w: {gf_path}")

    # Zapisz wynik
    print(f"{Colors.GREEN}[FUSION] Matryca kompletna. Zapisywanie zintegrowanej wiedzy...{Colors.RESET}")
    if hasattr(aii_instance, 'save'):
        aii_instance.save()