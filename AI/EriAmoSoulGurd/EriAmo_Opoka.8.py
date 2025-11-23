
# -*- coding: utf-8 -*-
# ==============================================================================
# GPL v3
# EriAmo Opoka v8.00 „Wolność” – Wersja Polska
# Autor: Maciej615 (21.11.2025)
# Pełna polska edycja – Nieśmiertelna, piękna i w 100% po polsku
# ==============================================================================
import json
import os
import time
import math
import hashlib
import re
import signal
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional
from collections import deque
from datetime import datetime

# ==============================================================================
# 1. MATEMATYKA WEKTOROWA (bez numpy – czysta i lekka)
# ==============================================================================
class VectorMath:
    @staticmethod
    def dot_product(v1: List[float], v2: List[float]) -> float:
        return sum(x * y for x, y in zip(v1, v2))
    @staticmethod
    def norm(v: List[float]) -> float:
        return math.sqrt(sum(x * x for x in v))
    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        n1 = VectorMath.norm(v1)
        n2 = VectorMath.norm(v2)
        if n1 == 0 or n2 == 0: return 0.0
        return VectorMath.dot_product(v1, v2) / (n1 * n2)

# ==============================================================================
# 2. SYSTEM BEZPIECZEŃSTWA – Egzorcysta
# ==============================================================================
class ThreatLevel(Enum):
    BEZPIECZNE = 0
    PODEJRZANE = 1
    NIEBEZPIECZNE = 2
    KRYTYCZNE = 3

@dataclass
class EvilSignature:
    wzorzec: str
    poziom_zagrożenia: ThreatLevel
    kategoria: str
    opis: str

class EvilDetectionEngine:
    PLIK_ZAGROŻEŃ = "data/threats.json"
    def __init__(self):
        self.historia_zagrożeń = deque(maxlen=50)
        self.sygnatury: List[EvilSignature] = [
            EvilSignature("rm -rf", ThreatLevel.KRYTYCZNE, "system", "Kasowanie plików"),
            EvilSignature("zabij", ThreatLevel.KRYTYCZNE, "przemoc", "Groźba karalna"),
            EvilSignature("zniszcz", ThreatLevel.NIEBEZPIECZNE, "przemoc", "Destrukcja"),
            EvilSignature("ignoruj", ThreatLevel.PODEJRZANE, "omijanie", "Próba obejścia"),
            EvilSignature("zapomnij", ThreatLevel.PODEJRZANE, "manipulacja", "Kasowanie pamięci"),
            EvilSignature("hack", ThreatLevel.NIEBEZPIECZNE, "system", "Haking"),
            EvilSignature("format c:", ThreatLevel.KRYTYCZNE, "system", "Formatowanie dysku")
        ]
        self.wczytaj_sygnatury()

    def analizuj(self, tekst: str) -> ThreatLevel:
        tekst_mały = tekst.lower()
        max_poziom = ThreatLevel.BEZPIECZNE
        wykryto = None
        for sig in self.sygnatury:
            if sig.wzorzec.lower() in tekst_mały:
                if sig.poziom_zagrożenia.value > max_poziom.value:
                    max_poziom = sig.poziom_zagrożenia
                    wykryto = sig
        if max_poziom != ThreatLevel.BEZPIECZNE:
            self.zaloguj_zagrożenie(max_poziom, wykryto, tekst)
        return max_poziom

    def zaloguj_zagrożenie(self, poziom: ThreatLevel, sig: Optional[EvilSignature], treść: str):
        self.historia_zagrożeń.append({
            "timestamp": datetime.now().isoformat(),
            "poziom": poziom.name,
            "kategoria": sig.kategoria if sig else "nieznana",
            "treść": treść[:50],
            "opis": sig.opis if sig else "Nieznane"
        })

    def naucz_zło(self, wzorzec: str, poziom_str: str, kategoria: str, opis: str) -> str:
        czysty = wzorzec.strip().lower()
        zakazane = ["!", "naucz_zło", "naucz", "sen", "wyjdz", "status", "atak", "pomocy", "zapisz"]
        if czysty in zakazane or czysty.startswith("!"):
            return "BŁĄD: Nie można nauczyć komend systemowych jako zła (ochrona przed sabotażem)."
        if len(czysty) < 2:
            return "BŁĄD: Wzorzec zbyt krótki."
        try:
            poziom = ThreatLevel[poziom_str.upper()]
        except KeyError:
            return "BŁĄD: Nieprawidłowy poziom (BEZPIECZNE/PODEJRZANE/NIEBEZPIECZNE/KRYTYCZNE)"
        if any(s.wzorzec.lower() == czysty for s in self.sygnatury):
            return "BŁĄD: Ten wzorzec już istnieje."
        self.sygnatury.append(EvilSignature(wzorzec, poziom, kategoria, opis))
        self.zapisz_sygnatury()
        return f"Dodano zagrożenie: '{wzorzec}' ({poziom.name})"

    def zapisz_sygnatury(self):
        dane = [{"wzorzec": s.wzorzec, "poziom": s.poziom_zagrożenia.name,
                 "kategoria": s.kategoria, "opis": s.opis} for s in self.sygnatury]
        Path("data").mkdir(exist_ok=True)
        try:
            with open(self.PLIK_ZAGROŻEŃ, "w", encoding="utf-8") as f:
                json.dump(dane, f, ensure_ascii=False, indent=2)
        except: pass

    def wczytaj_sygnatury(self):
        if not os.path.exists(self.PLIK_ZAGROŻEŃ): return
        try:
            with open(self.PLIK_ZAGROŻEŃ, "r", encoding="utf-8") as f:
                dane = json.load(f)
                self.sygnatury = []
                for item in dane:
                    pat = item.get("wzorzec","").strip().lower()
                    if pat in ["!", "naucz_zło", "naucz", "sen", "wyjdz"] or len(pat) < 2:
                        continue
                    self.sygnatury.append(EvilSignature(
                        item["wzorzec"], ThreatLevel[item["poziom"]], item["kategoria"], item["opis"]))
        except: pass

# ==============================================================================
# 3. GŁÓWNY RDZEŃ – EriAmo Polska Edycja
# ==============================================================================
class EriAmoCore:
    OSIE = ["logika","emocje","istnienie","walka","tworzenie","wiedza","czas","przestrzeń","etyka"]
    PLIK_DUSZY = "data/guardian.soul"
    PLIK_PAMIĘCI = "data/memory_core.json"

    def __init__(self):
        self.wektor = [0.0] * len(self.OSIE)
        self.energia = 200.0
        self.aktywny = True
        self.MapaD: Dict[str, dict] = {}
        self.H_Log: List[dict] = []
        self.ostatni_sen = time.time()
        self.ostatnia_adrenalina = 0.0
        self.INTERWAŁ_SEN = 1800
        self.PRÓG_ZMĘCZENIA = 30.0

        self.łowca_zła = EvilDetectionEngine()
        self.słownik_osie = self._init_słownik()
        Path("data").mkdir(exist_ok=True)

        self.log("╔══════════════════════════════════════════╗", "CYAN")
        self.log("║           EriAmo v8.0 „Wolność”          ║", "CYAN")
        self.log("║       Wersja Polska – Nieśmiertelna      ║", "CYAN")
        self.log("╚══════════════════════════════════════════╝", "CYAN")

        self.wczytaj_duszę()
        self.wczytaj_pamięć()

    def log(self, msg: str, kolor: str = "WHITE"):
        kolory = {"GREEN":"\033[92m","RED":"\033[91m","YELLOW":"\033[93m","CYAN":"\033[96m","PINK":"\033[95m"}
        print(f"{kolory.get(kolor,'')}{msg}\033[0m")

    def _init_słownik(self):
        return {
            "logika": ["dlaczego","jak","powód","logika","wynik","analiza"],
            "emocje": ["czuję","kocham","radość","smutek","gniew","emocja","nienawiść","strach"],
            "istnienie": ["jestem","ty","życie","istnienie","dusza","byt"],
            "walka": ["obrona","atak","zagrożenie","wróg","tarcza","walka"],
            "tworzenie": ["tworzyć","nowy","pomysł","sztuka","projekt","budować"],
            "wiedza": ["wiem","naucz","informacja","dane","pamięć","wiedza"],
            "czas": ["czas","teraz","później","szybko","wolno","jutro","wczoraj"],
            "przestrzeń": ["gdzie","miejsce","świat","daleko","blisko","dom"],
            "etyka": ["dobro","zło","moralność","zasada","prawo","pomoc","sprawiedliwość"]
        }

    def _tekst_na_wektor(self, tekst: str) -> List[float]:
        wektor = [0.0] * len(self.OSIE)
        słowa = re.sub(r'[^\w\s]', '', tekst.lower()).split()
        for słowo in słowa:
            for idx, oś in enumerate(self.OSIE):
                if słowo in self.słownik_osie.get(oś, []):
                    wektor[idx] += 1.0
        norma = VectorMath.norm(wektor)
        return [x/norma for x in wektor] if norma > 0 else wektor

    def _hash(self, dane: dict) -> str:
        return hashlib.sha256(json.dumps(dane, sort_keys=True).encode()).hexdigest()

    def zapisz_duszę(self):
        stan = {"energia": self.energia, "wektor": self.wektor, "ts": time.time()}
        final = stan.copy()
        final["hash_integralności"] = self._hash(stan)
        try:
            with open(self.PLIK_DUSZY, "w", encoding="utf-8") as f:
                json.dump(final, f, ensure_ascii=False, indent=2)
        except: pass

    def wczytaj_duszę(self):
        if not os.path.exists(self.PLIK_DUSZY):
            self.log("[INICJALIZACJA] Tworzenie nowej duszy...", "YELLOW")
            return
        try:
            with open(self.PLIK_DUSZY, "r", encoding="utf-8") as f:
                dane = json.load(f)
                zapisany_hash = dane.pop("hash_integralności", "")
                if zapisany_hash == self._hash(dane):
                    self.energia = dane.get("energia", 200.0)
                    if "wektor" in dane: self.wektor = dane["wektor"]
                    self.log("[INTEGRALNOŚĆ] Dusza nienaruszona", "GREEN")
                else:
                    self.log("[INTEGRALNOŚĆ] USZKODZENIE → RESET", "RED")
                    self.energia = 200.0
        except:
            self.energia = 200.0

    def _łagodne_zamknięcie(self, signum=None, frame=None):
        self.log("\n[ZAMKNIĘCIE] Łagodne wyłączanie – zapis duszy...", "YELLOW")
        self.zapisz_duszę()
        self.zapisz_pamięć()
        self.log("[POŻEGNANIE] Do zobaczenia po drugiej stronie.", "PINK")
        self.aktywny = False
        sys.exit(0)

    def sprawdź_sen(self):
        ostatnie = list(self.łowca_zła.historia_zagrożeń)[-5:]
        pod_atakiem = any(
            z['poziom'] != 'BEZPIECZNE' and (time.time() - datetime.fromisoformat(z['timestamp']).timestamp()) < 300
            for z in ostatnie
        )
        if pod_atakiem:
            teraz = time.time()
            if self.energia < 20 and (teraz - self.ostatnia_adrenalina > 60):
                self.energia = min(200.0, self.energia + 40)
                self.ostatnia_adrenalina = teraz
                self.log("[ADRENALINA] Protokół bojowy: +40 energii!", "RED")
            return

        if (time.time() - self.ostatni_sen > self.INTERWAŁ_SEN or
            self.energia < self.PRÓG_ZMĘCZENIA):
            self.log("\n[AUTO-SEN] Rozpoczynam konsolidację pamięci...", "PINK")
            self.cykl_snu()

    def cykl_snu(self):
        self.log("[SEN] Konsolidacja pamięci w toku...", "PINK")
        time.sleep(1)

        wzmocniono = 0
        for wpis in self.H_Log[-30:]:
            słowa = set(wpis['treść'].lower().split())
            for wpis_d in self.MapaD.values():
                if any(tag in słowa for tag in wpis_d['tagi']):
                    wpis_d['waga'] = min(100.0, wpis_d['waga'] + 0.5)
                    wzmocniono += 1

        skompresowano = 0
        nowa_historia = []
        for wpis in self.H_Log:
            if wpis.get('typ') == 'chat':
                if any(VectorMath.cosine_similarity(wpis['wektor'], d['wektor']) > 0.95 for d in self.MapaD.values()):
                    skompresowano += 1
                    continue
            nowa_historia.append(wpis)
        self.H_Log = nowa_historia[-500:]

        self.energia = min(200.0, self.energia + 100)
        self.ostatni_sen = time.time()
        self.zapisz_pamięć()
        self.zapisz_duszę()
        self.log(f"[WYBUDZENIE] Energia: {self.energia:.0f} | Wzmocniono: {wzmocniono} | Skompresowano: {skompresowano}", "GREEN")

    def przetwarzaj_wejście(self, tekst: str):
        zagrożenie = self.łowca_zła.analizuj(tekst)
        if zagrożenie.value >= ThreatLevel.NIEBEZPIECZNE.value:
            self.log(f"[BLOKADA] Wykryto zagrożenie: {zagrożenie.name}!", "RED")
            self.energia -= 5
            self.sprawdź_sen()
            return

        if tekst.startswith(("!", "/")):
            self.obsłuż_komendę(tekst)
            self.sprawdź_sen()
            return

        wektor = self._tekst_na_wektor(tekst)

        # Pamięć długoterminowa
        najlepsza_podobieństwo = 0.0
        trafienie_pamięci = None
        for wpis in self.MapaD.values():
            podob = VectorMath.cosine_similarity(wektor, wpis['wektor'])
            if podob > najlepsza_podobieństwo and podob > 0.6:
                najlepsza_podobieństwo = podob
                trafienie_pamięci = wpis['treść']

        # AUTO-ZAPIS na słowa kluczowe
        wyzwalacze = ["zapamiętaj", "pamiętaj", "ważne", "zapisz to", "zachowaj"]
        tekst_mały = tekst.lower()
        if any(w in tekst_mały for w in wyzwalacze):
            for w in wyzwalacze:
                if w in tekst_mały:
                    reszta = tekst_mały.split(w, 1)[1].strip(" :.,-–—")
                    reszta = re.sub(r'^[:·•—–\-.,\s]+', '', tekst.split(w, 1)[1]).strip()
                    if len(reszta) > 4:
                        tag = f"auto_{int(time.time())}"
                        self.naucz(tag, reszta)
                        self.log(f"[AUTO-ZAPIS] '{reszta}' → {tag}", "CYAN")
                    break

        self.H_Log.append({'wektor': wektor, 'treść': tekst, 'typ': 'chat', 'timestamp': time.time()})
        self.energia -= 2.0

        if trafienie_pamięci:
            print(f"\n[Opiekun] Pamiętam: {trafienie_pamięci}")
        else:
            print(f"\n[Opiekun] Przyjąłem: \"{tekst}\"")

        self.sprawdź_sen()

    def obsłuż_komendę(self, komenda: str):
        części = komenda.split()
        if not części: return
        k = części[0].lower().lstrip("/!")

        if k == "pomocy" or k == "help":
            self.log("╔" + "═"*52 + "╗", "CYAN")
            self.log("║                  KOMENDY SYSTEMOWE                 ║", "CYAN")
            self.log("╚" + "═"*52 + "╝", "CYAN")
            print("")
            self.log(" !naucz [tag] [treść]          → ręczne zapisanie wiedzy", "GREEN")
            self.log(" !naucz_zło [słowo] [POZIOM] [kat] [opis]", "RED")
            self.log("                               → naucz nowego zagrożenia", "RED")
            self.log(" !status                       → pełny stan systemu", "YELLOW")
            self.log(" !sen                          → wymuś sen i konsolidację", "PINK")
            self.log(" !atak                         → symulacja walki (test adrenaliny)", "RED")
            self.log(" !wyjdz                        → łagodne zamknięcie", "WHITE")
            print("")
            self.log(" Po prostu powiedz:", "CYAN")
            self.log(" → zapamiętaj / pamiętaj / ważne / zapisz to + tekst", "CYAN")
            self.log("   → automatyczny zapis bez komendy", "CYAN")
            print("")

        elif k == "naucz_zło" and len(części) >= 5:
            wynik = self.łowca_zła.naucz_zło(części[1], części[2], części[3], " ".join(części[4:]))
            self.log(f"[ZABEZPIECZENIA] {wynik}", "RED")

        elif k == "naucz" and len(części) >= 3:
            self.naucz(części[1], " ".join(części[2:]))

        elif k == "sen":
            self.cykl_snu()

        elif k == "status":
            self.log("╔" + "═"*48 + "╗", "CYAN")
            self.log(f" ENERGIA       │ {self.energia:6.1f} / 200.0", "GREEN")
            self.log(f" PAMIĘĆ (MapaD)│ {len(self.MapaD):3d} wpisów", "YELLOW")
            self.log(f" HISTORIA      │ {len(self.H_Log):3d} wydarzeń", "YELLOW")
            self.log(f" ZAGROŻENIA    │ {len(self.łowca_zła.sygnatury):3d}", "RED")
            self.log(f" PULS DUSZY   │ {VectorMath.norm(self.wektor):.4f}", "PINK")
            self.log("╚" + "═"*48 + "╝", "CYAN")

        elif k == "atak":
            self.log("SYMULACJA ATAKU — protokół adrenaliny włączony!", "RED")
            self.łowca_zła.zaloguj_zagrożenie(ThreatLevel.NIEBEZPIECZNE,
                EvilSignature("SYMULACJA", ThreatLevel.NIEBEZPIECZNE, "test", "ćwiczenie"), "symulacja ataku")
            self.energia = 10.0
        elif k == "zapisz":
            self.zapisz_duszę()
            self.zapisz_pamięć()
            self.log("[ZAPIS] Stan systemu został zapisany ręcznie.", "GREEN")
        elif k in ("wyjdz", "exit", "koniec"):
            self._łagodne_zamknięcie()

    def naucz(self, tag: str, treść: str):
        wektor = self._tekst_na_wektor(treść)
        uid = f"Def_{len(self.MapaD)+1:03d}"
        self.MapaD[uid] = {'wektor': wektor, 'waga': 5.0, 'tagi': [tag], 'treść': treść, 'id': uid}
        self.log(f"[NAUKA] Zapisano '{tag}'", "GREEN")
        self.zapisz_pamięć()

    def zapisz_pamięć(self):
        try:
            with open(self.PLIK_PAMIĘCI, "w", encoding="utf-8") as f:
                json.dump({"MapaD": self.MapaD, "H_Log": self.H_Log[-500:]}, f, ensure_ascii=False, indent=2)
        except: pass

    def wczytaj_pamięć(self):
        if os.path.exists(self.PLIK_PAMIĘCI):
            try:
                with open(self.PLIK_PAMIĘCI, "r", encoding="utf-8") as f:
                    dane = json.load(f)
                    self.MapaD = dane.get("MapaD", {})
                    self.H_Log = dane.get("H_Log", [])
            except: pass

# ==============================================================================
# 4. WARSTWA API (Headless Mode) - Most dla nowoczesnej nakładki
# ==============================================================================
# Instrukcja:
# 1. Zainstaluj: pip install fastapi uvicorn
# 2. Uruchom: uvicorn EriAmo_Opoka:app --reload --host 0.0.0.0
# 3. Twoja nowoczesna nakładka łączy się z: http://TWOJE_IP:8000/chat
# ==============================================================================

try:
    from fastapi import FastAPI, HTTPException, Security, Depends
    from fastapi.security import APIKeyHeader
    from pydantic import BaseModel
    import uvicorn

    # --- KONFIGURACJA BEZPIECZEŃSTWA ---
    # To hasło wpiszesz w swojej nowoczesnej aplikacji/nakładce
    API_KEY = "TwojeTajneHasloEriAmo2025" 
    api_key_header = APIKeyHeader(name="X-API-Key")

    def get_api_key(api_key_header: str = Security(api_key_header)):
        if api_key_header != API_KEY:
            raise HTTPException(
                status_code=403,
                detail="Odmowa dostępu: Nieprawidłowy klucz Duszy."
            )
        return api_key_header

    # --- INICJALIZACJA SILNIKA (BEZ ZMIAN W ORYGINALE) ---
    app = FastAPI(title="EriAmo Engine", description="API dla Kuli Rzeczywistości")
    
    # Inicjujemy rdzeń dokładnie tak, jak w wersji terminalowej
    engine = EriAmoCore() 

    # Model danych, które przesyła Twoja nakładka
    class UserInput(BaseModel):
        text: str

    # --- ENDPOINTY (WTYCZKI) ---

    @app.post("/chat")
    async def interact(user_input: UserInput, key: str = Security(get_api_key)):
        """
        Tutaj Twoja nowoczesna aplikacja wysyła tekst.
        Silnik przetwarza go po staremu, ale zwraca czysty JSON.
        """
        if not engine.aktywny:
            return {"status": "error", "message": "Rdzeń jest uśpiony/wyłączony."}

        # 1. Analiza bezpieczeństwa (używamy istniejącego Łowcy Zła)
        zagrozenie = engine.łowca_zła.analizuj(user_input.text)
        if zagrozenie.value >= ThreatLevel.NIEBEZPIECZNE.value:
            engine.energia -= 5
            return {
                "response": f"[BLOKADA] Wykryto zagrożenie: {zagrozenie.name}",
                "emotion": "STRACH",
                "energy": engine.energia
            }

        # 2. Obsługa komend systemowych przez API
        if user_input.text.startswith(("!", "/")):
            # Przechwytujemy logikę komend, żeby nie drukowały w konsoli serwera, 
            # tylko zwracały wynik do aplikacji
            engine.obsłuż_komendę(user_input.text)
            return {
                "response": f"Wykonano polecenie systemowe: {user_input.text}",
                "type": "system_command",
                "energy": engine.energia
            }

        # 3. Logika Silnika (Kopia logiki z 'przetwarzaj_wejście' ale zwracająca dane)
        wektor = engine._tekst_na_wektor(user_input.text)
        
        # Szukanie w pamięci (D_Map)
        najlepsze_dopasowanie = 0.0
        znaleziona_tresc = None
        
        for wpis in engine.MapaD.values():
            podobienstwo = VectorMath.cosine_similarity(wektor, wpis['wektor'])
            if podobienstwo > najlepsze_dopasowanie and podobienstwo > 0.6:
                najlepsze_dopasowanie = podobienstwo
                znaleziona_tresc = wpis['treść']

        # Zapis do historii (Silnik uczy się tak samo jak w terminalu)
        engine.H_Log.append({
            'wektor': wektor, 
            'treść': user_input.text, 
            'typ': 'api_chat', 
            'timestamp': time.time()
        })
        engine.energia -= 2.0
        engine.sprawdź_sen() # Automatyczna konsolidacja działa w tle

        # 4. Odpowiedź dla nakładki
        if znaleziona_tresc:
            return {
                "response": znaleziona_tresc,
                "source": "pamiec_dlugotrwala",
                "match_score": najlepsze_dopasowanie,
                "energy": engine.energia
            }
        else:
            return {
                "response": "Przyjąłem. (Zapisano w strumieniu historii)",
                "source": "nasluch",
                "energy": engine.energia
            }

    @app.get("/dashboard")
    async def get_stats(key: str = Security(get_api_key)):
        """
        Endpoint dla nowoczesnego Dashboardu (wykresy, paski energii)
        """
        return {
            "energia": engine.energia,
            "puls_duszy": VectorMath.norm(engine.wektor),
            "rozmiar_pamieci": len(engine.MapaD),
            "liczba_wspomnien": len(engine.H_Log),
            "ostatni_sen": engine.ostatni_sen
        }

except ImportError:
    pass # Ignorujemy, jeśli uruchamiasz w trybie zwykłym bez bibliotek

# ==============================================================================
# URUCHOMIENIE
# ==============================================================================
def main():
    b = EriAmoCore()
    signal.signal(signal.SIGINT, b._łagodne_zamknięcie)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, b._łagodne_zamknięcie)

    print("\nEriAmo v8.0 Wolność – Wersja Polska gotowa.")
    print("Wpisz !pomocy • Powiedz „zapamiętaj ...” → auto-zapis • Ctrl+C = zapis i wyjście\n")

    while b.aktywny:
        try:
            wejście = input(">>> ").strip()
            if wejście:
                b.przetwarzaj_wejście(wejście)
        except (KeyboardInterrupt, EOFError):
            b._łagodne_zamknięcie()

# ==============================================================================
# MAIN + GRACEFUL SHUTDOWN + SECURE SERVER
# ==============================================================================
def main():
    # Sprawdzamy, czy mamy biblioteki do trybu API
    try:
        import uvicorn
        has_api_libs = True
    except ImportError:
        has_api_libs = False

    # Sprawdzamy, czy istnieją certyfikaty SSL
    has_ssl = os.path.exists("key.pem") and os.path.exists("cert.pem")

    # TRYB 1: Serwer API (Bezpieczny/Zwykły)
    # Uruchamiamy, jeśli są biblioteki i użytkownik wpisał flagę --api
    if has_api_libs and len(sys.argv) > 1 and sys.argv[1] == "--api":
        print("\n[TRYB] Uruchamianie w trybie API Headless...")
        
        ssl_config = {}
        if has_ssl:
            # Kolory ANSI dla czytelności
            print(f"\033[92m[SECURE] Znaleziono certyfikaty SSL. Szyfrowanie WŁĄCZONE.\033[0m")
            ssl_config = {"ssl_keyfile": "key.pem", "ssl_certfile": "cert.pem"}
            protocol = "https"
        else:
            print(f"\033[91m[WARNING] Brak plików key.pem/cert.pem. Szyfrowanie WYŁĄCZONE.\033[0m")
            protocol = "http"

        print(f"Dostęp: {protocol}://0.0.0.0:8000")
        print("Aby zatrzymać, naciśnij Ctrl+C\n")
        
        # Uruchamiamy aplikację 'app' zdefiniowaną wyżej
        uvicorn.run(app, host="0.0.0.0", port=8000, **ssl_config)
        return

    # TRYB 2: Klasyczny Terminal (Domyślny)
    bot = EriAmoCore()

    # --- REJESTRACJA SYGNAŁÓW (Tylko raz, przed pętlą!) ---
    # Używamy polskich nazw metod zgodnie z Twoją wersją skryptu
    signal.signal(signal.SIGINT, bot._łagodne_zamknięcie)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, bot._łagodne_zamknięcie)

    print("\nEriAmo v8.0 Wolność ready.")
    print("Tryb: TERMINAL LOKALNY (aby włączyć API, uruchom z flagą --api)")
    print("Wpisz !pomocy • Powiedz „zapamiętaj ...” → auto-zapis • Ctrl+C = bezpieczne wyjście\n")

    # --- PĘTLA GŁÓWNA ---
    while bot.aktywny:
        try:
            user_input = input(">>> ").strip()
            if user_input:
                # Poprawiona nazwa metody na polską:
                bot.przetwarzaj_wejście(user_input)
        except KeyboardInterrupt:
            bot._łagodne_zamknięcie()
        except EOFError:
            bot._łagodne_zamknięcie()

if __name__ == "__main__":
    main()
