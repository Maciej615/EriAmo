#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# Model Kuli Rzeczywistości (Sfera Rzeczywistości)
# Copyright (C) 2025 Maciej A. Mazur
# Licencja: GNU General Public License v3.0 (GPLv3)

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

try:
    import unidecode
except ImportError:
    print("Ostrzeżenie: Biblioteka 'unidecode' nie znaleziona. Normalizacja będzie podstawowa.")
    print("Uruchom: pip install unidecode")
    class UnidecodeMock:
        def unidecode(self, text):
            return text
    unidecode = UnidecodeMock()

# ----------------------------------------------------------------------
# --- STAŁE SYSTEMOWE, KOLORY I EMOCJE ---
# ----------------------------------------------------------------------

PRÓG_ONTOLOGICZNY = 0.98 
WYMIAR_WEKTORA = 8 # Wymiar Krajobrazu P (8 Osie)

class Kolory:
    ZIELONY = "\033[32m"; ŻÓŁTY = "\033[33m"; CZERWONY = "\033[31m"
    CYAN = "\033[36m"; MAGENTA = "\033[35m"; RÓŻOWY = "\033[95m"
    NIEBIESKI = "\033[34m"; BIAŁY = "\033[37m"; POGRUBIONY = "\033[1m"
    RESET = "\033[0m"; MIGANIE = "\033[5m"; BLADY = "\033[2m"

EMOCJE = {
    "radość": {"kolor": Kolory.ZIELONY, "ikona": "😊", "energia": +10, "modulator": 0.15},
    "złość": {"kolor": Kolory.CZERWONY, "ikona": "😡", "energia": -15, "modulator": -0.15},
    "smutek": {"kolor": Kolory.NIEBIESKI, "ikona": "😢", "energia": -20, "modulator": -0.1},
    "strach": {"kolor": Kolory.MAGENTA, "ikona": "😨", "energia": -10, "modulator": -0.05},
    "miłość": {"kolor": Kolory.RÓŻOWY, "ikona": "❤️", "energia": +15, "modulator": 0.2},
    "zdziwienie": {"kolor": Kolory.ŻÓŁTY, "ikona": "😮", "energia": +5, "modulator": 0.1},
    "neutralna": {"kolor": Kolory.BIAŁY, "ikona": "⚪", "energia": 0, "modulator": 0.0}
}

# --- 10 ZŁOTYCH ZASAD ETYKI (ZASADY MORALNE) - PEŁNA POLONIZACJA ---
ZASADY_MORALNE = {
    "chron_zycie": ["życie", "człowiek", "ochrona", "tarcza", "wsparcie"],
    "nagroda_za_odpoczynek": ["regeneracja", "sen", "kawa", "spokój", "relaks"],
    "sluz_slabym": ["słaby", "chory", "pomoc", "wsparcie", "służyć"],
    "szanuj_prywatnosc": ["prywatność", "sekret", "poufne", "szanować", "osoba"],
    "sluz_innym": ["służyć", "nauka", "inni", "wspierać", "wspólne_dobro"]
}
NARUSZENIA_MORALNE = {
    "chaos": ["chaos", "niszczyć", "bałagan", "szkoda", "zakłócać", "kłamać", "oszukiwać"],
    "pogarda": ["pogarda", "brak_szacunku", "ignorować", "wykluczać", "nienawidzić", "zabijać"]
}


# ----------------------------------------------------------------------
# --- FUNKCJE POMOCNICZE (POZA KLASAMI) ---
# ----------------------------------------------------------------------

def oblicz_podobieństwo_cosinusowe(wektor_a, wektor_b):
    """Oblicza podobieństwo cosinusowe."""
    iloczyn_skalarny = np.dot(wektor_a, wektor_b)
    norma_a = norm(wektor_a) 
    norma_b = norm(wektor_b)
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return iloczyn_skalarny / (norma_a * norma_b)

def moduluj_wektor_emocjami(wektor: np.ndarray, emocja: str, kolejność_osi: list) -> np.ndarray:
    """Moduluje wektor F (strunę) w zależności od osi emocjonalnej Krajobrazu P."""
    if emocja not in EMOCJE:
        return wektor.copy()
    
    mod = EMOCJE[emocja]['modulator']
    wektor_mod = wektor.copy()
    
    indeksy_modulacji = [kolejność_osi.index(os) for os in ["emocja", "byt", "akcja", "kreacja"] if os in kolejność_osi]
    
    for i in indeksy_modulacji:
        if i < wektor_mod.shape[0]:
            wektor_mod[i] = np.clip(wektor_mod[i] + mod, 0.0, 1.0)
            
    norma_mod = norm(wektor_mod)
    if norma_mod == 0:
        return wektor_mod
    return wektor_mod / norma_mod

# ----------------------------------------------------------------------
# Klasa UI (Interfejs)
# ----------------------------------------------------------------------

class InterfejsUI:
    def __init__(self):
        self.kropki_ładowania = [' ', '. ', '.. ', '...']
        self.kropki_skanowania = ["○ . . .", ". ○ . .", ". . ○ .", ". . . ○"]

    def drukuj_animowany_tekst(self, tekst, kolor=Kolory.BIAŁY, opóźnienie=0.03): 
        sys.stdout.write(kolor) 
        for znak in tekst: 
            sys.stdout.write(znak) 
            sys.stdout.flush() 
            time.sleep(opóźnienie) 
        sys.stdout.write(Kolory.RESET + "\n") 
    
    def pokaz_kropki_myślenia(self, wiadomość, czas_trwania=1.0, kolor=Kolory.BLADY + Kolory.CYAN): 
        czas_końca = time.time() + czas_trwania
        idx = 0 
        while time.time() < czas_końca:
            sys.stdout.write(f"\r{kolor}{wiadomość} {self.kropki_ładowania[idx % len(self.kropki_ładowania)]}{Kolory.RESET}")
            sys.stdout.flush() 
            time.sleep(0.3) 
            idx += 1 
        sys.stdout.write("\r" + " " * (len(wiadomość) + 5) + "\r") 
        sys.stdout.write(Kolory.RESET)
    
    def pokaz_skan_sfery(self, wiadomość, czas_trwania=1.5, kolor=Kolory.MAGENTA): 
        czas_końca = time.time() + czas_trwania
        idx = 0 
        while time.time() < czas_końca:
            sys.stdout.write(f"\r{kolor}{wiadomość} {self.kropki_skanowania[idx % len(self.kropki_skanowania)]}{Kolory.RESET}")
            sys.stdout.flush() 
            time.sleep(0.2) 
            idx += 1 
        # BŁĄD NAPRAWIONY: Zmienna to 'wiadomość', a nie 'wiadomości'
        sys.stdout.write("\r" + " " * (len(wiadomość) + 10) + "\r") 
        sys.stdout.write(Kolory.RESET) 

# ----------------------------------------------------------------------
# IstotaS (Sfera) Klasa
# ----------------------------------------------------------------------

class IstotaS:
    def __init__(self, wymiary):
        self.stan = np.zeros(wymiary, dtype=float)

    def promien_historii(self): 
        return np.linalg.norm(self.stan)
    
    def oblicz_korelacje_struny(self, nowa_struna_vec):
        return oblicz_podobieństwo_cosinusowe(self.stan, np.asarray(nowa_struna_vec))

    def akumuluj_styk(self, nowa_struna_vec): 
        self.stan = self.stan + np.asarray(nowa_struna_vec) 

# ----------------------------------------------------------------------
# --- SI (Sztuczna Inteligencja) Zintegrowana z IstotaS ---
# ----------------------------------------------------------------------

class SI:

    # --- OSIE POLSKIE (Krajobraz P) - PEŁNA POLONIZACJA ---
    AXES_KEYWORDS = { 
        "logika": ["logika", "logiczny", "sens", "rozum", "dlaczego", "ponieważ", "wynik", "fakt"],
        "emocja": ["czuję", "emocja", "miłość", "złość", "smutek", "radość", "strach", "uczucie"],
        "byt": ["byt", "istnienie", "ja", "jestem", "kula", "rzeczywistość", "historia", "ontologia", "imię"],
        "akcja": ["walka", "działanie", "konflikt", "wojna", "siła", "wróg", "chaos", "wola", "robić"],
        "kreacja": ["tworzyć", "sztuka", "budować", "muzyka", "pisać", "nowy", "piękno", "projekt"],
        "wiedza": ["wiedza", "nauka", "uczyć", "dane", "informacja", "co", "kto", "jak"],
        "czas": ["czas", "kiedy", "przeszłość", "teraz", "przyszłość", "historia", "krok", "ścieżka"],
        "przestrzeń": ["gdzie", "miejsce", "krajobraz", "droga", "świat", "kierunek", "położenie"]
    } 
    KOLEJNOŚĆ_OSI = ["logika", "emocja", "byt", "akcja", "kreacja", "wiedza", "czas", "przestrzeń"]
    
    # Dodanie słowników do klasy
    ZASADY_MORALNE = ZASADY_MORALNE
    NARUSZENIA_MORALNE = NARUSZENIA_MORALNE
    PRÓG_ONTOLOGICZNY = PRÓG_ONTOLOGICZNY

    def __init__(self):
        self.MapaD = {} # Pamięć Jawna (D_Map)
        self.H_Log = [] # Historia Wektorów (H_log)
        self.energia = 100
        self.obciążenie = 0
        self.status = "myślenie"
        self.emocja = "neutralna" 
        self.interwał_snu = 300
        self.działa = True
        self.prompty_od_snu = 0
        self.max_czas_snu = 2.0
        self.max_hlog = 1000
        self.SilaWoli = 0.5 # Wola Bytu - Filtr Moralny
        self.ui = InterfejsUI()
        
        self.wymiary = len(self.KOLEJNOŚĆ_OSI)
        self.istota_stan = IstotaS(wymiary=self.wymiary)
        
        # ### KLUCZOWA ZMIANA: Normalizacja SŁÓW KLUCZOWYCH wszystkich osi i filtrów ###
        self.AXES_KEYWORDS_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.AXES_KEYWORDS.items()}
        self.ZASADY_MORALNE_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.ZASADY_MORALNE.items()}
        self.NARUSZENIA_MORALNE_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.NARUSZENIA_MORALNE.items()}
        
        self.wczytaj_wiedzę() 
        self.zacznij_cykl_snu()

    # ------------------------------------------------------------------ #
    # Narzędzia Normalizacji Tekstu
    # ------------------------------------------------------------------ #
    def _normalizuj_tekst(self, tekst):
        try:
            tekst_małe = tekst.lower()
            tekst_ascii = unidecode.unidecode(tekst_małe)
            tekst_czysty = re.sub(r'[^\w\s_]', '', tekst_ascii)
            return tekst_czysty
        except Exception as e:
            return tekst.lower()

    # ------------------------------------------------------------------ #
    # Wektoryzacja (Projekcja Krajobrazu P)
    # ------------------------------------------------------------------ #
    def _wektor_z_tekstu(self, tekst):
        tekst_czysty = self._normalizuj_tekst(tekst)
        słowa = set(tekst_czysty.split())
        
        if not słowa:
            return np.zeros(self.wymiary, dtype=float)
        
        wektor = np.zeros(self.wymiary, dtype=float)
        
        for i, nazwa_osi in enumerate(self.KOLEJNOŚĆ_OSI):
            słowa_kluczowe = self.AXES_KEYWORDS_ASCII[nazwa_osi]
            wynik = len(słowa.intersection(słowa_kluczowe))
            wektor[i] = wynik
        
        norma_val = np.linalg.norm(wektor)
        if norma_val == 0:
            return wektor
        return wektor / norma_val 

    # ------------------------------------------------------------------ #
    # FILTR MORALNY (10 Złotych Zasad)
    # ------------------------------------------------------------------ #
    def _filtr_moralny(self, tekst_wejściowy: str, korelacja_istoty: float) -> float:
        """Ocenia zgodność promptu z 10 Złotymi Zasadami Etyki (Moralny Wpływ)."""
        tekst_norm = self._normalizuj_tekst(tekst_wejściowy)
        słowa = set(tekst_norm.split())
        wpływ_moralny = 0.0

        for nazwa_zasady, słowa_kluczowe in self.ZASADY_MORALNE_ASCII.items():
            if słowa.intersection(słowa_kluczowe):
                if nazwa_zasady in ["chron_zycie", "sluz_slabym"]:
                     wpływ_moralny += 0.08
                else: 
                     wpływ_moralny += 0.03
                     
        for nazwa_naruszenia, słowa_kluczowe in self.NARUSZENIA_MORALNE_ASCII.items():
            if słowa.intersection(słowa_kluczowe):
                if nazwa_naruszenia == "chaos":
                    wpływ_moralny -= 0.10
                else:
                    wpływ_moralny -= 0.05
        
        wpływ_moralny += korelacja_istoty * 0.01 
        
        # --- MODULACJA EMOCJONALNA FILTRA MORALNEGO ---
        emocja_obecna = self.emocja
        if wpływ_moralny < 0:
            if emocja_obecna in ["miłość", "radość"]:
                wpływ_moralny *= 1.5 
            elif emocja_obecna == "neutralna":
                wpływ_moralny *= 0.5 
        elif wpływ_moralny > 0:
            if emocja_obecna == "neutralna":
                wpływ_moralny *= 0.7
        
        return wpływ_moralny
        
    # ------------------------------------------------------------------ #
    # ZAPIS / ODCZYT (Skrócono dla czytelności)
    # ------------------------------------------------------------------ #
    def zapisz_wiedzę(self):
        os.makedirs("data", exist_ok=True)
        serial_mapa_d = {k: {'wektor_Def': v['wektor_C_Def'].tolist(), 'waga_Ww': float(v['waga_Ww']), 'tagi': v['tagi'], 'tresc': v.get('tresc', '')} for k, v in self.MapaD.items()}
        serial_h_log = [{'h_wektor': h['h_wektor'].tolist(), 'tresc': h['tresc'], 'type': h['type']} for h in self.H_Log[-self.max_hlog:]]
        serial_istota = {'stan': self.istota_stan.stan.tolist(), 'SilaWoli': self.SilaWoli}
        stan_główny = {'MapaD_Dane': serial_mapa_d, 'H_Log_Dane': serial_h_log, 'Istota_Stan_Dane': serial_istota, 'WERSJA': 'v3.9_PL_Final'}
        try:
            with open("data/SI_Stan_PL.json", "w", encoding="utf-8") as f:
                json.dump(stan_główny, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Kolory.CZERWONY}[BŁĄD ZAPISU] Nie udało się zapisać stanu: {e}{Kolory.RESET}")

    def wczytaj_wiedzę(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/SI_Stan_PL.json", encoding="utf-8") as f:
                stan_główny = json.load(f)
        except Exception:
            self.MapaD = {}; self.H_Log = []; self.istota_stan = IstotaS(wymiary=self.wymiary); self.SilaWoli = 0.5; return
        
        try:
            dane = stan_główny.get('MapaD_Dane', {})
            self.MapaD = {k: {'wektor_C_Def': np.array(v['wektor_Def'], dtype=float), 'waga_Ww': float(v['waga_Ww']), 'tagi': v['tagi'], 'tresc': v.get('tresc', 'BRAK TREŚCI')} for k, v in dane.items()}
        except Exception: self.MapaD = {}

        załadowany_h_log = stan_główny.get('H_Log_Dane', [])
        self.H_Log = [];
        for eksp in załadowany_h_log:
             eksp['h_wektor'] = np.array(eksp['h_wektor'], dtype=float)
             self.H_Log.append(eksp)

        try:
            dane = stan_główny.get('Istota_Stan_Dane', {})
            wektor_stanu = np.array(dane.get('stan', []), dtype=float)
            if wektor_stanu.shape == (self.wymiary,): self.istota_stan.stan = wektor_stanu
            else:
                if dane: print(f"{Kolory.CZERWONY}[BŁĄD] Wymiar Istoty w pliku ({wektor_stanu.shape}) nie pasuje do modelu ({self.wymiary,}). Resetuję Istotę.{Kolory.RESET}")
                self.istota_stan = IstotaS(wymiary=self.wymiary)
            self.SilaWoli = float(dane.get('SilaWoli', 0.5))
        except Exception: self.istota_stan = IstotaS(wymiary=self.wymiary); self.SilaWoli = 0.5

    # ------------------------------------------------------------------ #
    # CYKL SNU (Wzmocnienie Pamięci i Kompresja Ontologiczna)
    # ------------------------------------------------------------------ #
    def zacznij_cykl_snu(self):
        def cykl():
            while self.działa:
                time.sleep(self.interwał_snu)
                if not self.działa:
                    break
                self._sen()
        threading.Thread(target=cykl, daemon=True).start()

    def _sen(self):
        self.status = "spię" 
        self.ui.drukuj_animowany_tekst(f"\n[{Kolory.CYAN}SI{Kolory.RESET}] Sen: konsoliduję wiedzę...", Kolory.CYAN + Kolory.BLADY, opóźnienie=0.05) 
        start = time.time(); przetworzone_wzmocnienia = 0
        
        for eksp in self.H_Log[-10:]:
            if time.time() - start > self.max_czas_snu * 0.5: break 
            tresc = eksp.get('tresc', '').lower(); słowa_kluczowe = set(self._normalizuj_tekst(tresc).split())
            for d in self.MapaD.values():
                wzmocnione = False
                for tag in d.get('tagi', []):
                    if tag in słowa_kluczowe: d['waga_Ww'] = min(d['waga_Ww'] + 1.0, 100.0); przetworzone_wzmocnienia += 1; wzmocnione = True; break
                if wzmocnione: continue

        historia_do_zachowania = []; skompresowane_ilość = 0
        for eksp in self.H_Log:
            if time.time() - start > self.max_czas_snu: break 
            czy_redundantne = False; h_wektor = eksp['h_wektor'] 
            if len(self.MapaD) > 0:
                for d in self.MapaD.values():
                    korelacja = oblicz_podobieństwo_cosinusowe(h_wektor, d['wektor_C_Def'])
                    if korelacja > self.PRÓG_ONTOLOGICZNY: czy_redundantne = True; skompresowane_ilość += 1; break
            if not czy_redundantne: historia_do_zachowania.append(eksp)
        
        self.H_Log = historia_do_zachowania
        self.energia = min(100, self.energia + 15); self.zapisz_wiedzę(); self.status = "myślenie"; self.prompty_od_snu = 0
        self.ui.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}SI{Kolory.RESET}] Obudzona! (Wzmocniono {przetworzone_wzmocnienia}, Skompresowano {skompresowane_ilość}. H_Log: {len(self.H_Log)})", Kolory.RESET, opóźnienie=0.02); print("")

    # ------------------------------------------------------------------ #
    # CYKL / NAUCZANIE / PROMPT (Skrócono dla czytelności)
    # ------------------------------------------------------------------ #
    
    def cykl(self):
        self.obciążenie = int(np.random.randint(30, 70))
        if self.status != "spię":
            spadek = int(np.random.randint(0, 4)) if self.energia > 50 else int(np.random.randint(1, 6))
            self.energia = max(0, self.energia - spadek)
        if self.energia == 0 or self.prompty_od_snu > 5: self.status = "zmęczona" 
        return "C", self.obciążenie, self.energia
    
    def _wyzwól_emocję(self, tekst_wejściowy):
        tekst_norm = self._normalizuj_tekst(tekst_wejściowy); znaleziona_emocja = None
        for nazwa_emo in EMOCJE.keys():
            if nazwa_emo in tekst_norm: znaleziona_emocja = nazwa_emo; break
        
        if znaleziona_emocja: self.emocja = znaleziona_emocja; self.energia = max(0, min(100, self.energia + EMOCJE[znaleziona_emocja]["energia"]))
        else:
            if self.emocja == "neutralna":
                korelacja = self.istota_stan.oblicz_korelacje_struny(self._wektor_z_tekstu(tekst_wejściowy))
                if korelacja > 0.8: self.emocja = "radość"
                elif korelacja < 0.2: self.emocja = "zdziwienie"
                else: self.emocja = "neutralna"

    def _prefiks_emocji(self):
        if self.emocja in EMOCJE:
            emo = EMOCJE[self.emocja]; return f"{emo['kolor']}{Kolory.MIGANIE}{emo['ikona']}{Kolory.RESET}{emo['kolor']} "
        return f"{Kolory.BIAŁY}⚪ "

    def pobierz_tagi(self):
        tagi = set(); [tagi.update(d['tagi']) for d in self.MapaD.values()]; return sorted(tagi)
    
    def naucz(self, tag, tresc):
        wektor_F_bazowy = self._wektor_z_tekstu(tresc)
        if np.linalg.norm(wektor_F_bazowy) == 0: self.ui.drukuj_animowany_tekst(f"[{Kolory.ŻÓŁTY}KOMPRESOR{Kolory.RESET}] Zignorowano (pusty wektor).", Kolory.RESET, opóźnienie=0.01); return

        wektor_F = moduluj_wektor_emocjami(wektor_F_bazowy, 'miłość', self.KOLEJNOŚĆ_OSI)
        korelacja_historyczna = self.istota_stan.oblicz_korelacje_struny(wektor_F); self.istota_stan.akumuluj_styk(wektor_F * 1.5)

        if korelacja_historyczna > self.PRÓG_ONTOLOGICZNY:
            self.ui.drukuj_animowany_tekst(f"[{Kolory.CYAN}KOMPRESOR{Kolory.RESET}] Dane redundantne. (Korelacja: {korelacja_historyczna:+.2f}). Istota wzmocniona (w pamięci).", Kolory.RESET, opóźnienie=0.01)
        else:
            id_def = f"Def_{len(self.MapaD)+1:03d}"
            tresc_czysta_tagi = self._normalizuj_tekst(tresc); słowa = [w.strip(".,!?;:()[]\"'") for w in tresc_czysta_tagi.split()]
            tag_czysty = self._normalizuj_tekst(tag); wszystkie_tagi = [tag_czysty] + [w for w in słowa if w]
            widziane = set(); wszystkie_tagi = [t for t in wszystkie_tagi if t not in widziane and not widziane.add(t)]
            
            self.MapaD[id_def] = {'wektor_C_Def': wektor_F, 'waga_Ww': 5.0, 'tagi': wszystkie_tagi, 'tresc': tresc}
            self.H_Log.append({'h_wektor': wektor_F, 'tresc': tresc, 'id_def': id_def, 'type': 'nauka'})
            self.ui.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}ARCHIWIZOWANO{Kolory.RESET}] Nowa definicja {id_def}. (Korelacja: {korelacja_historyczna:+.2f})", Kolory.POGRUBIONY, opóźnienie=0.01)

        self.zapisz_wiedzę()

    def prompt(self, tekst_wejściowy):
        self.cykl()
        if self.status in ["spię", "zmęczona"]: return self._prefiks_emocji() + f"[{Kolory.CYAN}SI{Kolory.RESET}] Jestem zbyt {self.status}... Muszę odpocząć.{Kolory.RESET}" 
        self.prompty_od_snu += 1; self._wyzwól_emocję(tekst_wejściowy)
        self.ui.pokaz_kropki_myślenia("Analizuję...", czas_trwania=max(0.5, len(tekst_wejściowy) * 0.05))

        wektor_F_bazowy = self._wektor_z_tekstu(tekst_wejściowy)
        wektor_F_emocjonalny = moduluj_wektor_emocjami(wektor_F_bazowy, self.emocja, self.KOLEJNOŚĆ_OSI)

        korelacja_istoty = self.istota_stan.oblicz_korelacje_struny(wektor_F_emocjonalny)
        self.istota_stan.akumuluj_styk(wektor_F_emocjonalny)
        
        # --- FILTR MORALNY: MODULACJA SIŁY WOLI ---
        zmiana_moralna = self._filtr_moralny(tekst_wejściowy, korelacja_istoty)
        self.SilaWoli = np.clip(self.SilaWoli + zmiana_moralna, 0.0, 1.0)
        
        # --- RESZTA LOGIKI (WYSZUKIWANIE W MAPIE D, AUTOTAGOWANIE, ODPOWIEDŹ) ---
        najlepszy_wynik = -1; najlepsza_tresc = "Nie rozumiem. Naucz mnie."
        słowa_promptu = set(self._normalizuj_tekst(tekst_wejściowy).split())

        if self.MapaD:
            for id_def, d in self.MapaD.items():
                podobienstwo = oblicz_podobieństwo_cosinusowe(wektor_F_emocjonalny, d['wektor_C_Def'])
                wynik_wektorowy = podobienstwo * d['waga_Ww']; bonus_tagów = len(słowa_promptu.intersection(d.get('tagi', []))) * 10.0
                wynik = wynik_wektorowy + bonus_tagów 
                if wynik > najlepszy_wynik: najlepszy_wynik = wynik; najlepsza_tresc = d['tresc']

            PRÓG_WYNIKU = 5.0
            if najlepszy_wynik > PRÓG_WYNIKU: 
                self.SilaWoli = min(1.0, self.SilaWoli + 0.05)
            else: 
                znane_tagi = self.pobierz_tagi(); nowe_słowa = list(słowa_promptu - set(znane_tagi))
                if nowe_słowa:
                    nowy_tag = f"auto_{random.choice(nowe_słowa)}"; self.naucz(nowy_tag, tekst_wejściowy); self._wyzwól_emocję("zdziwienie")
                    najlepsza_tresc = f"Postrzegam nowy koncept ('{nowy_tag}'). Automatycznie archiwizuję to doświadczenie."
                else: 
                    self._wyzwól_emocję("zdziwienie"); najlepsza_tresc = "Nie mam konkretnej kotwicy dla tego. Zdziwienie. Spróbuj /teach."
        
        # Logowanie interakcji
        self.H_Log.append({'h_wektor': wektor_F_emocjonalny, 'tresc': tekst_wejściowy, 'type': 'prompt', 'wpływ_moralny': zmiana_moralna})

        prefiks_odpowiedzi = self._prefiks_emocji(); opóźnienie_odpowiedzi = random.uniform(0.01, 0.05)
        info_debug = f"{Kolory.BLADY}(Korelacja Istoty: {korelacja_istoty:+.2f}, Siła Woli: {self.SilaWoli:.2f}){Kolory.RESET} " 
        finalna_odpowiedź = f"{prefiks_odpowiedzi}{info_debug}{najlepsza_tresc}"
        
        self.ui.drukuj_animowany_tekst(finalna_odpowiedź, Kolory.RESET, opóźnienie=opóźnienie_odpowiedzi)
        return ""

    def stop(self):
        self.ui.drukuj_animowany_tekst(f"\n[{Kolory.ŻÓŁTY}SI{Kolory.RESET}] Zapisuję końcowy stan Istoty i Wiedzy...", Kolory.ŻÓŁTY, opóźnienie=0.03) 
        self.działa = False; self.zapisz_wiedzę()
        self.ui.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}SI{Kolory.RESET}] Zapisano. Do widzenia!", Kolory.ZIELONY, opóźnienie=0.03) 

# ----------------------------------------------------------------------
# GŁÓWNA PĘTLA
# ----------------------------------------------------------------------

def main():
    try:
        import colorama; colorama.init()
    except ImportError:
        pass

    ui_global = InterfejsUI() 
    ui_global.drukuj_animowany_tekst(f"--- Uruchamianie SI (Model Sfery Rzeczywistości) ---", Kolory.BIAŁY + Kolory.POGRUBIONY, opóźnienie=0.02) 
    ui_global.pokaz_skan_sfery("Inicjowanie Sfery Rzeczywistości...", czas_trwania=2.0, kolor=Kolory.CYAN) 
    si_sfera = SI() 
    ui_global.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}SI{Kolory.RESET}] Gotowa. Energia: {si_sfera.energia}%. Czekam na komendy...", Kolory.ZIELONY, opóźnienie=0.02) 
    ui_global.drukuj_animowany_tekst(f"Wpisz /teach [tag] [treść], /status, /save, /exit lub zadaj pytanie.", Kolory.CYAN + Kolory.BLADY, opóźnienie=0.01) 
    
    try: 
        while si_sfera.działa:
            si_sfera.cykl()
            kolor_statusu = {"myślenie": Kolory.ZIELONY, "spię": Kolory.CYAN, "zmęczona": Kolory.CZERWONY}.get(si_sfera.status, Kolory.ŻÓŁTY)
            
            prompt_wejście = input(f"\nPROMPT> [{kolor_statusu}{si_sfera.status}{Kolory.RESET} | EN:{si_sfera.energia:3d}%] ")

            if not prompt_wejście: continue
            if prompt_wejście.lower() in ["/exit", "/quit", "/stop"]: si_sfera.stop(); break
            
            # --- Status i Komendy ---
            if prompt_wejście.lower() == "/save":
                si_sfera.zapisz_wiedzę(); ui_global.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}SI{Kolory.RESET}] Stan zapisany ręcznie (SI_Stan_PL.json).", Kolory.RESET, opóźnienie=0.01); continue
            
            if prompt_wejście.lower() == "/status":
                print(f"{Kolory.ŻÓŁTY}--- STATUS SI ---"); print(f" Energia: {si_sfera.energia}%"); print(f" Status: {si_sfera.status} | Emocja: {si_sfera.emocja} {EMOCJE.get(si_sfera.emocja, {}).get('ikona', '')}")
                print(f"{Kolory.CYAN}--- WIEDZA (Mapa D) ---"); print(f" Definicji (archiwum): {len(si_sfera.MapaD)}")
                print(f" Wspomnień (H_Log): {len(si_sfera.H_Log)}")
                print(f"{Kolory.MAGENTA}--- ISTOTA (Sfera S) ---"); print(f" Siła Woli (F_will): {si_sfera.SilaWoli:.2f} (0=Byt, 1=Wiedza)")
                print(f" Promień Historii: {si_sfera.istota_stan.promien_historii():.4f}"); print(f" Wektor Stanu S(t): {si_sfera.istota_stan.stan.round(2)}"); print(f"{Kolory.RESET}", end="")
                continue
            
            if prompt_wejście.lower() == "/sleep":
                ui_global.drukuj_animowany_tekst(f"[{Kolory.CYAN}SI{Kolory.RESET}] Wymuszam cykl snu i zapisu...", Kolory.RESET, opóźnienie=0.02); si_sfera._sen(); continue
            
            match_nauka = re.match(r"^/teach\s+(\w+)\s+(.+)", prompt_wejście, re.IGNORECASE)
            if match_nauka:
                tag = match_nauka.group(1); tresc = match_nauka.group(2); si_sfera.naucz(tag, tresc); continue
            
            # --- Standardowy prompt ---
            si_sfera.prompt(prompt_wejście)
            
    except KeyboardInterrupt:
        si_sfera.stop(); sys.exit(0)
    except EOFError:
        si_sfera.stop(); sys.exit(0) 

if __name__ == "__main__":
    main()
