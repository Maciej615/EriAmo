# -*- coding: utf-8 -*-
"""
axes_adapter.py v1.0.0
Adapter między modelem 15-osiowym (AII) a 9-osiowym (Music System).

Problem:
- AII używa 15 osi (8 Plutchik + 7 metafizycznych)
- System muzyczny (amocore) używa 9 osi (logika, emocje, affections, ...)

Rozwiązanie:
Ten adapter konwertuje wektory między modelami.
"""

import numpy as np
from typing import Dict, List

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINICJE MODELI
# ═══════════════════════════════════════════════════════════════════════════════

# Model 15-osiowy (AII - union_config.py)
AXES_15 = [
    'radość', 'smutek', 'strach', 'gniew',
    'miłość', 'wstręt', 'zaskoczenie', 'akceptacja',
    'logika', 'wiedza', 'czas', 'kreacja',
    'byt', 'przestrzeń', 'chaos'
]

# Model 9-osiowy (Music System - amocore.py)
AXES_9 = [
    'logika', 'emocje', 'affections', 'wiedza',
    'czas', 'kreacja', 'byt', 'przestrzen', 'etyka'
]

# Indeksy
IDX_15 = {axis: i for i, axis in enumerate(AXES_15)}
IDX_9 = {axis: i for i, axis in enumerate(AXES_9)}


# ═══════════════════════════════════════════════════════════════════════════════
# MAPOWANIE 15 → 9
# ═══════════════════════════════════════════════════════════════════════════════

def convert_15_to_9(vec_15: np.ndarray) -> np.ndarray:
    """
    Konwertuje wektor 15-osiowy na 9-osiowy.
    
    Mapowanie:
    - logika → logika (bezpośrednio)
    - wiedza → wiedza (bezpośrednio)
    - czas → czas (bezpośrednio)
    - kreacja → kreacja (bezpośrednio)
    - byt → byt (bezpośrednio)
    - przestrzeń → przestrzen (bezpośrednio)
    
    - radość, smutek, strach, gniew → emocje (suma/średnia)
    - miłość, akceptacja → affections (suma/średnia)
    - chaos → etyka (odwrócona skala)
    """
    if len(vec_15) != 15:
        raise ValueError(f"Oczekiwano 15 wymiarów, otrzymano {len(vec_15)}")
    
    vec_9 = np.zeros(9)
    
    # Bezpośrednie mapowania
    vec_9[IDX_9['logika']] = vec_15[IDX_15['logika']]
    vec_9[IDX_9['wiedza']] = vec_15[IDX_15['wiedza']]
    vec_9[IDX_9['czas']] = vec_15[IDX_15['czas']]
    vec_9[IDX_9['kreacja']] = vec_15[IDX_15['kreacja']]
    vec_9[IDX_9['byt']] = vec_15[IDX_15['byt']]
    vec_9[IDX_9['przestrzen']] = vec_15[IDX_15['przestrzeń']]
    
    # Agregacje emocji Plutchika
    # emocje = średnia z radość, smutek, strach, gniew (emocje podstawowe)
    basic_emotions = [
        vec_15[IDX_15['radość']],
        vec_15[IDX_15['smutek']],
        vec_15[IDX_15['strach']],
        vec_15[IDX_15['gniew']]
    ]
    # Znak: radość dodatnia, reszta ujemna
    vec_9[IDX_9['emocje']] = (
        vec_15[IDX_15['radość']] 
        - vec_15[IDX_15['smutek']] * 0.5
        - vec_15[IDX_15['strach']] * 0.3
        - vec_15[IDX_15['gniew']] * 0.2
    )
    
    # affections = miłość + akceptacja (głębokie uczucia)
    vec_9[IDX_9['affections']] = (
        vec_15[IDX_15['miłość']] * 0.7 +
        vec_15[IDX_15['akceptacja']] * 0.3
    )
    
    # etyka = odwrotność chaosu + wpływ wstrętu (moralność)
    vec_9[IDX_9['etyka']] = (
        (1.0 - vec_15[IDX_15['chaos']]) * 0.6 +
        vec_15[IDX_15['wstręt']] * 0.2 +  # Wstręt moralny
        vec_15[IDX_15['akceptacja']] * 0.2
    )
    
    return vec_9


def convert_9_to_15(vec_9: np.ndarray) -> np.ndarray:
    """
    Konwertuje wektor 9-osiowy na 15-osiowy.
    
    UWAGA: Ta konwersja jest stratna - nie da się odtworzyć
    pełnej informacji o 8 emocjach z jednej osi 'emocje'.
    """
    if len(vec_9) != 9:
        raise ValueError(f"Oczekiwano 9 wymiarów, otrzymano {len(vec_9)}")
    
    vec_15 = np.zeros(15)
    
    # Bezpośrednie mapowania
    vec_15[IDX_15['logika']] = vec_9[IDX_9['logika']]
    vec_15[IDX_15['wiedza']] = vec_9[IDX_9['wiedza']]
    vec_15[IDX_15['czas']] = vec_9[IDX_9['czas']]
    vec_15[IDX_15['kreacja']] = vec_9[IDX_9['kreacja']]
    vec_15[IDX_15['byt']] = vec_9[IDX_9['byt']]
    vec_15[IDX_15['przestrzeń']] = vec_9[IDX_9['przestrzen']]
    
    # Rozłożenie 'emocje' na Plutchika
    emocje = vec_9[IDX_9['emocje']]
    if emocje >= 0:
        vec_15[IDX_15['radość']] = emocje
        vec_15[IDX_15['smutek']] = 0
    else:
        vec_15[IDX_15['radość']] = 0
        vec_15[IDX_15['smutek']] = abs(emocje)
    
    # Rozłożenie 'affections'
    affections = vec_9[IDX_9['affections']]
    vec_15[IDX_15['miłość']] = affections * 0.7
    vec_15[IDX_15['akceptacja']] = affections * 0.3
    
    # Rozłożenie 'etyka'
    etyka = vec_9[IDX_9['etyka']]
    vec_15[IDX_15['chaos']] = 1.0 - etyka  # Odwrotność
    
    return vec_15


def get_emotion_from_15(vec_15: np.ndarray) -> Dict[str, float]:
    """
    Zwraca słownik emocji z wektora 15-osiowego.
    Kompatybilny z AII.get_emotions()
    """
    return {axis: float(vec_15[i]) for i, axis in enumerate(AXES_15)}


def get_music_state_from_9(vec_9: np.ndarray) -> Dict[str, float]:
    """
    Zwraca słownik stanu muzycznego z wektora 9-osiowego.
    Kompatybilny z amocore/music_analyzer.
    """
    return {axis: float(vec_9[i]) for i, axis in enumerate(AXES_9)}


# ═══════════════════════════════════════════════════════════════════════════════
# TEST
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== TEST ADAPTERA OSI ===\n")
    
    # Test 15 → 9
    vec_15 = np.array([
        0.8, 0.1, 0.2, 0.1,  # radość, smutek, strach, gniew
        0.6, 0.1, 0.3, 0.5,  # miłość, wstręt, zaskoczenie, akceptacja
        0.7, 0.5, 0.4, 0.6,  # logika, wiedza, czas, kreacja
        0.5, 0.4, 0.2        # byt, przestrzeń, chaos
    ])
    
    print("Wektor 15D:")
    for i, axis in enumerate(AXES_15):
        print(f"  {axis:12s}: {vec_15[i]:.2f}")
    
    vec_9 = convert_15_to_9(vec_15)
    
    print("\nWektor 9D (skonwertowany):")
    for i, axis in enumerate(AXES_9):
        print(f"  {axis:12s}: {vec_9[i]:.2f}")
    
    # Test 9 → 15
    vec_15_back = convert_9_to_15(vec_9)
    
    print("\nWektor 15D (z powrotem, STRATNY!):")
    for i, axis in enumerate(AXES_15):
        original = vec_15[i]
        recovered = vec_15_back[i]
        diff = abs(original - recovered)
        marker = "⚠️" if diff > 0.1 else "✓"
        print(f"  {axis:12s}: {recovered:.2f} (było: {original:.2f}) {marker}")
