#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Model Kuli Rzeczywistości (EriAmo) - Controller v5.1.0
# Z komendami dla rozszerzeń: Sen, Decay, Ciekawość
# Copyright (C) 2025 Maciej Mazur (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import sys
import re
import numpy as np
from config import Colors, EMOCJE
from ui import FancyUI
from aii import AII

def main():
    try: 
        import colorama
        colorama.init()
    except: 
        pass

    ui = FancyUI()
    ui.print_animated_text("--- EriAmo v5.1.0 (Integrated Extensions) ---", Colors.BOLD+Colors.WHITE, 0.02)
    ui.show_planet_scan("Inicjalizuję Neuronowy Leksykon...", 1.5, Colors.CYAN)

    ai = AII()
    ui.print_animated_text(f"[AII] Gotowy. Energia: {ai.energy}%.", Colors.GREEN, 0.02)
    
    print(f"\n{Colors.FAINT}Komendy podstawowe:{Colors.RESET}")
    print(f"{Colors.FAINT}  /teach, /axiom, /status, /lexicon, /word, /debug, /conscience, /commandment [1-10], /reset{Colors.RESET}")
    print(f"\n{Colors.CYAN}Komendy rozszerzeń:{Colors.RESET}")
    print(f"{Colors.CYAN}  /extensions - status rozszerzeń (sen, decay, ciekawość){Colors.RESET}")
    print(f"{Colors.CYAN}  /sleep      - wymuś konsolidację pamięci{Colors.RESET}")
    print(f"{Colors.CYAN}  /decay [n]  - wymuś wygaszenie emocji (n cykli){Colors.RESET}")
    print(f"{Colors.CYAN}  /curiosity  - pokaż szczegóły ciekawości{Colors.RESET}")

    try:
        while ai.running:
            try: 
                prompt = input(f"\n{Colors.BOLD}> {Colors.RESET}").strip()
            except: 
                break
            if not prompt: 
                continue
            
            low = prompt.lower()
            
            # === PODSTAWOWE KOMENDY ===
            
            if low in ["/exit", "/quit"]: 
                ai.stop()
                break
            
            if low == "/save": 
                ai.save_knowledge()
                print(f"{Colors.GREEN}Zapisano.{Colors.RESET}")
                continue
            
            if low == "/lexicon": 
                ai.show_lexicon_stats()
                continue
            
            if low == "/axioms": 
                ai.list_axioms()
                continue
            
            # === KOMENDY ROZSZERZEŃ ===
            
            if low == "/extensions":
                ai.show_extensions_status()
                continue
            
            if low == "/sleep":
                print(f"{Colors.CYAN}[SEN] Wymuszam konsolidację...{Colors.RESET}")
                ai._sleep()
                continue
            
            # /decay lub /decay 5
            decay_match = re.match(r"^/decay(?:\s+(\d+))?", low)
            if decay_match:
                cycles = int(decay_match.group(1)) if decay_match.group(1) else 5
                ai.context_vector = ai.decay_system.apply_decay(ai.context_vector, cycles=cycles)
                print(f"{Colors.GREEN}[DECAY] Wygaszono emocje ({cycles} cykli).{Colors.RESET}")
                print(f"{Colors.FAINT}Nowy wektor kontekstu:{Colors.RESET}")
                for i, axis in enumerate(ai.AXES_ORDER):
                    val = ai.context_vector[i]
                    if abs(val) > 0.01:
                        axis_type = ai.decay_system.get_axis_type(axis)
                        marker = "🔻" if axis_type == 'ephemeral' else "💎"
                        print(f"  {marker} {axis:12} {val:+.3f}")
                continue
            
            if low == "/curiosity":
                curiosity = ai.curiosity_engine.compute_curiosity(ai.context_vector)
                print(f"\n{Colors.CYAN}═══ CIEKAWOŚĆ ═══{Colors.RESET}")
                print(f"  Wartość: {curiosity['value']:.1f} / 100")
                print(f"  Stan: {curiosity['description']}")
                print(f"  Rekomendacja: {curiosity['recommendation']['action']}")
                print(f"\n{Colors.YELLOW}Komponenty:{Colors.RESET}")
                print(f"  Emocjonalny: {curiosity['components']['emotional']:.1f}")
                print(f"  Wiedza: {curiosity['components']['knowledge']:.1f}")
                print(f"  Bonus znudzenia: {curiosity['components']['boredom_bonus']:.1f}")
                print(f"  Penalty odkrycia: {curiosity['components']['discovery_penalty']:.1f}")
                print(f"\n{Colors.YELLOW}Tolerancja ryzyka:{Colors.RESET} {curiosity['recommendation']['risk_tolerance']:.1f}")
                print(f"{Colors.YELLOW}Szuka nowości:{Colors.RESET} {curiosity['recommendation']['novelty_seeking']}")
                continue
        
            # RESET - usuwa duszę i leksykon
            if low == "/reset":
                print(f"{Colors.RED}⚠️  UWAGA: To usunie całą duszę i leksykon!{Colors.RESET}")
                confirm = input("Wpisz 'TAK' aby potwierdzić: ").strip()
                if confirm == "TAK":
                    import os
                    try:
                        if os.path.exists("eriamo.soul"): 
                            os.remove("eriamo.soul")
                        if os.path.exists("lexicon.soul"): 
                            os.remove("lexicon.soul")
                        print(f"{Colors.GREEN}✔ Dusza i leksykon usunięte. Uruchom genesis.py{Colors.RESET}")
                        ai.running = False
                        break
                    except Exception as e:
                        print(f"{Colors.RED}Błąd: {e}{Colors.RESET}")
                else:
                    print("Reset anulowany.")
                continue
            
            if low == "/soul": 
                print(ai.introspect())
                continue
            
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
                print(f"{Colors.YELLOW}--- STATUS v{st['version']} ---{Colors.RESET}")
                print(f"  Energia: {st['energy']}% | Emocja: {st['emotion']}")
                print(f"  Pamięć: {st['memories']} (RAM) | Aksjomaty: {st['axioms']}")
                print(f"  Byt (Masa): {st['radius']:.4f}")
                print(f"  Pęd: {st['dominant_sector']} ({st['dominant_value']:.2f})")
                print(ai.introspect())
                continue

            # Word inspect
            wm = re.match(r"^/word\s+(.+)", prompt, re.IGNORECASE)
            if wm: 
                ai.inspect_word(wm.group(1))
                continue
            
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
                        axis_type = ai.decay_system.get_axis_type(axis)
                        marker = "🔻" if axis_type == 'ephemeral' else ("💎" if axis_type == 'persistent' else "○")
                        print(f"    {marker} {axis:12} {bar} {vec[i]:.3f}")
                print(f"  Dominanta: {sector}")
                print(f"  Nieznane: {unknown}")
                
                # Pokaż też ciekawość dla tego wektora
                curiosity = ai.curiosity_engine.compute_curiosity(vec)
                print(f"  Ciekawość: {curiosity['value']:.1f} ({curiosity['description']})")
                continue
            
            # Manual teach word
            tw = re.match(r"^/teachword\s+(\w+)\s+(\w+)", prompt, re.IGNORECASE)
            if tw: 
                ai.teach_word(tw.group(1), tw.group(2))
                continue

            # Challenge
            cm = re.match(r"^/challenge\s+(Def_\d+)\s+(.+)", prompt, re.IGNORECASE)
            if cm: 
                ai.challenge_belief(cm.group(1), cm.group(2))
                continue

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
def test_creativity(ai_instance):
    """Szybki test modułów twórczych."""
    print(f"\n{Colors.CYAN}[SYSTEM] Testowanie ekspresji twórczej...{Colors.RESET}")
    ai_instance.emocja = "radość"
    ai_instance.haiku.display()             #
    ai_instance.fractals.display('mandala')  #
    import time
    time.sleep(2)

if __name__ == "__main__":
    from aii import AII
    # 1. Inicjalizacja silnika
    ai_system = AII() 
    
    # 2. Uruchomienie testu "zabijacza samotności" [cite: 2025-12-14]
    test_creativity(ai_system) 
    
    # 3. Wejście w tryb interaktywny
    main()
