# menuet_generator_enhanced.py
# -*- coding: utf-8 -*-
"""
Generator Menuetów Mozarta z wzmocnieniem Neural Networks
Implementacja algorytmu K. 516f (Würfelspiel) + Tiny NN dla wariacji
"""

import random
import numpy as np
from typing import Dict, List, Tuple


class MenuetGeneratorEnhanced:
    """
    Zaawansowany generator menuetów łączący:
    - Algorytm Mozarta (K. 516f) - klasyczna logika
    - Tiny Neural Networks - dla wariacji i różnorodności
    - 15 osi emocji AII - kontrola ekspresji
    """
    
    # Pełna tabela Mozarta (Würfelspiel) - 11 możliwych rzutów (2-12)
    # Każdy rzut ma 16 taktów (kolumn)
    MOZART_TABLE = {
        2:  [96,  22, 141,  41, 105, 122,  11,  30, 70, 121,  26,   9, 112,  49, 109,  14],
        3:  [32,   6, 128,  63, 146,  46, 134,  81, 117, 39, 126,  56, 174,  18, 116,  83],
        4:  [69,  95, 158,  13, 153,  55, 110,  24, 66, 139,  15, 132,  73,  58, 145,  79],
        5:  [40,  17, 113,  85, 161,   2, 159, 100, 90, 176,   7,  34,  67, 160,  52, 170],
        6:  [148, 74, 163,  45,  80,  97,  36, 107, 25, 143,  64, 125,  76, 136,   1,  93],
        7:  [104, 157,  27, 167, 154,  68, 118,  91, 138,  71, 150,  29, 101, 162,  23, 151],
        8:  [152, 60, 171,  53,  99, 133,  21, 127, 16, 155,  57, 175,  43, 168,  89, 172],
        9:  [119, 84, 114,  50, 140,  86, 169,  94, 120,  88,  48, 166,  51, 115,  72, 111],
        10: [98, 142,  42, 156,  75, 129,  62, 123,  65,  77,  19,  82, 137,  38, 149,   8],
        11: [3,  87, 165,  61, 135,  47, 147,  33, 102,   4,  31, 164, 144,  59, 173,  78],
        12: [54, 130,  10, 103,  28,  37, 106,   5, 35,  20, 108,  92,  12, 124,  44, 131]
    }
    
    # Alternatywna tabela (Trio) - bardziej liryczna
    TRIO_TABLE = {
        2:  [72, 56,  75,  40,  83,  11,  89,  18, 25, 34,  29,  64,  41,  36,  81,  38],
        3:  [56, 82,  42,  74,  14,   7,  26,  71, 76, 20,  64,  84,   8,  35,  47,  88],
        4:  [75, 39,  54,   1,  65,  43,  15,  80, 9,  34,  93,  48,  69,  58,  90,  21],
        5:  [40, 73,  16,  68,  29,  55,   2,  61, 22, 67,  49,   77,  57,  87,  33,  10],
        6:  [83, 3,  28,  53,  37,  17,  44,  70, 63, 85,  32,   96,  12,  23,  50,  91],
        7:  [18, 45,  62,  38,   4,  27,  52,  94, 11, 92,  24,   46,  78,  71,  36,   5],
        8:  [89, 70,  95,  19,  66,   9,  41,  80, 30, 95,  28,   53,  37,  84,  13,  42],
        9:  [90, 176,  7,  34,  67, 160,  52, 170, 14, 116,  50, 59,  26,  93,  68,  15],
        10: [19, 66,  95,   2,  33,  46,  26,   1, 73, 81,  94,   43,  48,  13,  22,  54],
        11: [14, 11,  98,  96,  49, 109,  14,  36, 61, 23,  90,   7,  49,  11,  72,  19],
        12: [6,  82,  36,  69,  41,  32,  65,  43, 51, 4,   87,   44,  52,  14,  33,   8]
    }
    
    # Mapowanie motywów na struktury rytmiczne (uproszczone)
    RHYTHMIC_PATTERNS = {
        'waltz_basic': [1.0, 1.0, 1.0],           # Podstawowy 3/4
        'waltz_elegant': [1.5, 0.5, 1.0],         # Elegancki
        'waltz_dotted': [1.5, 0.25, 0.25, 1.0],   # Punktowany
        'waltz_syncopated': [0.5, 1.0, 0.5, 1.0], # Synkopa
    }
    
    def __init__(self, composer_instance, nn_instance=None):
        """
        Args:
            composer_instance: SoulComposerV8 lub Enhanced
            nn_instance: SoulComposerTinyNN (opcjonalny, dla wariacji)
        """
        self.composer = composer_instance
        self.nn = nn_instance
        
        # Wybór tabeli (Mozart vs Trio) może być sterowany przez emocje
        self.current_table = self.MOZART_TABLE
        
        print("[MENUET] Generator zainicjalizowany")
        if self.nn:
            print("[MENUET] Wzmocnienie NN aktywne!")
    
    def generate_full_menuet(self, use_nn_variations=False, 
                            key='C', minor=False) -> dict:
        """
        Generuje pełny menuet (32 takty: 16 + 16 z repetycjami).
        
        Args:
            use_nn_variations: Czy używać NN do wariacji melodycznych
            key: Tonacja (C, D, E, F, G, A, B)
            minor: Czy molowy (True) czy durowy (False)
            
        Returns:
            dict: {'melody': [...], 'harmony': [...], 'metadata': {...}}
        """
        metrics = self.composer._get_soul_metrics()
        
        print(f"\n[MENUET] Komponuję menuet w {key} {'moll' if minor else 'dur'}")
        print(f"[MENUET] Stan emocji - Logika: {metrics.get('logika', 0):.2f}, "
              f"Chaos: {metrics.get('chaos', 0):.2f}, "
              f"Radość: {metrics.get('radość', 0):.2f}")
        
        # Wybór tabeli na podstawie emocji
        if metrics.get('smutek', 0) > 0.6 or minor:
            self.current_table = self.TRIO_TABLE
            print("[MENUET] Używam tabeli TRIO (lirycznej)")
        else:
            self.current_table = self.MOZART_TABLE
            print("[MENUET] Używam tabeli MOZART (klasycznej)")
        
        # Ustal root note
        root_note = self._key_to_midi(key, minor)
        scale = self._get_scale(root_note, minor)
        
        # Część A (16 taktów)
        part_a = self._generate_part(
            metrics, root_note, scale, 
            part_name="A", 
            use_nn=use_nn_variations
        )
        
        # Część B (16 taktów) - może być w tonacji dominanty
        if not minor:
            root_note_b = root_note + 7  # Dominanta (dur)
        else:
            root_note_b = root_note + 3  # Tercja (moll)
        scale_b = self._get_scale(root_note_b, minor)
        
        part_b = self._generate_part(
            metrics, root_note_b, scale_b,
            part_name="B",
            use_nn=use_nn_variations
        )
        
        # Struktura: A A B B (klasyczny menuet z repetycjami)
        full_melody = part_a['melody'] + part_a['melody'] + part_b['melody'] + part_b['melody']
        full_harmony = part_a['harmony'] + part_a['harmony'] + part_b['harmony'] + part_b['harmony']
        
        metadata = {
            'form': 'Menuet (A-A-B-B)',
            'key': f"{key} {'minor' if minor else 'major'}",
            'measures': 64,  # 16*4 z repetycjami
            'table_used': 'TRIO' if self.current_table == self.TRIO_TABLE else 'MOZART',
            'nn_enhanced': use_nn_variations
        }
        
        return {
            'melody': full_melody,
            'harmony': full_harmony,
            'metadata': metadata
        }
    
    def _generate_part(self, metrics: dict, root_note: int, 
                       scale: list, part_name: str, use_nn: bool) -> dict:
        """Generuje 16 taktów (jedna część menuetu)"""
        melody = []
        harmony = []
        
        # Diversity factor (jeśli NN dostępne)
        diversity = 0.3
        if self.nn and use_nn:
            diversity = self.nn.calculate_diversity_factor(metrics)
            print(f"[MENUET] Część {part_name} - Diversity: {diversity:.2f}")
        
        for measure_idx in range(16):
            # Rzut kośćmi sterowany emocjami
            roll = self._emotion_dice_roll(metrics)
            
            # Wybór motywu z tabeli Mozarta
            motif_id = self.current_table[roll][measure_idx]
            
            # === MELODIA (Prawa ręka) ===
            # Podstawowa struktura z tabeli
            base_melody = self._motif_to_melody(
                motif_id, root_note, scale, metrics
            )
            
            # Wariacja z NN (jeśli aktywne)
            if self.nn and use_nn and random.random() < diversity:
                base_melody = self._apply_nn_variation(
                    base_melody, metrics, scale
                )
            
            melody.append(base_melody)
            
            # === HARMONIA (Lewa ręka) ===
            harmony_chord = self._generate_harmony(
                motif_id, root_note, scale, metrics
            )
            harmony.append(harmony_chord)
        
        return {'melody': melody, 'harmony': harmony}
    
    def _emotion_dice_roll(self, metrics: dict) -> int:
        """
        Rzut kośćmi sterowany przez emocje (logika z SoulComposer).
        """
        logika = metrics.get('logika', 0.5)
        chaos = metrics.get('chaos', 0.3)
        radość = metrics.get('radość', 0.5)
        
        # Podstawowy rzut 2d6
        base_roll = random.randint(1, 6) + random.randint(1, 6)
        
        # Modyfikatory
        modifier = 0
        if radość > 0.6:
            modifier += 1
        if metrics.get('smutek', 0) > 0.6:
            modifier -= 1
        
        result = base_roll + modifier
        
        # Chaos → ekstrema
        if chaos > 0.7 and random.random() < 0.4:
            result = random.choice([2, 3, 11, 12])
        
        # Logika → środek (7)
        if logika > 0.8:
            if result < 5:
                result += 2
            if result > 9:
                result -= 2
        
        return max(2, min(12, result))
    
    def _motif_to_melody(self, motif_id: int, root: int, 
                        scale: list, metrics: dict) -> list:
        """
        Przekłada ID motywu (z tabeli Mozarta) na rzeczywiste nuty.
        """
        # Wybór wzorca rytmicznego
        rhythm = self._select_rhythm(metrics)
        
        # Generuj nuty na podstawie motif_id
        # (To uproszczona wersja - w pełnej implementacji każdy motif_id
        #  miałby własny wzorzec melodyczny)
        
        melody_notes = []
        base_pitch = root
        
        # Wpływ PRZESTRZENI na rejestr
        if metrics.get('przestrzeń', 0) > 0.7:
            base_pitch += 12
        elif metrics.get('przestrzeń', 0) < 0.3:
            base_pitch -= 12
        
        # Wzorzec melodyczny bazujący na motif_id
        seed = motif_id
        random.seed(seed)  # Deterministyczny dla tego motywu
        
        for duration in rhythm:
            # Wybierz nutę ze skali
            scale_degree = (seed + len(melody_notes)) % len(scale)
            pitch = scale[scale_degree]
            
            # Dynamika
            dynamic = 'mf'
            if metrics.get('energia', 0) > 0.7:
                dynamic = 'f'
            elif metrics.get('energia', 0) < 0.3:
                dynamic = 'p'
            
            melody_notes.append({
                'type': 'note',
                'pitch': pitch + base_pitch,
                'duration': duration,
                'dynamic': dynamic
            })
        
        random.seed()  # Reset RNG
        
        return melody_notes
    
    def _generate_harmony(self, motif_id: int, root: int,
                         scale: list, metrics: dict) -> list:
        """Generuje akord harmonii dla taktu."""
        
        # Określ stopień harmoniczny (I, IV, V, etc.)
        # Bazując na pozycji w frazach
        degree = (motif_id % 8)
        
        # Klasyczne progresje menuetowe
        if degree in [0, 7]:  # Początek/koniec frazy
            chord_root = root
            chord_type = 'maj'
        elif degree in [3, 4]:  # Środek frazy
            chord_root = root + 7  # Dominanta
            chord_type = 'maj'
        elif degree in [1, 2]:
            chord_root = root + 5  # Subdominanta
            chord_type = 'maj'
        else:
            chord_root = root + 2  # ii
            chord_type = 'min'
        
        # Buduj akord
        if chord_type == 'maj':
            intervals = [0, 4, 7]
        else:
            intervals = [0, 3, 7]
        
        chord_notes = [chord_root - 12 + i for i in intervals]
        
        # Voicing (przestrzeń)
        if metrics.get('przestrzeń', 0) > 0.6:
            chord_notes = [chord_notes[0], chord_notes[1] + 12, chord_notes[2] + 12]
        
        return [{
            'type': 'chord',
            'pitch': chord_notes,
            'duration': 3.0,  # Cały takt 3/4
            'dynamic': 'mp'
        }]
    
    def _apply_nn_variation(self, base_melody: list, 
                           metrics: dict, scale: list) -> list:
        """Aplikuje wariacje z sieci neuronowej."""
        if not self.nn:
            return base_melody
        
        varied_melody = []
        previous_pitches = [note['pitch'] for note in base_melody[-3:]]
        
        for note in base_melody:
            # Z pewnym prawdopodobieństwem zmień nutę
            if random.random() < 0.3:  # 30% szans na wariację
                new_pitch = self.nn.generate_melody_variation(
                    metrics,
                    previous_pitches[-5:],
                    temperature=0.8
                )
                
                # Ogranicz do skali (opcjonalnie)
                if metrics.get('wiedza', 0) > 0.7:
                    # Znajdź najbliższą nutę w skali
                    closest = min(scale, key=lambda x: abs(x - (new_pitch % 12)))
                    octave = (new_pitch // 12) * 12
                    new_pitch = octave + closest
                
                note = note.copy()
                note['pitch'] = new_pitch
                previous_pitches.append(new_pitch)
            
            varied_melody.append(note)
        
        return varied_melody
    
    def _select_rhythm(self, metrics: dict) -> list:
        """Wybiera wzorzec rytmiczny na podstawie emocji."""
        czas = metrics.get('czas', 0.5)
        logika = metrics.get('logika', 0.5)
        
        if logika > 0.7:
            return self.RHYTHMIC_PATTERNS['waltz_basic']
        elif czas > 0.7:
            return self.RHYTHMIC_PATTERNS['waltz_dotted']
        elif metrics.get('kreacja', 0) > 0.6:
            return self.RHYTHMIC_PATTERNS['waltz_syncopated']
        else:
            return self.RHYTHMIC_PATTERNS['waltz_elegant']
    
    def _key_to_midi(self, key: str, minor: bool) -> int:
        """Konwertuje nazwę tonacji na MIDI root note."""
        key_map = {
            'C': 0, 'D': 2, 'E': 4, 'F': 5,
            'G': 7, 'A': 9, 'B': 11
        }
        
        base = 60  # C4
        offset = key_map.get(key.upper(), 0)
        
        if minor:
            # A minor = 57 (A3)
            return base - 3 + offset
        else:
            return base + offset
    
    def _get_scale(self, root: int, minor: bool) -> list:
        """Zwraca nuty w skali (indeksy od root)."""
        if minor:
            # Skala molowa naturalna
            intervals = [0, 2, 3, 5, 7, 8, 10]
        else:
            # Skala durowa
            intervals = [0, 2, 4, 5, 7, 9, 11]
        
        return intervals


# ==================== INTEGRACJA ====================

def integrate_menuet_generator(composer_instance, nn_instance=None):
    """
    Dodaje generator menuetów do SoulComposer.
    
    Usage:
        menuet_gen = integrate_menuet_generator(composer, nn)
        result = menuet_gen.generate_full_menuet(use_nn_variations=True, key='G')
    """
    return MenuetGeneratorEnhanced(composer_instance, nn_instance)


# ==================== PRZYKŁAD UŻYCIA ====================

if __name__ == "__main__":
    print("=" * 70)
    print("MENUET GENERATOR - Mozart K. 516f + Tiny NN")
    print("=" * 70)
    
    # Mock composer dla testów
    class MockComposer:
        def _get_soul_metrics(self):
            return {
                'logika': 0.8, 'kreacja': 0.6, 'chaos': 0.2,
                'radość': 0.7, 'smutek': 0.2, 'gniew': 0.0,
                'strach': 0.1, 'wstręt': 0.0, 'zaufanie': 0.8,
                'oczekiwanie': 0.5, 'zaskoczenie': 0.3, 'wiedza': 0.8,
                'czas': 0.5, 'przestrzeń': 0.6, 'energia': 0.6
            }
    
    # Test bez NN
    print("\n--- TEST 1: Klasyczny Menuet (bez NN) ---")
    composer = MockComposer()
    menuet_gen = MenuetGeneratorEnhanced(composer, nn_instance=None)
    
    result = menuet_gen.generate_full_menuet(
        use_nn_variations=False,
        key='C',
        minor=False
    )
    
    print(f"\nWygenerowano menuet:")
    print(f"  Forma: {result['metadata']['form']}")
    print(f"  Tonacja: {result['metadata']['key']}")
    print(f"  Liczba taktów: {result['metadata']['measures']}")
    print(f"  Użyta tabela: {result['metadata']['table_used']}")
    print(f"  Taktów melodii: {len(result['melody'])}")
    print(f"  Taktów harmonii: {len(result['harmony'])}")
    
    # Test z NN
    print("\n--- TEST 2: Menuet z wariacjami NN ---")
    try:
        from soul_composer_tiny_nn import SoulComposerTinyNN
        nn = SoulComposerTinyNN()
        
        menuet_gen_nn = MenuetGeneratorEnhanced(composer, nn_instance=nn)
        
        result_nn = menuet_gen_nn.generate_full_menuet(
            use_nn_variations=True,
            key='G',
            minor=False
        )
        
        print(f"\nWygenerowano menuet z NN:")
        print(f"  Tonacja: {result_nn['metadata']['key']}")
        print(f"  NN enhanced: {result_nn['metadata']['nn_enhanced']}")
        
    except ImportError:
        print("  [INFO] SoulComposerTinyNN niedostępny - pomiń test NN")
    
    print("\n" + "=" * 70)
    print("✓ Testy zakończone!")
    print("=" * 70)