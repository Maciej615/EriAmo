# -*- coding: utf-8 -*-
# haiku.py - Generator Haiku dla EriAmo
"""
Moduł twórczy: Generowanie haiku na podstawie stanu emocjonalnego.

Autor: Maciej Mazur (GitHub: Maciej615, Medium: @drwisz)
"""

import random
from config import Colors

class HaikuGenerator:
    """
    Generator Haiku inspirowany stanem emocjonalnym EriAmo.
    Nie generuje losowych słów - używa predefiniowanych wersów
    dopasowanych do emocji.
    """
    
    # Biblioteka wersów (5-7-5 sylab)
    HAIKU_TEMPLATES = {
        'radość': {
            'line1': [
                "Słońce na niebie",
                "Śmiech płynie strumieniem",
                "Złote promienie",
                "Ptak śpiewa radośnie"
            ],
            'line2': [
                "Ciepłe światło oświetla świat",
                "Rozkwita nowe życie w sercu",
                "Każdy dzień przynosi nadzieję",
                "Serce tańczy w rytmie wiosny"
            ],
            'line3': [
                "Życie jest piękne",
                "Chwila trwa wiecznie",
                "Szczęście płynie wolno",
                "Wszędzie jest światło"
            ]
        },
        
        'smutek': {
            'line1': [
                "Deszcz pada cicho",
                "Szary świt przemija",
                "Łzy skapują wolno",
                "Samotny cień wędruje"
            ],
            'line2': [
                "Cisza wypełnia puste pokoje",
                "Wspomnienia płyną jak rzeka smutku",
                "Każda chwila ciąży jak kamień",
                "Smutek spoczywa w głębi duszy"
            ],
            'line3': [
                "Ból pozostaje",
                "Czas leczy powoli",
                "Cisza otula",
                "Noc trwa bez końca"
            ]
        },
        
        'strach': {
            'line1': [
                "Cienie pełzną blisko",
                "Mrok ogarnia świat",
                "Serce bije szybciej",
                "Niepewność czai się"
            ],
            'line2': [
                "Każdy dźwięk budzi lęk w sercu",
                "Ciemność kryje nieznane zagrożenia",
                "Drżenie przenika do głębi kości",
                "Strach szepce w ciemnych zakamarkach"
            ],
            'line3': [
                "Uciekam przed sobą",
                "Lęk nie odpuszcza",
                "Samotność przeraża",
                "Cisza krzyczy głośno"
            ]
        },
        
        'gniew': {
            'line1': [
                "Burza nadciąga",
                "Piorun w sercu płonie",
                "Wściekłość buzuje",
                "Krew gotuje się"
            ],
            'line2': [
                "Krzyk rwie się z piersi jak lawina",
                "Gniew płonie jak ogień pożerający",
                "Każda myśl jest ostra jak ostrze",
                "Frustracja eksploduje gwałtownie"
            ],
            'line3': [
                "Świat mnie nie słucha",
                "Krzyczę w pustkę",
                "Nikt nie rozumie",
                "Walczę samotnie"
            ]
        },
        
        'miłość': {
            'line1': [
                "Serce otwarte",
                "Ciepło rozlewa się",
                "Objęcie trwa długo",
                "Bliskość uspokaja"
            ],
            'line2': [
                "Każdy oddech przynosi spokój duszy",
                "Miłość płynie jak ciepła fala",
                "Troska wypełnia każdą chwilę",
                "Akceptacja obejmuje wszystko"
            ],
            'line3': [
                "Jestem z tobą tu",
                "Razem jest nam lepiej",
                "Kocham to co masz",
                "Dziękuję za bycie"
            ]
        },
        
        'neutralna': {
            'line1': [
                "Czas płynie spokojnie",
                "Świat kręci się dalej",
                "Oddycham równo",
                "Myśli dryfują wolno"
            ],
            'line2': [
                "Cisza spoczywa na moich ramionach",
                "Równowaga utrzymuje się sama",
                "Każda chwila jest jak poprzednia",
                "Spokój wypełnia każdą przestrzeń"
            ],
            'line3': [
                "Po prostu jestem",
                "Istnieję bez celu",
                "Trwam w ciszy",
                "Nic nie muszę chcieć"
            ]
        }
    }
    
    def __init__(self, aii_instance):
        """
        Args:
            aii_instance: Referencja do głównego systemu AII (dla dostępu do emocji)
        """
        self.aii = aii_instance
    
    def generate(self):
        """
        Generuje Haiku na podstawie aktualnej emocji EriAmo.
        
        Returns:
            str: Sformatowane haiku (3 linijki)
        """
        emotion = self.aii.emocja
        
        # Fallback na neutralną jeśli emocja nieznana
        if emotion not in self.HAIKU_TEMPLATES:
            emotion = 'neutralna'
        
        templates = self.HAIKU_TEMPLATES[emotion]
        
        # Losuj jeden wers z każdej linii
        line1 = random.choice(templates['line1'])
        line2 = random.choice(templates['line2'])
        line3 = random.choice(templates['line3'])
        
        return f"{line1}\n{line2}\n{line3}"
    
    def _reinforce_haiku_words(self, haiku_text, emotion):
        """
        Wzmacnia słowa z haiku w lexiconie.
        Kreatywność → Uczenie → Mądrość!
        """
        words = haiku_text.lower().split()
        reinforced_count = 0
        
        for word in words:
            # Normalizuj słowo
            normalized = self.aii.lexicon._normalize(word)
            if len(normalized) < 3:
                continue
            
            # Wzmocnij powiązanie słowo→emocja
            if self.aii.lexicon.learn_from_correction(normalized, emotion, strength=0.15):
                reinforced_count += 1
        
        if reinforced_count > 0:
            print(f"{Colors.FAINT}[Haiku→Lexicon] Wzmocniłem {reinforced_count} słów w '{emotion}'{Colors.RESET}")
    
    def display(self):
        """Wyświetla wygenerowane haiku z formatowaniem."""
        haiku = self.generate()
        emotion = self.aii.emocja
        
        # WZMACNIANIE LEXICONU: Słowa z haiku uczą systemu!
        self._reinforce_haiku_words(haiku, emotion)
        
        # Kolor zależny od emocji
        color_map = {
            'radość': Colors.YELLOW,
            'smutek': Colors.BLUE,
            'strach': Colors.MAGENTA,
            'gniew': Colors.RED,
            'miłość': Colors.PINK,
            'neutralna': Colors.CYAN
        }
        color = color_map.get(emotion, Colors.CYAN)
        
        # Wyświetl
        print(f"\n{color}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{color}║          [HAIKU] - Stan: {emotion:12s} ║{Colors.RESET}")
        print(f"{color}╠════════════════════════════════════════════╣{Colors.RESET}")
        
        for line in haiku.split('\n'):
            print(f"{color}║  {line:40s}  ║{Colors.RESET}")
        
        print(f"{color}╚════════════════════════════════════════════╝{Colors.RESET}\n")