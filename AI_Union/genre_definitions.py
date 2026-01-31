# genre_definitions.py v2.0.0 [15-AXES MODEL]
# -*- coding: utf-8 -*-
"""
Definicje Gatunków Muzycznych EriAmo Union v2.0.0

Każdy gatunek jest zdefiniowany jako wektor 15-wymiarowy:
- Osie 0-7: Plutchik (radość, smutek, strach, gniew, miłość, wstręt, zaskoczenie, akceptacja)
- Osie 8-14: Metafizyczne (logika, wiedza, czas, kreacja, byt, przestrzeń, chaos)

Wartości w zakresie [-10, +10], gdzie:
- 0 = neutralny
- +10 = maksymalna obecność cechy
- -10 = maksymalna opozycja/brak cechy
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from union_config import AXES, DIMENSION


# ═══════════════════════════════════════════════════════════════════════════════
# INDEKSY OSI (dla czytelności)
# ═══════════════════════════════════════════════════════════════════════════════

# Plutchik
IDX_RADOSC = 0
IDX_SMUTEK = 1
IDX_STRACH = 2
IDX_GNIEW = 3
IDX_MILOSC = 4
IDX_WSTRET = 5
IDX_ZASKOCZENIE = 6
IDX_AKCEPTACJA = 7

# Metafizyczne
IDX_LOGIKA = 8
IDX_WIEDZA = 9
IDX_CZAS = 10
IDX_KREACJA = 11
IDX_BYT = 12
IDX_PRZESTRZEN = 13
IDX_CHAOS = 14


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINICJE GATUNKÓW (wektory 15D)
# ═══════════════════════════════════════════════════════════════════════════════

GENRE_DEFINITIONS: Dict[str, np.ndarray] = {
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MUZYKA KLASYCZNA
    # ═══════════════════════════════════════════════════════════════════════════
    
    "BAROQUE": np.array([
        2.0,   # radość (ornamentyka)
        0.0,   # smutek
        0.0,   # strach
        0.0,   # gniew
        1.0,   # miłość (piękno)
        0.0,   # wstręt
        1.0,   # zaskoczenie (kontrapunkt)
        3.0,   # akceptacja (porządek)
        7.0,   # logika (fuga, kontrapunkt)
        5.0,   # wiedza (tradycja)
        2.0,   # czas (allegro typowe)
        4.0,   # kreacja (ornamentyka)
        3.0,   # byt (instrumenty akustyczne)
        2.0,   # przestrzeń (kościoły)
        -3.0,  # chaos (porządek)
    ]),
    
    "KLASYCYZM": np.array([
        4.0,   # radość (harmonia, proporcje)
        0.0,   # smutek
        0.0,   # strach
        0.0,   # gniew
        2.0,   # miłość
        0.0,   # wstręt
        0.0,   # zaskoczenie
        5.0,   # akceptacja (równowaga)
        6.0,   # logika (forma sonatowa)
        4.0,   # wiedza
        3.0,   # czas (umiarkowane tempa)
        2.0,   # kreacja
        3.0,   # byt
        3.0,   # przestrzeń (sale koncertowe)
        -4.0,  # chaos (harmonia)
    ]),
    
    "ROMANTYZM": np.array([
        3.0,   # radość
        5.0,   # smutek (tęsknota)
        2.0,   # strach
        3.0,   # gniew (pasja)
        7.0,   # miłość (centralny motyw)
        0.0,   # wstręt
        3.0,   # zaskoczenie (dynamika)
        2.0,   # akceptacja
        3.0,   # logika
        5.0,   # wiedza (erudycja)
        4.0,   # czas (rubato, swoboda)
        6.0,   # kreacja (indywidualizm)
        4.0,   # byt (wielkie orkiestry)
        6.0,   # przestrzeń (symfoniczny rozmach)
        2.0,   # chaos (napięcia harmoniczne)
    ]),
    
    "IMPRESSIONISM": np.array([
        2.0,   # radość
        3.0,   # smutek (melancholia)
        0.0,   # strach
        0.0,   # gniew
        3.0,   # miłość (delikatność)
        0.0,   # wstręt
        4.0,   # zaskoczenie (barwy)
        4.0,   # akceptacja (kontemplacja)
        2.0,   # logika (rozmycie formy)
        4.0,   # wiedza
        -1.0,  # czas (zawieszenie)
        7.0,   # kreacja (nowatorstwo)
        2.0,   # byt
        8.0,   # przestrzeń (atmosfera, światło)
        1.0,   # chaos (ambiguity)
    ]),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # JAZZ
    # ═══════════════════════════════════════════════════════════════════════════
    
    "JAZZ_SWING": np.array([
        6.0,   # radość (energia)
        0.0,   # smutek
        0.0,   # strach
        0.0,   # gniew
        2.0,   # miłość
        0.0,   # wstręt
        3.0,   # zaskoczenie (improwizacja)
        4.0,   # akceptacja (groove)
        5.0,   # logika (harmonia)
        3.0,   # wiedza
        5.0,   # czas (swing rhythm)
        6.0,   # kreacja (improwizacja)
        4.0,   # byt (big band)
        3.0,   # przestrzeń
        2.0,   # chaos (spontaniczność)
    ]),
    
    "JAZZ_BEBOP": np.array([
        3.0,   # radość
        1.0,   # smutek
        0.0,   # strach
        2.0,   # gniew (intensywność)
        1.0,   # miłość
        0.0,   # wstręt
        5.0,   # zaskoczenie (złożoność)
        2.0,   # akceptacja
        7.0,   # logika (skomplikowana harmonia)
        5.0,   # wiedza (wirtuozeria)
        7.0,   # czas (szybkie tempa)
        8.0,   # kreacja (improwizacja solowa)
        3.0,   # byt (małe składy)
        2.0,   # przestrzeń
        4.0,   # chaos (chromatyzmy)
    ]),
    
    "JAZZ_COOL": np.array([
        2.0,   # radość
        3.0,   # smutek (melancholia)
        0.0,   # strach
        0.0,   # gniew
        3.0,   # miłość
        0.0,   # wstręt
        2.0,   # zaskoczenie
        5.0,   # akceptacja (relaks)
        5.0,   # logika
        4.0,   # wiedza
        -1.0,  # czas (laid back)
        5.0,   # kreacja
        3.0,   # byt
        4.0,   # przestrzeń (atmosfera)
        0.0,   # chaos
    ]),
    
    "FREE_JAZZ": np.array([
        2.0,   # radość
        2.0,   # smutek
        3.0,   # strach (niepokój)
        4.0,   # gniew (protest)
        1.0,   # miłość
        2.0,   # wstręt (konwencja)
        7.0,   # zaskoczenie (nieprzewidywalność)
        1.0,   # akceptacja
        -2.0,  # logika (odrzucenie formy)
        4.0,   # wiedza
        3.0,   # czas (nieregularny)
        9.0,   # kreacja (totalna wolność)
        4.0,   # byt (fizyczność gry)
        5.0,   # przestrzeń
        8.0,   # chaos (celowy)
    ]),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ROCK
    # ═══════════════════════════════════════════════════════════════════════════
    
    "ROCK_CLASSIC": np.array([
        5.0,   # radość (energia)
        1.0,   # smutek
        0.0,   # strach
        3.0,   # gniew (bunt)
        2.0,   # miłość
        0.0,   # wstręt
        2.0,   # zaskoczenie
        3.0,   # akceptacja
        3.0,   # logika (riff-based)
        2.0,   # wiedza
        5.0,   # czas (driving beat)
        4.0,   # kreacja
        6.0,   # byt (głośność, fizyczność)
        3.0,   # przestrzeń
        2.0,   # chaos
    ]),
    
    "PROG_ROCK": np.array([
        3.0,   # radość
        2.0,   # smutek
        1.0,   # strach
        1.0,   # gniew
        2.0,   # miłość
        0.0,   # wstręt
        6.0,   # zaskoczenie (zmienne metrum)
        3.0,   # akceptacja
        7.0,   # logika (złożone struktury)
        6.0,   # wiedza (koncepcje)
        4.0,   # czas (zmienne)
        8.0,   # kreacja (eksperyment)
        5.0,   # byt
        6.0,   # przestrzeń (epickość)
        3.0,   # chaos (kontrolowany)
    ]),
    
    "PUNK_ROCK": np.array([
        3.0,   # radość (energia)
        1.0,   # smutek
        1.0,   # strach
        7.0,   # gniew (bunt, protest)
        0.0,   # miłość
        3.0,   # wstręt (anty-establishment)
        2.0,   # zaskoczenie
        -1.0,  # akceptacja (odrzucenie)
        -2.0,  # logika (prostota)
        1.0,   # wiedza (DIY)
        7.0,   # czas (szybko)
        3.0,   # kreacja (surowa)
        7.0,   # byt (raw energy)
        1.0,   # przestrzeń (kluby)
        5.0,   # chaos
    ]),
    
    "HEAVY_METAL": np.array([
        2.0,   # radość
        2.0,   # smutek
        4.0,   # strach (mroczne tematy)
        7.0,   # gniew (agresja)
        0.0,   # miłość
        3.0,   # wstręt
        3.0,   # zaskoczenie
        1.0,   # akceptacja
        4.0,   # logika (riffy)
        3.0,   # wiedza
        6.0,   # czas (szybko)
        5.0,   # kreacja
        8.0,   # byt (ciężar, głośność)
        4.0,   # przestrzeń
        4.0,   # chaos
    ]),
    
    "POWER_METAL": np.array([
        7.0,   # radość (triumf)
        1.0,   # smutek
        1.0,   # strach
        3.0,   # gniew (energia)
        3.0,   # miłość (heroizm)
        0.0,   # wstręt
        3.0,   # zaskoczenie
        6.0,   # akceptacja (chwała)
        5.0,   # logika
        4.0,   # wiedza (fantasy)
        7.0,   # czas (szybko)
        5.0,   # kreacja
        6.0,   # byt
        7.0,   # przestrzeń (epickość)
        2.0,   # chaos
    ]),
    
    "BLACK_METAL": np.array([
        -2.0,  # radość (anty)
        4.0,   # smutek
        7.0,   # strach (przerażenie)
        6.0,   # gniew
        -3.0,  # miłość (anty)
        7.0,   # wstręt (transgresja)
        4.0,   # zaskoczenie
        -4.0,  # akceptacja (odrzucenie)
        2.0,   # logika
        3.0,   # wiedza (okultyzm)
        8.0,   # czas (blast beats)
        6.0,   # kreacja
        6.0,   # byt (surowy dźwięk)
        5.0,   # przestrzeń (atmosfera)
        8.0,   # chaos
    ]),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ELEKTRONIKA
    # ═══════════════════════════════════════════════════════════════════════════
    
    "TECHNO": np.array([
        3.0,   # radość
        0.0,   # smutek
        1.0,   # strach (industrial)
        2.0,   # gniew
        0.0,   # miłość
        0.0,   # wstręt
        3.0,   # zaskoczenie
        3.0,   # akceptacja (trans)
        5.0,   # logika (repetycja)
        2.0,   # wiedza
        6.0,   # czas (driving)
        6.0,   # kreacja
        -2.0,  # byt (syntetyczny)
        4.0,   # przestrzeń
        2.0,   # chaos
    ]),
    
    "AMBIENT": np.array([
        2.0,   # radość
        3.0,   # smutek (melancholia)
        1.0,   # strach (niepokój)
        0.0,   # gniew
        2.0,   # miłość
        0.0,   # wstręt
        2.0,   # zaskoczenie
        6.0,   # akceptacja (medytacja)
        2.0,   # logika
        3.0,   # wiedza
        -3.0,  # czas (zawieszenie)
        5.0,   # kreacja
        -1.0,  # byt (eteryczny)
        9.0,   # przestrzeń (maksymalna)
        1.0,   # chaos
    ]),
    
    "DRUM_AND_BASS": np.array([
        4.0,   # radość
        1.0,   # smutek
        2.0,   # strach (napięcie)
        3.0,   # gniew
        1.0,   # miłość
        0.0,   # wstręt
        5.0,   # zaskoczenie (breaks)
        2.0,   # akceptacja
        4.0,   # logika
        2.0,   # wiedza
        8.0,   # czas (wysokie BPM)
        6.0,   # kreacja
        3.0,   # byt (bass)
        5.0,   # przestrzeń
        4.0,   # chaos
    ]),
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INNE
    # ═══════════════════════════════════════════════════════════════════════════
    
    "BLUES": np.array([
        2.0,   # radość
        6.0,   # smutek (ból)
        1.0,   # strach
        2.0,   # gniew
        5.0,   # miłość (tęsknota)
        0.0,   # wstręt
        1.0,   # zaskoczenie
        3.0,   # akceptacja (pogodzenie)
        2.0,   # logika (12-taktowa forma)
        3.0,   # wiedza (tradycja)
        -1.0,  # czas (laid back)
        4.0,   # kreacja (improwizacja)
        6.0,   # byt (autentyczność)
        2.0,   # przestrzeń
        1.0,   # chaos
    ]),
    
    "REGGAE": np.array([
        5.0,   # radość (positive vibes)
        2.0,   # smutek (narzekanie)
        0.0,   # strach
        2.0,   # gniew (protest)
        4.0,   # miłość
        0.0,   # wstręt
        1.0,   # zaskoczenie
        7.0,   # akceptacja (Jah, pokój)
        2.0,   # logika
        3.0,   # wiedza (Rastafari)
        -2.0,  # czas (offbeat, laid back)
        3.0,   # kreacja
        4.0,   # byt
        3.0,   # przestrzeń (reverb)
        1.0,   # chaos
    ]),
    
    "FOLK": np.array([
        4.0,   # radość
        3.0,   # smutek (ballady)
        0.0,   # strach
        1.0,   # gniew
        4.0,   # miłość
        0.0,   # wstręt
        1.0,   # zaskoczenie
        6.0,   # akceptacja (tradycja)
        2.0,   # logika (proste formy)
        6.0,   # wiedza (dziedzictwo)
        2.0,   # czas
        2.0,   # kreacja
        7.0,   # byt (akustyczny, autentyczny)
        2.0,   # przestrzeń
        0.0,   # chaos
    ]),
    
    "SACRED": np.array([
        3.0,   # radość (duchowa)
        2.0,   # smutek (pokora)
        2.0,   # strach (sacrum)
        0.0,   # gniew
        5.0,   # miłość (agape)
        0.0,   # wstręt
        2.0,   # zaskoczenie (mistycyzm)
        8.0,   # akceptacja (wiara)
        3.0,   # logika (liturgia)
        5.0,   # wiedza (teologia)
        -1.0,  # czas (kontemplacja)
        3.0,   # kreacja
        3.0,   # byt (chóry)
        7.0,   # przestrzeń (katedry)
        -4.0,  # chaos (porządek boski)
    ]),
}


# ═══════════════════════════════════════════════════════════════════════════════
# FUNKCJE POMOCNICZE
# ═══════════════════════════════════════════════════════════════════════════════

def get_genre_vector(genre_name: str) -> Optional[np.ndarray]:
    """
    Zwraca wektor 15D dla danego gatunku.
    
    Args:
        genre_name: Nazwa gatunku (case-insensitive)
        
    Returns:
        np.ndarray lub None jeśli gatunek nieznany
    """
    key = genre_name.upper().replace(" ", "_").replace("-", "_")
    return GENRE_DEFINITIONS.get(key)


def list_all_genres() -> List[str]:
    """Zwraca listę wszystkich zdefiniowanych gatunków."""
    return sorted(GENRE_DEFINITIONS.keys())


def find_similar_genres(target_vector: np.ndarray, top_n: int = 5) -> List[Tuple[str, float]]:
    """
    Znajduje gatunki najbardziej podobne do podanego wektora.
    
    Args:
        target_vector: Wektor 15D do porównania
        top_n: Ile gatunków zwrócić
        
    Returns:
        Lista krotek (nazwa_gatunku, podobieństwo_cosinusowe)
    """
    similarities = []
    target_norm = np.linalg.norm(target_vector)
    
    if target_norm < 0.01:
        return []
    
    for name, vec in GENRE_DEFINITIONS.items():
        vec_norm = np.linalg.norm(vec)
        if vec_norm > 0.01:
            cos_sim = np.dot(target_vector, vec) / (target_norm * vec_norm)
            similarities.append((name, cos_sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]


def get_genre_profile(genre_name: str) -> Optional[dict]:
    """
    Zwraca szczegółowy profil gatunku.
    
    Args:
        genre_name: Nazwa gatunku
        
    Returns:
        dict z profilem lub None
    """
    vec = get_genre_vector(genre_name)
    if vec is None:
        return None
    
    # Znajdź dominujące cechy
    dominant_indices = np.argsort(np.abs(vec))[::-1][:5]
    
    return {
        'name': genre_name.upper(),
        'vector': vec,
        'dominant_axes': [(AXES[i], vec[i]) for i in dominant_indices],
        'energy': float(np.linalg.norm(vec)),
        'plutchik_sum': float(vec[:8].sum()),
        'metaphysical_sum': float(vec[8:].sum()),
    }


def blend_genres(genres: List[str], weights: List[float] = None) -> np.ndarray:
    """
    Miksuje wiele gatunków w jeden wektor.
    
    Args:
        genres: Lista nazw gatunków
        weights: Opcjonalne wagi (domyślnie równe)
        
    Returns:
        np.ndarray: Zmiksowany wektor 15D
    """
    vectors = [get_genre_vector(g) for g in genres]
    vectors = [v for v in vectors if v is not None]
    
    if not vectors:
        return np.zeros(DIMENSION)
    
    if weights is None:
        weights = [1.0] * len(vectors)
    
    # Normalizuj wagi
    total = sum(weights[:len(vectors)])
    weights = [w / total for w in weights[:len(vectors)]]
    
    result = np.zeros(DIMENSION)
    for vec, w in zip(vectors, weights):
        result += vec * w
    
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("TEST: Genre Definitions v2.0.0 (15 osi)")
    print("=" * 60)
    
    # Lista gatunków
    print(f"\nZdefiniowane gatunki ({len(GENRE_DEFINITIONS)}):")
    for g in list_all_genres():
        print(f"  • {g}")
    
    # Profil gatunku
    print("\n--- Profil JAZZ_BEBOP ---")
    profile = get_genre_profile("jazz_bebop")
    if profile:
        print(f"Energia: {profile['energy']:.2f}")
        print("Dominujące osie:")
        for axis, val in profile['dominant_axes']:
            print(f"  {axis:12s}: {val:+5.1f}")
    
    # Podobne gatunki
    print("\n--- Gatunki podobne do HEAVY_METAL ---")
    hm_vec = get_genre_vector("heavy_metal")
    if hm_vec is not None:
        similar = find_similar_genres(hm_vec)
        for name, sim in similar:
            print(f"  {name:20s}: {sim:.3f}")
    
    # Blend
    print("\n--- Blend: JAZZ_SWING + BLUES ---")
    blend = blend_genres(["jazz_swing", "blues"])
    print(f"Wektor: {blend[:5]}... (pierwszych 5 wartości)")
    
    print("\n✅ Testy genre_definitions zakończone!")