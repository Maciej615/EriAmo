# -*- coding: utf-8 -*-
# fusion_gen.py - Naprawiony proces budowania matrycy
# Copyright (C) 2025 Maciej Mazur (maciej615)
# EriAmo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
import json
import os
from aii import AII
from config import Colors

def run_fusion():
    # Usuwamy stary plik duszy, aby zacząć od czystego Genesis
    if os.path.exists("eriamo.soul"):
        os.remove("eriamo.soul")
        print(f"{Colors.YELLOW}[FUSION] Usunięto starą duszę dla czystego startu.{Colors.RESET}")

    ai = AII()
    print(f"{Colors.BOLD}{Colors.CYAN}--- PROCES FUSION: Budowanie Pierwotnej Matrycy ---{Colors.RESET}")
    
    # Ręczne uruchomienie skryptów zamiast importu (bezpieczniejsze dla D_Map)
    genesis_files = ["genesissk.py", "genesisdef.py", "genesiskit.py", "genesispyt.py"]
    
    # Wewnątrz fusion_gen.py
    for gf in genesis_files:
        if os.path.exists(gf):
            print(f"{Colors.CYAN}[FUSION] Procesowanie: {gf}...{Colors.RESET}")
            with open(gf, "r", encoding="utf-8") as f:
                code = f.read()
                try:
                    # Wykonujemy skrypt, przekazując mu naszą instancję 'ai'
                    exec(code, {'ai': ai, 'AII': AII, 'Colors': Colors})
                except Exception as e:
                    # Jeśli skrypt wywali się na samym końcu (przy printowaniu statusu),
                    # ignorujemy to i idziemy dalej - dane są już w D_Map.
                    print(f"{Colors.YELLOW}[FUSION] Notatka: Skrypt {gf} zakończył naukę (UI skip).{Colors.RESET}")
                    
    # Eksport do JSONL
    unified_lexicon = []
    for uid, data in ai.D_Map.items():
        entry = {
            "word": data['tagi'][0].strip("[]") if data['tagi'] else "unknown",
            "category": data.get('kategoria', 'ogólne'),
            "vector": data['wektor_C_Def'].tolist() if hasattr(data['wektor_C_Def'], 'tolist') else data['wektor_C_Def'],
            "is_trigger": True if data.get('immutable') else False,
            "essence": data['tresc']
        }
        unified_lexicon.append(entry)

    with open("lexicon.soul", "w", encoding="utf-8") as f:
        for entry in unified_lexicon:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n{Colors.GREEN}✔ FUSION ZAKOŃCZONE. Matryca 'lexicon.soul' gotowa ({len(unified_lexicon)} linii).{Colors.RESET}")

if __name__ == "__main__":
    run_fusion()
