# -*- coding: utf-8 -*-
"""
EriAmo Union - FINAL LAUNCHER (main.py)
Lokalizacja: /eriamo-union/main.py
"""

import sys
import os
import time

# 1. KONFIGURACJA ŚCIEŻEK
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'src', 'union'))
sys.path.append(os.path.join(current_dir, 'src', 'language'))
sys.path.append(os.path.join(current_dir, 'src', 'music'))

# 2. IMPORT MÓZGU
try:
    from union_core_v4 import EriAmoUnion
except ImportError as e:
    print(f"❌ BŁĄD KRYTYCZNY: Nie znaleziono mózgu (union_core_v4).")
    print(f"Szczegóły: {e}")
    sys.exit(1)

def main():
    print("""
    ╔════════════════════════════════════════════╗
    ║       EriAmo Union v1.3.1 (AGI)            ║
    ║       Phase 4: Awakening                   ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Inicjalizacja Unii
    union = EriAmoUnion(verbose=True)
    union.start()
    
    print("\n[INFO] Wędrowiec żyje i słucha.")
    print("[INFO] Pisz w każdej chwili. Naciśnij Ctrl+C, aby zakończyć.")
    
    try:
        while True:
            # Pobierz tekst od Ciebie
            cmd = input(f"\nTy > ")
            
            if cmd.lower() in ['exit', 'quit', 'koniec']:
                break
            
            if cmd.lower() == '/status':
                st = union.get_status()
                print(f"[STATUS] Energia: {st['energy']}% | Nuda: {st['boredom']:.1f}")
                continue
            
            # --- KLUCZOWA ZMIANA: Przekazujemy głos do mózgu ---
            # To wywoła aii.interact() i wyświetli prawdziwą odpowiedź z bazy 1111 definicji
            union.process_input(cmd)
            # ---------------------------------------------------
            
    except KeyboardInterrupt:
        print("\n\n[SYSTEM] Otrzymano sygnał zamknięcia.")
    finally:
        print("[SYSTEM] Zamykanie procesów...")
        union.stop()
        print("[SYSTEM] Dobranoc.")

if __name__ == "__main__":
    main()