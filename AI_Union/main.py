# -*- coding: utf-8 -*-
"""
main.py v8.6.1-FixedExit
Naprawiono obsługę komendy /exit (z ukośnikiem).
"""

import sys
import os
import io
import time

# --- FIX KODOWANIA ---
try:
    if sys.stdin.encoding != 'utf-8':
        sys.stdin = io.TextIOWrapper(sys.stdin.detach(), encoding='utf-8', errors='replace')
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', errors='replace')
except Exception as e:
    print(f"[SYSTEM] Ostrzeżenie kodowania: {e}")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from union_config import UnionConfig, Colors
    from union_core import EriAmoUnion
    from multimodal_agency import MultimodalAgency 
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
    sys.exit(1)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Colors.CYAN}🌌 EriAmo Union v8.6.1 - System Gotowy.{Colors.RESET}")
    
    try:
        union = EriAmoUnion(verbose=True)
        agency = MultimodalAgency(union, verbose=True)
    except Exception as e:
        print(f"{Colors.RED}❌ Błąd inicjalizacji: {e}{Colors.RESET}")
        return
    
    union.start()
    agency.start()
    
    print(f"\n{Colors.GREEN}[INFO] System słucha. Wpisz /exit aby zakończyć.{Colors.RESET}\n")

    try:
        while True:
            try:
                cmd = input(f"{Colors.YELLOW}Ty > {Colors.RESET}")
            except EOFError: break
            
            if not cmd: continue
            
            # --- POPRAWKA TUTAJ ---
            # Teraz łapie exit z ukośnikiem i bez, oraz usuwa spacje
            clean_cmd = cmd.strip().lower()
            if clean_cmd in ['exit', 'quit', '/exit', '/quit', 'koniec']:
                break
            # ----------------------
                
            if hasattr(agency, 'stimulate'):
                agency.stimulate(cmd)

            response = union.process_input(cmd)
            
            if response:
                print(f" [EriAmo] {response}")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[SYSTEM] Przerwanie klawiszowe.{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}[BŁĄD] {e}{Colors.RESET}")
    finally:
        # Ta sekcja wykona się ZAWSZE przy wyjściu (exit lub Ctrl+C)
        if 'union' in locals(): union.stop()
        if 'agency' in locals(): agency.stop()

if __name__ == "__main__":
    main()