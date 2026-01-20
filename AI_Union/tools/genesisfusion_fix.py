# -*- coding: utf-8 -*-
"""
genesisfusion_fix.py v3.0 - Auto-Path Fix
Naprawia błędy ścieżek i poprawnie integruje moduły Genesis.
"""

import os
import sys

# Ustawienie ścieżki, żeby widzieć moduły obok
current_dir = os.path.dirname(os.path.abspath(__file__))
# Fix: point to root
lang_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(lang_dir)

try:
    from aii import AII
    from config import Colors
except ImportError:
    # Fallback jeśli brak config
    class Colors:
        BOLD = '\033[1m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        RESET = '\033[0m'
    from aii import AII

def run_fusion_fix():
    print(f"{Colors.BOLD}{Colors.CYAN}--- PROCES FUSION v3.0: Naprawa Ścieżek ---{Colors.RESET}")
    
    # 1. Inicjalizacja GŁÓWNEGO mózgu (tego jednego, który ma się nauczyć)
    print("🧠 Inicjalizacja głównego rdzenia AII...")
    main_ai = AII()
    
    # 2. Dynamiczna ścieżka (działa na każdym komputerze)
    base_dir = lang_dir
    print(f"📂 Katalog roboczy: {base_dir}")
    
    # 3. Lista modułów w kolejności (logika -> słowa -> matematyka)
    genesis_files = [
        "genesissk.py",      # Składnia (jeśli istnieje)
        "genesisdef.py",     # Definicje faktów
        "genesis_grammar.py",# Gramatyka i zaimki
        "genesis_math.py",   # Matematyka
        "genesiskit.py",     # Emocje
        "genesispyt.py",     # Pytania
        "genesis.py"         # Asocjacje
    ]
    
    # Kontekst wykonania - podmieniamy 'ai' na naszą instancję
    context = {
        'ai': main_ai,
        'AII': lambda: main_ai, # Oszustwo: gdy skrypt zawoła AII(), dostanie main_ai
        'Colors': Colors,
        'print': print,
        '__name__': '__main__'
    }

    success_count = 0

    for gf_name in genesis_files:
        gf_path = os.path.join(base_dir, gf_name)
        
        if os.path.exists(gf_path):
            print(f"\n{Colors.CYAN}>>> Wczytywanie modułu: {gf_name}...{Colors.RESET}")
            try:
                with open(gf_path, "r", encoding="utf-8") as f:
                    script_content = f.read()
                
                # --- CHIRURGIA KODU ---
                # Usuwamy linijki, które resetują mózg w pod-plikach
                lines = script_content.splitlines()
                safe_lines = []
                for line in lines:
                    if "ai = AII()" in line:
                        safe_lines.append("# [FUSION BLOCKED] " + line)
                    elif "from aii import AII" in line:
                        safe_lines.append("# [FUSION BLOCKED] " + line)
                    else:
                        safe_lines.append(line)
                
                safe_code = "\n".join(safe_lines)
                
                # Wykonujemy kod w kontekście naszego main_ai
                exec(safe_code, context)
                success_count += 1
                print(f"{Colors.GREEN}✓ Moduł {gf_name} zintegrowany.{Colors.RESET}")
                
            except Exception as e:
                print(f"{Colors.RED}⚠️ Błąd w module {gf_name}: {e}{Colors.RESET}")
        else:
            # Niektóre pliki mogą nie istnieć (np. genesissk.py), to normalne
            pass

    # Zapisz wynik
    print(f"\n{Colors.MAGENTA}{'='*60}")
    print(f"FUSION ZAKOŃCZONE. Zintegrowano {success_count} modułów.")
    print(f"{'='*60}{Colors.RESET}")
    
    main_ai.save()
    print(f"{Colors.GREEN}💾 Wiedza zapisana do pliku eriamo.soul (lub lexicon.soul){Colors.RESET}")

if __name__ == "__main__":
    run_fusion_fix()
