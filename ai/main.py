#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Model Kuli Rzeczywistości (EriAmo) - Controller v5.0
import sys
import re
import numpy as np
from config import Colors, EMOCJE
from ui import FancyUI
from aii import AII

def main():
    try: import colorama; colorama.init()
    except: pass

    ui = FancyUI()
    ui.print_animated_text("--- EriAmo v5.0.2 (Critical Fix) ---", Colors.BOLD+Colors.WHITE, 0.02)
    ui.show_planet_scan("Inicjalizuję Neuronowy Leksykon...", 1.5, Colors.CYAN)

    ai = AII()
    ui.print_animated_text(f"[AII] Gotowy. Energia: {ai.energy}%.", Colors.GREEN, 0.02)
    
    print(f"\n{Colors.FAINT}Komendy: /teach, /axiom, /status, /lexicon, /word, /debug, /conscience, /commandment [1-10], /reset{Colors.RESET}")

    try:
        while ai.running:
            try: prompt = input(f"\n{Colors.BOLD}> {Colors.RESET}").strip()
            except: break
            if not prompt: continue
            
            low = prompt.lower()
            
            if low in ["/exit", "/quit"]: ai.stop(); break
            if low == "/save": ai.save_knowledge(); print(f"{Colors.GREEN}Zapisano.{Colors.RESET}"); continue
            if low == "/sleep": ai._sleep(); continue
            if low == "/lexicon": ai.show_lexicon_stats(); continue
            if low == "/axioms": ai.list_axioms(); continue
            
            # RESET - usuwa duszę i leksykon, wymaga potwierdzenia
            if low == "/reset":
                print(f"{Colors.RED}⚠️  UWAGA: To usunie całą duszę i leksykon!{Colors.RESET}")
                confirm = input("Wpisz 'TAK' aby potwierdzić: ").strip()
                if confirm == "TAK":
                    import os
                    try:
                        if os.path.exists("eriamo.soul"): os.remove("eriamo.soul")
                        if os.path.exists("lexicon.soul"): os.remove("lexicon.soul")
                        print(f"{Colors.GREEN}✓ Dusza i leksykon usunięte. Uruchom genesis.py{Colors.RESET}")
                        ai.running = False
                        break
                    except Exception as e:
                        print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
                else:
                    print("Reset anulowany.")
                continue
            
            # [FIX] Naprawiona komenda /soul - teraz wyświetla dane
            if low == "/soul": 
                print(ai.introspect())
                continue
            
            # SUMIENIE - Status i przykazania
            if low == "/conscience":
                ai.show_conscience_status()
                continue
            
            # Wyjaśnienie konkretnego przykazania
            cm = re.match(r"^/commandment\s+(\d+)", prompt, re.IGNORECASE)
            if cm:
                ai.explain_commandment(cm.group(1))
                continue
            
            if low == "/status":
                st = ai.get_soul_status()
                print(f"{Colors.YELLOW}--- STATUS v{st['version']} ---")
                print(f"  Energia: {st['energy']}% | Emocja: {st['emotion']}")
                print(f"  Pamięć: {st['memories']} (RAM) | Aksjomaty: {st['axioms']}")
                print(f"  Byt (Masa): {st['radius']:.4f}")
                print(f"  Pęd: {st['dominant_sector']} ({st['dominant_value']:.2f})")
                print(f"{Colors.RESET}", end="")
                print(ai.introspect())
                continue

            # Word inspect
            wm = re.match(r"^/word\s+(.+)", prompt, re.IGNORECASE)
            if wm: ai.inspect_word(wm.group(1)); continue
            
            # DEBUG: Sprawdź jak system widzi zdanie
            dm = re.match(r"^/debug\s+(.+)", prompt, re.IGNORECASE)
            if dm: 
                text = dm.group(1)
                vec, sector, unknown = ai.lexicon.analyze_text(text, enable_reinforcement=False)
                print(f"{Colors.CYAN}[DEBUG] '{text}'{Colors.RESET}")
                print(f"  Wektor (norma={np.linalg.norm(vec):.3f}):")
                for i, axis in enumerate(ai.AXES_ORDER):
                    if vec[i] > 0.01:
                        bar = "█" * int(vec[i] * 20)
                        print(f"    {axis:12} {bar} {vec[i]:.3f}")
                print(f"  Dominanta: {sector}")
                print(f"  Nieznane: {unknown}")
                continue
            
            # Manual teach word
            tw = re.match(r"^/teachword\s+(\w+)\s+(\w+)", prompt, re.IGNORECASE)
            if tw: ai.teach_word(tw.group(1), tw.group(2)); continue

            # Challenge
            cm = re.match(r"^/challenge\s+(Def_\d+)\s+(.+)", prompt, re.IGNORECASE)
            if cm: ai.challenge_belief(cm.group(1), cm.group(2)); continue

            # Teach / Axiom
            tm = re.match(r"^/(teach|axiom)\s+(\[.*?\]|\w+)\s+(.+)", prompt, re.IGNORECASE)
            if tm:
                mode, tag, content = tm.groups()
                tag = tag.replace("[","").replace("]","")
                ai.teach(tag, content, is_axiom=(mode.lower()=="axiom"))
                continue

            # Chat
            ai.prompt(prompt)

    except KeyboardInterrupt:
        ai.stop()

if __name__ == "__main__":
    main()