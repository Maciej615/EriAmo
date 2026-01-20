#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import signal
import sys
import os

# Dodaj ścieżki
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src', 'union'))
sys.path.insert(0, os.path.join(current_dir, 'src', 'language'))
sys.path.insert(0, os.path.join(current_dir, 'src', 'music'))

from union_core import EriAmoUnion

# Globalny reference do union (dla signal handlera)
union_instance = None

def graceful_shutdown(signum, frame):
    """Handler dla Ctrl+C - zapisuje stan przed wyjściem"""
    print("\n\n[SYSTEM] 🛑 Otrzymano sygnał przerwania...")
    if union_instance:
        union_instance.stop()  # To wywoła save_all_systems()
    print("[SYSTEM] ✓ Stan zapisany. Do zobaczenia!")
    sys.exit(0)

def main():
    global union_instance
    
    # Rejestruj signal handler
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    
    # Inicjalizuj Union
    union_instance = EriAmoUnion(verbose=True, use_unified_memory=True)
    union_instance.start()
    
    print("\n[INFO] Podróżniczka żyje i słucha.")
    print("[INFO] Pisz w każdej chwili. Naciśnij Ctrl+C, aby zakończyć.\n")
    
    try:
        while True:
            try:
                cmd = input("Ty > ")
                
                if not cmd.strip():
                    continue
                    
                if cmd.lower() in ['exit', 'quit', 'wyjście']:
                    break
                
                union_instance.process_input(cmd)
                
            except EOFError:
                # EOF (Ctrl+D) też powinien zapisać
                break
                
    except KeyboardInterrupt:
        # To jest backup - normalnie powinien złapać signal handler
        pass
    finally:
        # Zawsze zapisz przed wyjściem
        print("\n[SYSTEM] Zamykanie...")
        union_instance.stop()

if __name__ == "__main__":
    main()
