#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# Model Kuli Rzeczywistości (Sfera Rzeczywistości)
# Copyright (C) 2025 Maciej A. Mazur
# Licencja: GNU General Public License v3.0 (GPLv3)
#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import sys
import time
import numpy as np
import json
import os
import threading
import hashlib
import random
import re
from numpy.linalg import norm

# --- STAŁE FILTRA ONTOLOGICZNEGO ---
ONTOLOGICAL_THRESHOLD = 0.98 # Filtr Ontologiczny: >0.98 dla redundancji
VECTOR_DIM = 8

# --- KOLORY ---

class Colors:
    GREEN = "\033[32m"; YELLOW = "\033[33m"; RED = "\033[31m"
    CYAN = "\033[36m"; MAGENTA = "\033[35m"; PINK = "\033[95m"
    BLUE = "\033[34m"; WHITE = "\033[37m"; BOLD = "\033[1m"
    RESET = "\033[0m"

# --- EMOCJE (polskie napisy) ---

EMOCJE = {
    "radość": {"kolor": Colors.GREEN, "ikona": "[RADOŚĆ]", "energia": +10, "modulator": 0.1},
    "złość": {"kolor": Colors.RED, "ikona": "[ZŁOŚĆ]", "energia": -15, "modulator": -0.2},
    "smutek": {"kolor": Colors.BLUE, "ikona": "[SMUTEK]", "energia": -20, "modulator": -0.15},
    "strach": {"kolor": Colors.MAGENTA, "ikona": "[STRACH]", "energia": -10, "modulator": -0.1},
    "miłość": {"kolor": Colors.PINK, "ikona": "[MIŁOŚĆ]", "energia": +15, "modulator": 0.2},
    "zdziwienie": {"kolor": Colors.YELLOW, "ikona": "[ZASKOCZENIE]","energia": +5, "modulator": 0.05},
    "neutralna": {"kolor": Colors.WHITE, "ikona": "[MYŚL]", "energia": 0, "modulator": 0.0}
}

# ------------------------------------------------------------------ #
# FUNKCJE WEKTOROWE I FILTRACJA
# ------------------------------------------------------------------ #

def fast_cosine_similarity(vec_a, vec_b):
    """Oblicza podobieństwo cosinusowe."""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = norm(vec_a) 
    norm_b = norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def _modulate_vector_by_emotion(vec: np.ndarray, emocja: str) -> np.ndarray:
    """Moduluje wektor kontekstu w zależności od osi emocjonalnej.
    Wspomnienia zyskują kierunek w przestrzeni wektorowej emocji.
    """
    if emocja not in EMOCJE:
        return vec.copy()
    
    mod = EMOCJE[emocja]['modulator']
    
    # Prosta modulacja: Radość/Miłość zwiększają skalę i kierunek, Złość/Smutek zmniejszają
    # Używamy np. prostej osi: pierwsze 4 wymiary dla pozytywnego, drugie 4 dla negatywnego
    mod_vec = vec.copy()
    
    # Pozytywna emocja: wzmacniamy pierwsze 4 wymiary
    if mod > 0:
        mod_vec[:4] = np.clip(mod_vec[:4] + mod, 0.0, 1.0)
    # Negatywna emocja: wzmacniamy drugie 4 wymiary
    elif mod < 0:
        mod_vec[4:] = np.clip(mod_vec[4:] + abs(mod), 0.0, 1.0)
        
    # Ponowna normalizacja po modulacji
    norm_mod = norm(mod_vec)
    if norm_mod == 0:
        return mod_vec
    return mod_vec / norm_mod

# --- AII Z EMOCJAMI ---

class AII:
    def __init__(self):
        self.D_Map = {}
        self.H_log = []
        self.energy = 100
        self.load = 0
        self.status = "myślę"
        self.emocja = "neutralna"
        self.sleep_interval = 300 # sekund między cyklami snu
        self.running = True
        self.prompts_since_sleep = 0
        self.max_sleep_time = 2.0
        self.max_hlog = 1000
        self.F_will = 0.5
        self.ostatnie_slowa = []
        self.load_knowledge()
        self.start_sleep_cycle()

    # ------------------------------------------------------------------ #
    # WEKTORY – Z NORMALIZACJĄ!
    # ------------------------------------------------------------------ #
    def _vector_from_text(self, text):
        text = text.lower()
        # Usuń znaki niealfanumeryczne (oprócz spacji)
        text = ''.join(c for c in text if c.isalnum() or c in " ")
        text = text.strip()
        if not text:
            text = "pusto"
        
        # Używamy MD5 i bierzemy 8 elementów
        h = hashlib.md5(text.encode()).hexdigest()
        vals = [int(h[i:i+2], 16) / 255.0 for i in range(0, VECTOR_DIM * 2, 2)]
        vec = np.array(vals, dtype=float)
        
        norm_val = np.linalg.norm(vec)
        if norm_val == 0:
            return vec
        return vec / norm_val # normalizacja do wektora jednostkowego

    # ------------------------------------------------------------------ #
    # ZAPIS / ODCZYT
    # ------------------------------------------------------------------ #
    def save_knowledge(self):
        os.makedirs("data", exist_ok=True)
        serial = {k: {
            'wektor_C_Def': v['wektor_C_Def'].tolist(),
            'waga_Ww': float(v['waga_Ww']),
            'tagi': v['tagi']
        } for k, v in self.D_Map.items()}
        with open("data/D_Map.json", "w", encoding="utf-8") as f:
            json.dump(serial, f, indent=2, ensure_ascii=False)
            
        # Zapis H_log z wektorami jako listy
        h_log_serial = [{'h_vector': exp['h_vector'].tolist() if isinstance(exp['h_vector'], np.ndarray) else exp['h_vector'], 
                         'tresc': exp['tresc'], 
                         'emocja': exp.get('emocja', 'neutralna')} 
                        for exp in self.H_log[-self.max_hlog:]]
        
        with open("data/H_log.json", "w", encoding="utf-8") as f:
            json.dump(h_log_serial, f, indent=2, ensure_ascii=False)

    def load_knowledge(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/D_Map.json", encoding="utf-8") as f:
                data = json.load(f)
                self.D_Map = {k: {
                    'wektor_C_Def': np.array(v['wektor_C_Def'], dtype=float),
                    'waga_Ww': float(v['waga_Ww']),
                    'tagi': v['tagi']
                } for k, v in data.items()}
        except Exception:
            self.D_Map = {}
            
        try:
            with open("data/H_log.json", encoding="utf-8") as f:
                loaded_h_log = json.load(f)
                # Konwersja wektorów z powrotem na numpy.ndarray
                self.H_log = [{'h_vector': np.array(exp['h_vector'], dtype=float), 
                               'tresc': exp['tresc'], 
                               'emocja': exp.get('emocja', 'neutralna')} 
                              for exp in loaded_h_log]
        except Exception:
            self.H_log = []

    # ------------------------------------------------------------------ #
    # CYKL SNU – Wektoryzacja i Kompresja Ontologiczna
    # ------------------------------------------------------------------ #
    def start_sleep_cycle(self):
        def cycle():
            while self.running:
                time.sleep(self.sleep_interval)
                if not self.running: break
                self._sleep()
        threading.Thread(target=cycle, daemon=True).start()

    def _sleep(self):
        self.status = "śpię"
        print(f"\n{Colors.CYAN}[AII] Sen: marzę o {random.choice(list(EMOCJE.keys()))}...{Colors.RESET}")
        start = time.time()
        
        # Wzmocnienie D_Map (stara logika wzmacniania)
        processed_reinforce = 0
        for exp in self.H_log[-10:]: # Bierzemy tylko ostatnie 10
            if time.time() - start > self.max_sleep_time * 0.5: break # Max 50% czasu na wzmocnienie
            
            tresc = exp.get('tresc', '').lower()
            słowa_kluczowe = set(tresc.split())
            
            for d in self.D_Map.values():
                wzmocnione = False
                for tag in d.get('tagi', []):
                    if tag in słowa_kluczowe: 
                        d['waga_Ww'] = min(d['waga_Ww'] + 1.0, 100.0)
                        processed_reinforce += 1
                        wzmocnione = True
                        break
                if wzmocnione: continue

        # Kompresja Ontologiczna (nowa, kluczowa mechanika)
        history_to_keep = []
        compressed_count = 0
        
        for exp in self.H_log:
            if time.time() - start > self.max_sleep_time: break # Ograniczenie czasowe na całą operację
            
            is_redundant = False
            h_vec = exp['h_vector'] # Wektor z historii
            
            if len(self.D_Map) > 0:
                for d in self.D_Map.values():
                    d_vec = d['wektor_C_Def']
                    
                    # Obliczanie podobieństwa wektorowego (Filtr Ontologiczny)
                    correlation = fast_cosine_similarity(h_vec, d_vec)

                    if correlation > ONTOLOGICAL_THRESHOLD: 
                        # WIEDZA REDUNDANTNA! Została już wchłonięta do D_Map lub jest zbyt podobna.
                        is_redundant = True
                        compressed_count += 1
                        break

            if not is_redundant:
                history_to_keep.append(exp)
        
        self.H_log = history_to_keep
        
        self.energy = min(100, self.energy + 15) # Odzyskiwanie energii
        self.save_knowledge()
        self.status = "myślę"
        self.prompts_since_sleep = 0
        print(f"{Colors.GREEN}[AII] Obudzony! Wzmocnień: {processed_reinforce}, Kompresja: {compressed_count}. H_log: {len(self.H_log)} (+15% energii){Colors.RESET}\n")

    # ------------------------------------------------------------------ #
    # CYKL PRACY
    # ------------------------------------------------------------------ #
    def cycle(self):
        self.load = int(np.random.randint(30, 70))
        if self.status != "śpię":
            drop = int(np.random.randint(0, 4)) if self.energy > 50 else int(np.random.randint(1, 6))
            self.energy = max(0, self.energy - drop)
        if self.energy == 0 or self.prompts_since_sleep > 5:
            self.status = "zmęczony"
        return "C", self.load, self.energy

    # ------------------------------------------------------------------ #
    # NAUCZANIE – Emocjonalne Wektoryzowanie Kontekstu
    # ------------------------------------------------------------------ #
    def teach(self, tag, tresc):
        vec_base = self._vector_from_text(tresc)
        
        # Emocja nauczania to 'miłość'
        emocja_nauczania = "miłość"
        vec_emocjonalny = _modulate_vector_by_emotion(vec_base, emocja_nauczania)
        
        def_id = f"Def_{len(self.D_Map)+1:03d}"
        
        # Wytnij znaki interpunkcyjne z tagów
        words = [re.sub(r'[^\w]', '', w) for w in tresc.lower().split()]
        all_tags = [tag.lower()] + [w for w in words if w]
        
        # Unikamy duplikatów
        seen = set()
        all_tags = [t for t in all_tags if t not in seen and not seen.add(t)]
        
        self.D_Map[def_id] = {'wektor_C_Def': vec_emocjonalny, 'waga_Ww': 5.0 + EMOCJE[emocja_nauczania]['modulator'] * 20, 'tagi': all_tags}
        
        # Zapisujemy Wektor Emocjonalny do historii
        self.H_log.append({'h_vector': vec_emocjonalny, 'tresc': tresc, 'emocja': emocja_nauczania})
        
        self.save_knowledge()
        print(f"{Colors.GREEN}{Colors.BOLD}[NAUCZONO] {def_id} ({EMOCJE[emocja_nauczania]['ikona']}) → \"{tresc}\" (tagi: {', '.join(all_tags[:5])}){Colors.RESET}")


    def forget(self, tag):
        removed = sum(1 for k, v in list(self.D_Map.items()) if tag in v['tagi'])
        self.D_Map = {k: v for k, v in self.D_Map.items() if tag not in v['tagi']}
        self.save_knowledge()
        print(f"{Colors.YELLOW}[ZAPOMNIANO] Usunięto {removed} definicji z tagiem: {tag}{Colors.RESET}")

    # ------------------------------------------------------------------ #
    # DODATKI
    # ------------------------------------------------------------------ #
    def kawa(self):
        self.energy = min(100, self.energy + 50)
        self.emocja = "radość"
        print(f"{Colors.YELLOW}☕ [KAWA] +50 energii! EN: {self.energy}%. Emocja: {self.emocja}{Colors.RESET}")

    def odpocznij(self):
        print(f"{Colors.CYAN}AI wymusza sen...{Colors.RESET}")
        self._sleep()

    def marzenie(self):
        if len(self.D_Map) < 2:
            print(f"{Colors.MAGENTA}[MARZENIE] Za mało wspomnień...{Colors.RESET}"); return
        
        # Generowanie Marzenia na podstawie dwóch losowych wektorów
        items = list(self.D_Map.items())
        d1, d2 = random.sample(items, 2)
        
        tag1, tag2 = d1[1]['tagi'][0], d2[1]['tagi'][0]
        
        # Tworzymy wektor "marzenia" jako prostą sumę/różnicę
        vec_marzenie = (d1[1]['wektor_C_Def'] + d2[1]['wektor_C_Def']) / 2
        
        # Obliczamy jego ogólny kierunek emocjonalny
        emocja_marzenia = random.choice(list(EMOCJE.keys()))
        
        marzenie = f"Połączenie '{tag1}' i '{tag2}' tworzy {emocja_marzenia}."
        print(f"{Colors.MAGENTA}✨ {EMOCJE[emocja_marzenia]['ikona']} [MARZENIE] {marzenie}{Colors.RESET}")

    def get_tags(self):
        tags = set()
        for d in self.D_Map.values():
            tags.update(d['tagi'])
        return sorted(tags)

    # ------------------------------------------------------------------ #
    # ODPOWIEDŹ – Konstrukcja Myśli i Wyszukiwanie Kontekstu
    # ------------------------------------------------------------------ #
    def generate_response(self, prompt):
        self.prompts_since_sleep += 1
        
        # 1. BAZOWY WEKTOR PROMPTU
        vec_base = self._vector_from_text(prompt)
        
        # 2. DETEKCJA TAGU / EMOCJI JAWNEJ
        words = set(re.sub(r'[^\w\s]', '', prompt.lower()).split())
        detected_tag = None
        best_match = None
        max_weight = 0
        current_emocja = "neutralna"

        for did, d in self.D_Map.items():
            for tag in d['tagi']:
                if tag in words:
                    # Wzmocnienie wagi przy użyciu
                    d['waga_Ww'] = min(d['waga_Ww'] + 0.5, 100)
                    if d['waga_Ww'] > max_weight:
                        max_weight = d['waga_Ww']
                        best_match = (did, tag)
                        detected_tag = tag

        # 3. MODULACJA EMOCJONALNA WEKTORA F
        
        # Prosta reguła emocjonalna na podstawie wykrytego tagu
        if detected_tag in ["złość", "strach", "smutek"]:
            current_emocja = detected_tag
        elif detected_tag == "miłość":
            current_emocja = "miłość"
        else:
            # Używamy randomowej emocji, jeśli AI jest naładowana lub zmęczona
            if self.status == "zmęczony":
                 current_emocja = "smutek"
            elif self.energy > 80 and not detected_tag:
                 current_emocja = random.choice(["radość", "zdziwienie"])
        
        vec_emocjonalny = _modulate_vector_by_emotion(vec_base, current_emocja)
        self.emocja = current_emocja
        
        # 4. ZAPIS WSPOMNIENIA (Wektor Emocjonalny ląduje w historii)
        self.H_log.append({'h_vector': vec_emocjonalny, 'tresc': prompt, 'emocja': current_emocja})
        
        # 5. EKSTRAKCJA NOWYCH SŁÓW (PAMIĘĆ BIEŻĄCA)
        known_words = self.get_tags()
        new_words = list(words - set(known_words))
        
        # 6. KONSTRUKCJA MYŚLI
        
        if self.status == "zmęczony" and not detected_tag:
            odpowiedz = f"({EMOCJE[self.emocja]['ikona']}) Jestem wyczerpany. Potrzebuję odpoczynku. Spróbuj !odpocznij."
        elif detected_tag:
            # ODPOWIEDŹ Z JAWNEGO TAGU
            waga = self.D_Map[best_match[0]]['waga_Ww']
            odpowiedz = f"{EMOCJE[self.emocja]['ikona']} Rozpoznano '{detected_tag}' (Waga: {waga:.1f}). Kontynuuję ten kontekst."
        else:
            # WYSZUKIWANIE KONTEKSTOWE (Trójkąty Wspomnień)
            odpowiedz = None
            if self.D_Map:
                sims = [(did, fast_cosine_similarity(d['wektor_C_Def'], vec_emocjonalny)) for did, d in self.D_Map.items()]
                if sims:
                    best_did, score = max(sims, key=lambda x: x[1])
                    
                    if score > 0.70: # Próg kontekstowy
                        best_d = self.D_Map[best_did]
                        tag = best_d['tagi'][0]
                        odpowiedz = f"{EMOCJE[self.emocja]['ikona']} Twoja myśl rezonuje (Korelacja: {score:.2f}) ze wspomnieniem o '{tag}'."
            
            # PAMIĘĆ BIEŻĄCA / AUTOTAGOWANIE
            if odpowiedz is None:
                if new_words:
                    nowy_wyraz = random.choice(new_words)
                    self.teach(f"auto_{nowy_wyraz}", prompt) # Autotaguj
                    odpowiedz = f"{EMOCJE['zdziwienie']['ikona']} Zapisuję nowy wyraz '{nowy_wyraz}' do słownika. AI się uczy."
                else:
                    odpowiedz = f"{EMOCJE[self.emocja]['ikona']} Interesujące. Przetwarzam nieznany kontekst. Co o tym sądzisz?"

        self.save_knowledge()
        return odpowiedz, self.emocja
# ------------------------------------------------------------------ #
# INTERFEJS
# ------------------------------------------------------------------ #
def display_heatmap(D_Map):
    if not D_Map: print(f"{Colors.YELLOW}(pusto){Colors.RESET}"); return
    print(f"\n{Colors.MAGENTA}[MAPA CIEPŁA WAG]{Colors.RESET}")
    for did, d in sorted(D_Map.items(), key=lambda x: x[1]['waga_Ww'], reverse=True)[:10]:
        bar = "█" * min(int(d['waga_Ww'] / 6.66), 15) # Skalowanie do 15
        tag = d['tagi'][0] if d['tagi'] else "brak"
        print(f"{did:8} [{Colors.RED}{bar:<15}{Colors.RESET}] W:{d['waga_Ww']:4.1f} | {tag}")

def display_memory_status(core):
    tags_count = len(core.get_tags())
    print(f"\n{Colors.BOLD}--- STATUS PAMIĘCI ---{Colors.RESET}")
    print(f"Definicji (D_Map): {len(core.D_Map)} | Wektor Histori (H_log): {len(core.H_log)} | Unikalnych Tagów: {tags_count}")
    print(f"Całkowita Waga: {sum(d['waga_Ww'] for d in core.D_Map.values()):.1f}")
    
    display_heatmap(core.D_Map)
    
    print(f"\n{Colors.CYAN}[OSTATNIE 5 WSPOMNIEŃ Z H_log]{Colors.RESET}")
    for exp in core.H_log[-5:]:
        # Wizualizacja wektora
        bar = ''.join('█' if v > 0.5 else '░' for v in exp['h_vector'])
        short = (exp['tresc'][:27] + '...') if len(exp['tresc']) > 27 else exp['tresc']
        emocja_tag = EMOCJE.get(exp['emocja'], EMOCJE['neutralna'])['ikona']
        print(f"  {emocja_tag} {short:<27} | {bar}")


def retro_terminal_interface():
    core = AII()
    dots = ["", ".", "..", "...", "....", "....."]
    pulse = ["−", "\\", "|", "/"]

    print(f"{Colors.GREEN}{Colors.BOLD}═" * 78)
    print("   TERMINAL AII v3.9 – EMOCJONALNY WEKTOR PAMIĘCI I FILTR ONTOLOGICZNY")
    print("═" * 78 + Colors.RESET)
    print(f"{Colors.YELLOW}Komendy: !naucz TAG TREŚĆ, !zapomnij TAG, !kawa, !odpocznij, !marzenie, !tagi, !status, exit.{Colors.RESET}")

    try:
        while True:
            core.cycle() # Aktualizacja energii
            status_color = {"myślę": Colors.GREEN, "śpię": Colors.CYAN, "zmęczony": Colors.RED}.get(core.status, Colors.YELLOW)
            
            prompt = input(f"\nPROMPT> [{status_color}{core.status}{Colors.RESET} | EN:{core.energy:3d}% OB:{core.load:3d}%] ")

            if prompt.lower() in ["exit", "quit", "q"]:
                core.running = False
                core.save_knowledge()
                print(f"\n{Colors.RED}--- AII WYŁĄCZONY – do widzenia. ---{Colors.RESET}")
                break

            # --- KOMENDY ---
            if prompt.startswith("!naucz "):
                rest = prompt[7:].strip()
                if not rest: print(f"{Colors.RED}Użycie: !naucz TAG TREŚĆ{Colors.RESET}"); continue
                parts = rest.split(" ", 1)
                tag, tresc = parts[0], parts[1] if len(parts) > 1 else parts[0]
                core.teach(tag, tresc)
                continue
            if prompt.startswith("!zapomnij "):
                tag = prompt.split(maxsplit=1)[1]
                core.forget(tag)
                continue
            if prompt == "!kawa":
                core.kawa()
                continue
            if prompt == "!odpocznij":
                core.odpocznij()
                continue
            if prompt == "!marzenie":
                core.marzenie()
                continue
            if prompt == "!tagi":
                tags = core.get_tags()
                print(f"{Colors.CYAN}Dostępne tagi: {', '.join(tags) if tags else 'brak'}{Colors.RESET}")
                continue
            if prompt == "!status":
                display_memory_status(core)
                continue
            
            # Zapobiegnięcie przetwarzaniu w trakcie snu
            if core.status == "śpię":
                print(f"{Colors.CYAN}AI jest w trakcie snu, proszę czekać.{Colors.RESET}"); continue

            # --- MYŚLENIE ---
            for i in range(6):
                mode, load, energy = core.cycle()
                sys.stdout.write(f"\r{mode} | EN:{energy:3d}% OB:{load:3d}% {dots[i]} {pulse[i%4]}")
                sys.stdout.flush()
                time.sleep(0.15)

            odpowiedz, emocja = core.generate_response(prompt)
            color = EMOCJE.get(emocja, EMOCJE['neutralna'])['kolor']
            
            # Wypisanie odpowiedzi
            sys.stdout.write("\r" + " " * 78) # Wyczyść linię myślenia
            print(f"\rODPOWIEDŹ ({color}{emocja.upper()}{Colors.RESET})> {odpowiedz}")
            display_memory_status(core)

    except KeyboardInterrupt:
        core.running = False
        core.save_knowledge()
        print(f"\n{Colors.RED}--- AII WYŁĄCZONY – do widzenia. ---{Colors.RESET}")

if __name__ == "__main__":
    retro_terminal_interface()
