# genre_definitions.py v8.1.0 (Migrated)
# -*- coding: utf-8 -*-
"""
Definicje Gatunków Muzycznych EriAmo v8.1.0

Zaktualizowane do architektury 15-osiowej (UnionConfig).
Mapowanie starych pojęć na nowe osie:
- affections/emocje -> Konkretne osie biologiczne (Radość, Smutek, Gniew...)
- etyka -> Byt/Akceptacja
- logika, czas, kreacja -> Bez zmian
"""

GENRE_DEFINITIONS = {
    
    # === FORMY KLASYCZNE ===
    
    "MENUET": {
        "opis": "Taniec barokowy w metrum 3/4. Elegancki, symetryczny.",
        "f_intencja_wektor": {
            "logika": 0.4,       # Struktura
            "radość": 0.3,       # Delikatna pogoda ducha
            "akceptacja": 0.2,   # Dworska etykieta
            "czas": 0.2,         # Umiarkowane tempo
            "wiedza": 0.4,       # Forma
            "kreacja": 0.3
        }
    },
    
    "KANON": {
        "opis": "Ścisła polifonia imitacyjna. Logika jako fundament.",
        "f_intencja_wektor": {
            "logika": 0.9,       # Dominanta absolutna
            "wiedza": 0.6,       # Kontrapunkt
            "akceptacja": 0.2,   # Harmonia współbrzmienia
            "czas": 0.2,
            "kreacja": 0.4
        }
    },
    
    "FUGA": {
        "opis": "Złożona forma polifoniczna z tematem i odpowiedziami.",
        "f_intencja_wektor": {
            "logika": 1.0,       # Szczyt intelektu
            "wiedza": 0.7,
            "kreacja": 0.5,
            "akceptacja": 0.3,   # Satysfakcja z rozwiązania
            "czas": 0.1
        }
    },
    
    "MARSZ": {
        "opis": "Silny puls w metrum 4/4. Wojskowy charakter.",
        "f_intencja_wektor": {
            "logika": 0.3,
            "czas": 0.7,         # Rytm jest kluczowy
            "gniew": 0.4,        # Agresja/Siła
            "akceptacja": 0.3,   # Dyscyplina/Duma
            "kreacja": 0.2
        }
    },
    
    # === EKSPRESJA EMOCJONALNA ===
    
    "LAMENT": {
        "opis": "Pieśń żałobna. Chromatyka, opadające linie melodyczne.",
        "f_intencja_wektor": {
            "smutek": 0.9,       # Głęboki żal
            "czas": 0.1,         # Zatrzymanie czasu
            "kreacja": 0.5,      # Ekspresja bólu
            "przestrzeń": 0.3,   # Pustka
            "byt": 0.4           # Refleksja nad istnieniem
        }
    },
    
    "REQUIEM": {
        "opis": "Msza żałobna. Wzniosłość i transcendencja.",
        "f_intencja_wektor": {
            "smutek": 0.7,
            "byt": 0.6,          # Sprawy ostateczne (Etyka/Śmierć)
            "przestrzeń": 0.6,   # Sakralność/Katedra
            "wiedza": 0.4,       # Liturgia
            "akceptacja": 0.5    # Pogodzenie się
        }
    },
    
    "EKSTAZA": {
        "opis": "Muzyka transowa, ekstaza duchowa.",
        "f_intencja_wektor": {
            "radość": 0.8,       # Euforia
            "miłość": 0.5,       # Uniesienie
            "przestrzeń": 0.5,   # Wyjście poza ciało
            "kreacja": 0.6,
            "chaos": 0.3         # Utrata kontroli
        }
    },
    
    # === GATUNKI POPULARNE ===
    
    "BLUES": {
        "opis": "12-taktowy blues. Melancholia i autentyczność.",
        "f_intencja_wektor": {
            "logika": 0.4,       # Schemat 12-taktowy
            "czas": 0.3,         # Swingujący puls
            "smutek": 0.6,       # Blues feeling
            "byt": 0.4,          # Życiowa prawda
            "akceptacja": 0.3    # Pogodzenie z losem
        }
    },
    
    "ROCK_AND_ROLL": {
        "opis": "Klasyczny Rock'n'Roll. Energia i bunt.",
        "f_intencja_wektor": {
            "czas": 0.8,         # Energia kinetyczna
            "radość": 0.7,       # Zabawa
            "kreacja": 0.4,
            "chaos": 0.3,        # Odrobina szaleństwa
            "logika": 0.2
        }
    },
    
    "HEAVY_METAL": {
        "opis": "Ciężki metal. Agresja i moc.",
        "f_intencja_wektor": {
            "gniew": 0.8,        # Agresja
            "strach": 0.3,       # Mrok
            "czas": 0.6,         # Szybkość/Ciężar
            "logika": 0.4,       # Techniczne riffy
            "kreacja": 0.5
        }
    },
    
    "PUNK": {
        "opis": "Punk rock. Surowy, szybki, buntowniczy.",
        "f_intencja_wektor": {
            "gniew": 0.7,        # Bunt
            "wstręt": 0.4,       # Antysystemowość
            "chaos": 0.6,        # Brudne brzmienie
            "czas": 0.8,         # Szybkość
            "logika": 0.1        # Prostota
        }
    },
    
    "JAZZ": {
        "opis": "Jazz. Improwizacja i złożoność harmoniczna.",
        "f_intencja_wektor": {
            "logika": 0.6,       # Harmonia
            "kreacja": 0.9,      # Improwizacja
            "chaos": 0.4,        # Nieprzewidywalność
            "wiedza": 0.5,
            "radość": 0.3        # Swing
        }
    },
    
    "POP": {
        "opis": "Muzyka popularna. Przystępność i chwytliwość.",
        "f_intencja_wektor": {
            "radość": 0.6,       # Chwytliwość
            "akceptacja": 0.5,   # Mainstream
            "logika": 0.2,       # Prosta forma
            "czas": 0.4,
            "kreacja": 0.2
        }
    },
    
    # === MUZYKA WSPÓŁCZESNA / EKSPERYMENTALNA ===
    
    "AMBIENT": {
        "opis": "Muzyka otoczenia. Przestrzeń i tekstura.",
        "f_intencja_wektor": {
            "przestrzeń": 0.9,   # Dominanta
            "czas": 0.1,         # Bezczas
            "akceptacja": 0.5,   # Spokój
            "logika": 0.1,
            "kreacja": 0.6
        }
    },
    
    "MINIMALIZM": {
        "opis": "Minimalizm. Powtarzalność i subtelna ewolucja.",
        "f_intencja_wektor": {
            "logika": 0.7,       # Pętle
            "czas": 0.5,         # Trans
            "kreacja": 0.5,
            "akceptacja": 0.4,   # Zgoda na powtarzalność
            "emocje": 0.0        # Neutralność (brak silnych osi bio)
        }
    },
    
    "ELEKTRONIKA": {
        "opis": "Muzyka elektroniczna. Syntezatory i beat.",
        "f_intencja_wektor": {
            "kreacja": 0.7,      # Synteza dźwięku
            "logika": 0.5,       # Sekwencery
            "czas": 0.6,         # Grid rytmiczny
            "przestrzeń": 0.6,   # Sztuczne pogłosy
            "wiedza": 0.4
        }
    },
    
    # === MUZYKA TRADYCYJNA / REGIONALNA ===
    
    "FOLK": {
        "opis": "Muzyka ludowa. Tradycja i prostota.",
        "f_intencja_wektor": {
            "wiedza": 0.4,       # Tradycja
            "byt": 0.5,          # Korzenie/Wspólnota
            "radość": 0.4,       # Taniec
            "smutek": 0.3,       # Nostalgia
            "logika": 0.2
        }
    },
    
    "TANGO": {
        "opis": "Argentyńskie tango. Pasja i dramat.",
        "f_intencja_wektor": {
            "miłość": 0.7,       # Namiętność
            "gniew": 0.4,        # Napięcie
            "czas": 0.5,         # Rytm
            "kreacja": 0.5,
            "przestrzeń": 0.3
        }
    },
    
    "WALC": {
        "opis": "Walc wiedeński. Elegancja w 3/4.",
        "f_intencja_wektor": {
            "czas": 0.6,         # Wirowanie
            "miłość": 0.4,       # Romantyzm
            "radość": 0.3,
            "logika": 0.3,
            "przestrzeń": 0.4    # Sala balowa
        }
    }
}

def get_genre_info(genre_name: str) -> dict:
    """Zwraca informacje o gatunku (kompatybilne z v8.1)."""
    return GENRE_DEFINITIONS.get(genre_name.upper(), None)

def list_genres() -> list:
    """Zwraca listę wszystkich gatunków."""
    return list(GENRE_DEFINITIONS.keys())

def get_genres_by_axis(axis: str, threshold: float = 0.5) -> list:
    """
    Filtruje gatunki, które silnie stymulują daną oś v8.1.
    """
    result = []
    for name, data in GENRE_DEFINITIONS.items():
        val = data['f_intencja_wektor'].get(axis, 0.0)
        if val >= threshold:
            result.append(name)
    return result