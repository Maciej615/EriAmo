#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Model Kuli Rzeczywistości (EriAmo) - Controller v5.1
import sys
import re
from config import Colors, EMOCJE
from ui import FancyUI
from aii import AII

def main():
    try: import colorama; colorama.init()
    except: pass

    ui = FancyUI()
    ui.print_animated_text("--- EriAmo AGI v5.1 (Fixed) ---", Colors.BOLD+Colors.WHITE, 0.02)
    ui.show_planet_scan("Inicjalizuję Neuronowy Leksykon...", 1.5, Colors.CYAN)

    ai = AII()
    ui.print_animated_text(f"[AII] Gotowy. Energia: {ai.energy}%.", Colors.GREEN, 0.02)
    
    print(f"\n{Colors.FAINT}Komendy: /teach, /axiom, /challenge, /status, /soul, /lexicon, /word [słowo]{Colors.RESET}")

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
            
            # [FIX] Naprawiona komenda /soul - teraz wyświetla dane
            if low == "/soul": 
                print(ai.introspect())
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