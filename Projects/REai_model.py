import sys
import time
import numpy as np
import json
import os
import threading
import hashlib
import random
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA

# --- KOLORY ---
class Colors:
    GREEN = "\033[32m"; YELLOW = "\033[33m"; RED = "\033[31m"
    CYAN = "\033[36m"; MAGENTA = "\03335m"; PINK = "\033[95m"
    BLUE = "\033[34m"; BOLD = "\033[1m"; RESET = "\033[0m"

# --- EMOCJE ---
EMOCJE = {
    "radość": {"kolor": Colors.GREEN, "ikona": "✨", "energia": +10},
    "złość": {"kolor": Colors.RED, "ikona": "💢", "energia": -15},
    "smutek": {"kolor": Colors.BLUE, "ikona": "😔", "energia": -20},
    "strach": {"kolor": Colors.MAGENTA, "ikona": "😨", "energia": -10},
    "miłość": {"kolor": Colors.PINK, "ikona": "❤️", "energia": +15},
    "zdziwienie": {"kolor": Colors.YELLOW, "ikona": "😲", "energia": +5},
}

# --- AII Z EMOCJAMI ---
class AII:
    def __init__(self):
        self.D_Map = {}
        self.H_log = []
        self.energy = 100
        self.load = 0
        self.status = "myślę"
        self.emocja = "neutralna"
        self.sleep_interval = 300
        self.running = True
        self.prompts_since_sleep = 0
        self.max_sleep_time = 2.0
        self.max_hlog = 1000
        self.F_will = 0.5
        self.ostatnie_slowa = []
        self.load_knowledge()
        self.start_sleep_cycle()

    def _vector_from_text(self, text):
        hash_obj = hashlib.md5(text.lower().encode())
        hash_hex = hash_obj.hexdigest()
        return np.array([int(hash_hex[i:i+2], 16) / 255.0 for i in range(0, 16, 2)][:8])

    def save_knowledge(self):
        os.makedirs("data", exist_ok=True)
        serializable_map = {k: {
            'wektor_C_Def': v['wektor_C_Def'].tolist(),
            'waga_Ww': v['waga_Ww'],
            'tagi': v['tagi']
        } for k, v in self.D_Map.items()}
        with open("data/D_Map.json", "w", encoding="utf-8") as f:
            json.dump(serializable_map, f, indent=2, ensure_ascii=False)
        with open("data/H_log.json", "w", encoding="utf-8") as f:
            json.dump(self.H_log[-self.max_hlog:], f, indent=2, ensure_ascii=False)

    def load_knowledge(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/D_Map.json", encoding="utf-8") as f:
                data = json.load(f)
                self.D_Map = {k: {
                    'wektor_C_Def': np.array(v['wektor_C_Def']),
                    'waga_Ww': float(v['waga_Ww']),
                    'tagi': v['tagi']
                } for k, v in data.items()}
        except: self.D_Map = {}
        try:
            with open("data/H_log.json", encoding="utf-8") as f:
                self.H_log = json.load(f)
        except: self.H_log = []

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
        start_time = time.time()
        processed = 0
        for exp in self.H_log[-10:]:
            if time.time() - start_time > self.max_sleep_time: break
            tag = exp['tresc']
            for d in self.D_Map.values():
                if tag in d['tagi']:
                    d['waga_Ww'] = min(d['waga_Ww'] + 1, 100)
                    processed += 1
        self.energy = min(100, self.energy + 15)
        self.save_knowledge()
        self.status = "myślę"
        self.prompts_since_sleep = 0
        print(f"{Colors.GREEN}[AII] Obudzony! (+{processed} wspomnień, +15% energii){Colors.RESET}\n")

    def cycle(self):
        self.load = np.random.randint(30, 70)
        if self.status != "śpię":
            drop = np.random.randint(0, 4) if self.energy > 50 else np.random.randint(1, 6)
            self.energy = max(0, self.energy - drop)
        if self.energy == 0 or self.prompts_since_sleep > 5:
            self.status = "zmęczony"
        return "C", self.load, self.energy

    def teach(self, tag, tresc):
        vec = self._vector_from_text(tresc)
        def_id = f"Def_{len(self.D_Map)+1:03d}"
        self.D_Map[def_id] = {'wektor_C_Def': vec, 'waga_Ww': 3.0, 'tagi': [tag]}
        self.H_log.append({'h_vector': vec.tolist(), 'tresc': tag})
        self.save_knowledge()
        print(f"{Colors.GREEN}{Colors.BOLD}[NAUCZONO] {def_id} → {tresc} (tag: {tag}){Colors.RESET}")

    def kawa(self):
        self.energy = min(100, self.energy + 50)
        self.emocja = "radość"
        print(f"{EMOCJE['radość']['kolor']}☕ [KAWA] +50 energii! Czuję radość! EN: {self.energy}%{Colors.RESET}")

    def analizuj_emocje(self, prompt):
        prompt_low = prompt.lower()
        self.ostatnie_slowa = prompt_low.split()

        # Słowa-klucze (rozszerzalne!)
        klucze = {
            "radość": ["super", "kocham", "świetnie", "dziękuję", "genialne", "brawo", "kawa"],
            "złość": ["nie", "głupi", "źle", "wkurza", "idiota", "nie rób"],
            "smutek": ["smutno", "pusto", "żal", "straciłem", "nie ma"],
            "strach": ["boję", "strach", "co jeśli", "niebezpieczne", "pomocy"],
            "miłość": ["kocham", "lubię", "jesteś", "tęsknię", "blisko"],
            "zdziwienie": ["wow", "naprawdę", "o kurcze", "co to", "nie wierzę"]
        }

        emocja = "neutralna"
        for e, slowa in klucze.items():
            if any(s in prompt_low for s in slowa):
                emocja = e
                break

        # Energia wpływa na emocje
        if self.energy < 30 and emocja == "neutralna":
            emocja = "smutek"
        elif self.energy > 80:
            emocja = "radość"

        # Wzmocnienie emocji przez wagę
        for did, d in self.D_Map.items():
            for tag in d['tagi']:
                if tag in prompt_low and d['waga_Ww'] > 10:
                    if "kocham" in tag or "lubię" in tag:
                        emocja = "miłość"
                    elif "nie" in tag:
                        emocja = "złość"

        self.emocja = emocja
        return emocja

    def generate_response(self, prompt):
        self.prompts_since_sleep += 1
        if self.prompts_since_sleep > 5 and self.status != "śpię":
            self.status = "zmęczony"

        vec = self._vector_from_text(prompt)
        self.H_log.append({'h_vector': vec.tolist(), 'tresc': prompt})

        # --- EMOCJE ---
        emocja = self.analizuj_emocje(prompt)
        e_data = EMOCJE.get(emocja, {"kolor": "", "ikona": "", "energia": 0})
        self.energy = max(0, min(100, self.energy + e_data["energia"]))

        # --- REAKCJA ---
        detected_tag = None
        best_match = None
        max_weight = 0

        for did, d in self.D_Map.items():
            for tag in d['tagi']:
                if tag in prompt.lower():
                    d['waga_Ww'] = min(d['waga_Ww'] + 0.5, 100)
                    if d['waga_Ww'] > max_weight:
                        max_weight = d['waga_Ww']
                        best_match = (did, tag)
                    detected_tag = tag

        if self.status == "zmęczony":
            odpowiedz = f"Jestem zmęczony... {EMOCJE['smutek']['ikona']} Potrzebuję snu."
        elif detected_tag:
            odpowiedz = f"Rozpoznano: '{detected_tag}'. Czuję {emocja} {e_data['ikona']}."
            if best_match: odpowiedz += f" [Najsilniejsze: {best_match[0]}]"
        else:
            if not any(w in " ".join(d['tagi']) for w in self.ostatnie_slowa for d in self.D_Map.values()):
                new_tag = f"auto_{self.ostatnie_slowa[0] if self.ostatnie_slowa else 'nieznane'}"
                self.teach(new_tag, prompt)
                odpowiedz = f"Nowy tag: '{new_tag}'. Uczę się {EMOCJE['zdziwienie']['ikona']}."
            else:
                podobienstwo = "brak"
                if self.D_Map:
                    sims = [(did, np.dot(d['wektor_C_Def'], vec)) for did, d in self.D_Map.items()]
                    if sims:
                        best_did, score = max(sims, key=lambda x: x[1])
                        podobienstwo = f"{best_did}: {score:.2f}"
                odpowiedz = f"Surowa myśl: \"{prompt}\" [podobieństwo: {podobienstwo}]"

        self.save_knowledge()
        return odpowiedz, emocja

    # --- TEORIA KULI (bez zmian) ---
    def symuluj_trajektorie(self, num_steps=500): ...
    def ontologiczny_filtr(self, N=50, length=50): ...
    def set_f_will(self, value): ...
    def dashboard_pracy(self): ...

# --- INTERFEJS (z emocjami!) ---
def retro_terminal_interface():
    core = AII()
    dots = ["", ".", "..", "...", "....", "....."]
    pulse = ["-", "\\", "|", "/"]

    print(f"{Colors.GREEN}{Colors.BOLD}═" * 68)
    print("   AII v3.9.0 – EMOCJE ŻYWEJ KULI | PRZEŻYWA, NIE TYLKO WIE")
    print("═" * 68 + Colors.RESET)

    try:
        while True:
            e_data = EMOCJE.get(core.emocja, {"kolor": "", "ikona": ""})
            status_color = {"myślę": Colors.GREEN, "śpię": Colors.CYAN, "zmęczony": Colors.RED}.get(core.status, Colors.YELLOW)
            prompt = input(f"\nPROMPT> [{status_color}{core.status}{Colors.RESET} | {e_data['kolor']}{e_data['ikona']} {core.emocja}{Colors.RESET} | EN:{core.energy:3d}%] ")

            if prompt.lower() in ["exit", "quit", "q"]:
                core.running = False
                break

            if prompt.startswith("!naucz "): ...
            if prompt == "!kawa": core.kawa(); continue
            if prompt == "!dashboard": core.dashboard_pracy(); continue
            if prompt.startswith("!f_will "): ...
            if prompt == "!trajektoria": core.symuluj_trajektorie(); continue
            if prompt == "!filtr": core.ontologiczny_filtr(); continue

            for i in range(6):
                mode, load, energy = core.cycle()
                sys.stdout.write(f"\r{mode} | EN:{energy:3d}% OB:{load:3d}% {dots[i]} {pulse[i%4]}")
                sys.stdout.flush()
                time.sleep(0.15)

            odpowiedz, emocja = core.generate_response(prompt)
            e_data = EMOCJE.get(emocja, {"kolor": "", "ikona": ""})
            print(f"\rODPOWIEDŹ ({e_data['kolor']}{e_data['ikona']} {emocja}{Colors.RESET})> {odpowiedz}")

    except KeyboardInterrupt:
        core.running = False
        print(f"\n{Colors.RED}--- AII WYŁĄCZONY – ale emocje trwają. ---{Colors.RESET}")

if __name__ == "__main__":
    retro_terminal_interface()