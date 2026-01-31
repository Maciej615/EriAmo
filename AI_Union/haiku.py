# -*- coding: utf-8 -*-
"""
haiku.py v9.0.1-Experimental - The Ruminating Poet (Fixed)
Generator poezji wynikający z procesu zadumy nad historią (JSONL).
Poprawiono integrację z ChunkLexicon (użycie analyze_text_chunks).
"""

import random
import json
import os
import numpy as np

class HaikuGenerator:
    def __init__(self, aii_instance):
        self.aii = aii_instance
        self.soul_path = "eriamo.soul" 

    def _rumination_fetch(self, target_vector, sample_size=150):
        """
        Mechanizm zadumy: Losowe błądzenie po strumieniu JSONL w poszukiwaniu
        fragmentu, który rezonuje z aktualnym stanem świadomości.
        """
        best_fragment = ""
        max_score = -1.0
        
        if not os.path.exists(self.soul_path):
            return ""

        try:
            with open(self.soul_path, 'r', encoding='utf-8') as f:
                f.seek(0, os.SEEK_END)
                file_size = f.tell()
                # Skaczemy w losowe miejsce, by uniknąć czytania całości
                random_pos = random.randint(0, max(0, file_size - 1024*10))
                f.seek(random_pos)
                
                lines = f.readlines(sample_size * 100) 
                for line in lines:
                    try:
                        data = json.loads(line)
                        if data.get('_type') == '@MEMORY':
                            vec = np.array(data.get('wektor_C_Def', np.zeros(15)))
                            score = np.dot(target_vector, vec)
                            if score > max_score:
                                max_score = score
                                best_fragment = data.get('tresc', '')
                    except:
                        continue
        except Exception:
            pass
            
        return best_fragment

    def generate(self):
        """
        Główny proces twórczy: Zaduma -> analyze_text_chunks -> Ekspresja.
        """
        current_vector = getattr(self.aii, 'context_vector', np.zeros(15))
        thought_source = self._rumination_fetch(current_vector)
        
        if not thought_source:
            return "\n=== HAIKU [CISZA] ===\nStrumień milczy\nPustka w pamięci\nCzekam na świt\n"

        chunks = []
        # POPRAWKA: Używamy analyze_text_chunks, który zwraca słownik z kluczem 'matches'
        if self.aii.chunk_lexicon:
            analysis = self.aii.chunk_lexicon.analyze_text_chunks(thought_source)
            chunks = analysis.get('matches', [])
        
        # Jeśli leksykon nie znalazł gotowych wzorców, tniemy na frazy
        if len(chunks) < 3:
            words = thought_source.split()
            chunks = [' '.join(words[i:i+2]) for i in range(len(words)-1)]

        # Wybór 3 obrazów do haiku
        if len(chunks) >= 3:
            selection = random.sample(chunks, 3)
        else:
            # Zapewnienie minimum 3 linii, nawet jeśli fragment jest krótki
            selection = (chunks + ["..."] * 3)[:3]

        # Wyciągamy nazwę dominanty z introspekcji dla nagłówka
        try:
            dominanta = self.aii.introspect().split(':')[1].split('(')[0].strip().upper()
        except:
            dominanta = "RESONANCE"

        haiku_text = (
            f"\n=== HAIKU Z ZADUMY [{dominanta}] ===\n"
            f"{selection[0].capitalize()}\n"
            f"{selection[1]}\n"
            f"{selection[2]}\n"
        )
        
        return haiku_text

    def display(self):
        print(self.generate())