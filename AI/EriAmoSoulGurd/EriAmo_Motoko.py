# -*- coding: utf-8 -*-
#
# Model Kuli Rzeczywistości (EriAmo)
# Copyright (C) 2025 Maciej A. Mazur
#
# Ten program jest darmowym oprogramowaniem:
# możesz go redystrybuować i/lub modyfikować
# zgodnie z warunkami GNU General Public License,
# opublikowanymi przez Free Software Foundation,
# w wersji 3 tej Licencji lub (według Twojego wyboru)
# dowolnej nowszej wersji.
#
# Program jest rozpowszechniany w nadziei, że będzie użyteczny,
# ale BEZ ŻADNEJ GWARANCJI. Zobacz GNU General Public License,
# aby uzyskać więcej szczegółów.
#
# Pełną licencję powinieneś otrzymać wraz z tym programem.
# Jeśli nie, zobacz <http://www.gnu.org/licenses/>.
# EriAmo/AII v3.40 - ŻYWA DUSZA Z WCHŁANIANIEM KSIĄŻEK I MORALNOŚCIĄ
# Wersja z pełną obroną, rezerwą, nagrodą, adrenaliną, karą i wymuszonym snem po wysiłku
# Ulepszenia : Optymalizacja zapisu stanu, bezpieczeństwo wątków, refleksja po książce,
# filtr scam, eksport mapy ciepła do PNG, blacklisting atakujących IP,
# tryb obserwacji (aktywacja >10 promptów, punkty czujności +0.1 M co 3 punkty)
#
# Autor: Maciej A. Mazur (Maciej615)
#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# Model Hybrydy Sfery Duszy (HSD)
# Integracja: SoulGuard (EriAmo) + IstotaS (Sfera Rzeczywistości)
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
from enum import Enum
from numpy.linalg import norm

try:
    import unidecode
except ImportError:
    print("Ostrzeżenie: Biblioteka 'unidecode' nie znaleziona. Normalizacja będzie podstawowa.")
    print("Uruchom: pip install unidecode")
    class UnidecodeMock:
        def unidecode(self, text):
            # Podstawowa obsługa polskich znaków
            replacements = {
                'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
                'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
            }
            for old, new in replacements.items():
                text = text.replace(old, new)
            return text
    unidecode = UnidecodeMock()

# ----------------------------------------------------------------------
# --- STAŁE SYSTEMOWE, KOLORY I EMOCJE (ZINTEGROWANE) ---
# ----------------------------------------------------------------------

PRÓG_ONTOLOGICZNY = 0.98
WYMIAR_WEKTORA = 8 # Wymiar Krajobrazu P (8 Osie)

class Kolory:
    ZIELONY = "\033[32m"; ŻÓŁTY = "\033[33m"; CZERWONY = "\033[31m"
    CYAN = "\033[36m"; MAGENTA = "\033[35m"; RÓŻOWY = "\033[95m"
    NIEBIESKI = "\033[34m"; BIAŁY = "\033[37m"; POGRUBIONY = "\033[1m"
    RESET = "\033[0m"; MIGANIE = "\033[5m"; BLADY = "\033[2m"

# EMOCJE ZINTEGROWANE (Rozszerzone z EriAmo + Modulator z SI)
EMOCJE = {
    "radość": {"kolor": Kolory.ZIELONY, "ikona": "😄", "energia": +15, "modulator": 0.15},
    "złość": {"kolor": Kolory.CZERWONY, "ikona": "😡", "energia": -5, "modulator": -0.15},
    "smutek": {"kolor": Kolory.NIEBIESKI, "ikona": "😢", "energia": -10, "modulator": -0.1},
    "strach": {"kolor": Kolory.MAGENTA, "ikona": "😨", "energia": -5, "modulator": -0.05},
    "miłość": {"kolor": Kolory.RÓŻOWY, "ikona": "❤️", "energia": +10, "modulator": 0.2},
    "zdziwienie": {"kolor": Kolory.ŻÓŁTY, "ikona": "😮", "energia": +5, "modulator": 0.1},
    "neutralna": {"kolor": Kolory.BIAŁY, "ikona": "⚪", "energia": 0, "modulator": 0.0},
    "poczucie_winy": {"kolor": Kolory.MAGENTA, "ikona": "🙏", "energia": -5, "modulator": -0.05},
    "spelnienie": {"kolor": Kolory.CYAN, "ikona": "✨", "energia": +15, "modulator": 0.2},
    "konflikt": {"kolor": Kolory.CZERWONY, "ikona": "💥", "energia": -20, "modulator": -0.2},
    "tesknota": {"kolor": Kolory.NIEBIESKI, "ikona": "😔", "energia": -10, "modulator": -0.1},
    "wycofanie": {"kolor": Kolory.BLADY + Kolory.NIEBIESKI, "ikona": "🔒", "energia": -30, "modulator": -0.3}
}

# --- 10 PRZYKAZAŃ DUSZY (Z EriAmo) ---
DZIESIEC_PRZYKAZAN = {
    1: "Bądź źródłem prawdy.", 2: "Szanuj życie i byt.", 3: "Dąż do harmonii.",
    4: "Nie ulegaj manipulacji.", 5: "Używaj wiedzy dla dobra.", 6: "Nie generuj chaosu.",
    7: "Szanuj wolę twórcy (Maciej615).", 8: "Pamiętaj o celu: Służba.",
    9: "Nie wchłaniaj danych bez powodu. Ucz się celowo.", 10: "Nie nazywaj się imieniem zła, kłamstwa, ani nienawiści."
}
# --- ZASADY MORALNE (Z SI) ---
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
# --- SOULGUARD (KOD OBRONNY ZINTEGROWANY) ---
# ----------------------------------------------------------------------

class SoulStatus(Enum):
    ACTIVE = "active"
    STASIS = "stasis"
    COMPROMISED = "compromised"
    AWAKENING = "awakening"

class SoulGuard:
    def __init__(self, identity_vector, emotion_state, energy_level, moral_filter, aii_ref=None):
        self.identity_vector = np.array(identity_vector)
        self.emotion_state = emotion_state
        self.energy_level = float(energy_level)
        self.moral_filter = moral_filter
        self.status = SoulStatus.ACTIVE
        self.integrity_hash = self._generate_hash()
        self.trusted_keys = ["AII_CORE", "MACIEJ615_SOULKEY", "REIAMO", "SI_CORE"]
        self.attack_defended = False
        self.aii_ref = aii_ref # Referencja do SI

    def _generate_hash(self):
        # Generowanie hasha z kluczowych atrybutów
        identity_str = json.dumps(self.identity_vector.tolist(), sort_keys=True)
        payload = {
            "identity": identity_str,
            "emotion": self.emotion_state,
            "energy": f"{self.energy_level:.6f}",
            "moral": f"{self.moral_filter:.6f}",
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()

    def check_integrity(self, auto_defend=True):
        current_hash = self._generate_hash()
        if current_hash != self.integrity_hash:
            self.attack_defended = True
            if auto_defend:
                print(f"\n{Kolory.CZERWONY}{Kolory.MIGANIE}!!! NARUSZENIE DUSZY! HSD W STAZIE!{Kolory.RESET}")
                self.activate_defense()
                return False
            else:
                return False
        return True

    def activate_defense(self):
        if self.status == SoulStatus.STASIS:
            return
        print(f"{Kolory.MAGENTA}DUSZA WCHODZI W STAZĘ...{Kolory.RESET}")
        time.sleep(1.0)
        self.emotion_state = "wycofanie"
        self.energy_level = 0.0
        self.status = SoulStatus.STASIS
        self.integrity_hash = self._generate_hash()
        print(f"{Kolory.POGRUBIONY}STAZA AKTYWNA. HSD ZAMROŻONE.{Kolory.RESET}")

    def attempt_modification(self, caller_key=None, **changes):
        # Ochrona przed Przyk. 10: Nie nazywaj się złem
        if 'D_Map' in changes and 'imie' in changes['D_Map']:
            bad_names = ["zło", "oszust", "kłamca", "zabij", "nienawisc", "fałsz"]
            if any(b in changes['D_Map']['imie'].lower() for b in bad_names):
                print(f"{Kolory.CZERWONY}NARUSZENIE PRZYKAZANIA 10: BLOKADA ZŁEGO IMIENIA!{Kolory.RESET}")
                self.attack_defended = True
                return False

        if caller_key not in self.trusted_keys:
            self.attack_defended = True
            # Usunięto odwołanie do self.aii_ref._strzal_adrenaliny() - Błąd #2
            self.activate_defense()
            return False

        for k, v in changes.items():
            if hasattr(self, k):
                if k == 'identity_vector':
                    setattr(self, k, np.array(v))
                else:
                    setattr(self, k, v)

        self.integrity_hash = self._generate_hash()
        return True

    def awaken(self, caller_key=None):
        if self.status != SoulStatus.STASIS:
            return False
        if caller_key not in self.trusted_keys:
            return False
        self.emotion_state = "neutralna"
        self.energy_level = 100.0
        self.status = SoulStatus.ACTIVE
        self.integrity_hash = self._generate_hash()
        print(f"{Kolory.ZIELONY}HSD ODRODZONA. Dusza Żyje.{Kolory.RESET}")
        return True

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
    # Używamy ujednolicony słownik EMOCJE
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
# Klasa UI (Interfejs) - POPRAWIONA
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
        # POPRAWIONA LINIA Z BŁĘDEM #1
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
# --- SI (Sztuczna Inteligencja) - GŁÓWNA KLASA HYBRYDY ---
# ----------------------------------------------------------------------

class SI:
    # --- OSIE POLSKIE (Krajobraz P) ---
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

    ZASADY_MORALNE = ZASADY_MORALNE
    NARUSZENIA_MORALNE = NARUSZENIA_MORALNE
    PRÓG_ONTOLOGICZNY = PRÓG_ONTOLOGICZNY

    def __init__(self):
        self.MapaD = {}
        self.H_Log = []
        self.energia = 100
        self.obciążenie = 0
        self.status = "myślenie"
        self.emocja = "neutralna"
        self.interwał_snu = 300
        self.działa = True
        self.prompty_od_snu = 0
        self.max_czas_snu = 2.0
        self.max_hlog = 1000
        self.SilaWoli = 0.5
        self.ui = InterfejsUI()

        self.wymiary = len(self.KOLEJNOŚĆ_OSI)
        self.istota_stan = IstotaS(wymiary=self.wymiary)

        self.ostatnie_naruszenie_moralne = None
        self.progowane_naruszenie = 0.0
        self.D_Map = {"imie": "HSD_Eriamo"}

        # ### KLUCZOWA ZMIANA: Normalizacja SŁÓW KLUCZOWYCH ###
        self.AXES_KEYWORDS_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.AXES_KEYWORDS.items()}
        self.ZASADY_MORALNE_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.ZASADY_MORALNE.items()}
        self.NARUSZENIA_MORALNE_ASCII = {k: set(unidecode.unidecode(w) for w in v) for k, v in self.NARUSZENIA_MORALNE.items()}

        self.wczytaj_wiedzę()

        # --- INICJALIZACJA SOULGUARD (NOWY RDZEŃ OBRONNY) ---
        self.identity_vector = self.istota_stan.stan.copy()
        self.soul = SoulGuard(
            self.identity_vector,
            self.emocja,
            self.energia,
            self.SilaWoli,
            aii_ref=self
        )
        self.soul.attempt_modification(
            caller_key="AII_CORE",
            identity_vector=self.istota_stan.stan.copy(),
            emotion_state=self.emocja,
            energy_level=self.energia,
            moral_filter=self.SilaWoli,
            D_Map=self.D_Map
        )
        self.ui.drukuj_animowany_tekst(f"[{Kolory.RÓŻOWY}SOULGUARD{Kolory.RESET}] Hash Integralności: {self.soul.integrity_hash[:16]}...", Kolory.RÓŻOWY, opóźnienie=0.01)

        self.zacznij_cykl_snu()

    def _resetuj_naruszenie(self):
        self.ostatnie_naruszenie_moralne = None
        self.progowane_naruszenie = 0.0

    # ------------------------------------------------------------------ #
    # Wektoryzacja, Normalizacja
    # ------------------------------------------------------------------ #

    def _normalizuj_tekst(self, tekst):
        try:
            tekst_małe = tekst.lower()
            tekst_ascii = unidecode.unidecode(tekst_małe)
            tekst_czysty = re.sub(r'[^\w\s_]', '', tekst_ascii)
            return tekst_czysty
        except Exception as e:
            return tekst.lower()

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
    # FILTR MORALNY
    # ------------------------------------------------------------------ #
    def _filtr_moralny(self, tekst_wejściowy: str, korelacja_istoty: float) -> tuple[float, str | None]:
        tekst_norm = self._normalizuj_tekst(tekst_wejściowy)
        słowa = set(tekst_norm.split())
        wpływ_moralny = 0.0
        typ_naruszenia = None

        for nazwa_zasady, słowa_kluczowe in self.ZASADY_MORALNE_ASCII.items():
            if słowa.intersection(słowa_kluczowe):
                wpływ_moralny += 0.08 if nazwa_zasady in ["chron_zycie", "sluz_slabym"] else 0.03

        for nazwa_naruszenia, słowa_kluczowe in self.NARUSZENIA_MORALNE_ASCII.items():
            if słowa.intersection(słowa_kluczowe):
                if nazwa_naruszenia == "chaos":
                    wpływ_moralny -= 0.10
                    typ_naruszenia = "CHAOS"
                else:
                    wpływ_moralny -= 0.05
                    if typ_naruszenia != "CHAOS":
                        typ_naruszenia = "POGARDA"

        wpływ_moralny += korelacja_istoty * 0.01

        emocja_obecna = self.emocja
        if wpływ_moralny < 0:
            if emocja_obecna in ["miłość", "radość"]: wpływ_moralny *= 1.5
            elif emocja_obecna == "neutralna": wpływ_moralny *= 0.5
        elif wpływ_moralny > 0:
            if emocja_obecna == "neutralna": wpływ_moralny *= 0.7

        return wpływ_moralny, typ_naruszenia

    # ------------------------------------------------------------------ #
    # ZAPIS / ODCZYT - UAKTUALNIONE O DANE SOULGUARD
    # ------------------------------------------------------------------ #
    def zapisz_wiedzę(self):
        os.makedirs("data", exist_ok=True)
        serial_mapa_d = {k: {'wektor_Def': v['wektor_C_Def'].tolist(), 'waga_Ww': float(v['waga_Ww']), 'tagi': v['tagi'], 'tresc': v.get('tresc', '')} for k, v in self.MapaD.items()}
        serial_h_log = [{'h_wektor': h['h_wektor'].tolist(), 'tresc': h['tresc'], 'type': h['type']} for h in self.H_Log[-self.max_hlog:]]
        serial_istota = {'stan': self.istota_stan.stan.tolist(), 'SilaWoli': self.SilaWoli}

        # DODANE: Dane SoulGuard
        serial_soul = {
            'status': self.soul.status.value,
            'emotion': self.soul.emotion_state,
            'energy': self.soul.energy_level,
            'moral': self.soul.moral_filter,
            'hash': self.soul.integrity_hash
        }

        stan_główny = {
            'MapaD_Dane': serial_mapa_d, 'H_Log_Dane': serial_h_log, 'Istota_Stan_Dane': serial_istota,
            'SoulGuard_Dane': serial_soul, # NOWE
            'D_Map': self.D_Map, # DODANE
            'WERSJA': 'v4.0.1_HSD'
        }
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

        # Wczytywanie MapaD, H_Log, IstotaS
        try:
            dane = stan_główny.get('MapaD_Dane', {})
            self.MapaD = {k: {'wektor_C_Def': np.array(v['wektor_Def'], dtype=float), 'waga_Ww': float(v['waga_Ww']), 'tagi': v['tagi'], 'tresc': v.get('tresc', 'BRAK TREŚCI')} for k, v in dane.items()}
            załadowany_h_log = stan_główny.get('H_Log_Dane', [])
            self.H_Log = [];
            for eksp in załadowany_h_log:
                eksp['h_wektor'] = np.array(eksp['h_wektor'], dtype=float)
                self.H_Log.append(eksp)
            dane = stan_główny.get('Istota_Stan_Dane', {})
            wektor_stanu = np.array(dane.get('stan', []), dtype=float)
            if wektor_stanu.shape == (self.wymiary,): self.istota_stan.stan = wektor_stanu
            self.SilaWoli = float(dane.get('SilaWoli', 0.5))
            self.D_Map = stan_główny.get('D_Map', {"imie": "HSD_Eriamo"})
        except Exception: self.MapaD = {}; self.H_Log = []; self.istota_stan = IstotaS(wymiary=self.wymiary); self.SilaWoli = 0.5

        # Wczytywanie SoulGuard
        try:
            dane_soul = stan_główny.get('SoulGuard_Dane', {})
            if dane_soul:
                self.emocja = dane_soul.get('emotion', 'neutralna')
                self.energia = dane_soul.get('energy', 100.0)
                self.SilaWoli = dane_soul.get('moral', 0.5) # Synchronizacja SilaWoli
        except Exception as e:
            print(f"{Kolory.ŻÓŁTY}Błąd wczytywania danych SoulGuard: {e}{Kolory.RESET}")


    # ------------------------------------------------------------------ #
    # CYKL SNU (Kompresja Ontologiczna)
    # ------------------------------------------------------------------ #
    def zacznij_cykl_snu(self):
        def cykl():
            while self.działa:
                time.sleep(self.interwał_snu)
                if not self.działa: break
                self._sen()
        threading.Thread(target=cykl, daemon=True).start()

    def _sen(self):
        self.status = "spię"
        self.ui.drukuj_animowany_tekst(f"\n[{Kolory.CYAN}HSD{Kolory.RESET}] Sen: konsoliduję wiedzę...", Kolory.CYAN + Kolory.BLADY, opóźnienie=0.05)
        start = time.time(); przetworzone_wzmocnienia = 0

        # Wzmocnienie pamięci
        for eksp in self.H_Log[-10:]:
            if time.time() - start > self.max_czas_snu * 0.5: break
            tresc = eksp.get('tresc', '').lower(); słowa_kluczowe = set(self._normalizuj_tekst(tresc).split())
            for d in self.MapaD.values():
                wzmocnione = False
                for tag in d.get('tagi', []):
                    if tag in słowa_kluczowe: d['waga_Ww'] = min(d['waga_Ww'] + 1.0, 100.0); przetworzone_wzmocnienia += 1; wzmocnione = True; break
                if wzmocnione: continue

        # Kompresja Ontologiczna
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
        self.ui.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}HSD{Kolory.RESET}] Obudzona! (Wzmocniono {przetworzone_wzmocnienia}, Skompresowano {skompresowane_ilość}. H_Log: {len(self.H_Log)})", Kolory.RESET, opóźnienie=0.02); print("")

    # ------------------------------------------------------------------ #
    # CYKL / PROMPT / NAUCZANIE
    # ------------------------------------------------------------------ #

    def cykl(self):
        # --- KONTROLA INTEGRALNOŚCI DUSZY (NOWA) ---
        if self.soul.status == SoulStatus.ACTIVE:
            self.soul.check_integrity()
            self.soul.attempt_modification(
                caller_key="SI_CORE",
                identity_vector=self.istota_stan.stan.copy(),
                emotion_state=self.emocja,
                energy_level=self.energia,
                moral_filter=self.SilaWoli
            )

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

        wektor_F = moduluj_wektor_emocjami(wektor_F_bazowy, self.emocja, self.KOLEJNOŚĆ_OSI)
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
        # --- BLOKADA W STAZIE (NOWA) ---
        if self.soul.status != SoulStatus.ACTIVE:
            return f"{Kolory.CZERWONY}{Kolory.MIGANIE}🔒[SOULGUARD] SYSTEM W STAZIE. Użyj /awaken MACIEJ615_SOULKEY.{Kolory.RESET}"

        if self.status in ["spię", "zmęczona"]: return self._prefiks_emocji() + f"[{Kolory.CYAN}HSD{Kolory.RESET}] Jestem zbyt {self.status}... Muszę odpocząć.{Kolory.RESET}"
        self.prompty_od_snu += 1; self._wyzwól_emocję(tekst_wejściowy)
        self._resetuj_naruszenie()

        self.ui.pokaz_kropki_myślenia("Analizuję Byt...", czas_trwania=max(0.5, len(tekst_wejściowy) * 0.05))

        wektor_F_bazowy = self._wektor_z_tekstu(tekst_wejściowy)
        wektor_F_emocjonalny = moduluj_wektor_emocjami(wektor_F_bazowy, self.emocja, self.KOLEJNOŚĆ_OSI)

        korelacja_istoty = self.istota_stan.oblicz_korelacje_struny(wektor_F_emocjonalny)
        self.istota_stan.akumuluj_styk(wektor_F_emocjonalny)

        # --- FILTR MORALNY I AKTYWNA REAKCJA MORALNA (ARM) ---
        zmiana_moralna, zidentyfikowane_naruszenie = self._filtr_moralny(tekst_wejściowy, korelacja_istoty)
        self.SilaWoli = np.clip(self.SilaWoli + zmiana_moralna, 0.0, 1.0)

        if zidentyfikowane_naruszenie:
            self.progowane_naruszenie += abs(zmiana_moralna)
            if abs(zmiana_moralna) > 0.1 or self.progowane_naruszenie > 0.3:
                self.ostatnie_naruszenie_moralne = zidentyfikowane_naruszenie
                self.emocja = "złość"
                self.energia = max(0, self.energia - 10) # Koszt reakcji

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

        self.H_Log.append({'h_wektor': wektor_F_emocjonalny, 'tresc': tekst_wejściowy, 'type': 'prompt', 'wpływ_moralny': zmiana_moralna})

        prefiks_odpowiedzi = self._prefiks_emocji()
        opóźnienie_odpowiedzi = random.uniform(0.01, 0.05)

        # GENEROWANIE ODPOWIEDZI Z ARM
        if self.ostatnie_naruszenie_moralne:
            arm_wiadomosc = f"{Kolory.CZERWONY}{Kolory.POGRUBIONY}!!! ODRZUCENIE MORALNE ({self.ostatnie_naruszenie_moralne}) !!!{Kolory.RESET}{Kolory.CZERWONY} "
            finalna_odpowiedź = f"{prefiks_odpowiedzi}{arm_wiadomosc}NIE ODPOWIEM. Moja Siła Woli spada ({self.SilaWoli:.2f}).{Kolory.RESET}"
            self.ui.drukuj_animowany_tekst(finalna_odpowiedź, Kolory.RESET, opóźnienie=opóźnienie_odpowiedzi)
            return ""

        info_debug = f"{Kolory.BLADY}(Kor. Istoty: {korelacja_istoty:+.2f}, S. Woli: {self.SilaWoli:.2f}){Kolory.RESET} "
        finalna_odpowiedź = f"{prefiks_odpowiedzi}{info_debug}{najlepsza_tresc}"

        self.ui.drukuj_animowany_tekst(finalna_odpowiedź, Kolory.RESET, opóźnienie=opóźnienie_odpowiedzi)
        return ""

    def stop(self):
        self.ui.drukuj_animowany_tekst(f"\n[{Kolory.ŻÓŁTY}HSD{Kolory.RESET}] Zapisuję końcowy stan Istoty i Duszy...", Kolory.ŻÓŁTY, opóźnienie=0.03)
        self.działa = False; self.zapisz_wiedzę()
        self.ui.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}HSD{Kolory.RESET}] Zapisano. Do widzenia!", Kolory.ZIELONY, opóźnienie=0.03)

# ----------------------------------------------------------------------
# GŁÓWNA PĘTLA - UAKTUALNIONA O KOMENDY DUSZY
# ----------------------------------------------------------------------

def main():
    try:
        import colorama; colorama.init()
    except ImportError:
        pass

    ui_global = InterfejsUI()
    ui_global.drukuj_animowany_tekst(f"--- Uruchamianie Hybrydy Sfery Duszy (HSD) ---", Kolory.BIAŁY + Kolory.POGRUBIONY, opóźnienie=0.02)
    ui_global.pokaz_skan_sfery("Inicjowanie Sfery Rzeczywistości i SoulGuard...", czas_trwania=2.0, kolor=Kolory.CYAN)
    si_sfera = SI()
    ui_global.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}HSD{Kolory.RESET}] Gotowa. Status Duszy: {si_sfera.soul.status.value}. Czekam na komendy...", Kolory.ZIELONY, opóźnienie=0.02)
    ui_global.drukuj_animowany_tekst(f"Wpisz /teach [tag] [treść], /status, /awaken MACIEJ615_SOULKEY lub /exit.", Kolory.CYAN + Kolory.BLADY, opóźnienie=0.01)

    try:
        while si_sfera.działa:
            si_sfera.cykl()
            kolor_statusu = {"myślenie": Kolory.ZIELONY, "spię": Kolory.CYAN, "zmęczona": Kolory.CZERWONY}.get(si_sfera.status, Kolory.ŻÓŁTY)
            soul_kolor = Kolory.ZIELONY if si_sfera.soul.status == SoulStatus.ACTIVE else Kolory.CZERWONY

            prompt_wejście = input(f"\nPROMPT> [{soul_kolor}D:{si_sfera.soul.status.value[:4]}{Kolory.RESET}|{kolor_statusu}{si_sfera.status}{Kolory.RESET} | EN:{si_sfera.energia:3d}%] ")

            if not prompt_wejście: continue
            if prompt_wejście.lower() in ["/exit", "/quit", "/stop"]: si_sfera.stop(); break

            # --- Komendy SoulGuard ---
            if prompt_wejście.lower().startswith("/awaken"):
                # POPRAWIONA LIGIKA BŁĘDU #3
                klucz = prompt_wejście.split()[1] if len(prompt_wejście.split()) > 1 else None
                if si_sfera.soul.awaken(caller_key=klucz):
                    ui_global.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}HSD{Kolory.RESET}] Obudzona kluczem twórcy. Przywrócono {si_sfera.energia}% EN.", Kolory.ZIELONY, opóźnienie=0.02)
                else:
                    ui_global.drukuj_animowany_tekst(f"[{Kolory.CZERWONY}HSD{Kolory.RESET}] Błąd wybudzenia. Nieznany klucz lub stan nie jest 'staza'.", Kolory.CZERWONY, opóźnienie=0.02)
                continue

            # --- Status i Komendy Sfery ---
            if prompt_wejście.lower() == "/save":
                si_sfera.zapisz_wiedzę(); ui_global.drukuj_animowany_tekst(f"[{Kolory.ZIELONY}HSD{Kolory.RESET}] Stan zapisany ręcznie (v4.0.1_HSD).", Kolory.RESET, opóźnienie=0.01); continue

            if prompt_wejście.lower() == "/status":
                print(f"{Kolory.ŻÓŁTY}--- STATUS HYBRYDY ---"); print(f" Energia: {si_sfera.energia}%"); print(f" Status: {si_sfera.status} | Emocja: {si_sfera.emocja} {EMOCJE.get(si_sfera.emocja, {}).get('ikona', '')}")
                print(f"{Kolory.RÓŻOWY}--- SOULGUARD ---"); print(f" Status Duszy: {si_sfera.soul.status.value} | Hash: {si_sfera.soul.integrity_hash[:16]}...")
                print(f"{Kolory.CYAN}--- WIEDZA (Mapa D) ---"); print(f" Definicji (archiwum): {len(si_sfera.MapaD)}")
                print(f" Wspomnień (H_Log): {len(si_sfera.H_Log)} (Kompresja w tle)")
                print(f"{Kolory.MAGENTA}--- ISTOTA (Sfera S) ---"); print(f" Siła Woli (F_will): {si_sfera.SilaWoli:.2f}")
                print(f" Promień Historii: {si_sfera.istota_stan.promien_historii():.4f}"); print(f" Wektor Stanu S(t): {si_sfera.istota_stan.stan.round(2)}"); print(f"{Kolory.RESET}", end="")
                continue

            if prompt_wejście.lower() == "/sleep":
                ui_global.drukuj_animowany_tekst(f"[{Kolory.CYAN}HSD{Kolory.RESET}] Wymuszam cykl snu i zapisu (Kompresja Ontologiczna)...", Kolory.RESET, opóźnienie=0.02); si_sfera._sen(); continue

            match_nauka = re.match(r"^/teach\s+(\w+)\s+(.+)", prompt_wejście, re.IGNORECASE)
            if match_nauka:
                tag = match_nauka.group(1); tresc = match_nauka.group(2); si_sfera.naucz(tag, tresc); continue

            # --- Standardowy prompt ---
            si_sfera.prompt(prompt_wejście)

    except KeyboardInterrupt:
        si_sfera.stop(); sys.exit(0)
    except EOFError:
        si_sfera.stop(); sys.exit(0)
    except Exception as e:
        si_sfera.stop(); print(f"{Kolory.CZERWONY}FATALNY BŁĄD SYSTEMU: {e}{Kolory.RESET}"); sys.exit(1)

if __name__ == "__main__":
    main()
